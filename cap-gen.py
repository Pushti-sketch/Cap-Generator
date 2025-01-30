import easyocr
import google.generativeai as genai
import streamlit as st
from PIL import Image

# Initialize the EasyOCR reader (English language)
reader = easyocr.Reader(['en'])
api_key_1 = st.secrets["google_api_key"]
# Function to extract text from an image using EasyOCR
def extract_text_from_image(image):
    result = reader.readtext(image)
    extracted_text = ' '.join([text[1] for text in result])
    return extracted_text

# Function to generate caption using Gemini API (via Google SDK)
def generate_caption_with_gemini(extracted_text):
    # Set up the API key and model using google.generativeai
    genai.configure(api_key=api_key_1)  # Replace with your actual API key
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Prepare the prompt
    prompt = f"{extracted_text} This is for Charusat University, Create an attractive caption from the following details provided also use emojis."
    
    # Generate content with the model
    response = model.generate_content(prompt)
    
    return response.text

# Streamlit UI for file upload and display
st.title("Text Extraction and Caption Generation using Gemini")
st.markdown("Upload an image to extract text and generate an attractive caption.")

# Image upload by the user
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Display uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Extract text from the image
    with st.spinner("Extracting text from the image..."):
        extracted_text = extract_text_from_image(image)
        st.write("Extracted Text:")
        st.write(extracted_text)

    # Button to generate the caption using Gemini API
    generate_button = st.button("Generate Caption with Gemini")

    if generate_button:
        with st.spinner("Generating caption..."):
            caption = generate_caption_with_gemini(extracted_text)
            st.write("Generated Caption:")
            st.write(caption)
