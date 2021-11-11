import requests
import logging
import argparse
import os
import sys
from shutil import copyfile

SESSION_COOKIE = "53616c7465645f5ffe90eacec787dcaad52b7408769e4aec1c50df83e99f97854972a9cdc5fb22c74bdf84e6598a85d8"

def downloadPuzzle(day, year):
    url = 'https://adventofcode.com/' + str(year) + '/day/' + str(day) + '/input'

    logger.info(f'Day {day}')
    logger.info(f'Year {year}')
    logger.info(f'URL {url}')

    s = requests.session()
    # Note that domain keyword parameter is the only optional parameter here
    cookie_obj = requests.cookies.create_cookie(name="session", value=SESSION_COOKIE)
    s.cookies.set_cookie(cookie_obj)
    logger.debug(f"Session cookie set to: {SESSION_COOKIE}")

    respond = s.get(url)

    if respond.status_code == 200:
        open("input.txt", "wb").write(respond.content)
        logger.info("File successfully downloaded")
    else:
        logger.warning(f"Error: Download failed. Respond status code: {respond.status_code}")
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
    parser.add_argument('-l', action='store', type=str, required=True, choices=['py', 'c', 'cpp', 'rs'], help='select the language which you use to solve the puzzle. Available selections: py, c, cpp, rs')
    args = parser.parse_args()
    return args

def createDirectories(day, year, language):
    cwd = os.getcwd()
    dayZeroPadding = f"{day:02d}"
    path1 = f"{cwd}\\AoC_{year}\\{dayZeroPadding}_{language}\\{dayZeroPadding}_01"
    path2 = f"{cwd}\\AoC_{year}\\{dayZeroPadding}_{language}\\{dayZeroPadding}_02"
    os.makedirs(path1)
    os.makedirs(path2)

    copyfile(cwd + f"\\input.txt", path1 + f"\\input.txt")
    os.rename(cwd + f"\\input.txt", path2 + f"\\input.txt")

if __name__ == "__main__":
    setupLoggger()
    args = getArguments()
    downloadPuzzle(args.d, args.y)
    createDirectories(args.d, args.y, args.l)