import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, image, prompt):
    # Use the updated model name here
    model = genai.GenerativeModel('gemini-1.5-flash')
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

# Initialize the Streamlit app
st.set_page_config(page_title="Food Calorie Meter", page_icon="🍏")





st.title("Food Calorie Meter")

input = st.text_input("Input Prompt: ", key="input")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image = ""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the Total Calories")

input_prompt = """
You are an expert nutritionist. Your task is to analyze the food items shown in an image and calculate the total calories. Additionally, provide detailed information for each food item, including its calorie intake, in the following format:

1. Item 1 - no. of calories
2. Item 2 - no. of calories
----

Your model should take an image containing various food items as input and output the total calorie count, along with a detailed list of each food item and its respective calorie intake.

Additionally, include both the PROS and CONS of consuming each food item, such as health benefits or potential risks.
"""

# If submit button is clicked
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, input)

    st.subheader("The Response is")
    st.markdown(f'<div class="response-text">{response}</div>', unsafe_allow_html=True)
