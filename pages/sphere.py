import streamlit.components.v1 as components
import streamlit as st

def show_glowing_sphere(height=800, with_about_text=True):
    """Display a 3D glowing sphere using Three.js embedded HTML/JS with animation."""
    html_code = """
    <div style="display: flex; width: 100%; height: 100vh;">
        <div id="sphere-container" style="width:50%; height:100vh;"></div>
        <div id="about-text" style="width:50%; height:100vh; display: flex; align-items: center; opacity: 0; transition: opacity 2s ease-in-out;">
            <div style="padding: 3rem; color: #f4f4f4; font-family: 'IBM Plex Sans', sans-serif;">
                <h1 style="font-family: 'IBM Plex Sans', sans-serif; font-size: 2.5rem; margin-bottom: 2rem; color: #ffffff; font-weight: 600;">Welcome to Myriad</h1>
                <p style="font-size: 1.1rem; line-height: 1.6; margin-bottom: 1.5rem; color: #f4f4f4;">Explore the quantum realm through interactive visualizations and engaging content.</p>
                <p style="font-size: 1.1rem; line-height: 1.6; color: #f4f4f4;">Myriad brings quantum computing concepts to life with beautiful animations and intuitive interfaces.</p>
                <div style="margin-top: 2rem;">
                    <a href="/?page=visualization" style="display: inline-block; background-color: #0f62fe; color: white; text-decoration: none; padding: 0.8rem 1.5rem; font-weight: 500; border-radius: 0; transition: background-color 0.2s ease;">Explore Now</a>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
    
    <!-- Three.js -->
    <script src="https://cdn.jsdelivr.net/npm/three@0.152.2/build/three.min.js"></script>
    <script>
        // Scene, Camera, Renderer
        const scene = new THREE.Scene();
        const container = document.getElementById("sphere-container");
        const camera = new THREE.PerspectiveCamera(75, container.clientWidth/container.clientHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        // Sphere geometry with points
        const geometry = new THREE.SphereGeometry(5, 60, 60);

        const textureLoader = new THREE.TextureLoader();
        const sprite = textureLoader.load("https://threejs.org/examples/textures/sprites/disc.png");

        const material = new THREE.PointsMaterial({
            color: 0x0f62fe,
            size: 0.08,
            map: sprite,
            transparent: true,
            opacity: 0.8
        });

        const points = new THREE.Points(geometry, material);
        scene.add(points);

        // Background & fog for glow - IBM inspired
        scene.background = new THREE.Color("#161616");
        scene.fog = new THREE.FogExp2("#161616", 0.05);

        // Lighting
        const ambientLight = new THREE.AmbientLight(0x0f62fe, 0.5);
        scene.add(ambientLight);

        camera.position.z = 12;

        // Initial position (center)
        points.position.x = 0;
        
        // Animation variables
        let animationStarted = false;
        let animationProgress = 0;
        const animationDuration = 120; // frames
        
        // Animation
        function animate() {
            requestAnimationFrame(animate);
            
            // Rotate the sphere
            points.rotation.y += 0.002;
            points.rotation.x += 0.001;
            
            // Start animation after 1 second
            if (!animationStarted) {
                setTimeout(() => {
                    animationStarted = true;
                }, 1000);
            }
            
            // Animate sphere position from center to left
            if (animationStarted && animationProgress < animationDuration) {
                animationProgress++;
                const progress = animationProgress / animationDuration;
                
                // Move sphere to the left (center of left half)
                points.position.x = -2.5 * progress;
                
                // Show about text when animation is complete
                if (progress >= 0.9) {
                    document.getElementById("about-text").style.opacity = "1";
                }
            }
            
            renderer.render(scene, camera);
        }
        animate();

        // Resize handling
        window.addEventListener("resize", () => {
            const container = document.getElementById("sphere-container");
            camera.aspect = container.clientWidth / container.clientHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(container.clientWidth, container.clientHeight);
        });
    </script>
    """
    components.html(html_code, height=height, scrolling=False)
    
    # Add additional about text if needed (for mobile or alternative layouts)
    if with_about_text:
        st.markdown("""
        <style>
        @media (max-width: 768px) {
            #about-text-mobile { display: block; }
        }
        @media (min-width: 769px) {
            #about-text-mobile { display: none; }
        }
        </style>
        <div id="about-text-mobile" style="padding: 1.5rem; margin-top: 1.5rem; background-color: #262626;">
            <h2 style="font-family: 'IBM Plex Sans', sans-serif; font-size: 1.8rem; margin-bottom: 1rem; font-weight: 600;">Welcome to Myriad</h2>
            <p style="font-family: 'IBM Plex Sans', sans-serif; font-size: 1rem; line-height: 1.5; margin-bottom: 1.5rem;">Explore the quantum realm through interactive visualizations and engaging content.</p>
            <a href="/?page=visualization" style="display: inline-block; background-color: #0f62fe; color: white; text-decoration: none; padding: 0.7rem 1.2rem; font-weight: 500; font-family: 'IBM Plex Sans', sans-serif;">Explore Now</a>
        </div>
        """, unsafe_allow_html=True)
