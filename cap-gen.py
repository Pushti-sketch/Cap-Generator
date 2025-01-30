import easyocr
import google.generativeai as genai
import streamlit as st
from PIL import Image
import random
import re

reader = easyocr.Reader(['en'])
api_key_1 = st.secrets["google_api_key"]

def extract_text_from_image(image):
    result = reader.readtext(image)
    extracted_text = ' '.join([text[1] for text in result])
    return extracted_text

# def clean_text_for_caption(extracted_text):
#     cleaned_text = re.sub(r'(@[A-Za-z0-9_]+)', '', extracted_text)
#     cleaned_text = re.sub(r'#\w+', '', cleaned_text)
#     return cleaned_text.strip()

def generate_caption_with_gemini(extracted_text):
    genai.configure(api_key=api_key_1)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = f"{extracted_text} This is for Charusat University, Create an attractive and detailed caption from the following details provided also use emojis. also in output just give me a single detailed and attractive clear caption and dont write anything else"
    
    response = model.generate_content(prompt)
    
    return response.text

loading_words = ["Cooking", "Cooking hard", "Whipping up something cool", "Crafting the magic", "Making it perfect", "Preparing your masterpiece"]

st.title("CSE Caption Generator 🖼️")
st.markdown("Upload an image to generate an attractive caption.")

uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    with st.spinner(f"{random.choice(loading_words)}..."):
        extracted_text = extract_text_from_image(image)
        # cleaned_text = clean_text_for_caption(extracted_text)

    generate_button = st.button("Generate Caption")

    if generate_button:
        with st.spinner(f"{random.choice(loading_words)}..."):
            caption = generate_caption_with_gemini(extracted_text)
            st.write("Caption Output :")
            st.write(caption)
footer="""<style>
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
color: grey;
text-align: center;
}
</style>
<div class="footer">
<p>Developed by Jay AKA GameOn</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
