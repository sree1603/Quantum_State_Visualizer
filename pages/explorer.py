# pages/explorer.py

import streamlit as st
import numpy as np
import plotly.graph_objects as go

def app():
    # --- Page Configuration & Styling ---
    # st.set_page_config(layout="wide") # This is now controlled by the main app.py

    st.markdown("""
    <style>
        /* Core App Styling */
        .stApp {
            background-color: #0D1117;
        }

        /* Main content area */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 3rem;
            padding-right: 3rem;
        }

        /* Custom Title */
        h1 {
            color: #FFFFFF;
            text-shadow: 0 0 15px rgba(0, 191, 255, 0.8);
            text-align: center;
        }
        
        /* Custom Sub-headers */
        h3 {
            color: #00BFFF; /* DeepSkyBlue */
            border-bottom: 2px solid #00BFFF;
            padding-bottom: 5px;
            margin-top: 2rem;
        }

        /* Slider Styling */
        .stSlider [data-baseweb="slider"] {
            -webkit-appearance: none;
            width: 100%;
            height: 10px;
            background: #2c3e50;
            outline: none;
            opacity: 0.7;
            -webkit-transition: .2s;
            transition: opacity .2s;
            border-radius: 5px;
        }
        
        /* Code Block Styling */
        .stCodeBlock {
            border: 1px solid #00BFFF;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 191, 255, 0.3);
        }
        
        /* Progress Bar Styling */
        .st-emotion-cache-zt5igj {
            background-color: #00BFFF;
        }
    </style>
    """, unsafe_allow_html=True)

    # --- Helper Functions ---
    def get_state_label(theta):
        """Determines the state label based on the theta angle."""
        if np.isclose(theta, 0):
            return "Basis |0⟩", "success"
        elif np.isclose(theta, np.pi):
            return "Basis |1⟩", "error"
        else:
            return "Superposition", "info"

    def create_bloch_sphere(theta, phi):
        """Creates an interactive 3D Bloch sphere visualization using Plotly."""
        # Calculate Cartesian coordinates for the state vector
        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)

        fig = go.Figure()

        # 1. Add the sphere surface
        fig.add_trace(go.Surface(
            x=np.outer(np.cos(np.linspace(0, 2*np.pi, 30)), np.sin(np.linspace(0, np.pi, 30))),
            y=np.outer(np.sin(np.linspace(0, 2*np.pi, 30)), np.sin(np.linspace(0, np.pi, 30))),
            z=np.outer(np.ones(30), np.cos(np.linspace(0, np.pi, 30))),
            colorscale=[[0, '#1c2833'], [1, '#283747']],
            opacity=0.3,
            showscale=False,
            cmin=-1, cmax=1
        ))

        # 2. Add the state vector
        fig.add_trace(go.Scatter3d(
            x=[0, x], y=[0, y], z=[0, z],
            mode='lines',
            line=dict(color='#00BFFF', width=8),
            name='State Vector |ψ⟩'
        ))
        
        # Add a cone at the tip for direction
        fig.add_trace(go.Cone(
            x=[x], y=[y], z=[z],
            u=[x], v=[y], w=[z],
            sizemode="absolute", sizeref=0.05,
            showscale=False,
            colorscale=[[0, '#00BFFF'], [1, '#00BFFF']],
            anchor="tip"
        ))

        # 3. Add basis state annotations
        annotations = {
            '|0⟩': (0, 0, 1.1), '|1⟩': (0, 0, -1.2),
            '|+⟩': (1.1, 0, 0), '|−⟩': (-1.2, 0, 0),
            '|i⟩': (0, 1.1, 0), '|−i⟩': (0, -1.2, 0)
        }
        for text, (ax, ay, az) in annotations.items():
            fig.add_trace(go.Scatter3d(
                x=[ax], y=[ay], z=[az],
                mode='text',
                text=[text],
                textfont=dict(color='#FFFFFF', size=16)
            ))

        # 4. Configure layout
        fig.update_layout(
            title=dict(text="Bloch Sphere Visualization", x=0.5, font=dict(size=20, color='white')),
            showlegend=False,
            template="plotly_dark",
            scene=dict(
                xaxis=dict(title='X-axis', range=[-1.3, 1.3], color='white', showbackground=False),
                yaxis=dict(title='Y-axis', range=[-1.3, 1.3], color='white', showbackground=False),
                zaxis=dict(title='Z-axis', range=[-1.3, 1.3], color='white', showbackground=False),
                aspectratio=dict(x=1, y=1, z=1),
                camera=dict(eye=dict(x=1.2, y=1.2, z=0.8))
            ),
            margin=dict(l=0, r=0, b=0, t=40)
        )
        return fig

    # --- Main Application UI ---
    st.title("🌌 Interactive Bloch Sphere Explorer")
    st.markdown("---")

    left_col, right_col = st.columns([1, 1], gap="large")

    # --- Left Column: Controls & Analysis ---
    with left_col:
        st.header("⚙️ Control Panel")
        
        # Sliders for Theta and Phi
        theta = st.slider("Theta (θ) Angle", 0.0, np.pi, 0.0, 0.01, format="%.3f rad")
        phi = st.slider("Phi (φ) Angle", 0.0, 2 * np.pi, 0.0, 0.01, format="%.3f rad")

        # State Analysis
        st.header("🔬 State Analysis")
        state_label, state_type = get_state_label(theta)
        
        if state_type == "success":
            st.success(f"**State:** {state_label}")
        elif state_type == "error":
            st.error(f"**State:** {state_label}")
        else:
            st.info(f"**State:** {state_label}")

        # Generated Qiskit Code
        st.header("💻 Qiskit Circuit")
        st.markdown("This Qiskit code generates the current quantum state from the initial `|0⟩` state.")
        qiskit_code = f"""from qiskit import QuantumCircuit
import numpy as np

# Create a quantum circuit with one qubit
qc = QuantumCircuit(1)

# Define the angles
theta = {theta:.4f} # θ
phi = {phi:.4f}   # φ

# Apply gates to achieve the desired state
# |ψ⟩ = Rz(φ) Ry(θ) |0⟩
# Note: Qiskit's U gate is U(θ, φ, λ). U(theta, phi, 0) is a common way.
# A more direct way is applying Ry then Rz.
qc.ry(theta, 0)
qc.rz(phi, 0)

# The circuit is now prepared in the state |ψ⟩
print(qc)"""
        st.code(qiskit_code, language='python')

    # --- Right Column: Visualization & Mathematics ---
    with right_col:
        # Real-Time Visualization
        st.header("🌐 Real-Time Visualization")
        st.plotly_chart(create_bloch_sphere(theta, phi), use_container_width=True)

        # Quantum State Information
        st.header("🧮 Quantum State Information")
        
        # Mathematical representation (Ket notation)
        cos_theta_2 = np.cos(theta / 2)
        sin_theta_2 = np.sin(theta / 2)
        
        # Format the complex number e^(iφ)
        c1_real = sin_theta_2 * np.cos(phi)
        c1_imag = sin_theta_2 * np.sin(phi)
        
        if np.isclose(c1_imag, 0):
            complex_part = f"{c1_real:.3f}"
        else:
            sign = "+" if c1_imag > 0 else "-"
            complex_part = f"({c1_real:.3f} {sign} {abs(c1_imag):.3f}i)"
        
        ket_notation = f"|ψ⟩ = {cos_theta_2:.3f} |0⟩ + {complex_part} |1⟩"
        st.latex(ket_notation)

        # Probabilities
        st.markdown("#### Measurement Probabilities")
        prob_0 = cos_theta_2**2
        prob_1 = sin_theta_2**2
        
        st.markdown(f"**Probability of measuring |0⟩:** `{prob_0:.1%}`")
        st.progress(prob_0)
        
        st.markdown(f"**Probability of measuring |1⟩:** `{prob_1:.1%}`")
        st.progress(prob_1)

# To run this, ensure you are calling this app() function from your main app.py
# if __name__ == "__main__":
#     app()