import streamlit as st
import imageio
import tempfile
import os

st.set_page_config(page_title="GifCraft 🎨", page_icon="🌀")

st.title("🎨 GifCraft - Create Your Own GIFs")
st.write("Upload images and get a fun looping GIF instantly!")

# Upload multiple image files
uploaded_files = st.file_uploader(
    "📸 Upload 2 or more images (JPG/PNG)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Fixed duration per frame in milliseconds
duration = 500

if uploaded_files and len(uploaded_files) >= 2:
    with st.spinner("Creating your GIF..."):

        # Save uploaded images to a temp directory
        temp_dir = tempfile.mkdtemp()
        filenames = []

        for i, file in enumerate(uploaded_files):
            temp_path = os.path.join(temp_dir, f"frame_{i}.png")
            with open(temp_path, "wb") as f:
                f.write(file.read())
            filenames.append(temp_path)

        # Read images and create GIF
        images = [imageio.imread(fname) for fname in filenames]
        gif_path = os.path.join(temp_dir, "output.gif")
        imageio.mimsave(gif_path, images, duration=duration / 1000.0)  # convert ms to seconds

        # Display GIF with HTML (to ensure animation works)
        st.success("✅ GIF created successfully!")

        st.markdown("### 🔄 Preview your animated GIF:")
        gif_data = open(gif_path, "rb").read()
        st.markdown(
            f'<img src="data:image/gif;base64,{gif_data.encode("base64").decode()}" alt="gif preview" style="max-width:100%;">',
            unsafe_allow_html=True
        )

        # Provide download button
        st.download_button(
            "📥 Download GIF",
            gif_data,
            file_name="your_gif.gif",
            mime="image/gif"
        )

else:
    st.info("Please upload at least 2 image files to create a GIF.")
