import requests
import logging
import argparse
import os
import sys
from shutil import copyfile
import config
from codeTemplates import languageTemplates
from codeTemplates import filenameReplaceTag

def downloadPuzzle(day, year, dir):
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
        open(os.path.join(dir, config.inputFileName), "wb").write(respond.content)
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
    parser.add_argument('-y', '--year', action='store', type=int, required=True, help='select the year')
    parser.add_argument('-l', '--lang', action='store', type=str, required=True, choices=list(languageTemplates.keys()), help=f'select the language which you use to solve the puzzle. Available selections: {languageTemplates.keys()}')
    parser.add_argument('-c', '--cookie', action='store', type=str, required=False, help='set your personal session cookie for adventofcode.com')
    parser.add_argument('-p', '--path', action='store', type=str, required=False, help='directory where the folders and files should be created (default: current directory)')
    parser.add_argument('-sd', '--skipDownload', action='store_true', help='skip the download and create folder and dummy input file')

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d',  '--day',action='store', type=int, help='select the day')
    group.add_argument('-a', '--all', action='store_true', help='download all days')

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
        logger.warning(f"{sourceFile} file alread existed. Replaced with the latest file.")

    copyfile(sourceFile, destinationFile)
    logger.info(f"{sourceFile} saved at: {destinationFile}")

def createDirectories(day, year, language, createDirectories):
    dayZeroPadding = f"{day:02d}"
    path1 = os.path.join(createDirectories, "AoC_" + str(year), dayZeroPadding + "_" + language, dayZeroPadding + "_01")
    path2 = os.path.join(createDirectories, "AoC_" + str(year), dayZeroPadding + "_" + language, dayZeroPadding + "_02")

    checkAndCreateDir(path1)
    checkAndCreateDir(path2)

    inputFile1 = os.path.join(path1,  config.inputFileName)
    inputFile2 = os.path.join(path2,  config.inputFileName)

    testFile1 = os.path.join(path1,  config.testFileName)
    testFile2 = os.path.join(path2,  config.testFileName)


    checkAndCopyFile(os.path.join(createDirectories, config.inputFileName), inputFile1)
    checkAndCopyFile(os.path.join(createDirectories, config.inputFileName), inputFile2)
    checkAndCopyFile(os.path.join(createDirectories, config.inputFileName), testFile1)
    checkAndCopyFile(os.path.join(createDirectories, config.inputFileName), testFile2)

    os.remove(os.path.join(createDirectories, config.inputFileName))

    return (path1, path2)

def createCodeTemplateFiles(language, sourceCodeFilename):
    if(language in languageTemplates.keys()):
        codeTemplate = languageTemplates[language]
        codeTemplate = codeTemplate.replace(filenameReplaceTag, config.inputFileName)

        open(sourceCodeFilename, "w").write(codeTemplate)
        logger.info(f"Source code file successfully written: {sourceCodeFilename}")

    else:
        logger.error(f"Wrong language selected. Available languages: {languageTemplates.keys()}")

def prepareDay(day, year, language, creationDirectory, skipDownload):
    if skipDownload:
        open(os.path.join(creationDirectory, config.inputFileName), "w").write('Test1\nTest2')
        logger.info("Download skipped, dummy file created.")
    else:
        downloadPuzzle(day, year, creationDirectory)

    dayZeroPadding = f"{day:02d}"

    dir1, dir2 = createDirectories(day, year, language, creationDirectory)
    createCodeTemplateFiles(language, os.path.join(dir1, dayZeroPadding + "_01." + language))
    createCodeTemplateFiles(language, os.path.join(dir2, dayZeroPadding + "_02." + language))


if __name__ == "__main__":
    setupLoggger()
    args = getArguments()

    if(args.cookie is not None):
        config.SESSION_COOKIE = args.cookie

    if(args.path is None):
        creationDirectory = os.getcwd()
    else:
        creationDirectory = args.path
        if(not os.path.exists(creationDirectory)):
            os.makedirs(creationDirectory)

    if(args.all):
        for i in range(1,26):
            prepareDay(i, args.year, args.lang, creationDirectory, args.skipDownload)
    else:
        prepareDay(args.day, args.year, args.lang, creationDirectory, args.skipDownload)

