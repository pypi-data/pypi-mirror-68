#!/usr/bin/env python

# Copyright (C) 2017 Fassio Blatter

import os
import numpy

import stopeight.logging as log
log.disable(log.WARNING)

def find_files(dir_path,suffix='.npy',base_dir=os.getcwd()):
    dir_path = os.path.join(base_dir,dir_path)
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

def process_directory(dir_path,suffix,file_adapter,analyzer,base_dir=os.getcwd(),filename:str=None,drawResize=True):
    if filename != None:
        from stopeight.util import tableau_printer
        tprinter = tableau_printer.tPrinter(filename,6)
    lines = []
    files = find_files(dir_path,suffix,base_dir)
    count = 0
    succeeded = 0
    for final_path in files:
        try:
            graph = file_adapter(final_path)
            log.info("SUCCESS: "+str(file_adapter.__name__) + " " + final_path)
            count+=1
            if filename != None:
                tprinter.draw(graph,drawResize)
            try:
                points = analyzer(graph)
                succeeded+=1
                if filename != None:
                    tprinter.draw(points,drawResize)
                try:
                    lines.append(points)
                except:
                    log.critical("Cast from Analyzer Failed")
                    return
            except:
                log.warning("FAILED: "+str(analyzer.__name__))
                if filename != None:
                    tprinter.text("#" + str(count) + " " + str(final_path))
        except:
            log.warning("FAILED: "+str(file_adapter.__name__) + " " + final_path)
    if filename != None:
        tprinter.text("Extracted " + str(len(lines)) + " Comparator lines out of " + str(count) + " readable Graph files.")
        tprinter.write()
    if len(lines)!=count:
        log.critical(str(len(files)-count) + " files out of " + str(len(files)) + " corrupted.")
    if count!=succeeded:
        log.critical(str(count-succeeded)+" inputs out of "+str(count)+" failed.")
    return lines
