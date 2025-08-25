import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import DensityMatrix, partial_trace, Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt

import io

st.title("Quantum State Visualizer (Hackathon Prototype)")

# Demo circuit for first demo/testing
demo_code = '''
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
h q[0];
cx q[0],q[1];
'''

qasm_input = st.text_area("Paste your Quantum Circuit in QASM format (or use demo):", demo_code, height=200)

if st.button('Visualize quantum states'):
    try:
        # Parse and simulate circuit
        qc = QuantumCircuit.from_qasm_str(qasm_input)
        qc.save_statevector()
        simulator = AerSimulator(method='statevector')
        qc = transpile(qc, simulator)
        result = simulator.run(qc).result()
        state = result.get_statevector(0)
        dm_full = DensityMatrix(state)

        st.write(f"### Simulated Quantum Circuit ({qc.num_qubits} qubits)")
        st.write(qc.draw('mpl'))
        n = qc.num_qubits
        st.write(f"### Single-Qubit Reduced Density Matrices (Partial Trace + Bloch Sphere)")
        for i in range(n):
            traced = partial_trace(dm_full, [j for j in range(n) if j != i])
            st.write(f"**Qubit {i}:**")
            st.write(f"Purity of Qubit {i}: {traced.purity()}")
            # Convert reduced density matrix to statevector if pure, else use as is
            try:
                sv = Statevector(traced)
                fig = plot_bloch_multivector(sv)
            except Exception:
                fig = plot_bloch_multivector(traced)
            st.pyplot(fig)
    except Exception as e:
        st.error(f"Error: {str(e)}")