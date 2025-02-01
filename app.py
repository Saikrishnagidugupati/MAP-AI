from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# configure Google generative ai with api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#function to gemini response 
def get_gemini_response(input_text,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generative_content([input_txt,image[0]],prompt)
    return response.text

#function to setup input image
def input_image_setup(uploaed_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("NO file uploaded")
            

input_prompt = """
you are a tour guide. please describe landmark in image and provide detailed,including its name
"""

st.set_page_config(page_title="Gemini Landmark Description app",page_icon="🌎")
st.header("🌎 Gemini Landmark Description App")
input_text=st.text_input("📝 Input prompt:",key="input")
uploaded_file = st.file_uploader(" 🖼️ choose an image...",type=["jpg","jpeg","png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="uploaded Image.",use_column_width=True)

submit = st.button(" 🚀 Describe Landmark")

#if submit button is clicked
if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_response(input_text, image_data, input_text)
        st.subheader("📝 Description of Landmark:")
        st.write(response)
    except Exception as e:
        st.error(f" Error:{str(e)}")