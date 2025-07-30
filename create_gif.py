import streamlit as st
import imageio
import tempfile
import os
from PIL import Image
import numpy as np
import base64

st.set_page_config(page_title="GifCraft 🎨", page_icon="🌀")
st.title("🎨 GifCraft - Create Your Own GIFs")
st.write("Upload images and get a fun looping GIF instantly!")

uploaded_files = st.file_uploader(
    "📸 Upload 2 or more images (JPG/PNG)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Fixed duration in milliseconds
duration = 500

if uploaded_files and len(uploaded_files) >= 2:
    with st.spinner("Creating your GIF..."):

        temp_dir = tempfile.mkdtemp()
        frames = []

        # Get target size from first image
        base_img = Image.open(uploaded_files[0]).convert("RGB")
        target_size = base_img.size
        frames.append(np.array(base_img.resize(target_size)))

        for file in uploaded_files[1:]:
            img = Image.open(file).convert("RGB")
            img = img.resize(target_size)
            frames.append(np.array(img))

        # Save GIF
        gif_path = os.path.join(temp_dir, "output.gif")
        imageio.mimsave(gif_path, frames, duration=duration / 1000.0)

        st.success("✅ GIF created successfully!")

        # 🔁 Show GIF using base64 + HTML
        st.markdown("### 🔄 Preview your animated GIF:")
        with open(gif_path, "rb") as f:
            gif_bytes = f.read()
            gif_b64 = base64.b64encode(gif_bytes).decode("utf-8")
            st.markdown(
                f"""
                <div style="text-align:center">
                    <img src="data:image/gif;base64,{gif_b64}" alt="Animated GIF" style="max-width:100%; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.2);">
                </div>
                """,
                unsafe_allow_html=True
            )

        # 📥 Download button
        st.download_button("📥 Download GIF", gif_bytes, file_name="your_gif.gif", mime="image/gif")
else:
    st.info("Please upload at least 2 image files to create a GIF.")
