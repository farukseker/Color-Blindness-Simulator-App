import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(page_title="Color Blindness Simulator", layout="centered")

st.title("🎨 Color Blindness Simulator")
st.write("Upload an image and instantly see how it looks for different types of color blindness.")

MATRICES = {
    "Normal": np.array([
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1]
    ]),
    "Protanopi": np.array([
        [0.56667, 0.43333, 0],
        [0.55833, 0.44167, 0],
        [0,       0.24167, 0.75833]
    ]),
    "Deuteranopi": np.array([
        [0.625,   0.375,   0],
        [0.7,     0.3,     0],
        [0,       0.3,     0.7]
    ]),
    "Tritanopi": np.array([
        [0.95,    0.05,     0],
        [0,       0.43333,  0.56667],
        [0,       0.475,    0.525]
    ])
}

def simulate_color_blindness(img: Image.Image, matrix: np.ndarray) -> Image.Image:
    img = img.convert("RGB")
    np_img = np.array(img) / 255.0
    reshaped = np_img.reshape(-1, 3)
    transformed = reshaped @ matrix.T
    transformed = np.clip(transformed, 0, 1)
    transformed_img = (transformed.reshape(np_img.shape) * 255).astype(np.uint8)
    return Image.fromarray(transformed_img)

uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    original = Image.open(uploaded_file)
    st.image(original, caption="Original Image", use_container_width=True)

    st.subheader("👓 Simulations")

    cols = st.columns(2)
    sim_names = list(MATRICES.keys())

    for i, name in enumerate(sim_names):
        result = simulate_color_blindness(original, MATRICES[name])
        with cols[i % 2]:
            st.image(result, caption=name)
