import streamlit as st
import imageio.v3 as iio
import tempfile
import os

st.set_page_config(page_title="GifCraft 🎨", page_icon="🌀")

st.title("🎨 GifCraft - Create Your Own GIFs")
st.write("Upload images and get a fun looping GIF instantly!")

# Step 1: Upload multiple images
uploaded_files = st.file_uploader("📸 Upload multiple images", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Duration input
duration = st.slider("⏱️ Duration per frame (ms)", min_value=100, max_value=2000, step=100, value=500)

if uploaded_files:
    with st.spinner("Creating your GIF..."):

        # Step 2: Save uploaded images temporarily
        temp_dir = tempfile.mkdtemp()
        filenames = []

        for i, file in enumerate(uploaded_files):
            temp_path = os.path.join(temp_dir, f"frame_{i}.png")  # uniform format
            with open(temp_path, "wb") as f:
                f.write(file.read())
            filenames.append(temp_path)

        # Step 3: Read images and create GIF
        images = [iio.imread(fname) for fname in filenames]
        gif_path = os.path.join(temp_dir, "output.gif")
        iio.imwrite(gif_path, images, duration=duration, loop=0)

        # Step 4: Show the GIF
        st.success("✅ GIF created successfully!")
        st.image(gif_path, caption="Your Animated GIF 🎉", use_column_width=True)

        # Step 5: Download option
        with open(gif_path, "rb") as f:
            st.download_button("📥 Download GIF", f, file_name="your_gif.gif", mime="image/gif")

else:
    st.info("Upload 2 or more images (JPG or PNG) to get started.")
