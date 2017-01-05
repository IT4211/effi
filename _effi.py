import os
import csv
import argparse
import logging

log = logging.getLogger('main._effi')

def ParseCommandLine():

    parser = argparse.ArgumentParser('Extract a file from dd/raw/ewf image file(s)')

    parser.add_argument('-v', '--verbose', help='enables printing of additional program messages', action='store_true')
    parser.add_argument('-f', '--file', type=ValidateFile,
                        required=True, help='Specify the image file from which to extract the file.')
    parser.add_argument('-p', '--fullpath', help='Specifies whether to extract the file by implementing the full path.', action='store_true')
    global gl_args

    gl_args = parser.parse_args() # image file

    DisplayMessage("Command line processed: Successfully")

    return gl_args.file, gl_args.fullpath

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

class _CSVWriter:

    def __init__(self, fileName):
        try:
            self.csvFile = open(fileName, 'ab')
            self.writer = csv.writer(self.csvFile, delimiter=',', quoting=csv.QUOTE_ALL)
            self.writer.writerow(('FileName', 'Ext', 'Path', 'Size', 'Modified Time',
                                  'Access Time', 'Create Time', 'Entry Time'))
        except:
            log.error('CSV File Failure')

    def writeCSVRow(self, fileName, fileExt, filePath, fileSize,
                    mTime, aTime, cTime, eTime):
        self.writer.writerow((fileName, fileExt, filePath, fileSize,
                              mTime, aTime, cTime, eTime))

    def writerClose(self):
        self.csvFile.close()