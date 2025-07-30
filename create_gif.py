import streamlit as st
import imageio
import tempfile
import os
from PIL import Image
import numpy as np

st.set_page_config(page_title="GifCraft 🎨", page_icon="🌀")

st.title("🎨 GifCraft - Create Your Own GIFs")
st.write("Upload images and get a fun looping GIF instantly!")

uploaded_files = st.file_uploader(
    "📸 Upload 2 or more images (JPG/PNG)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Fixed duration (500ms per frame)
duration = 500

if uploaded_files and len(uploaded_files) >= 2:
    with st.spinner("Creating your GIF..."):

        temp_dir = tempfile.mkdtemp()
        frames = []

        # Get target size from the first image
        first_img = Image.open(uploaded_files[0]).convert("RGB")
        target_size = first_img.size
        frames.append(np.array(first_img.resize(target_size)))

        # Resize and store remaining images
        for file in uploaded_files[1:]:
            img = Image.open(file).convert("RGB")
            img = img.resize(target_size)
            frames.append(np.array(img))

        # Create and save the GIF
        gif_path = os.path.join(temp_dir, "output.gif")
        imageio.mimsave(gif_path, frames, duration=duration / 1000.0)

        st.success("✅ GIF created successfully!")

        # GIF preview using HTML that actually animates
        st.markdown("### 🔄 Preview your animated GIF:")
        st.markdown(
            f'<img src="file://{gif_path}" alt="Generated GIF" style="max-width: 100%;">',
            unsafe_allow_html=True
        )

        # Download option
        with open(gif_path, "rb") as f:
            st.download_button("📥 Download GIF", f, file_name="your_gif.gif", mime="image/gif")

else:
    st.info("Please upload at least 2 image files to create a GIF.")
