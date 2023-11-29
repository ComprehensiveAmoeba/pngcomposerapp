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
# ****** Good luck with the Thrassvent Quest!


#  ______  _______  _______  ______     ______            _______ 
#(  ____ \(  ___  )(  ___  )(  __  \   (  ___ \ |\     /|(  ____ \
#| (    \/| (   ) || (   ) || (  \  )  | (   ) )( \   / )| (    \/
#| |      | |   | || |   | || |   ) |  | (__/ /  \ (_) / | (__    
#| | ____ | |   | || |   | || |   | |  |  __ (    \   /  |  __)   
#| | \_  )| |   | || |   | || |   ) |  | (  \ \    ) (   | (      
#| (___) || (___) || (___) || (__/  )  | )___) )   | |   | (____/\
#(_______)(_______)(_______)(______/   |/ \___/    \_/   (_______/






# Constants
MAX_IMAGES = 24
IMAGE_WIDTH = 4
IMAGE_HEIGHT = 6
FRAME_OPTIONS = {"chukwa": 2, "chak k’an": 1}
CORRECT_CHOICES = {
    8: "chak k’an",
    10: "chak k’an",
    12: "chak k’an",
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

def create_final_image(uploaded_files_data):
    frame_size = Image.open(uploaded_files_data[0]['file']).size
    final_img = Image.new('RGBA', (IMAGE_WIDTH * frame_size[0], IMAGE_HEIGHT * frame_size[1]))

    for data in uploaded_files_data:
        frame = extract_frame(data['file'], FRAME_OPTIONS[data['frame_choice']])
        if frame:
            x = ((data['position'] - 1) % IMAGE_WIDTH) * frame.width
            y = ((data['position'] - 1) // IMAGE_WIDTH) * frame.height
            final_img.paste(frame, (x, y))

    return final_img

def check_win_conditions(uploaded_files_data):
    for data in uploaded_files_data:
        correct_choice = CORRECT_CHOICES.get(data['position'], "chukwa")
        if FRAME_OPTIONS[data['frame_choice']] != FRAME_OPTIONS[correct_choice]:
            return False
    return True

def are_positions_unique(uploaded_files_data):
    positions = [data['position'] for data in uploaded_files_data]
    return len(positions) == len(set(positions))

def main():
    st.title("Amazonian Workshop")

    uploaded_files = st.file_uploader("Upload mosaic shards", type="gif", accept_multiple_files=True)

    uploaded_files_data = []

    if len(uploaded_files) > 0:
        for i, uploaded_file in enumerate(uploaded_files):
            file_label = uploaded_file.name
            unique_key = f"{file_label}_{i}"
            col1, col2 = st.columns([3, 1])
            with col1:
                position = st.number_input(f"{file_label} - Position (1-24):", min_value=1, max_value=24, key=f"pos_{unique_key}")
            with col2:
                frame_choice = st.radio("", options=list(FRAME_OPTIONS.keys()), key=f"choice_{unique_key}", horizontal=True)
            uploaded_files_data.append({'file': uploaded_file, 'position': position, 'frame_choice': frame_choice})

    if st.button("Craft the Mosaic"):
        if len(uploaded_files) == MAX_IMAGES:
            if are_positions_unique(uploaded_files_data):
                if check_win_conditions(uploaded_files_data):
                    final_image = create_final_image(uploaded_files_data)
                    st.image(final_image)
                    st.success("As the hidden message of the ancient mosaic unites...")
                else:
                    st.error("The mosaic pieces are not in the correct order. Try again.")
            else:
                st.error("There are overlapping positions. Each image must have a unique position.")
        else:
            st.error("You need to upload exactly 24 images to craft the mosaic.")

if __name__ == "__main__":
    main()




