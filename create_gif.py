import streamlit as st
import imageio
import tempfile
import os
from PIL import Image
import base64
import numpy as np

st.set_page_config(page_title="GifCraft 🎨", page_icon="🌀")

st.title("🎨 GifCraft - Create Your Own GIFs")
st.write("Upload images and get a fun looping GIF instantly!")

# Upload image files
uploaded_files = st.file_uploader(
    "📸 Upload 2 or more images (JPG/PNG)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Fixed duration per frame
duration = 500  # ms

if uploaded_files and len(uploaded_files) >= 2:
    with st.spinner("Creating your GIF..."):

        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()
        frames = []

        # Resize all images to the size of the first image
        base_image = Image.open(uploaded_files[0]).convert("RGB")
        target_size = base_image.size
        frames.append(np.array(base_image.resize(target_size)))

        for file in uploaded_files[1:]:
            img = Image.open(file).convert("RGB")
            resized_img = img.resize(target_size)
            frames.append(np.array(resized_img))

        # Create the GIF
        gif_path = os.path.join(temp_dir, "output.gif")
        imageio.mimsave(gif_path, frames, duration=duration / 1000.0)

        # Show GIF preview using HTML + base64
        st.success("✅ GIF created successfully!")

        st.markdown("### 🔄 Preview your animated GIF:")
        with open(gif_path, "rb") as f:
            gif_bytes = f.read()
            b64 = base64.b64encode(gif_bytes).decode()
            st.markdown(
                f'<img src="data:image/gif;base64,{b64}" alt="GIF preview" style="max-width:100%;">',
                unsafe_allow_html=True
            )

        # Download button
        st.download_button(
            "📥 Download GIF",
            gif_bytes,
            file_name="your_gif.gif",
            mime="image/gif"
        )
else:
    st.info("Please upload at least 2 image files to create a GIF.")
