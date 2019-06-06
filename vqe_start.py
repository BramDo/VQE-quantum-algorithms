#!/usr/bin/env python
# coding: utf-8

# # _*Using Qiskit Aqua algorithms, a how to guide*_
# 
# This notebook demonstrates how to use the `Qiskit Aqua` library to invoke a specific algorithm and process the result.
# 
# Further information is available for the algorithms in the github repo aqua/readme.md



from qiskit.aqua import Operator, run_algorithm
from qiskit.aqua.input import EnergyInput


# Here an Operator instance is created for our Hamiltonian. In this case the paulis are from a previously computed Hamiltonian for simplicity

pauli_dict = {
    'paulis': [{"coeff": {"imag": 0.0, "real": 1}, "label": "Z"},
              
              ]
}

qubitOp = Operator.load_from_dict(pauli_dict)
print(qubitOp)

algorithm_cfg = {
    'name': 'VQE',
    'operator_mode': 'matrix'
}

optimizer_cfg = {
    'name': 'L_BFGS_B',
    'maxfun': 1000
}

var_form_cfg = {
    'name': 'RYRZ',
    'depth': 3,
    'entanglement': 'linear'
}

params = {
    'algorithm': algorithm_cfg,
    'optimizer': optimizer_cfg,
    'variational_form': var_form_cfg,
    'backend': {'name': 'statevector_simulator'}
}

algo_input = EnergyInput(qubitOp)
result = run_algorithm(params,algo_input)
print(result)


# Now we want VQE and so change it and add its other configuration parameters. VQE also needs and optimizer and variational form. While we can omit them from the dictionary, such that defaults are used, here we specify them explicitly so we can set their parameters as we desire.








