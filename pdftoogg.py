#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# A short Python script that converts a pdf into an ogg file.
# Ideas and bits of code shamelessly ripped from http://picospeaker.tk/ and
# https://github.com/redacted/XKCD-password-generator then cobbled togeather by
# Michael Van Delft 2013-07-13
#
# Requires pdftotext (Should be on most linux systems) and pico2wave can be
# found by installing libttspico0, libttspico-data and libttspico-utils.
#
# This is free and unencumbered software released into the public domain.
# see http://unlicense.org
#

import optparse
import subprocess
import os
import sys
import math


supportedLanguages = ["en-US", "en-GB", "de-DE", "es-ES", "fr-FR", "it-IT"]

#If the pdf is more than 32766 characters long it needs to be split.
numberOfWaveFiles = 1

#Compatiblity with python 2 and 3
try:
    input = raw_input
except NameError:
    pass


def check_file_exists(location):
    """Checks a location and if there is allready a file asks if it should
    be overwiten, if no exits the program"""
    if os.path.exists(location):
        overwrite = input(str(location) + " allready exists, overwrite? [y/N]")
        if overwrite.lower() not in ["y", "yes"]:
            sys.exit(0)


def setup_options():
    """Setst up options that that can be set"""
    usage = "usage: %prog [input file] [options]"
    parser = optparse.OptionParser(usage)

    parser.add_option("-i", "--input", dest="inFile",
                      default=None,
                      help="The PDF file to be converted:")
    parser.add_option("-o", "--output", dest="outFile",
                      default=None,  # The default for this is the name of the
                      #input file but this is set in validate_options.
                      help="Output to the specified file: (ogg format)")
    parser.add_option("-l", "--language", dest="language",
                      default="en-US",
                      help="Language to speak: (default is en-US) Avalible"
                      "languages are " + ", ".join(supportedLanguages[:-1]) +
                      " and " + supportedLanguages[-1])
    parser.add_option("-r", "--rate", dest="rate",
                      default=100, type="int",
                      help="Rate of speech from 10 to 300: (default is 100) "
                      "50 is half speed, 200 is double speed")
    parser.add_option("-p", "--pitch", dest="pitch",
                      default=0, type="int",
                      help="Voice pitch from -20 to 20: (default is 0)")

    return(parser.parse_args())


def validate_options(options, args):
    """
    Given a set of command line options, performs various validation checks
    """
    if len(args) > 1:
        sys.stderr.write("Too many arguments.\n")
        sys.exit(1)

    if len(args) == 1:
        # supporting either -i or args[0] for input file, but not both
        if options.inFile is None:
            options.inFile = args[0]
        elif options.inFile == args[0]:
            pass
        else:
            sys.stderr.write("Conflicting values for input: " + args[0] +
                             " and " + options.wordfile)

    if options.inFile is None:
        sys.stderr.write("No input file specified. Try using -i <file name>\n")
        sys.exit(1)

    if not os.path.exists(options.inFile):
        sys.stderr.write("Could not open the specified PDF file.\n")
        sys.exit(1)

    if options.language not in supportedLanguages:
        sys.stderr.write(("Language " + options.language +
        " is currently not available.\n Available languages are "
        + ", ".join(supportedLanguages[:-1]) + " and " + supportedLanguages[-1]
        + ".\n"))
        sys.exit(1)

    #Check if the rate is between 10 and 300
    if not 10 <= options.rate <= 300:
        sys.stderr.write("Rate must be between 10 and 300. (default is 100)\n")
        sys.exit(1)

    if not -20 <= options.pitch <= 20:
        sys.stderr.write("Pitch must be between -20 and 20. (default is 0)\n")
        sys.exit(1)

    if options.outFile is None:
        options.outFile = str(options.inFile) + ".ogg"

    #Moved to last because it requires user input and it's a pain to press 'Y'
    #only to find out one of the other options is wrong.
    check_file_exists(options.outFile)


def read_pdf_file(fileLocation, outLocation):
    """
    Takes the location of a pdf file and uses pdftotext to the text as a big
    string. This needs to be able to write to the current directory.
    """
    #Assumes that the fileLocation is valid because its allready been tested
    #in validate_option
    tempLocation = outLocation + ".txt"

    #Check if file allready exists
    check_file_exists(tempLocation)

    #Convert the PDF outputing to .pdfTemp
    subprocess.call(["pdftotext", fileLocation, tempLocation])

    #Read back in from .pdfTemp as a single string
    with open(tempLocation, "r") as textFile:
        data = textFile.read().replace("\n", "")

    #Clean up after ourselfs
    os.remove(tempLocation)

    return(data)


def text_to_wave(language, location, text):
    """Converts Text to Speach using Pico2wave, Splits into multiple files if
    the text is more than 32766 characters long"""
    global numberOfWaveFiles
    numberOfWaveFiles = int(math.ceil(len(text) / 32766))

    for i in range(0, numberOfWaveFiles + 1):
        #Check if file allready exists
        check_file_exists(location + str(i) + ".wav")

        start = int(i * 32766)
        end = int((i + 1) * 32766)

        #Convert the text to  a wave
        subprocess.call(["pico2wave",
                         "-w", location + str(i) + ".wav",
                         "-l", language,
                         "--", text[start:end]])


def wave_to_ogg(location, pitch, rate):
    """Converts a wave file to an ogg"""
    #Assume the output location has been validated by validate_options.
    convert = ["sox"]

    for i in range(0, numberOfWaveFiles + 1):
        convert.append(location + str(i) + ".wav")

    convert.extend(["-t", "ogg",
                     location,
                     "pitch", str(float(pitch) * 100),
                     "tempo", "-s", str(float(rate) / 100)])

    subprocess.call(convert)  # This producese and errror becasue the audio
    #length that is recorded at the beginning of the file does not match the
    #actual length. see http://sourceforge.net/p/sox/bugs/171/

    #Clean up the temp wave file
    for i in range(0, numberOfWaveFiles + 1):
        os.remove(location + str(i) + ".wav")

    return None

if __name__ == "__main__":
    (options, args) = setup_options()
    validate_options(options, args)
    text = read_pdf_file(options.inFile, options.outFile)
    text_to_wave(options.language, options.outFile, text)
    wave_to_ogg(options.outFile, options.pitch, options.rate)