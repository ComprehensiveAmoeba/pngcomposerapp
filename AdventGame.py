import streamlit as st
from PIL import Image, UnidentifiedImageError
import io

# ('-. .-.                .-') _    ('-. .-.   ('-.  _  .-')     ('-.  ,---. 
#( OO )  /               (  OO) )  ( OO )  / _(  OO)( \( -O )  _(  OO) |   | 
#,--. ,--.  ,-.-')       /     '._ ,--. ,--.(,------.,------. (,------.|   | 
#|  | |  |  |  |OO)      |'--...__)|  | |  | |  .---'|   /`. ' |  .---'|   | 
#|   .|  |  |  |  \      '--.  .--'|   .|  | |  |    |  /  | | |  |    |   | 
#|       |  |  |(_/         |  |   |       |(|  '--. |  |_.' |(|  '--. |  .' 
#|  .-.  | ,|  |_.'         |  |   |  .-.  | |  .--' |  .  '.' |  .--' `--'  
#|  | |  |(_|  |            |  |   |  | |  | |  `---.|  |\  \  |  `---..--.  
#`--' `--'  `--'            `--'   `--' `--' `------'`--' '--' `------''--'  
# ****** Hello black hat Shaman!!!
# ****** You were very smart for coming here, 
# ****** but even this way it won't be that easy to guess the password 
# ****** without reading the full letter unveiled by the mosaic. 


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
    st.title("Amazonian Workshop")

    uploaded_files = st.file_uploader("Upload mosaic shards", type="gif", accept_multiple_files=True)

    positions = []
    frame_choices = []

    if len(uploaded_files) > 0:
        for i, uploaded_file in enumerate(uploaded_files):
            file_label = uploaded_file.name
            col1, col2 = st.columns([3, 1])
            with col1:
                pos_label = f"{file_label} - Position (1-24):"
                positions.append(st.number_input(pos_label, min_value=1, max_value=24, key=f"pos_{i}"))
            with col2:
                frame_choice_label = f""
                frame_choices.append(st.radio(frame_choice_label, options=list(FRAME_OPTIONS.keys()), key=f"choice_{i}", horizontal=True))

        if st.button("Craft the Mosaic"):
            if len(uploaded_files) == MAX_IMAGES and check_win_conditions(positions, frame_choices):
                final_image = create_final_image(uploaded_files, positions, frame_choices)
                st.image(final_image)
                st.success("The password to open the chamber of secrets is one of the options posted in our slack channel, in the same way it was written")

                # Save the final image to a buffer
                buf = io.BytesIO()
                final_image.save(buf, format="PNG")

                # Provide a download link to the final image
                st.download_button(
                    label="Download the full mosaic",
                    data=buf.getvalue(),
                    file_name="final_image.png",
                    mime="image/png"
                )
            else:
                st.warning("Try harder to unveil the decisive hint to the password")

if __name__ == "__main__":
    main()
