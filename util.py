import logging
import subprocess
import sys
import time

def getArg(desiredArgName, mustAbsolutelyBeAnArray = False):
    desiredArgName = "-" + desiredArgName
    values = []
    argName = ""
    for arg in sys.argv:
        if arg[0] == "-":
            argName = arg
        elif (argName == desiredArgName):
            values.append(arg)
    if len(values) == 1 and mustAbsolutelyBeAnArray == False:
        return values[0]
    return values


def mkDir(filePath):
    mkdir = subprocess.Popen(['mkdir', '-p', filePath], stdout=subprocess.PIPE).communicate()[0]
    dolog(mkdir)

def dolog(tolog):
    #print tolog
    logging.debug(time.strftime("%H:%M:%S", time.localtime()) + "\t" + tolog)

LOG_FILENAME = sys.path[0] + "/" + 'logs.txt'
logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
