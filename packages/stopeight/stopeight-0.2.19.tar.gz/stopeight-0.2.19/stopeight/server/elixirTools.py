#!/usr/bin/env python

# Copyright (C) 2009-2012 Specific Purpose Software GmbH

from stopeight.comparator import vectorTools
from stopeight.server.zsiTools import ABCPoint, ABCLine

from stopeight.server import server_include

from elixir import *

metadata.bind = server_include.metadata_bind
metadata.bind.echo = server_include.metadata_bind_echo

class DBPoint(ABCPoint,Entity):
    using_options(tablename='points')
    x = Field(Integer)
    y = Field(Integer)
    line = ManyToOne('DBLine')

class DBLine(ABCLine,Entity):
    using_options(tablename='slines')
    points = OneToMany('DBPoint')

    def store(self):
        # not needed if default autoFlush=true
        #session.flush()
        # needed if default autoCommit=false
        session.commit()
        pass

    @staticmethod
    def get(key):
        return DBLine.get_by(id=key)

    @staticmethod
    def getAll():
        return DBLine.query.all()

    def remove(self):
        # for some reason elixir does not support this, we have to do it manually...
        #points = DBPoint.query.filter_by(line_id=dbline.id)
        for p in self.points:
            p.delete()
        self.delete()
        self.store()

    @staticmethod
    def from_numpy_array(mynumpyarray):
        line = DBLine()
        for vector in mynumpyarray:
            point = DBPoint()
            point.x=int(vector[0])
            point.y=int(vector[1])
            line.add_point(point)
        return line

setup_all()

def create_database():
    create_all()
    print('elixirTools.py::create_database on '+str(metadata.bind))

if __name__ == "__main__":
    create_database()
    
def storage_example():
    import numpy
    vector = DBLine.from_numpy_array(numpy.array([[13,40],[50,125],[80,61],[123,79],[191,11]]))
    vector.store()
    for dbrecord in DBLine.getAll():
        print(str(dbrecord.to_numpy_array()))

