import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from fpdf import FPDF
import unicodedata
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt


# ------------------ Load API Key ------------------ #
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ GOOGLE_API_KEY not found. Please set it in Streamlit Secrets or .env file.")
    st.stop()

genai.configure(api_key=api_key)

# ------------------ Gemini Call Function ------------------ #
@st.cache_data(show_spinner=False)
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
- Avoid using complex formatting; write cleanly and clearly.
- Use plain English with a professional, friendly tone.
- Keep content unique for each day of the workout section.
"""

    response = model.generate_content([prompt])
    return response.text

# ------------------ PDF Export Helper ------------------ #
def export_to_pdf(content, filename="fitness_plan.pdf"):
    # Normalize Unicode to remove unsupported characters
    clean_content = unicodedata.normalize("NFKD", content).encode("ascii", "ignore").decode("ascii")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in clean_content.split('\n'):
        pdf.multi_cell(0, 10, line)

    pdf.output(filename)
    return filename

# ------------------ Generate Charts ------------------ #
def plot_workout_chart():
    # Example data: workout frequency per day
    days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat']
    workouts = [1, 2, 2, 1, 3, 2, 1]

    fig, ax = plt.subplots()
    ax.bar(days, workouts, color='skyblue')
    ax.set_title("Weekly Workout Frequency")
    ax.set_xlabel("Days of the Week")
    ax.set_ylabel("Number of Workouts")
    st.pyplot(fig)

def plot_nutrition_chart():
    # Example data for macronutrients (grams)
    macros = ['Protein', 'Carbs', 'Fats']
    daily_values = [150, 200, 70]

    fig = px.pie(
        names=macros, 
        values=daily_values, 
        title="Daily Nutrition Breakdown (Macronutrients)",
        labels=macros
    )
    st.plotly_chart(fig)

# ------------------ Streamlit UI ------------------ #
st.set_page_config(page_title="Quantum Fit", page_icon="💪🏼", layout="centered")
st.title("💪🏼 Quantum Fit")
st.markdown("### Your AI-Powered Personalized Fitness Planner")
st.markdown("Get a **custom workout + nutrition plan** based on your stats and goals — powered by Google's Gemini AI.")

# ------------------ Form Inputs ------------------ #
with st.form("fitness_form"):
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Height (in cm):", min_value=50, max_value=300)
        age = st.number_input("Age (in years):", min_value=5, max_value=100)
    with col2:
        weight = st.number_input("Weight (in kg):", min_value=10, max_value=300)
        gender = st.selectbox("Gender:", ["Male", "Female"])

    goal = st.selectbox("Fitness Goal:", ["Cutting", "Bulking", "Recomp"])
    input_text = st.text_area("Any fitness preferences, allergies, injuries, or dietary notes:")

    submitted = st.form_submit_button("Generate My Plan")

# ------------------ Result ------------------ #
if submitted:
    if not height or not weight or not age:
        st.error("Please enter height, weight, and age.")
        st.stop()

    bmi = weight / ((height / 100) ** 2)
    st.metric("📊 Your BMI", f"{bmi:.1f}")

    with st.spinner("Generating your personalized plan..."):
        try:
            response_text = get_gemini_response(height, weight, age, gender, goal, input_text)

            if "---" in response_text:
                sections = response_text.split('---')
                tabs = st.tabs(["📝 Overview", "📆 Workout", "🥗 Nutrition", "💊 Supplements", "🛡️ Lifestyle"])
                titles = ["Overview", "Workout Plan", "Nutrition Guidelines", "Supplement Advice", "Lifestyle & Safety"]

                for tab, title, section in zip(tabs, titles, sections):
                    with tab:
                        st.subheader(title)
                        st.markdown(section.strip())
            else:
                st.warning("Couldn't separate sections properly. Showing full text.")
                st.markdown(response_text)

            # Generate Charts
            st.subheader("📊 Visualize Your Weekly Plan")
            plot_workout_chart()
            plot_nutrition_chart()

            # Export to PDF
            filename = export_to_pdf(response_text)
            with open(filename, "rb") as pdf_file:
                st.download_button("📄 Download as PDF", pdf_file, file_name="My_Fitness_Plan.pdf")

        except Exception as e:
            st.error(f"An error occurred: {e}")
