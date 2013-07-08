#!/usr/bin/python
# -*- coding: utf-8 -*-
# Ideas and code ripped shamelessly from http://picospeaker.tk/ and
# https://github.com/redacted/XKCD-password-generator then cobbled togeather by
# Michael Van Delft 2013-07-08
#
#

import optparse

def validate_options(options, args):
    """
    Given a set of command line options, performs various validation checks
    """

    if len(args) > 1:
        parser.error("Too many arguments.")


if __name__ == '__main__':

    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage)

    parser.add_option("-i", "--infile", dest="inFile",
                      default='./test.pdf',
                      help="The file to be converted")

    parser.add_option("-o", "--outfile", dest="outFile",
                      default='./test.ogg',
                      help="The location to output to")

    (options, args) = parser.parse_args()
    validate_options(options, args)

    print(options.inFile)