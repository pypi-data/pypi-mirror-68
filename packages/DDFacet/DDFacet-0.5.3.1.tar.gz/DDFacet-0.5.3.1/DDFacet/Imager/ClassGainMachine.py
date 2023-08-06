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

import numpy as np
from DDFacet.Other import logger
from DDFacet.Other import ClassTimeIt
from DDFacet.Other import ModColor
from DDFacet.Other.progressbar import ProgressBar
import threading

log=logger.getLogger("ClassGainMachine")

def get_instance():
    return ClassGainMachine.get_instance()

class ClassGainMachine():
    __SINGLETON__ = None
    __SINGLETON_LOCK__ = threading.Lock()
    @classmethod
    def get_instance(cls):
        return cls.__SINGLETON__

    def __init__(self,
                 GainMax=0.9,
                 GainMin=0.1,
                 SigmaScale=10.,
                 Sigma0=1.,
                 Mode="Constant"):
        # double checked locking pattern:
        if not self.get_instance():
            with ClassGainMachine.__SINGLETON_LOCK__:
                if not self.get_instance():
                    ClassGainMachine.__SINGLETON__ = self
                    self.SigmaScale=SigmaScale
                    self.Sigma0=Sigma0
                    self.Mode=Mode
                    self.GainMax=GainMax
                    self.GainMin=GainMin
                    self.CurrentGain=GainMin
        else:
            raise RuntimeError("Singleton is already initialized. This is a bug.")

    def SetRMS(self,rms):
        self.rms=rms
        
    def SetFluxMax(self,ThisFlux):
        if self.Mode=="Dynamic":
            x=np.abs(ThisFlux)
            ExpGain=self.GainMax*np.exp(-(x/(self.rms)-self.Sigma0)/self.SigmaScale)
            self.CurrentGain=np.min([self.GainMax,ExpGain])
            self.CurrentGain=np.max([self.CurrentGain,self.GainMin])
            #print "========="
            #print "Flux = %f\nRMS  = %f\nsig0 = %f\nsigs = %f\n"%(ThisFlux,self.rms,self.Sigma0,self.SigmaScale)
        else:
            self.CurrentGain=self.GainMin

    def GiveGain(self):
        return self.CurrentGain

    def Update(self,ThisFluxMax):
        self.ListFlux.append(ThisFluxMax)
        self.CurrentIter+=1
        if not((self.CurrentIter%self.IterUpdate)==0): return
            
        ArrayFlux = np.array(self.ListFlux)
        Slopes = np.abs(ArrayFlux[1::]-ArrayFlux[0:-1])
        


        if len(self.ListFlux)>LookBackStep:
            MeanSlope=np.median(Slopes[-LookBackStep::]) # cleaned Jy/Iteration
        else:
            MeanSlope=np.median(Slopes) # cleaned Jy/Iteration
            
        if MeanSlope<ThresholdAccelerate:
            self.CurrentGain*=1.1

        if self.CurrentGain>self.GainMax:
            self.CurrentGain=self.GainMax
