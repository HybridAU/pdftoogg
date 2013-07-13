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

supportedLanguages = ["en-US", "en-GB", "de-DE", "es-ES", "fr-FR", "it-IT"]

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
    usage = "usage: %prog [options]"
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
    if len(args) > 0:
        sys.stderr.write("Too many arguments.\n")
        sys.exit(1)

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


def read_pdf_file(fileLocation):
    """
    Takes the location of a pdf file and uses pdftotext to the text as a big
    string. This needs to be able to write to the current directory.
    """
    #Assumes that the fileLocation is valid because its allready been tested
    #in validate_option
    tempLocation = ".pdfTemp.txt"

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


def text_to_wave(language, text):
    """Converts Text to Speach using Pico2wave"""
    tempLocation = ".pdfTemp.wav"

    #Check if file allready exists
    check_file_exists(tempLocation)

    #Convert the text to  a wave
    subprocess.call(["pico2wave",
                     "-w", tempLocation,
                     "-l", language,
                     "--", text])
    #Return the file loaction (It will be cleaned up after it's been compressed.
    return(tempLocation)


def wave_to_ogg(waveFile, outputLocation, pitch, rate):
    """Converts a wave file to an ogg"""
    #Assume the output location has been validated by validate_options.

    subprocess.call(["sox",
                     waveFile,
                     "-t", "ogg",
                     outputLocation,
                     "pitch", str(float(pitch) * 100),
                     "tempo", "-s", str(float(rate) / 100)
                     ])

    #Clean up the temp wave file
    os.remove(waveFile)

    return None

if __name__ == "__main__":
    (options, args) = setup_options()
    validate_options(options, args)
    text = read_pdf_file(options.inFile)
    waveFile = text_to_wave(options.language, text)
    wave_to_ogg(waveFile, options.outFile, options.pitch, options.rate)