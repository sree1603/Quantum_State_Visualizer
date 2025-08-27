# pages/realms.py

import streamlit as st
from streamlit_lottie import st_lottie
import requests
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_bloch_multivector
import matplotlib.pyplot as plt

def app():
    # --- Asset Loading ---
    @st.cache_data
    def load_lottieurl(url: str):
        """Helper function to load Lottie animation from URL."""
        try:
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                return None
            return r.json()
        except requests.exceptions.RequestException:
            return None

    # Lottie animations for Quantum Citizens
    LOTTIE_URLS = {
        "idle": "https://assets6.lottiefiles.com/packages/lf20_vjyb0d7k.json",
        "superposition": "https://assets9.lottiefiles.com/packages/lf20_jR22ei.json",
        "entangled": "https://assets5.lottiefiles.com/packages/lf20_f1dhz0e5.json",
        "success": "https://assets1.lottiefiles.com/packages/lf20_touohb1k.json"
    }
    lottie_animations = {name: load_lottieurl(url) for name, url in LOTTIE_URLS.items()}

    # Comic panel images
    COMIC_URL_BRIEFING = "https://placehold.co/800x300/0D1117/FFFFFF?text=Comic+Panel%0AProfessor+Qubit+and+the+Spooky+Link"
    COMIC_URL_SUCCESS = "https://placehold.co/800x300/0D1117/28A745?text=Mission+Complete!%0AThe+citizens+are+entangled!"

    # --- Custom UI Styling ---
    st.markdown("""
    <style>
        /* Core App Styling */
        .stApp {
            background: url("https://images.unsplash.com/photo-1534796636912-3b95b3ab5986?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2071&q=80");
            background-size: cover;
        }

        /* Main content area */
        .main .block-container {
            padding-top: 2rem; padding-bottom: 2rem;
            padding-left: 5rem; padding-right: 5rem;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: rgba(13, 17, 23, 0.8);
            backdrop-filter: blur(10px);
            border-right: 1px solid #4A00E0;
        }
        
        /* Custom Buttons */
        .stButton>button {
            border: 2px solid #8E2DE2; border-radius: 10px;
            color: white; background-color: rgba(74, 0, 224, 0.3);
            transition: all 0.3s ease-in-out;
            box-shadow: 0 0 15px rgba(142, 45, 226, 0.5);
            font-family: 'Courier New', Courier, monospace;
            font-weight: bold; font-size: 1.2rem;
            height: 4em; /* Ensure buttons have consistent height */
        }
        .stButton>button:hover {
            background-color: #4A00E0; border-color: #FFFFFF;
            box-shadow: 0 0 25px rgba(255, 255, 255, 0.7);
        }
        
        /* Custom Containers */
        .custom-container {
            background-color: rgba(13, 17, 23, 0.8);
            backdrop-filter: blur(5px); border: 1px solid #4A00E0;
            border-radius: 15px; padding: 2rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }
        
        /* Typography */
        h1, h2, h3, h4 {
            color: #FFFFFF;
            text-shadow: 0 0 8px rgba(142, 45, 226, 0.8);
        }

        /* CNOT Connector Line Style */
        .cnot-line-container {
            position: relative;
            width: 100%;
            height: 4em; /* Match button height */
            margin-top: -4.5em; /* Pull up to align with buttons */
            margin-bottom: -1em; /* Reduce space below */
        }
        .cnot-line {
            position: absolute;
            left: 50%;
            top: 20%; /* Start below the top button */
            bottom: 20%; /* End above the bottom button */
            width: 4px;
            background-color: #8E2DE2;
            box-shadow: 0 0 10px #8E2DE2;
            transform: translateX(-50%);
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Quantum Logic ---
    def get_state_label(statevector):
        """Determine the state of the qubits from the statevector."""
        is_bell_state = np.allclose(statevector, [1/np.sqrt(2), 0, 0, 1/np.sqrt(2)]) or \
                        np.allclose(statevector, [0, 1/np.sqrt(2), 1/np.sqrt(2), 0]) or \
                        np.allclose(statevector, [1/np.sqrt(2), 0, 0, -1/np.sqrt(2)]) or \
                        np.allclose(statevector, [0, 1/np.sqrt(2), -1/np.sqrt(2), 0])
        
        if is_bell_state:
            return "entangled", "entangled"

        prob_q0_is_0 = np.abs(statevector[0])**2 + np.abs(statevector[1])**2
        prob_q1_is_0 = np.abs(statevector[0])**2 + np.abs(statevector[2])**2
        
        q0_state = "superposition" if 0.01 < prob_q0_is_0 < 0.99 else "idle"
        q1_state = "superposition" if 0.01 < prob_q1_is_0 < 0.99 else "idle"
        
        return q0_state, q1_state

    def run_circuit(circuit_grid):
        """Builds and simulates the quantum circuit."""
        qc = QuantumCircuit(2, 2)
        num_steps = len(circuit_grid[0])

        for step in range(num_steps):
            gate_q0 = circuit_grid[0][step]
            gate_q1 = circuit_grid[1][step]

            if gate_q0 == 'H': qc.h(0)
            elif gate_q0 == 'X': qc.x(0)
            
            if gate_q1 == 'H': qc.h(1)
            elif gate_q1 == 'X': qc.x(1)

            if gate_q0 == 'CNOT_C' and gate_q1 == 'CNOT_T':
                qc.cx(0, 1)
            elif gate_q0 == 'CNOT_T' and gate_q1 == 'CNOT_C':
                qc.cx(1, 0)
            
            qc.barrier()

        simulator = Aer.get_backend('statevector_simulator')
        job = simulator.run(qc)
        result = job.result()
        statevector = result.get_statevector()
        
        plt.close('all')
        bloch_fig = plot_bloch_multivector(statevector)
        
        q0_state, q1_state = get_state_label(statevector)
        
        return statevector, bloch_fig, q0_state, q1_state

    # --- Session State Initialization ---
    if 'circuit_grid' not in st.session_state:
        st.session_state.circuit_grid = [[None] * 3 for _ in range(2)]
    if 'selected_gate' not in st.session_state:
        st.session_state.selected_gate = 'H'
    if 'mission_complete' not in st.session_state:
        st.session_state.mission_complete = False
    if 'comic_url' not in st.session_state:
        st.session_state.comic_url = COMIC_URL_BRIEFING

    # --- UI Components ---
    with st.sidebar:
        st.markdown("<h1>Gate Palette</h1>", unsafe_allow_html=True)
        st.markdown("Select a gate, then click a slot to place it. Click a placed gate to remove it.")
        
        gate_options = {
            "Hadamard (H)": "H",
            "Pauli-X (X)": "X",
            "CNOT (Control ●)": "CNOT_C",
            "CNOT (Target ⊕)": "CNOT_T"
        }
        
        selected_gate_label = st.radio(
            "Available Gates",
            options=gate_options.keys(),
            index=0,
            label_visibility="collapsed"
        )
        st.session_state.selected_gate = gate_options[selected_gate_label]
        
        st.markdown("---")
        if st.button("Reset Circuit", use_container_width=True):
            st.session_state.circuit_grid = [[None] * 3 for _ in range(2)]
            st.session_state.mission_complete = False
            st.session_state.comic_url = COMIC_URL_BRIEFING
            st.toast("Circuit has been reset!", icon="🧹")
            st.rerun()

    st.title("🌌 Quantum Realms: The State Architect")
    st.header("Mission 01: Create a Bell State")

    with st.expander("📖 View Mission Briefing (Comic)", expanded=True):
        st.image(st.session_state.comic_url)
        
    # --- NEW: State Showcase ---
    with st.expander("🔬 State Showcase: Meet the Quantum Citizens!", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<h4>Idle State</h4>", unsafe_allow_html=True)
            if lottie_animations["idle"]:
                st_lottie(lottie_animations["idle"], height=150, key="showcase_idle")
            st.info("The Citizen is in a definite state, either **0** or **1**. It's resting and waiting for a command.")

        with col2:
            st.markdown("<h4>Superposition</h4>", unsafe_allow_html=True)
            if lottie_animations["superposition"]:
                st_lottie(lottie_animations["superposition"], height=150, key="showcase_superposition")
            st.info("The Citizen is in a mix of both **0 and 1** at the same time, like a spinning coin before it lands.")
            
        with col3:
            st.markdown("<h4>Entangled State</h4>", unsafe_allow_html=True)
            if lottie_animations["entangled"]:
                st_lottie(lottie_animations["entangled"], height=150, key="showcase_entangled")
            st.info("Two Citizens are spookily linked. Measuring one instantly determines the state of the other!")

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Interactive Circuit Builder ---
    with st.container():
        st.markdown('<div class="custom-container">', unsafe_allow_html=True)
        
        c1, c2 = st.columns([2, 3])

        with c1:
            st.subheader("Quantum Circuit Canvas")
            grid_cols = st.columns(len(st.session_state.circuit_grid[0]))
            
            for j, col in enumerate(grid_cols):
                with col:
                    gate_q0 = st.session_state.circuit_grid[0][j]
                    label_q0 = gate_q0.replace('_C', '●').replace('_T', '⊕') if gate_q0 else " "
                    if st.button(label_q0, key=f'btn_0_{j}', use_container_width=True):
                        st.session_state.circuit_grid[0][j] = st.session_state.selected_gate if not gate_q0 else None
                        st.rerun()
                        
                    gate_q1 = st.session_state.circuit_grid[1][j]
                    label_q1 = gate_q1.replace('_C', '●').replace('_T', '⊕') if gate_q1 else " "
                    if st.button(label_q1, key=f'btn_1_{j}', use_container_width=True):
                        st.session_state.circuit_grid[1][j] = st.session_state.selected_gate if not gate_q1 else None
                        st.rerun()

                    is_cnot_pair = (gate_q0 == 'CNOT_C' and gate_q1 == 'CNOT_T') or \
                                   (gate_q0 == 'CNOT_T' and gate_q1 == 'CNOT_C')
                    if is_cnot_pair:
                        st.markdown('<div class="cnot-line-container"><div class="cnot-line"></div></div>', unsafe_allow_html=True)

        statevector, bloch_fig, q0_state, q1_state = run_circuit(st.session_state.circuit_grid)

        with c2:
            st.subheader("Real-Time Visualization")
            
            viz_col1, viz_col2 = st.columns(2)
            
            with viz_col1:
                st.write("**Citizen Q0**")
                anim = lottie_animations.get(q0_state)
                if anim:
                    st_lottie(anim, height=150, key=f"lottie_q0_{q0_state}")
                st.write(f"State: `{q0_state.capitalize()}`")

            with viz_col2:
                st.write("**Citizen Q1**")
                anim = lottie_animations.get(q1_state)
                if anim:
                    st_lottie(anim, height=150, key=f"lottie_q1_{q1_state}")
                st.write(f"State: `{q1_state.capitalize()}`")
            
            st.markdown("---")
            st.write("**Combined State Analysis (Bloch Spheres)**")
            st.pyplot(bloch_fig)

        st.markdown('</div>', unsafe_allow_html=True)

    # --- Mission Completion Logic ---
    target_bell_state = np.array([1/np.sqrt(2), 0, 0, 1/np.sqrt(2)])
    if np.allclose(statevector, target_bell_state):
        if not st.session_state.mission_complete:
            st.session_state.mission_complete = True
            st.session_state.comic_url = COMIC_URL_SUCCESS
            st.balloons()
            st.toast("BELL STATE CREATED!", icon="🎉")
            st.rerun()

    if st.session_state.mission_complete:
        st.success("### 🎉 Mission Complete! 🎉\nYou've successfully entangled two qubits and created a Bell State.")
        if lottie_animations["success"]:
            st_lottie(lottie_animations["success"], key="success_anim", height=200)