# Quantum Fit: AI-Powered Personalized Fitness Planner
Quantum Fit is a Streamlit-based web application designed to help users achieve their fitness goals. By leveraging Google's Gemini AI (via `google.generativeai`), this app generates personalized weekly exercise plans and dietary recommendations based on user inputs such as height, weight, fitness goals, and preferences.

---

## **Preface**

![](https://github.com/aditya-raaj/quantum-fit/blob/main/archive/Quantum%20Fit.png?raw=true)
![](https://github.com/aditya-raaj/quantum-fit/blob/main/archive/Quantum%20Fit%20I.png?raw=true)
![](https://github.com/aditya-raaj/quantum-fit/blob/main/archive/Quantum%20Fit%20II.png?raw=true)


---

## Features
- **Personalized Weekly Exercise Plan**: Get a detailed, day-wise Push-Pull-Legs workout routine customized for your fitness goals (Cutting, Bulking, or Recomp).
- **Calorie Analysis**: Each exercise in the plan includes an estimation of calories burned.
- **Nutrition Guidance**: Provides a daily nutrient chart with Indian food recommendations tailored to your routine.
- **Safety Advice**: Offers safety precautions to follow during your exercise routine.
- **Streamlined User Experience**: Intuitive inputs for height, weight, fitness goals, and special requirements.

---

## Installation

To run the Quantum Fit application, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/quantum-fit.git
    cd quantum-fit
    ```

2. **Set Up Environment**:
    - Install [Python 3.7+](https://www.python.org/downloads/) if not already installed.
    - Install required dependencies:
      ```bash
      pip install -r requirements.txt
      ```
    - Create a `.env` file in the root directory and add your Google API key:
      ```
      GOOGLE_API_KEY=your_google_api_key_here
      ```

3. **Run the Application**:
    ```bash
    streamlit run app.py
    ```

---

## Usage

1. Open the application in your browser at `http://localhost:8501`.
2. Enter the following details:
   - **Height** (in cm)
   - **Weight** (in kg)
   - **Fitness Goal**: Choose from Cutting, Bulking, or Recomp.
   - **Additional Information**: Specify preferences like allergies, injuries, or other special requirements.
3. Click on the **Help me with Exercises** button to generate your customized plan.

---

## File Structure

```plaintext
quantum-fit/
│
├── app.py                  # Main application script
├── requirements.txt        # List of dependencies
├── .env                    # Environment variables (API key)
└── README.md               # Project documentation (this file)
```
---

## Requirements

  - Python 3.7 or higher
  - Dependencies (specified in requirements.txt):
    - ```streamlit```
    - ```google-generativeai```
    - ```python-dotenv```

---

## Contribution
Contributions are welcome! Please follow these steps to contribute:

1.Fork the repository.

2.Create a new branch:
```bash
      git checkout -b feature/your-feature-name
```

3.Make your changes and commit::
```bash
      git commit -m "Add your descriptive commit message"
```

4.Make your changes and commit::
```bash
      git push origin feature/your-feature-name
```

5.Open a pull request.

---

## License

This project is licensed under the MIT License.

---

## Disclaimer

This app provides general fitness advice based on AI-generated recommendations. Always consult a healthcare professional or certified trainer before starting any exercise routine, especially if you have pre-existing conditions or injuries.

  
