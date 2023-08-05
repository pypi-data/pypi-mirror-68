#!/usr/bin/env python

# Copyright (C) 2009-2012 Specific Purpose Software GmbH

from ZODB.FileStorage import FileStorage
from ZODB.DB import DB

from stopeight.logging import logSwitch
log = logSwitch.logPrint()

from stopeight.server import server_include

import os
if not os.path.isfile(server_include.zodb_filename):
    print('import stopeight.server.zodbTools: Please create database file first.')
    print('Like: '+'storage = FileStorage(server_include.zodb_filename)')
else:
    storage = FileStorage(server_include.zodb_filename)
    db = DB(storage)
    connection = db.open()
    root = connection.root()
    log.debug('zodb File-Database connection opened...')

    import atexit
    def close_database():
        db.close()
        log.debug('...zodb Database connection closed.')

    atexit.register(close_database)

from stopeight.comparator import vectorTools
from stopeight.server import zsiTools
from stopeight.server.zsiTools import ABCPoint,ABCLine

class DBPoint(ABCPoint):
    pass

import persistent,transaction

class DBLine(ABCLine,persistent.Persistent):
    def __init__(self, **args):
        ABCLine.__init__(self, **args)
        if len(root.keys())>0:
            self.id = root.keys()[-1] + 1
        else:
            self.id = 1

    def store(self):
        root[self.id]=self
        transaction.commit()
        pass

    @staticmethod
    def get(key):
        try:
            return root[key]
        except:
            raise Exception('database object id %d not found'%(key))

    @staticmethod
    def getAll():
        return root.values()

    def remove(self):
        try:
            del root[self.id]
            transaction.commit()
        except Exception:
            raise Exception('Error has ocurred during deletion of id %d'%(self.id))

    @staticmethod
    def from_numpy_array(mynumpyarray):
        line = DBLine()
        for vector in mynumpyarray:
            point = DBPoint()
            point.x=int(vector[0])
            point.y=int(vector[1])
            line.add_point(point)
        return line

if __name__ == "__main__":
    pass

def storage_example():
    import numpy
    vector = DBLine.from_numpy_array(numpy.array([[13,40],[50,125],[80,61],[123,79],[191,11]]))
    vector.store()
    for dbrecord in DBLine.getAll():
        print(dbrecord.to_numpy_array())
