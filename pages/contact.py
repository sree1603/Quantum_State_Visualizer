import streamlit as st

def app():
    st.markdown("<h1 style='text-align: center; font-family: IBM Plex Sans, sans-serif; font-weight: 600; margin-bottom: 1.5rem;'>Contact Us</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #262626; padding: 1.5rem; margin-bottom: 2rem; border-left: 4px solid #0f62fe;">
        <p style="font-family: 'IBM Plex Sans', sans-serif; font-size: 1rem; line-height: 1.5;">
            Have questions about quantum computing or want to learn more about Myriad? Reach out to us using the form below.
        </p>
    </div>
    
    <style>
    .contact-form {
        background-color: #262626;
        padding: 2rem;
        border: 1px solid #393939;
        max-width: 600px;
        margin: 0 auto;
    }
    .form-group {
        margin-bottom: 1.5rem;
    }
    .form-label {
        display: block;
        margin-bottom: 0.5rem;
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 500;
        color: #f4f4f4;
        font-size: 0.9rem;
    }
    .form-input {
        width: 100%;
        padding: 0.75rem;
        border: none;
        border-bottom: 1px solid #6f6f6f;
        background-color: #262626;
        color: #f4f4f4;
        font-family: 'IBM Plex Sans', sans-serif;
        transition: border-color 0.2s ease;
    }
    .form-input:focus {
        outline: none;
        border-color: #0f62fe;
    }
    .form-textarea {
        min-height: 150px;
        resize: vertical;
        border: 1px solid #6f6f6f;
    }
    .submit-button {
        background-color: #0f62fe;
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 400;
        cursor: pointer;
        transition: background-color 0.2s ease;
        display: inline-block;
        text-transform: uppercase;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
    }
    .submit-button:hover {
        background-color: #0353e9;
    }
    .success-message {
        background-color: #022d0d;
        border-left: 4px solid #24a148;
        color: #f4f4f4;
        padding: 1rem;
        margin-top: 1rem;
        font-family: 'IBM Plex Sans', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Contact form HTML
    st.markdown("""
    <div class="contact-form">
        <form id="quantum-contact-form">
            <div class="form-group">
                <label class="form-label" for="name">Name</label>
                <input type="text" id="name" class="form-input" placeholder="Your name" required>
            </div>
            
            <div class="form-group">
                <label class="form-label" for="email">Email</label>
                <input type="email" id="email" class="form-input" placeholder="your.email@example.com" required>
            </div>
            
            <div class="form-group">
                <label class="form-label" for="message">Message</label>
                <textarea id="message" class="form-input form-textarea" placeholder="Your message here..." required></textarea>
            </div>
            
            <button type="submit" class="submit-button">Send Message</button>
        </form>
        <div id="success-message" style="display: none;" class="success-message">
            Thank you for your message! We'll respond to your quantum inquiry soon.
        </div>
    </div>
    
    <script>
    document.getElementById('quantum-contact-form').addEventListener('submit', function(e) {
        e.preventDefault();
        // In a real app, you would send the form data to a server here
        // For demo purposes, we'll just show a success message
        document.getElementById('quantum-contact-form').style.display = 'none';
        document.getElementById('success-message').style.display = 'block';
    });
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    app()