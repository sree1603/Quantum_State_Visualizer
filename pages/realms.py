# pages/realms.py

import streamlit as st
from streamlit_lottie import st_lottie
import requests
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_bloch_multivector

def app(): # 👈 WRAP EVERYTHING IN THIS FUNCTION
    # --- Page Configuration ---
    # This is now controlled by app.py, but we can set specific styles here if needed.
    # st.set_page_config(...) # You can remove this line

    # --- Asset Loading ---
    def load_lottieurl(url: str):
        """Helper function to load Lottie animation from URL."""
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    # Lottie animations for Quantum Citizens
    LOTTIE_URLS = {
        "idle": "https://assets6.lottiefiles.com/packages/lf20_vjyb0d7k.json",
        "superposition": "https://assets9.lottiefiles.com/packages/lf20_jR22ei.json",
        "entangled": "https://assets5.lottiefiles.com/packages/lf20_f1dhz0e5.json",
        "success": "https://assets1.lottiefiles.com/packages/lf20_touohb1k.json"
    }
    lottie_animations = {name: load_lottieurl(url) for name, url in LOTTIE_URLS.items()}

    # Placeholder for comic panel image
    COMIC_URL = "https://placehold.co/800x300/0D1117/FFFFFF?text=Comic+Panel%0AProfessor+Qubit+and+the+Spooky+Link"

    # --- Custom UI Styling (Inspired by modern game UI) ---
    st.markdown("""
    <style>
        /* Core App Styling */
        .stApp {
            background: url("https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2071&q=80");
            background-size: cover;
        }

        /* Main content area */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }

        /* Sidebar Styling */
        .st-emotion-cache-16txtl3 {
            background-color: rgba(13, 17, 23, 0.8);
            backdrop-filter: blur(10px);
            border-right: 1px solid #4A00E0;
        }
        .st-emotion-cache-16txtl3 h1, .st-emotion-cache-16txtl3 .st-emotion-cache-1g8p3r6 {
            color: #FFFFFF;
            text-shadow: 0 0 10px #8E2DE2;
        }
        
        /* Custom Buttons */
        .stButton>button {
            border: 2px solid #8E2DE2;
            border-radius: 10px;
            color: white;
            background-color: rgba(74, 0, 224, 0.3);
            transition: all 0.3s ease-in-out;
            box-shadow: 0 0 15px rgba(142, 45, 226, 0.5);
        }
        .stButton>button:hover {
            background-color: #4A00E0;
            border-color: #FFFFFF;
            box-shadow: 0 0 25px rgba(255, 255, 255, 0.7);
        }
        .stButton>button:active {
            background-color: #3c00b3 !important;
        }

        /* Custom Containers (for circuits, visualizations, etc.) */
        .custom-container {
            background-color: rgba(13, 17, 23, 0.8);
            backdrop-filter: blur(5px);
            border: 1px solid #4A00E0;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        
        /* Expander for Comic Panel */
        .st-emotion-cache-p5msec {
            background-color: rgba(13, 17, 23, 0.9);
            border-radius: 10px;
            border: 1px solid #4A00E0;
        }

        /* Typography */
        h1, h2, h3 {
            color: #FFFFFF;
            text-shadow: 0 0 8px rgba(142, 45, 226, 0.8);
        }
    </style>
    """, unsafe_allow_html=True)


    # --- Quantum Logic ---
    def get_state_label(statevector):
        """Determine the state of the qubits from the statevector."""
        is_bell_state = np.allclose(statevector, [1/np.sqrt(2), 0, 0, 1/np.sqrt(2)]) or \
                          np.allclose(statevector, [0, 1/np.sqrt(2), 1/np.sqrt(2), 0])
        
        if is_bell_state:
            return "entangled", "entangled"

        prob_q0_is_0 = np.abs(statevector[0])**2 + np.abs(statevector[1])**2
        
        q0_state = "superposition" if 0.01 < prob_q0_is_0 < 0.99 else "idle"
        q1_state = "superposition" if 0.01 < (np.abs(statevector[0])**2 + np.abs(statevector[2])**2) < 0.99 else "idle"

        if q0_state == "idle" and q1_state == "idle":
            return "idle", "idle"
            
        return q0_state, q1_state

    def run_circuit(circuit_grid):
        """Builds and simulates the quantum circuit."""
        qc = QuantumCircuit(2, 2)
        num_steps = len(circuit_grid[0])

        for step in range(num_steps):
            gate_q0 = circuit_grid[0][step]
            if gate_q0 == 'H':
                qc.h(0)
            elif gate_q0 == 'X':
                qc.x(0)
            
            gate_q1 = circuit_grid[1][step]
            if gate_q1 == 'H':
                qc.h(1)
            elif gate_q1 == 'X':
                qc.x(1)

            if gate_q0 == 'CNOT_C' and gate_q1 == 'CNOT_T':
                qc.cx(0, 1)
            elif gate_q0 == 'CNOT_T' and gate_q1 == 'CNOT_C':
                qc.cx(1, 0)
            
            qc.barrier()

        # Simulate and get the statevector
        simulator = Aer.get_backend('statevector_simulator')
        job = simulator.run(qc) # Replace execute() with the simulator's run() method
        result = job.result()   # Get the result from the job
        statevector = result.get_statevector()
                
        bloch_fig = plot_bloch_multivector(statevector)
        
        q0_state, q1_state = get_state_label(statevector)
        
        return statevector, bloch_fig, q0_state, q1_state

    # --- Session State Initialization ---
    if 'circuit_grid' not in st.session_state:
        st.session_state.circuit_grid = [[None, None, None] for _ in range(2)]
    if 'selected_gate' not in st.session_state:
        st.session_state.selected_gate = None
    if 'mission_complete' not in st.session_state:
        st.session_state.mission_complete = False

    # --- UI Components ---
    with st.sidebar:
        st.markdown("<h1>Gate Palette</h1>", unsafe_allow_html=True)
        st.markdown("Select a gate, then click on a slot in the circuit to place it.")
        
        if st.button("Hadamard (H)"):
            st.session_state.selected_gate = 'H'
        if st.button("Pauli-X (X)"):
            st.session_state.selected_gate = 'X'
        if st.button("CNOT (Control)"):
            st.session_state.selected_gate = 'CNOT_C'
        if st.button("CNOT (Target)"):
            st.session_state.selected_gate = 'CNOT_T'
        
        st.markdown("---")
        if st.button("Reset Circuit"):
            st.session_state.circuit_grid = [[None, None, None] for _ in range(2)]
            st.session_state.mission_complete = False
            st.rerun()

        st.markdown(f"**Selected Gate:** `{st.session_state.selected_gate}`")

    st.title("🌌 Quantum Realms: The State Architect")
    st.header("Mission 01: Create a Bell State")

    with st.expander("📖 View Mission Briefing (Comic)"):
        st.image(COMIC_URL, caption="Professor Qubit explains the spooky link between two particles.")

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="custom-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 3])

        with col1:
            st.subheader("Quantum Circuit Canvas")
            st.write("Construct a circuit to entangle the two Quantum Citizens.")
            
            for i in range(2):
                st.write(f"**Citizen Q{i}**")
                cols = st.columns(len(st.session_state.circuit_grid[0]))
                for j in range(len(st.session_state.circuit_grid[0])):
                    with cols[j]:
                        gate = st.session_state.circuit_grid[i][j]
                        gate_label = gate.replace('_C', ' ●').replace('_T', ' ⊕') if gate else " "
                        if st.button(gate_label, key=f'btn_{i}_{j}', use_container_width=True):
                            st.session_state.circuit_grid[i][j] = st.session_state.selected_gate
                            st.rerun()

        statevector, bloch_fig, q0_state, q1_state = run_circuit(st.session_state.circuit_grid)

        with col2:
            st.subheader("Real-Time Visualization")
            
            viz_col1, viz_col2 = st.columns(2)
            
            with viz_col1:
                st.write("**Citizen Q0**")
                animation_key = q0_state
                if lottie_animations[animation_key]:
                    st_lottie(lottie_animations[animation_key], height=150, key=f"lottie_q0_{animation_key}")
                st.write(f"State: `{q0_state.capitalize()}`")

            with viz_col2:
                st.write("**Citizen Q1**")
                animation_key = q1_state
                if lottie_animations[animation_key]:
                    st_lottie(lottie_animations[animation_key], height=150, key=f"lottie_q1_{animation_key}")
                st.write(f"State: `{q1_state.capitalize()}`")
                
            st.markdown("---")
            st.write("**Combined State Analysis**")
            st.pyplot(bloch_fig)

        st.markdown('</div>', unsafe_allow_html=True)

    target_bell_state = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
    if np.allclose(statevector, target_bell_state) and not st.session_state.mission_complete:
        st.session_state.mission_complete = True
        st.balloons()
        st.toast("BELL STATE CREATED!", icon="🎉")

    if st.session_state.mission_complete:
        st.success("### 🎉 Mission Complete! 🎉\nYou've successfully entangled two qubits and created a Bell State. Professor Qubit is proud!")
        if lottie_animations["success"]:
            st_lottie(lottie_animations["success"], key="success_anim")