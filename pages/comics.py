import streamlit as st
import os
import fitz  # PyMuPDF
import base64
from io import BytesIO

def get_pdf_thumbnail(pdf_path, page_num=0):
    """Extract the first page of a PDF as a thumbnail image."""
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5))  # Scale down for thumbnail
        img_bytes = pix.tobytes("png")
        base64_img = base64.b64encode(img_bytes).decode()
        return f"data:image/png;base64,{base64_img}"
    except Exception as e:
        st.error(f"Error generating thumbnail for {pdf_path}: {str(e)}")
        return None
    finally:
        if 'doc' in locals():
            doc.close()

def app():
    st.markdown("<h1 style='text-align: center; font-family: IBM Plex Sans, sans-serif; font-weight: 600; margin-bottom: 1.5rem;'>Quantum Comics</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #262626; padding: 1.5rem; margin-bottom: 2rem; border-left: 4px solid #0f62fe;">
        <p style="font-family: 'IBM Plex Sans', sans-serif; font-size: 1rem; line-height: 1.5;">
            Explore our collection of quantum-themed comics. Click on any comic to view it in full.
        </p>
    </div>
    
    <style>
    .comic-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    .comic-tile {
        background-color: #262626;
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid #393939;
    }
    .comic-tile:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        border-color: #0f62fe;
    }
    .comic-thumbnail {
        width: 100%;
        aspect-ratio: 0.7;
        object-fit: cover;
        border-bottom: 1px solid #393939;
    }
    .comic-info {
        padding: 1.2rem;
        text-align: left;
    }
    .comic-title {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    .comic-description {
        font-family: 'IBM Plex Sans', sans-serif;
        font-size: 0.9rem;
        color: #c6c6c6;
        margin-bottom: 1rem;
    }
    .view-button {
        background-color: #0f62fe;
        color: white;
        border: none;
        padding: 0.6rem 1rem;
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 400;
        cursor: pointer;
        transition: background-color 0.2s ease;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.5px;
    }
    .view-button:hover {
        background-color: #0353e9;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get comics from the comics folder
    comics_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "comics")
    
    if not os.path.exists(comics_folder):
        st.warning("Comics folder not found. Please create a 'comics' folder in the project root and add PDF comics.")
        return
    
    comics = [f for f in os.listdir(comics_folder) if f.lower().endswith('.pdf')]
    
    if not comics:
        st.info("No comics found in the comics folder. Add PDF files to display them here.")
        return
    
    # Display comics in a grid
    st.markdown('<div class="comic-grid">', unsafe_allow_html=True)
    
    for comic in comics:
        comic_path = os.path.join(comics_folder, comic)
        thumbnail = get_pdf_thumbnail(comic_path)
        
        if thumbnail:
            # Extract title from filename (remove extension and replace underscores with spaces)
            title = os.path.splitext(comic)[0].replace('_', ' ')
            
            # Create a unique key for this comic
            comic_key = f"comic_{title.replace(' ', '_')}"
            
            # Display comic tile
            st.markdown(f"""
            <div class="comic-tile" id="{comic_key}">
                <img src="{thumbnail}" class="comic-thumbnail" alt="{title}">
                <div class="comic-info">
                    <div class="comic-title">{title}</div>
                    <div class="comic-description">A quantum adventure awaits!</div>
                    <button class="view-button" onclick="openComic('{comic_path}')">View Comic</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # JavaScript for handling comic viewing
    st.markdown(f"""
    <script>
    function openComic(comicPath) {{
        // Use Streamlit's postMessage to communicate with Python
        window.parent.postMessage({{
            type: "streamlit:setComponentValue",
            value: comicPath
        }}, "*");
    }}
    </script>
    """, unsafe_allow_html=True)
    
    # Handle comic selection
    if "selected_comic" in st.session_state:
        comic_path = st.session_state.selected_comic
        try:
            with open(comic_path, "rb") as file:
                pdf_bytes = file.read()
            
            # Display PDF viewer
            st.markdown(f"<h2>Viewing: {os.path.basename(comic_path)}</h2>", unsafe_allow_html=True)
            base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
            
            # Close button
            if st.button("Close Comic"):
                del st.session_state.selected_comic
                st.experimental_rerun()
        except Exception as e:
            st.error(f"Error opening comic: {str(e)}")

