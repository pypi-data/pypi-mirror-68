#!/usr/bin/env python
# -*- coding: utf-8 -*-

# European Southern Observatory
# For any scientific or technical question,
# please contact usd-help@eso.org

from __future__ import print_function
import pkg_resources
import sys
import json
import getopt
from .skycalc import SkyModel
from .skycalc import AlmanacQuery


def loadTxt(inputFile):

    result = {}

    lineN = 0
    for line in inputFile.readlines():

        lineN += 1

        originalLine = line
        line = line.strip()
        if len(line) == 0 or line[0] == '#':
            continue
        line = line.split(':')
        if len(line) > 2 and line[0].strip() == 'date':
            line = [line[0], ':'.join(line[1::])]
        elif len(line) != 2 or (len(line) == 2 and (line[0].strip() == '' or
                                                    line[1].strip() == '')):
            print('WARNING: input file line ' + str(lineN) +
                  ': wrong format: ignored.')
            print(originalLine.rstrip())
            continue
        key = line[0].strip()
        value = line[1].strip()

        # Is it an integer?
        try:
            value = int(value)
        except ValueError:
            # Is it an float?
            try:
                value = float(value)
            except ValueError:
                pass

        result[key] = value

    return result


def fixObservatory(indic):

    if 'observatory' in indic:
        if indic['observatory'] == 'lasilla':
            indic['observatory'] = '2400'
        elif indic['observatory'] == 'paranal':
            indic['observatory'] = '2640'
        elif (indic['observatory'] == '3060m' or
              indic['observatory'] == 'armazones'):
            indic['observatory'] = '3060'
#        elif indic['observatory'] == '5000m':
#            indic['observatory'] = '5000'
        else:
            raise ValueError('Wrong Observatory name, please refer to the '
                             'documentation.')
    return indic


def usage():

    print('usage: skycalc_cli -i|--in inputfile -o|--out file.fits ' +
          '[-a|--alm almanacparameterfile] [-v|--verbose] [--version]')


def main():

    argv = sys.argv[1:]

    almFilename = None
    inputFilename = None
    outputFilename = None
    isVerbose = False

    # Read command line arguments
    try:
        opts, args = getopt.getopt(argv, "hva:i:o:", ["help", "verbose",
                                                      "version",
                                                      "alm=", "in=", "out="])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("--version"):
            version = pkg_resources.require("skycalc_cli")[0].version
            print('skycalc_cli version ' + version)
            sys.exit(0)
        elif opt in ("-v", "--verbose"):
            isVerbose = True
        elif opt in ("-a", "--alm"):
            almFilename = arg
        elif opt in ("-i", "--in"):
            inputFilename = arg
        elif opt in ("-o", "--out"):
            outputFilename = arg

    if not ((inputFilename or almFilename) and outputFilename):
        usage()
        sys.exit(1)

    dic = {}

    # Query the Almanac if alm option is enabled
    if almFilename:

        # Read the input parameters
        inputalmdic = None
        try:
            with open(almFilename, 'r') as f:
                inputalmdic = json.load(f)
        except ValueError:
            with open(almFilename, 'r') as f:
                inputalmdic = loadTxt(f)

        if not inputalmdic:
            raise ValueError('Error: cannot read' + almFilename)

        alm = AlmanacQuery(inputalmdic)
        dic = alm.query()

    if isVerbose:
        print('Data retrieved from the Almanac:')
        for key, value in dic.items():
            print('\t' + str(key) + ': ' + str(value))

    if inputFilename:

        # Read input parameters
        inputdic = None
        try:
            with open(inputFilename, 'r') as f:
                inputdic = json.load(f)
        except ValueError:
            with open(inputFilename, 'r') as f:
                inputdic = loadTxt(f)

        if not inputdic:
            raise ValueError('Error: cannot read ' + inputFilename)

        # Override input parameters
        if isVerbose:
            print('Data overridden by the user\'s input file:')
        for key, value in inputdic.items():
            if isVerbose and key in dic:
                print('\t' + str(key) + ': ' + str(value))
            dic[key] = value

    # Fix the observatory to fit the backend
    try:
        dic = fixObservatory(dic)
    except ValueError:
        raise

    if isVerbose:
        print('Data submitted to SkyCalc:')
        for key, value in dic.items():
            print('\t' + str(key) + ': ' + str(value))

    # Get the Sky
    skyModel = SkyModel()
    skyModel.callwith(dic)
    skyModel.write(outputFilename)
