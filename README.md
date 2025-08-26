# Myriad - Quantum Visualization Web App

Myriad is a modern, interactive Streamlit web application designed to visualize and explore quantum computing concepts through beautiful UI, responsive layouts, and smooth animations. The app features a quantum/astro-inspired design with clean, scroll-bar-centric layouts.

## Features

### Loading Page
- Full-screen "Quantum Loader" animation on initial visit
- Covers the app until all resources/components are ready

### Home Page
- Animated 3D glowing sphere (Three.js) that starts at center, then animates/slides left
- About text that fades/slides in on the right once animation completes
- Stylish, animated horizontal scroller at the top with quantum-themed text
- Sticky/fixed menu bar with underline-hover effect

### Visualization Page
- Quantum state visualizer with QASM input
- Bloch Sphere representations of quantum states
- Circuit rendering
- Quantum/math-themed layout

### Comics Page
- Displays local PDFs from the /comics folder
- Shows cover page as a tile/grid for each comic
- Tiles zoom/expand slightly on hover for an engaging effect
- View button to preview the whole comic

### Contact Us Page
- Styled form for Name, Email, Message
- Matches the Myriad dark/astro/qubit-inspired theme

## Design Elements

### Color Palette
- Dark-themed colors suited for quantum topics
- Deep navy, black backgrounds, teal, cyan, violet, soft glows, and neon/futuristic accents

### Fonts
- Headings: Raleway
- Body text: Quicksand

### Animations
- Full-screen quantum-styled loader
- Smooth sphere animation from center to left
- Menu bar underline-hover effect
- Smooth CSS scroll animation for scrolling bar
- CSS transition for comics tiles zoom/scale effect

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
streamlit run app.py
```

## Project Structure

```
├── app.py                # Main application file
├── pages/                # Page modules
│   ├── loader.py         # Quantum loader animation
│   ├── sphere.py         # 3D glowing sphere component
│   ├── visualization.py  # Quantum state visualizer
│   ├── comics.py         # Comics viewer
│   └── contact.py        # Contact form
├── comics/               # PDF comics folder
└── requirements.txt      # Project dependencies
```

## Requirements

- Python 3.8+
- Streamlit 1.22.0+
- Qiskit 0.42.0+
- PyMuPDF 1.22.3+
- Other dependencies listed in requirements.txt

## License

This project is licensed under the MIT License - see the LICENSE file for details.