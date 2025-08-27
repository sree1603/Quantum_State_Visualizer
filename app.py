import streamlit as st
import streamlit.components.v1 as components
import os
import time

# Import page modules from the 'pages' directory
from pages.loader import quantum_loader
from pages.sphere import show_glowing_sphere
# --- MODIFICATION: Import the new explorer page ---
from pages import visualization, comics, contact, realms, explorer 

# Page configuration
st.set_page_config(
    page_title="Myriad - Quantum Visualization",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply global styling
st.markdown("""
<style>
    /* Global styles - IBM inspired */
    body {
        background-color: #161616;
        color: #f4f4f4;
        font-family: 'IBM Plex Sans', sans-serif;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #262626;
    }
    ::-webkit-scrollbar-thumb {
        background: #0f62fe;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #0353e9;
    }
    
    /* Streamlit component styling */
    .stApp {
        background-color: #161616;
    }
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 1200px;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'IBM Plex Sans', sans-serif;
        color: #ffffff;
        font-weight: 600;
    }
    
    /* Menu bar styling - IBM inspired */
    .menu-bar {
        display: flex;
        justify-content: center;
        padding: 0;
        background-color: #262626;
        position: sticky;
        top: 0;
        z-index: 100;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    .menu-item {
        margin: 0;
        padding: 1.2rem 2rem;
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 500;
        font-size: 0.9rem;
        color: #f4f4f4;
        text-decoration: none;
        position: relative;
        transition: background-color 0.2s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .menu-item:hover {
        background-color: #393939;
        color: #ffffff;
    }
    .menu-item.active {
        color: #ffffff;
        border-bottom: 3px solid #0f62fe;
    }
    .menu-item.active:hover {
        background-color: #393939;
    }
    
    /* Scrolling text bar - IBM inspired */
    .scroll-container {
        overflow: hidden;
        white-space: nowrap;
        background-color: #0f62fe;
        padding: 0.6rem 0;
        margin-bottom: 1.5rem;
    }
    .scroll-text {
        display: inline-block;
        animation: scroll 30s linear infinite;
        color: #ffffff;
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 400;
        font-size: 0.85rem;
        letter-spacing: 0.3px;
    }
    @keyframes scroll {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
</style>

<!-- Google Fonts -->
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Show loader on first load
if 'first_load' not in st.session_state:
    st.session_state.first_load = True
    quantum_loader(message="Initializing Myriad", duration=3)
    st.session_state.first_load = False

# --- Menu Bar and Routing Logic ---

# Get the current page from the URL query parameters
page = st.query_params.get("page", None)

# Segmented control (tab navigation) style navbar using Streamlit buttons
st.markdown("""
<style>
    /* Hide default Streamlit button styling */
    div.stButton > button {
        background: transparent;
        border: none;
        color: inherit;
        font-weight: inherit;
        padding: 0.7rem 1.8rem;
        border-radius: 2rem;
        box-shadow: none;
        width: 100%;
        height: 100%;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        border: none;
        box-shadow: none;
    }
    div.stButton > button:focus {
        box-shadow: none;
    }
    
    /* Navbar container */
    .nav-container {
        display: flex;
        justify-content: center;
        margin: 1.2rem auto 1.5rem auto;
    }
    
    /* Segmented control styling */
    .segmented-control {
        display: flex;
        background: #262626;
        border-radius: 2rem;
        padding: 0.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.18);
        max-width: 800px; /* Increased width for new item */
        margin: 0 auto;
    }
    
    /* Tab button styling */
    .tab-item {
        position: relative;
        z-index: 1;
    }
    .tab-item.active button {
        background: #0f62fe;
        color: #fff !important;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(15,98,254,0.25);
        transform: translateY(-1px);
    }
    .tab-item button {
        color: #b3b3b3 !important;
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 1rem;
    }
    .tab-item:not(.active) button:hover {
        background: #393939;
        color: #fff !important;
        transform: translateY(-1px);
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        div.stButton > button {
            padding: 0.6rem 1rem;
            font-size: 0.9rem;
        }
        .segmented-control {
            max-width: 95%;
        }
    }
</style>
""", unsafe_allow_html=True)

def set_page(new_page):
    st.query_params["page"] = new_page if new_page else None
    st.rerun()

# --- MODIFICATION: Add "Explorer" to the navigation tabs ---
tab_items = [
    ("Home", None),
    ("Visualization", "visualization"),
    ("Explorer", "explorer"),
    ("Comics", "comics"),
    ("Realms", "realms"),
    ("Contact Us", "contact")
]

# Create the segmented control navbar container
st.markdown('<div class="nav-container"><div class="segmented-control">', unsafe_allow_html=True)

# Render navbar using Streamlit columns inside the segmented control
cols = st.columns(len(tab_items))
for idx, (label, value) in enumerate(tab_items):
    active = (page == value) or (value is None and page is None)
    tab_class = "tab-item active" if active else "tab-item"
    
    # Apply the tab-item class to the column
    with cols[idx]:
        st.markdown(f'<div class="{tab_class}">', unsafe_allow_html=True)
        if st.button(label, key=f"tab_{label}"):
            set_page(value)
        st.markdown('</div>', unsafe_allow_html=True)

# Close the segmented control container
st.markdown('</div></div>', unsafe_allow_html=True)

# Scrolling text bar
st.markdown("""
<div class="scroll-container">
    <div class="scroll-text">✨ EXPLORE THE BLOCH SPHERE | BUILD QUANTUM CIRCUITS IN THE REALMS | VISUALIZE QUANTUM STATES | READ QUANTUM COMICS | ⟨ψ| WELCOME TO MYRIAD |ψ⟩ | ✨</div>
</div>
""", unsafe_allow_html=True)


# --- NEW HOME PAGE FUNCTION ---
def show_home_page():
    """
    Displays the main home page content, including the new
    infinitely scrolling card section and the glowing sphere.
    """
    st.markdown("""
    <style>
        @keyframes scroll-horizontal {
            0% { transform: translateX(0); }
            100% { transform: translateX(-50%); }
        }
        .scroller-container {
            overflow: hidden;
            padding: 2rem 0;
            background: #161616;
            -webkit-mask: linear-gradient(90deg, transparent, white 20%, white 80%, transparent);
            mask: linear-gradient(90deg, transparent, white 20%, white 80%, transparent);
        }
        .scroller-inner {
            display: flex;
            gap: 1.5rem;
            width: max-content;
            animation: scroll-horizontal 40s linear infinite;
        }
        .scroller-container:hover .scroller-inner {
            animation-play-state: paused;
        }
        .milestone-card {
            background-color: #262626;
            border-radius: 12px;
            padding: 1.5rem;
            width: 350px;
            border: 1px solid #393939;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            display: flex;
            flex-direction: column;
        }
        .milestone-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 10px 25px rgba(15, 98, 254, 0.2);
            border-color: #0f62fe;
        }
        .milestone-card h3 {
            font-size: 1.25rem;
            color: #ffffff;
            margin-top: 0;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
        }
        .milestone-card h3 span {
            font-size: 1.8rem;
            margin-right: 0.75rem;
            color: #0f62fe;
        }
        .milestone-card p {
            font-size: 0.95rem;
            color: #c6c6c6;
            line-height: 1.6;
            flex-grow: 1; /* Pushes the link to the bottom */
        }
        .milestone-card a {
            color: #0f62fe;
            text-decoration: none;
            font-weight: 600;
            margin-top: 1rem;
            display: inline-block;
        }
        .milestone-card a:hover {
            text-decoration: underline;
        }
        .home-title {
            text-align: center;
            margin-bottom: 1rem;
            color: #f4f4f4;
        }
        .home-subtitle {
            text-align: center;
            max-width: 700px;
            margin: 0 auto 2rem auto;
            color: #c6c6c6;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 class='home-title'>From Theory to Reality: The Quantum Revolution</h2>", unsafe_allow_html=True)
    st.markdown("<p class='home-subtitle'>Quantum computing isn't just a futuristic dream—it's a rapidly evolving field with groundbreaking achievements and world-changing applications. Explore some of the key milestones that are paving the way for the future of computation.</p>", unsafe_allow_html=True)

    # --- Card Data ---
    # Each tuple: (Emoji, Title, Description, URL)
    cards_data = [
        ("🏆", "Quantum Supremacy", "In 2019, Google claimed to have built a quantum computer that performed a calculation in 200 seconds that would take the world's fastest supercomputer 10,000 years. This was a major demonstration of potential.", "https://www.forbes.com/sites/bernardmarr/2023/07/28/the-race-for-quantum-supremacy-whos-leading-the-pack-in-2023/"),
        ("💊", "Drug Discovery", "Quantum computers can simulate molecules with incredible precision, a task impossible for classical machines. This is accelerating the discovery of new medicines and materials, revolutionizing healthcare.", "https://www.forbes.com/councils/forbesbusinessdevelopmentcouncil/2024/10/15/how-quantum-computing-is-accelerating-drug-discovery-and-development/"),
        ("🔒", "Shor's Algorithm", "In 1994, Peter Shor developed a quantum algorithm that could, in principle, break most of the encryption we use today. This discovery ignited the race to build both quantum computers and quantum-safe cryptography.", "https://en.wikipedia.org/wiki/Shor%27s_algorithm"),
        ("📈", "Financial Modeling", "The world of finance is filled with complex optimization problems. Quantum computing promises to deliver more accurate risk models, optimized trading strategies, and new financial instruments.", "https://www.ibm.com/thought-leadership/institute-business-value/en-us/report/exploring-quantum-financial"),
        ("🛠️", "Error Correction", "Qubits are fragile. A huge breakthrough is the development of quantum error correction codes, which protect quantum information from noise, making large-scale, fault-tolerant quantum computers a real possibility.", "https://www.livescience.com/technology/computing/scientists-make-magic-state-breakthrough-after-20-years-without-it-quantum-computers-can-never-be-truly-useful"),
        ("⚛️", "Single-Atom Control", "Recent breakthroughs allow scientists to entangle the vibrations within a single atom, creating powerful logic gates. This reduces the number of physical qubits needed, paving the way for more efficient quantum machines.", "https://scitechdaily.com/scientists-unlock-quantum-computing-power-by-entangling-vibrations-in-a-single-atom/")
    ]
    
    # --- HTML for Scroller ---
    # Duplicate the cards to create a seamless loop
    card_html_items = ""
    for emoji, title, desc, url in cards_data * 2:
        card_html_items += f"""
        <div class="milestone-card">
            <h3><span>{emoji}</span>{title}</h3>
            <p>{desc}</p>
            <a href="{url}" target="_blank" rel="noopener noreferrer">Learn More &rarr;</a>
        </div>
        """

    scroller_html = f"""
    <div class="scroller-container">
        <div class="scroller-inner">
            {card_html_items}
        </div>
    </div>
    """
    
    st.markdown(scroller_html, unsafe_allow_html=True)

    # --- Show the original glowing sphere below the new section ---
    show_glowing_sphere(height=800)


# --- Page Routing ---
# Display the appropriate page based on the 'page' query parameter
if page == "visualization":
    visualization.app()
elif page == "explorer":
    explorer.app()
elif page == "comics":
    comics.app()
elif page == "realms":
    realms.app()
elif page == "contact":
    contact.app()
else:
    # Default to the NEW Home page function
    show_home_page()
