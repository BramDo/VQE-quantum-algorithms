#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 18:09:04 2019

@author: bram
"""


import numpy as np
from scipy.optimize import minimize

from pyquil import Program, get_qc

#==============================================================================
# Variational-Quantum-Eigensolver
#==============================================================================
# Create connection with QVM
qc = get_qc('2q-qvm')

# Define matrix
from pyquil.paulis import sZ
H = sZ(0)

# Define ansatz
from pyquil.gates import RY
def ansatz(params):
    return Program(RY(params[0], 0))


from grove.pyvqe.vqe import VQE

vqe = VQE(minimizer=minimize, minimizer_kwargs={'method': 'nelder-mead',
          'options':{'initial_simplex': np.array([[0.0],[0.05]]), 'xatol': 1.0e-2}})

initial_params = [0.0]
result = vqe.vqe_run(ansatz, H, initial_params, samples=10000, qc=qc)
print(result)

