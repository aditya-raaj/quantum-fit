import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ------------------ Load API Key Securely ------------------ #
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ GOOGLE_API_KEY not found. Please set it in Streamlit Secrets or .env.")
    st.stop()

genai.configure(api_key=api_key)

# ------------------ Gemini AI Function ------------------ #
def get_gemini_response(height, weight, goal, input_text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
You are an expert fitness coach. Analyze the following inputs:
- Height: {height} cm
- Weight: {weight} kg
- Goal: {goal}
- Notes: {input_text}

Tasks:
1. Create a detailed 7-day Push-Pull-Legs workout plan (no repetition of same description).
2. Include estimated calorie usage per exercise.
3. Provide a basic daily nutrient breakdown with Indian food references.
4. Mention general safety tips.

Format:
- Use horizontal lines (---) to separate sections.
- Avoid tables and keep formatting clean and readable.
"""
    response = model.generate_content([prompt])
    return response.text

# ------------------ Streamlit UI ------------------ #
st.set_page_config(page_title="Quantum Fit", page_icon="💪🏼", layout="centered")
st.title("💪🏼 Quantum Fit")
st.markdown("### Your AI-Powered Personalized Fitness Planner")
st.markdown("Get a **custom workout + nutrition plan** based on your stats and goals — powered by Google's Gemini AI.")

# --- User Inputs --- #
with st.form("fitness_form"):
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Height (in cm):", min_value=50, max_value=300, step=1)
    with col2:
        weight = st.number_input("Weight (in kg):", min_value=10, max_value=300, step=1)

    goal = st.selectbox("Fitness Goal:", ["Cutting", "Bulking", "Recomp"])
    input_text = st.text_area("Any fitness preferences, allergies, injuries, or dietary notes:")

    submitted = st.form_submit_button("Generate My Plan")

# --- Generate Plan --- #
if submitted:
    if not height or not weight:
        st.error("Please enter both height and weight.")
    else:
        with st.spinner("Generating your personalized plan... 💡"):
            try:
                response = get_gemini_response(height, weight, goal, input_text)
                st.markdown("## 🏋🏼 Personalized Exercise & Nutrition Plan")
                st.markdown(response)
            except Exception as e:
                st.error(f"An error occurred while generating your plan: {e}")
