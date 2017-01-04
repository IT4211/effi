import os
import argparse
import logging

log = logging.getLogger('main._effi')

def ParseCommandLine():

    parser = argparse.ArgumentParser('Extract a file from dd/raw image file(s)')

    parser.add_argument('-v', '--verbose', help='enables printing of additional program messages', action='store_true')
    parser.add_argument('-f', '--file', type=ValidateFile,
                        required=True, help='Specify the image file from which to extract the file.')

    global gl_args

    gl_args = parser.parse_args() # image file

    DisplayMessage("Command line processed: Successfully")

    return gl_args.file

def ValidateFile(theFile):
    if not os.path.exists(theFile):
        raise argparse.ArgumentTypeError('File does not exist')

    if os.access(theFile, os.R_OK):
        return theFile
    else:
        raise argparse.ArgumentTypeError('File is not readable')

def DisplayMessage(msg):

    if gl_args.verbose:
        print(msg)

    return

