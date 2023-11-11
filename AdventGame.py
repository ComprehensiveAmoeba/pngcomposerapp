import streamlit as st
from PIL import Image, UnidentifiedImageError
import io

# Constants
MAX_IMAGES = 24
IMAGE_WIDTH = 4
IMAGE_HEIGHT = 6
FRAME_OPTIONS = {"chukwa": 2, "chak k’an": 1}
CORRECT_CHOICES = {
    8: "chak k’an",
    10: "chak k’an",
    15: "chak k’an",
    16: "chak k’an",
    24: "chak k’an"
}

def extract_frame(uploaded_file, frame_number):
    try:
        gif = Image.open(uploaded_file)
        if frame_number < gif.n_frames:
            gif.seek(frame_number)
            return gif.copy()
        else:
            return None
    except UnidentifiedImageError:
        return None

def create_final_image(uploaded_files, positions, frame_choices):
    frame_size = Image.open(uploaded_files[0]).size
    final_img = Image.new('RGBA', (IMAGE_WIDTH * frame_size[0], IMAGE_HEIGHT * frame_size[1]))

    for file, pos, choice in zip(uploaded_files, positions, frame_choices):
        frame = extract_frame(file, FRAME_OPTIONS[choice])
        if frame:
            x = ((pos - 1) % IMAGE_WIDTH) * frame.width
            y = ((pos - 1) // IMAGE_WIDTH) * frame.height
            final_img.paste(frame, (x, y))

    return final_img

def check_win_conditions(positions, frame_choices):
    for pos, choice in zip(positions, frame_choices):
        correct_choice = CORRECT_CHOICES.get(pos, "chukwa")
        if choice != correct_choice:
            return False
    return True

def main():
    st.title("GIF Frame Composer")

    uploaded_files = st.file_uploader("Upload GIFs", type="gif", accept_multiple_files=True)

    if len(uploaded_files) > 0:
        positions = [st.number_input(f"Position for GIF {i+1} (1-24)", min_value=1, max_value=24, key=f"pos_{i}") for i in range(len(uploaded_files))]
        frame_choices = [st.radio(f"Frame Choice for GIF {i+1}", options=list(FRAME_OPTIONS.keys()), key=f"choice_{i}") for i in range(len(uploaded_files))]

        if st.button("Create Mosaic"):
            final_image = create_final_image(uploaded_files, positions, frame_choices)
            st.image(final_image)

            # Check win conditions
            if check_win_conditions(positions, frame_choices):
                st.success("Choose one of the options posted in our slack channel")
            else:
                st.warning("Try harder to unveil the decisive hint")

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
