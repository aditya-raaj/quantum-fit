import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

##initialize our streamlit app
st.set_page_config(page_title="Food Calorie Meter", page_icon="🍏")

# Set custom styles
st.markdown("""
    <style>
        .main {
            background-color: #f0f0f0;
            padding: 2rem;
            border-radius: 10px;
        }
        .header-text {
            font-size: 24px;
            color: #333333;
        }
        .button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
        }
        .subheader-text {
            font-size: 20px;
            color: #555555;
            margin-top: 1.5rem;
        }
        .response-text {
            font-size: 18px;
            color: #444444;
            white-space: pre-line;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Food Calorie Meter")

input = st.text_input("Input Prompt: ", key="input")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the Total Calories")

input_prompt = """
You are an expert in nutritionist where you need to see the food items from the image
and calculate the total calories, also provide the details of every food item with calories intake
in the below format:

1. Item 1 - no of calories
2. Item 2 - no of calories
----

Your task is to create a model that takes an image containing various food items as input
and outputs the total calories along with a detailed list of each food item and its respective calorie intake.
Give both PRO'S and CON'S of eating that food.
"""

## If submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)

    st.subheader("The Response is")
    st.markdown(f'<div class="response-text">{response}</div>', unsafe_allow_html=True)
