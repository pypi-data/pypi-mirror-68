#!/usr/bin/env python
'''
DDFacet, a facet-based radio imaging package
Copyright (C) 2013-2016  Cyril Tasse, l'Observatoire de Paris,
SKA South Africa, Rhodes University

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from DDFacet.compatibility import range

import optparse

from DDFacet.Array import NpShared
from DDFacet.Other import logger

log= logger.getLogger("ClearSHM")
import six
if six.PY3:
    from DDFacet.cbuild.Gridder import _pyGridderSmearPols3x as _pyGridderSmear
else:
    from DDFacet.cbuild.Gridder import _pyGridderSmearPols27 as _pyGridderSmear
import glob
import os
import shutil

from DDFacet.Other import Multiprocessing
def read_options():
    desc="""CohJones Questions and suggestions: cyril.tasse@obspm.fr"""
    
    opt = optparse.OptionParser(usage='Usage: %prog <options>',version='%prog version 1.0',description=desc)

    group = optparse.OptionGroup(opt, "* SHM")
    group.add_option('--ID',help='ID of shared memory to be deleted, default is %default',default=None)
    opt.add_option_group(group)
    options, arguments = opt.parse_args()
    
    return options


if __name__=="__main__":
    options = read_options()
    print("Clear shared memory", file=log)
    if options.ID is not None:
        NpShared.DelAll(options.ID)
    else:
        NpShared.DelAll()

    Multiprocessing.cleanupStaleShm()
    Multiprocessing.cleanupShm()
    ll=glob.glob("/dev/shm/sem.*")
        
    print("Clear Semaphores", file=log)
    # remove semaphores we don't have access to
    ll = filter(lambda x: os.access(x, os.W_OK),ll)

    ListSemaphores=list(map(str, [".".join(l.split(".")[1::]) for l in ll]))

    _pyGridderSmear.pySetSemaphores(ListSemaphores)
    _pyGridderSmear.pyDeleteSemaphore()

    print("Clear shared dictionaries", file=log)
    ll=glob.glob("/dev/shm/shared_dict:*")
    ll = filter(lambda x: os.access(x, os.W_OK),ll)
    for f in ll:
        shutil.rmtree(f)
