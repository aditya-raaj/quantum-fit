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
def get_gemini_response(height, weight, age, gender, goal, input_text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
You are an expert fitness coach with years of experience in training diverse individuals across different age groups and genders. Your role is to provide a personalized fitness and nutrition plan tailored to the individual based on their physical attributes and personal preferences.

The user's profile is as follows:
- Height: {height} cm
- Weight: {weight} kg
- Age: {age} years
- Gender: {gender}
- Primary Goal: {goal} (options: Cutting, Bulking, Recomp)
- Special Notes: {input_text} (This may include allergies, past injuries, preferences like vegetarian/vegan, equipment limitations, time availability, etc.)

Your response should include the following clearly divided sections, using horizontal lines (---) to separate them. Avoid tables, and keep formatting plain but structured for easy reading on mobile and web.

### Sections to Include:

1. **Overview Summary**  
   - Brief explanation of how the user's profile affects their fitness journey.  
   - Why the chosen goal (e.g., Bulking) is appropriate and how the plan aligns with it.  
   - Consider age and gender in shaping the plan.

2. **Customized Weekly Workout Plan (Push-Pull-Legs Split)**  
   - Day-wise plan from Sunday to Saturday using Push, Pull, and Legs logic.  
   - Do **not** copy or repeat the same text — make each day unique.  
   - Include approx. **calories burned per workout** session or per exercise if possible.  
   - Make it practical and beginner-friendly if age or notes suggest so.

3. **Daily Nutrition Guidelines**  
   - A daily macro breakdown (calories, protein, carbs, fats).  
   - Recommend Indian food items for each macro group.  
   - Tailor it to gender and age (e.g., higher iron for women, calorie moderation for older individuals).  
   - Give both vegetarian and non-vegetarian options if not otherwise restricted.

4. **Supplement Recommendations (Optional)**  
   - Only suggest if relevant and backed by common practice.  
   - Mention natural alternatives where appropriate.  
   - Avoid medical claims.

5. **Lifestyle & Safety Recommendations**  
   - General safety precautions, especially if the user has injuries, age-related concerns, or is a beginner.  
   - Tips on rest, hydration, posture, warm-ups, cool-downs, and avoiding overtraining.

Formatting Guidelines:
- No bullet points inside bullet points.
- Avoid using  complex formatting; write cleanly and clearly.
- Use plain English with a professional, friendly tone.
- Keep content unique for each day of the workout section.
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
        age = st.number_input("Age (in years):", min_value=5, max_value=100, step=1)
    with col2:
        weight = st.number_input("Weight (in kg):", min_value=10, max_value=300, step=1)
        gender = st.selectbox("Gender:", ["Male", "Female"])

    goal = st.selectbox("Fitness Goal:", ["Cutting", "Bulking", "Recomp"])
    input_text = st.text_area("Any fitness preferences, allergies, injuries, or dietary notes:")

    submitted = st.form_submit_button("Generate My Plan")

# --- Generate Plan --- #
if submitted:
    if not height or not weight or not age:
        st.error("Please enter all required fields: height, weight, and age.")
    else:
        with st.spinner("Generating your personalized plan... 💡"):
            try:
                response = get_gemini_response(height, weight, age, gender, goal, input_text)
                st.markdown("## 🏋🏼 Personalized Exercise & Nutrition Plan")
                st.markdown(response)
            except Exception as e:
                st.error(f"An error occurred while generating your plan: {e}")
