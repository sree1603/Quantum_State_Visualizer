import streamlit as st
import streamlit.components.v1 as components
import os
import time

# Import page modules from the 'pages' directory
from pages.loader import quantum_loader
from pages.sphere import show_glowing_sphere
from pages import visualization, comics, contact, realms, explorer

# Page configuration
st.set_page_config(
    page_title="Myriad - Quantum Visualization",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- NEW FUNCTION FOR THE HOMEPAGE CONTENT ---
def show_homepage_content():
    """
    Displays the creative and informative homepage content, including the hero sphere
    and the interactive cards section.
    """
    # 1. Hero Section with the Glowing Sphere
    show_glowing_sphere(height=600)

    # 2. "Quantum Leaps" Section
    st.markdown("<h2 style='text-align: center; font-weight: 600; margin-top: 3rem; margin-bottom: 1rem;'>Quantum Leaps: Where the Future is Being Built</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; max-width: 700px; margin: 0 auto 2.5rem auto; color: #c6c6c6;'>Quantum computing isn't just theory—it's poised to revolutionize industries. Explore some of the groundbreaking applications being developed today.</p>", unsafe_allow_html=True)

    # Card data: A list of dictionaries for easy modification
    cards_data = [
        {
            "title": "Designing New Drugs & Materials",
            "description": "Simulate molecules with incredible precision to discover life-saving medicines and create revolutionary materials.",
            "image_url": "https://images.unsplash.com/photo-1581093458791-9a6680c1bf10?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80",
            "link": "https://www.ibm.com/quantum/science/molecule-simulation/"
        },
        {
            "title": "The Future of Cryptography",
            "description": "Understand how quantum computers could break today's encryption and why developing quantum-safe algorithms is vital.",
            "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80",
            "link": "https://www.technologyreview.com/2022/01/12/1043452/quantum-computing-cryptography-security/"
        },
        {
            "title": "Optimizing Complex Systems",
            "description": "Solve logistical nightmares and create hyper-efficient financial models by finding the best solution among trillions of possibilities.",
            "image_url": "https://images.unsplash.com/photo-1554224155-1696413565d3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80",
            "link": "https://www.quantamagazine.org/how-quantum-computers-will-correct-their-own-errors-20220913/"
        },
        {
            "title": "Quantum Machine Learning",
            "description": "Explore the next frontier of AI, where quantum algorithms could enhance machine learning for more powerful and intelligent systems.",
            "image_url": "https://images.unsplash.com/photo-1620712943543-2858200e944a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1170&q=80",
            "link": "https://qiskit.org/learn/machine-learning"
        }
    ]

    # CSS for the cards
    st.markdown("""
    <style>
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
        }
        .card {
            background-color: #262626;
            border-radius: 8px;
            overflow: hidden;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            text-decoration: none;
            color: inherit;
            border: 1px solid #393939;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4);
            border-color: #0f62fe;
        }
        .card img {
            width: 100%;
            height: 180px;
            object-fit: cover;
        }
        .card-content {
            padding: 1.2rem;
        }
        .card-title {
            font-family: 'IBM Plex Sans', sans-serif;
            font-weight: 600;
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
            color: #ffffff;
        }
        .card-description {
            font-family: 'IBM Plex Sans', sans-serif;
            font-size: 0.95rem;
            color: #c6c6c6;
            line-height: 1.5;
        }
    </style>
    """, unsafe_allow_html=True)

    # Generate the cards
    st.markdown('<div class="card-grid">', unsafe_allow_html=True)
    for card in cards_data:
        st.markdown(f"""
        <a href="{card['link']}" target="_blank" class="card">
            <img src="{card['image_url']}" alt="{card['title']}">
            <div class="card-content">
                <div class="card-title">{card['title']}</div>
                <div class="card-description">{card['description']}</div>
            </div>
        </a>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# --- MAIN APP LOGIC ---

# Apply global styling
st.markdown("""
<style>
    /* Global styles - IBM inspired */
    body {
        background-color: #161616;
        color: #f4f4f4;
        font-family: 'IBM Plex Sans', sans-serif;
    }
    /* ... (rest of your existing global CSS) ... */
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
    /* Navbar styling */
    .nav-container {
        display: flex;
        justify-content: center;
        margin: 1.2rem auto 1.5rem auto;
    }
    .segmented-control {
        display: flex;
        background: #262626;
        border-radius: 2rem;
        padding: 0.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.18);
        max-width: 800px;
        margin: 0 auto;
    }
    .tab-item { position: relative; z-index: 1; }
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
    div.stButton > button {
        background: transparent; border: none; color: inherit; font-weight: inherit;
        padding: 0.7rem 1.8rem; border-radius: 2rem; box-shadow: none;
        width: 100%; height: 100%; transition: all 0.3s ease;
    }
    /* Scrolling text bar */
    .scroll-container {
        overflow: hidden; white-space: nowrap; background-color: #0f62fe;
        padding: 0.6rem 0; margin-bottom: 1.5rem;
    }
    .scroll-text {
        display: inline-block; animation: scroll 30s linear infinite; color: #ffffff;
        font-family: 'IBM Plex Sans', sans-serif; font-weight: 400; font-size: 0.85rem;
        letter-spacing: 0.3px;
    }
    @keyframes scroll {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
</style>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# Show loader on first load
if 'first_load' not in st.session_state:
    st.session_state.first_load = True
    quantum_loader(message="Initializing Myriad", duration=3)
    st.session_state.first_load = False

# --- Menu Bar and Routing Logic ---
page = st.query_params.get("page", None)

def set_page(new_page):
    st.query_params["page"] = new_page if new_page else None
    st.rerun()

tab_items = [
    ("Home", None), ("Visualization", "visualization"), ("Explorer", "explorer"),
    ("Comics", "comics"), ("Realms", "realms"), ("Contact Us", "contact")
]

st.markdown('<div class="nav-container"><div class="segmented-control">', unsafe_allow_html=True)
cols = st.columns(len(tab_items))
for idx, (label, value) in enumerate(tab_items):
    active = (page == value) or (value is None and page is None)
    tab_class = "tab-item active" if active else "tab-item"
    with cols[idx]:
        st.markdown(f'<div class="{tab_class}">', unsafe_allow_html=True)
        if st.button(label, key=f"tab_{label}"):
            set_page(value)
        st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)

# Scrolling text bar
st.markdown("""
<div class="scroll-container">
    <div class="scroll-text">✨ EXPLORE THE BLOCH SPHERE | BUILD QUANTUM CIRCUITS IN THE REALMS | VISUALIZE QUANTUM STATES | READ QUANTUM COMICS | ⟨ψ| WELCOME TO MYRIAD |ψ⟩ | ✨</div>
</div>
""", unsafe_allow_html=True)

# --- Page Routing ---
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
    # --- MODIFICATION: Call the new homepage function ---
    show_homepage_content()