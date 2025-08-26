# pages/loader.py

import streamlit as st
import streamlit.components.v1 as components
import time

def quantum_loader(message="Initializing quantum state…", duration=5):
    """
    Displays a visually appealing, animated quantum-style loader for a specified duration.
    This version uses a self-contained HTML/CSS component for a richer visual effect.

    Args:
        message (str): The loading message to display beneath the animation.
        duration (int): The number of seconds to display the loader.
    """
    
    # Custom loader HTML with CSS for animation.
    # The message is dynamically inserted using an f-string.
    loader_html = f"""
    <div class="loader-container">
      <div class="loader">
        <div class="orbit"></div>
        <div class="orbit"></div>
        <div class="orbit"></div>
        <div class="center"></div>
        <div class="symbols">
          <span>|0⟩</span>
          <span>|1⟩</span>
          <span>|ψ⟩</span>
          <span>ℏ</span>
          <span>⊕</span>
          <span>⊗</span>
        </div>
      </div>
      <p class="loading-text">{message}</p>
    </div>

    <style>
    .loader-container {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 90vh; /* Use viewport height to center vertically */
      background: #161616; /* Match your app's background */
      color: #e5e7eb;
      font-family: 'IBM Plex Sans', sans-serif;
    }}

    .loader {{
      position: relative;
      width: 180px;
      height: 180px;
    }}

    .center {{
      position: absolute;
      top: 50%;
      left: 50%;
      width: 50px;
      height: 50px;
      transform: translate(-50%, -50%);
      border-radius: 50%;
      background: conic-gradient(from 180deg, #60a5fa, #a78bfa, #6366f1, #60a5fa);
      animation: spin 6s linear infinite;
      box-shadow: 0 0 20px rgba(96,165,250,0.8);
    }}

    .orbit {{
      position: absolute;
      border: 2px solid rgba(15, 98, 254, 0.35); /* IBM Blue */
      border-radius: 50%;
      top: 50%;
      left: 50%;
      transform-origin: center center;
      animation: spin 12s linear infinite;
    }}

    .orbit:nth-child(1) {{
      width: 180px;
      height: 180px;
      transform: translate(-50%, -50%) rotate(0deg);
    }}
    .orbit:nth-child(2) {{
      width: 140px;
      height: 140px;
      border-color: rgba(168,85,247,0.35);
      animation-duration: 10s;
      animation-direction: reverse;
      transform: translate(-50%, -50%) rotate(0deg);
    }}
    .orbit:nth-child(3) {{
      width: 100px;
      height: 100px;
      border-color: rgba(59,130,246,0.35);
      animation-duration: 8s;
      transform: translate(-50%, -50%) rotate(0deg);
    }}

    .symbols span {{
      position: absolute;
      font-size: 18px;
      font-weight: bold;
      color: #e5e7eb;
      text-shadow: 0 0 6px rgba(96,165,250,0.9), 0 0 14px rgba(167,139,250,0.7);
      animation: spin-reverse 8s linear infinite; /* Counter-rotate */
    }}
    
    /* Position symbols around the orbits */
    .symbols span:nth-child(1) {{ top: -10px; left: 50%; transform: translateX(-50%); }}
    .symbols span:nth-child(2) {{ right: -10px; top: 50%; transform: translateY(-50%); }}
    .symbols span:nth-child(3) {{ bottom: -10px; left: 50%; transform: translateX(-50%); }}
    .symbols span:nth-child(4) {{ left: -10px; top: 50%; transform: translateY(-50%); }}
    .symbols span:nth-child(5) {{ top: 15%; left: 15%; }}
    .symbols span:nth-child(6) {{ bottom: 15%; right: 15%; }}


    .loading-text {{
      margin-top: 30px;
      font-size: 16px;
      letter-spacing: 1px;
      color: #cbd5e1;
      animation: blink 1.5s infinite ease-in-out;
    }}

    @keyframes spin {{
      from {{ transform: translate(-50%, -50%) rotate(0deg); }}
      to {{ transform: translate(-50%, -50%) rotate(360deg); }}
    }}
    
    @keyframes spin-reverse {{
      from {{ transform: rotate(0deg); }}
      to {{ transform: rotate(-360deg); }}
    }}

    @keyframes blink {{
      0%, 100% {{ opacity: 1; }}
      50% {{ opacity: 0.4; }}
    }}
    </style>
    """

    # Use st.empty() to create a container that can be cleared after the loader is done.
    placeholder = st.empty()
    
    with placeholder.container():
        components.html(loader_html, height=400) # Display the loader
    
    time.sleep(duration) # Wait for the specified duration
    
    placeholder.empty() # Clear the loader from the screen
