import requests
import logging
import argparse
import os
import sys
from shutil import copyfile
import config
from codeTemplates import languageTemplates
from codeTemplates import filenameReplaceTag

def downloadPuzzle(day, year):
    url = 'https://adventofcode.com/' + str(year) + '/day/' + str(day) + '/input'

    logger.info(f'Day {day}')
    logger.info(f'Year {year}')
    logger.info(f'URL {url}')

    s = requests.session()
    # Note that domain keyword parameter is the only optional parameter here
    cookie_obj = requests.cookies.create_cookie(name="session", value=config.SESSION_COOKIE)
    s.cookies.set_cookie(cookie_obj)
    logger.debug(f"Session cookie set to: {config.SESSION_COOKIE}")

    respond = s.get(url)

    if respond.status_code == 200:
        open(config.inputFileName, "wb").write(respond.content)
        logger.info("File successfully downloaded")
    else:
        logger.warning(f"Error: Download failed. Respond status code: {respond.status_code}")
        logger.warning(f"Is the session cookie set corretly in the config file?")
        sys.exit()

def setupLoggger():
    global logger
    logger = logging.getLogger('prepareAoCLogger')
    logger.setLevel(logging.DEBUG)
    
    stdOutHandler = logging.StreamHandler()
    stdOutHandler.setLevel(logging.DEBUG)
    formatterStdOut = logging.Formatter('%(asctime)s [%(levelname)s] \t %(message)s')
    formatterStdOut.datefmt = '%H:%M:%S'
    stdOutHandler.setFormatter(formatterStdOut)

    logger.addHandler(stdOutHandler)

def getArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-y', action='store', type=int, required=True, help='select the year')
    parser.add_argument('-d', action='store', type=int, required=True, help='select the day')
    parser.add_argument('-l', action='store', type=str, required=True, choices=list(languageTemplates.keys()), help=f'select the language which you use to solve the puzzle. Available selections: {languageTemplates.keys()}')
    args = parser.parse_args()
    return args

def checkAndCreateDir(path):
    if(not os.path.exists(path)):
        os.makedirs(path)
        logger.info(f"Directory created: {path} ")
    else:
        logger.warning(f"Directory already exists: {path} ")

def checkAndCopyFile(sourceFile, destinationFile):
    if os.path.exists(destinationFile):
        os.remove(destinationFile)
        logger.warning(f"{config.inputFileName} file alread existed. Replaced with the latest file.")

    copyfile(sourceFile, destinationFile)
    logger.info(f"{config.inputFileName} saved at: {destinationFile}")

def createDirectories(day, year, language):
    cwd = os.getcwd()

    dayZeroPadding = f"{day:02d}"
    path1 = f"{cwd}\\AoC_{year}\\{dayZeroPadding}_{language}\\{dayZeroPadding}_01"
    path2 = f"{cwd}\\AoC_{year}\\{dayZeroPadding}_{language}\\{dayZeroPadding}_02"

    checkAndCreateDir(path1)
    checkAndCreateDir(path2)

    inputFile1 = path1 + f"\\" + config.inputFileName
    inputFile2 = path2 + f"\\" + config.inputFileName

    checkAndCopyFile(cwd + f"\\" + config.inputFileName, inputFile1)
    checkAndCopyFile(cwd + f"\\" + config.inputFileName, inputFile2)
    os.remove(cwd + f"\\" + config.inputFileName)

    return (path1, path2)

def createCodeTemplateFiles(language, sourceCodeFilename):
    if(language in languageTemplates.keys()):
        codeTemplate = languageTemplates[language]
        codeTemplate = codeTemplate.replace(filenameReplaceTag, ".\\\\" + config.inputFileName.replace("\\", "\\\\"))
        logger.debug(codeTemplate)

        open(sourceCodeFilename, "w").write(codeTemplate)
        logger.info(f"Source code file successfully written: {sourceCodeFilename}")

    else:
        logger.error(f"Wrong language selected. Available languages: {languageTemplates.keys()}")

if __name__ == "__main__":
    setupLoggger()
    args = getArguments()
    downloadPuzzle(args.d, args.y)
    dir1, dir2 = createDirectories(args.d, args.y, args.l)

    createCodeTemplateFiles(args.l, dir1 + f"\\{args.d}_01.{args.l}")
    createCodeTemplateFiles(args.l, dir2 + f"\\{args.d}_02.{args.l}")
