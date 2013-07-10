#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ideas and code ripped shamelessly from http://picospeaker.tk/ and
# https://github.com/redacted/XKCD-password-generator then cobbled togeather by
# Michael Van Delft 2013-07-08
#
#
import optparse
import pyPdf

supportedLanguages = ['en-US', 'en-GB', 'de-DE', 'es-ES', 'fr-FR', 'it-IT']


def validate_options(options, args):
    """
    Given a set of command line options, performs various validation checks
    """

    if len(args) > 0:
        parser.error("Too many arguments.")

    if options.language not in supportedLanguages:
        print(("Language " + options.language + " is currently not available.\n"
        "Available languages are " + ", ".join(supportedLanguages[:-1]) +
        " and " + supportedLanguages[-1] + ".\n"))


def read_pdf_file(fileLocation):
    #It's assume that the fileLocation is valid because its allready been tested
    #in validate_options. Otherwise we would check that first.
    inFile = pyPdf.PdfFileReader(file(fileLocation, "rb"))


if __name__ == '__main__':

    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage)

    parser.add_option("-i", "--input", dest="inFile",
                      default="./test.pdf",
                      help="The PDF file to be converted:")
    parser.add_option("-o", "--output", dest="outFile",
                      default="./test.ogg",
                      help="Output to the specified file: (ogg format)")
    parser.add_option("-l", "--language", dest="language",
                      default="en-US",
                      help="Language to speak: (default is en-US) avalible"
                      "languages inclue 'en-US', 'en-GB', 'de-DE', 'es-ES',"
                      "'fr-FR', 'it-IT'")
    parser.add_option("-v", "--volume", dest="volume",
                      default=1.0, type="float",
                      help="Output volume: (default is 1.0)")
    parser.add_option("-r", "--rate", dest="rate",
                      default=0, type="int",
                      help="Rate of speech from -90 to 9900: (default is 0)")
    parser.add_option("-p", "--pitch", dest="pitch",
                      default=0, type="int",
                      help="Voice pitch from -79 to 39: (default is 0)")

    (options, args) = parser.parse_args()
    validate_options(options, args)