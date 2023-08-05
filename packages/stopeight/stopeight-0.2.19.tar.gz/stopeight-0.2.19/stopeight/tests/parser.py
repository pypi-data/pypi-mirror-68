#!/usr/bin/env python

# Copyright (C) 2017 Fassio Blatter

from stopeight.logging import logSwitch
log = logSwitch.logPrint()
from stopeight.util import tableau_printer

import os

from stopeight import legacy

import numpy

def find_files(dir_path,suffix='.sp'):
    paths = []
    if os.path.isdir(dir_path):
        log.debug('Parsing directory ' + dir_path)
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if f.endswith(suffix):
                    final_path = os.path.join(root,f)
                    paths.append(final_path)
    else:
        raise Exception('Path ' + dir_path + ' is not a directory under ' + os.getcwd())
    return paths

def process_directory(dir_path,analyzer=legacy.stroke_parallel):
    tprinter = tableau_printer.tPrinter('parser.out',6)
    lines = []
    files = find_files(dir_path)
    count = 0
    for final_path in files:
        log.info('Loading file ' + final_path + '... ')
        try:
            graph = legacy.parse_file(final_path)
            count+=1
            tprinter.draw(graph)
            try:
                points = analyzer(graph)
                tprinter.draw(points)
                try:
                    lines.append(numpy.array(points))
                except:
                    log.info('Cast from Analyzer Failed')
                log.info('Success')
            except:
                log.info('Analyzer Failed')
                tprinter.text('#' + str(count) + str(final_path) + ' parser failed.')
        except:
            log.info('Loading Failed')
    tprinter.text('Extracted ' + str(len(lines)) + ' Comparator lines out of ' + str(count) + ' readable Graph files.')
    tprinter.write()

    return lines

from stopeight.multiprocessing import pooling

if __name__ == '__main__':
    nopath = False
    import sys
    if len(sys.argv)>1:
        if sys.argv[1]==None:
            nopath = True
    else:
        nopath = True
    if nopath:
        raise Exception("Please specify the directory containing unpacked legacy pen-stroke files (i.e. stopeight-clibs/legacy/tests/)")
    lines = process_directory(sys.argv[1],legacy.stroke_sequential)
    comparator = pooling.MPLine(lines)
    for i,line in enumerate(lines):
        matches = comparator.matchLine(line)
        print('Line ' + str(i) + ' matched ' + str(len(matches)) + ' occurences ' + str(matches))
