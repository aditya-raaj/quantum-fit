import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to interact with the generative AI model
def get_gemini_response(height, weight, goal, input_text):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Use the correct model name
    prompt = f"""
    You are an expert fitness coach. Your task is to analyze the following inputs:
    - Height: {height} cm
    - Weight: {weight} kg
    - Goal: {goal} (e.g., Cutting, Bulking, Recomp)
    - Other Important Info: {input_text} (eg. for any allergy or preference or injury record)
    
    Based on these inputs:
    1. Create a detailed, full-week exercise plan (Sunday to Saturday) based on a Push-Pull-Legs routine ( DONT SAY REPEAT LIKE THE PREVIOUS DAY GIVE DAY WISE IN DEPTH ANALYSIS ).
    2. Include the calorie usage for each exercise in the plan.
    3. Also give a basic chart of amount of nutrients to consume per day according to the exercise ( i am from india so give food references according to it if required )
    3. Provide safety precautions for overall exercise.

    Additional Instructions: Keep a similar formatting and dont use table

    """
    response = model.generate_content([prompt])
    return response.text

# Streamlit UI setup
st.set_page_config(page_title="Quantum Fit", page_icon="💪🏼")
st.title("💪🏼 Quantum Fit")
st.subheader("Your One-Stop Solution for Fitness Goals")

# Input fields
height = st.number_input("Enter your Height (in cm):", min_value=50, max_value=300, step=1, format="%d")
weight = st.number_input("Enter your Weight (in kg):", min_value=10, max_value=300, step=1, format="%d")
goal = st.selectbox("What is your Goal?", ["Cutting", "Bulking", "Recomp"])
input_text = st.text_input("Describe your fitness preferences or special requirements :")

# Submit button
if st.button("Help me with Exercises"):
    if height and weight and goal:
        try:
            response = get_gemini_response(height, weight, goal, input_text)
            st.subheader("Generated Exercise Plan")
            st.write(response)  # Use plain text display for the response
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.error("Please fill in all inputs to proceed.")
