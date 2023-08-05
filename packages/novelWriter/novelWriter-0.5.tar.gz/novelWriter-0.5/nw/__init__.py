# -*- coding: utf-8 -*-
"""novelWriter Init

 novelWriter – Init File
=========================
 Application initialisation

 File History:
 Created: 2018-09-22 [0.0.1]

 This file is a part of novelWriter
 Copyright 2020, Veronica Berglyd Olsen

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful, but
 WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import getopt
import logging

from os import path, remove, rename

from PyQt5.QtWidgets import QApplication

from nw.guimain import GuiMain
from nw.config import Config

__package__    = "novelWriter"
__author__     = "Veronica Berglyd Olsen"
__copyright__  = "Copyright 2018–2020, Veronica Berglyd Olsen"
__license__    = "GPLv3"
__version__    = "0.5"
__date__       = "2020-05-09"
__maintainer__ = "Veronica Berglyd Olsen"
__email__      = "code@vkbo.net"
__status__     = "Development"
__url__        = "https://github.com/vkbo/novelWriter"
__docurl__     = "https://novelwriter.readthedocs.io"
__credits__    = [
    "Veronica Berglyd Olsen (developer)",
    "Marian Lückhof (contributor, tester)"
]

#
#  Logging
# =========
#  Standard used for logging levels in novelWriter:
#    CRITICAL  Use for errors that result in termination of the program
#    ERROR     Use when an action fails, but execution continues
#    WARNING   When something unexpected, but non-critical happens
#    INFO      Any useful user information like open, save, exit initiated
#  ----------- SPAM Threshold : Output above should be minimal -----------------
#    DEBUG     Use for descriptions of main program flow
#    VERBOSE   Use for outputting values and program flow details
#

# Adding verbose logging levels
VERBOSE = 5
logging.addLevelName(VERBOSE, "VERBOSE")
def logVerbose(self, message, *args, **kws):
    if self.isEnabledFor(VERBOSE):
        self._log(VERBOSE, message, args, **kws)
logging.Logger.verbose = logVerbose

# Initiating logging
logger = logging.getLogger(__name__)

#
#  Main Program
# ==============
#

# Load the main config as a global object
CONFIG = Config()

def main(sysArgs=None):
    """Parses command line, sets up logging, and launches main GUI.
    """

    if sysArgs is None:
        sysArgs = sys.argv[1:]

    # Valid Input Options
    shortOpt = "hidvql:"
    longOpt  = [
        "help",
        "version",
        "info",
        "debug",
        "verbose",
        "quiet",
        "logfile=",
        "style=",
        "config=",
        "data=",
        "testmode",
    ]

    helpMsg = (
        "{appname} {version} ({status})\n"
        "{copyright}\n"
        "\n"
        "This program is distributed in the hope that it will be useful,\n"
        "but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
        "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\n"
        "GNU General Public License for more details.\n"
        "\n"
        "Usage:\n"
        " -h, --help      Print this message.\n"
        "     --version   Print program version and exit.\n"
        " -i, --info      Print additional runtime information.\n"
        " -d, --debug     Print debug output. Includes -i.\n"
        " -v, --verbose   Increase verbosity of debug output. Includes -d.\n"
        " -q, --quiet     Disable output to command line. Does not affect log file.\n"
        " -l, --logfile=  Specify log file.\n"
        "     --style=    Sets Qt5 style flag. Defaults to 'Fusion'.\n"
        "     --config=   Alternative config file.\n"
        "     --data=     Alternative user data path.\n"
        "     --testmode  Do not display GUI. Used by the test suite.\n"
    ).format(
        appname   = __package__,
        version   = __version__,
        status    = __status__,
        copyright = __copyright__
    )

    # Defaults
    debugLevel = logging.WARN
    logFormat  = "{levelname:8}  {message:}"
    logFile    = ""
    toFile     = False
    toStd      = True
    confPath   = None
    dataPath   = None
    testMode   = False
    qtStyle    = "Fusion"
    cmdOpen    = None

    # Parse Options
    try:
        inOpts, inRemain = getopt.getopt(sysArgs,shortOpt,longOpt)
    except getopt.GetoptError as E:
        print(helpMsg)
        print("ERROR: %s" % str(E))
        sys.exit(2)

    if len(inRemain) > 0:
        cmdOpen = inRemain[0]

    for inOpt, inArg in inOpts:
        if inOpt in ("-h","--help"):
            print(helpMsg)
            sys.exit()
        elif inOpt == "--version":
            print("%s %s Version %s" % (__package__,__status__,__version__))
            sys.exit()
        elif inOpt in ("-i", "--info"):
            debugLevel = logging.INFO
        elif inOpt in ("-d", "--debug"):
            debugLevel = logging.DEBUG
            logFormat  = "[{asctime:}] {name:>30}:{lineno:<4d}  {levelname:8}  {message:}"
        elif inOpt in ("-l","--logfile"):
            logFile = inArg
            toFile  = True
        elif inOpt in ("-q","--quiet"):
            toStd = False
        elif inOpt in ("-v","--verbose"):
            debugLevel = VERBOSE
            logFormat  = "[{asctime:}] {name:>30}:{lineno:<4d}  {levelname:8}  {message:}"
        elif inOpt == "--style":
            qtStyle = inArg
        elif inOpt == "--config":
            confPath = inArg
        elif inOpt == "--data":
            dataPath = inArg
        elif inOpt == "--testmode":
            testMode = True

    # Set Config Options
    CONFIG.showGUI   = not testMode
    CONFIG.debugInfo = debugLevel < logging.INFO
    CONFIG.cmdOpen   = cmdOpen

    # Set Logging
    logFmt = logging.Formatter(fmt=logFormat,datefmt="%Y-%m-%d %H:%M:%S",style="{")

    if not logFile == "" and toFile:
        if path.isfile(logFile+".bak"):
            remove(logFile+".bak")
        if path.isfile(logFile):
            rename(logFile,logFile+".bak")

        fHandle = logging.FileHandler(logFile)
        fHandle.setLevel(debugLevel)
        fHandle.setFormatter(logFmt)
        logger.addHandler(fHandle)

    if toStd:
        cHandle = logging.StreamHandler()
        cHandle.setLevel(debugLevel)
        cHandle.setFormatter(logFmt)
        logger.addHandler(cHandle)

    logger.setLevel(debugLevel)

    CONFIG.initConfig(confPath, dataPath)

    if testMode:
        nwGUI = GuiMain()
        return nwGUI
    else:
        nwApp = QApplication([__package__,("-style=%s" % qtStyle)])
        nwApp.setApplicationName(__package__)
        nwApp.setApplicationVersion(__version__)
        nwGUI = GuiMain()
        sys.exit(nwApp.exec_())

    return
