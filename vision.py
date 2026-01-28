# Q&A Chatbot

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

import streamlit as st
import os
import base64
import io
from PIL import Image
from groq import Groq

# Configure Groq API
api_key = os.getenv("GROQ_API_KEY")
# We'll just init client here, maybe check validity later or let it fail gracefully if key is missing
client = Groq(api_key=api_key) if api_key else None

def get_base64_of_image(image):
    buffered = io.BytesIO()
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

def get_groq_response(input_text, image):
    if not client:
        return "Error: GROQ_API_KEY not found."

    base64_image = get_base64_of_image(image)
    
    # Construct the message content
    content = []
    if input_text:
        content.append({"type": "text", "text": input_text})
    
    # Add image
    content.append({
        "type": "image_url", 
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
        }
    })
    
    try:
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

##initialize our streamlit app

st.set_page_config(page_title="Groq Vision Demo")

st.header("Groq Vision Application")
input_text=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Tell me about the image")

## If ask button is clicked

if submit:
    if uploaded_file is None:
        st.error("Please upload an image first")
    else:
        response=get_groq_response(input_text, image)
        st.subheader("The Response is")
        st.write(response)
