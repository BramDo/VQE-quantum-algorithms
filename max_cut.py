from qiskit import IBMQ
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from qiskit import BasicAer 
from qiskit.aqua import *
from qiskit.aqua.input import EnergyInput
from qiskit.aqua.algorithms import VQE, ExactEigensolver
from qiskit.aqua.components.optimizers import SPSA
from qiskit.aqua.components.variational_forms import RY
from qiskit.aqua.translators.ising import max_cut
from qiskit.aqua import QuantumInstance

n=4 # Number of nodes in graph
G=nx.Graph()
G.add_nodes_from(np.arange(0,n,1))
elist=[(0,1,1.0),(0,3,1.0),(1,2,1.0),(2,3,1.0)]
# tuple is (i,j,weight) where (i,j) is the edge
G.add_weighted_edges_from(elist)
print(list(nx.connected_components(G)))
print(list(G.edges))
square_ring = list(G.edges)
print(square_ring)

w = np.zeros([n,n])
for i in range(n):
    for j in range(n):
        temp = G.get_edge_data(i,j,default=0)
        if temp != 0:
            w[i,j] = temp['weight']
print(w)


qubitOp, offset = max_cut.get_max_cut_qubitops(w)

algo_input = EnergyInput(qubitOp)

seed = 10598

spsa = SPSA(max_trials=300)
ry = RY(qubitOp.num_qubits, depth=5, entanglement='linear')
vqe = VQE(qubitOp, ry, spsa, 'matrix')

backend = BasicAer.get_backend('statevector_simulator')
quantum_instance = QuantumInstance(backend, seed=seed, seed_transpiler=seed)

result = vqe.run(quantum_instance)

"""declarative approach
algorithm_cfg = {
    'name': 'VQE',
    'operator_mode': 'matrix'
}

optimizer_cfg = {
    'name': 'SPSA',
    'max_trials': 300
}

var_form_cfg = {
    'name': 'RY',
    'depth': 5,
    'entanglement': 'linear'
}

params = {
    'problem': {'name': 'ising', 'random_seed': seed},
    'algorithm': algorithm_cfg,
    'optimizer': optimizer_cfg,
    'variational_form': var_form_cfg,
    'backend': {provider': 'qiskit.BasicAer', 'name': 'statevector_simulator'}
}

result = run_algorithm(params, algo_input)
"""
x = max_cut.sample_most_likely(result['eigvecs'][0])

print('energy:', result['energy'])
print('solution:', max_cut.get_graph_solution(x))

