

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 19:16:11 2019

@author: bram
"""

import numpy as np
from pyquil.api import WavefunctionSimulator

from grove.pyqaoa.maxcut_qaoa import maxcut_qaoa
steps = 2
square_ring = [(0,1),(1,2),(2,3),(3,0)]

inst = maxcut_qaoa(square_ring, steps=steps)
opt_betas, opt_gammas = inst.get_angles()

t = np.hstack((opt_betas, opt_gammas))
param_prog = inst.get_parameterized_program()
prog = param_prog(t)
wf = WavefunctionSimulator().wavefunction(prog)
wf = wf.amplitudes

for state_index in range(inst.nstates):
    print(inst.states[state_index], np.conj(wf[state_index]) * wf[state_index])