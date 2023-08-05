#!/usr/bin/env python

# Copyright (C) 2009-2012 Specific Purpose Software GmbH

from ZSI import dispatch
from stopeight.server import zsiTools
from stopeight.server import zsiServer

def run(port):
    """ This will launch a SOAP server.
        The default port can be found in :mod:`stopeight.server.server_include` or supplied as an argument
    """
    dispatch.AsServer(port,modules=(zsiServer,),typesmodule=zsiTools,rpc=True)

if __name__ == "__main__":
    from stopeight.server import server_include
    run(server_include.server_port)
