import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import DensityMatrix, partial_trace, Statevector
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt
import io

def app():
    st.markdown("<h1 style='text-align: center; font-family: IBM Plex Sans, sans-serif; font-weight: 600; margin-bottom: 1.5rem;'>Quantum State Visualizer</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #262626; padding: 1.5rem; margin-bottom: 2rem; border-left: 4px solid #0f62fe;">
        <p style="font-family: 'IBM Plex Sans', sans-serif; font-size: 1rem; line-height: 1.5;">
            Enter your quantum circuit in QASM format below to visualize the quantum states and Bloch sphere representations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Demo circuit for first demo/testing
    demo_code = '''OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
h q[0];
cx q[0],q[1];
'''

    qasm_input = st.text_area("Paste your Quantum Circuit in QASM format (or use demo):", demo_code, height=200)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("""
        <style>
        div.stButton > button {
            background-color: #0f62fe;
            color: white;
            border: none;
            padding: 0.6rem 1rem;
            font-family: 'IBM Plex Sans', sans-serif;
            font-weight: 500;
            border-radius: 0;
            width: 100%;
        }
        div.stButton > button:hover {
            background-color: #0353e9;
        }
        </style>
        """, unsafe_allow_html=True)
        visualize_button = st.button('Visualize Quantum States', use_container_width=True)

    if visualize_button:
        try:
            # Show a loading animation
            with st.spinner("Calculating quantum states..."):
                # Parse and simulate circuit
                qc = QuantumCircuit.from_qasm_str(qasm_input)
                qc.save_statevector()
                simulator = AerSimulator(method='statevector')
                qc = transpile(qc, simulator)
                result = simulator.run(qc).result()
                state = result.get_statevector(0)
                dm_full = DensityMatrix(state)

            # Display results in a nice layout
            st.markdown("<h2 style='text-align: center; margin-top: 2.5rem; font-family: IBM Plex Sans, sans-serif; font-weight: 600;'>Simulation Results</h2>", unsafe_allow_html=True)
            
            # Circuit visualization
            st.markdown(f"<h3 style='margin-top: 2rem; font-family: IBM Plex Sans, sans-serif; font-weight: 500; color: #f4f4f4; border-bottom: 1px solid #393939; padding-bottom: 0.5rem;'>Quantum Circuit ({qc.num_qubits} qubits)</h3>", unsafe_allow_html=True)
            
            # Apply custom styling to the matplotlib figure
            fig = qc.draw('mpl', style={'backgroundcolor': '#0a1a1a', 'textcolor': '#E5E7EB'})
            st.pyplot(fig)
            
            # Bloch spheres
            st.markdown(f"<h3 style='margin-top: 2.5rem; font-family: IBM Plex Sans, sans-serif; font-weight: 500; color: #f4f4f4; border-bottom: 1px solid #393939; padding-bottom: 0.5rem;'>Qubit States (Bloch Sphere Representation)</h3>", unsafe_allow_html=True)
            
            # Create columns for Bloch spheres
            n = qc.num_qubits
            cols = st.columns(min(n, 3))
            
            for i in range(n):
                with cols[i % min(n, 3)]:
                    traced = partial_trace(dm_full, [j for j in range(n) if j != i])
                    st.markdown(f"<h4 style='text-align: center; font-family: IBM Plex Sans, sans-serif; font-weight: 500; color: #f4f4f4;'>Qubit {i}</h4>", unsafe_allow_html=True)
                    st.markdown(f"<p style='text-align: center; font-family: IBM Plex Sans, sans-serif; color: #0f62fe;'>Purity: {traced.purity():.4f}</p>", unsafe_allow_html=True)
                    
                    # Convert reduced density matrix to statevector if pure, else use as is
                    try:
                        sv = Statevector(traced)
                        fig = plot_bloch_multivector(sv)
                    except Exception:
                        fig = plot_bloch_multivector(traced)
                    
                    # Customize the figure
                    fig.patch.set_facecolor('#0a1a1a')
                    for ax in fig.get_axes():
                        ax.set_facecolor('#0a1a1a')
                        ax.tick_params(colors='#E5E7EB')
                        for spine in ax.spines.values():
                            spine.set_edgecolor('#E5E7EB')
                    
                    st.pyplot(fig)
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.markdown("""
            <div style="background-color: #2d0709; padding: 1rem; border-left: 4px solid #da1e28;">
                <p style="font-family: 'IBM Plex Sans', sans-serif; color: #f4f4f4;">Please check your QASM code and try again. Make sure it follows the correct syntax.</p>
            </div>
            """, unsafe_allow_html=True)

