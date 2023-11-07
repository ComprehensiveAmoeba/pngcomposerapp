import streamlit as st
from PIL import Image, UnidentifiedImageError
import io

# Define constants
MAX_IMAGES = 24
IMAGE_WIDTH = 4
IMAGE_HEIGHT = 6
PASS_CODES = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]  # Add your list of pass codes here

def validate_and_extract_frames(uploaded_files, pass_codes):
    # This will hold the extracted frames
    frames = []

    for i, uploaded_file in enumerate(uploaded_files):
        try:
            # Open the uploaded image file
            gif = Image.open(uploaded_file)

            # Validate pass code
            if pass_codes[i] < gif.n_frames:
                gif.seek(pass_codes[i])
                frame = gif.copy()
                frames.append(frame)
            else:
                frames.append(None)

        except UnidentifiedImageError:
            frames.append(None)

    return frames

def create_final_image(frames):
    # Create an empty image with the correct dimensions
    final_img = Image.new('RGBA', (IMAGE_WIDTH * frames[0].width, IMAGE_HEIGHT * frames[0].height))

    # Populate the final image with the frames
    for i, frame in enumerate(frames):
        if frame:
            x = (i % IMAGE_WIDTH) * frame.width
            y = (i // IMAGE_WIDTH) * frame.height
            final_img.paste(frame, (x, y))

    return final_img

def main():
    st.title("GIF Frame Composer")

    # File uploader allows user to add up to 24 GIFs
    uploaded_files = st.file_uploader("Upload GIFs", type="gif", accept_multiple_files=True)

    if len(uploaded_files) > 0:
        # Prompt for pass codes
        pass_codes = []
        for i, uploaded_file in enumerate(uploaded_files):
            pass_code = st.text_input(f"Enter Pass Code for GIF {i+1}", key=i)
            try:
                pass_codes.append(int(pass_code))
            except ValueError:
                st.error(f"Invalid Pass Code for GIF {i+1}. Please enter a number.")
                return
        
        # Process the GIFs
        frames = validate_and_extract_frames(uploaded_files, pass_codes)

        # Check if all passcodes are valid
        if None not in frames and len(frames) == MAX_IMAGES:
            st.success("You cracked the code, here's another hint: It is Paulsible you could try any of the provided options in our Slack Channel")
        else:
            st.warning("Try harder to get an additional hint")

        # Create the final image
        final_image = create_final_image(frames)

        # Display the final image
        st.image(final_image)

        # Save the final image to a buffer
        buf = io.BytesIO()
        final_image.save(buf, format="PNG")

        # Provide a download link to the final image
        st.download_button(
            label="Download the final image",
            data=buf.getvalue(),
            file_name="final_image.png",
            mime="image/png"
        )

if __name__ == "__main__":
    main()
