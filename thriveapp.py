import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder
import pickle
import google.generativeai as genai
import os
import speech_recognition as sr

# Set page configuration
st.set_page_config(page_title="SUD Patient Analysis", page_icon="\ud83d\udd70", layout="wide")

# Set up the API key
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', st.secrets.get("GOOGLE_API_KEY"))
genai.configure(api_key=GOOGLE_API_KEY)

# Data Loading and Preprocessing
@st.cache_data
def load_and_preprocess_data():
    # Load data from CSV files
    sud_df = pd.read_csv("Synthetic_SUD_Patient_Data.csv")
    har_df = pd.read_csv("Synthetic_HAR_Data_for_SUD_Patients2.csv")

    # Merge datasets on Patient_ID
    combined_df = pd.merge(sud_df, har_df, on="Patient_ID", how="inner")

    # Fill missing values with a placeholder
    combined_df.fillna(value="Unknown", inplace=True)

    return combined_df

# Dashboard Page
def dashboard(data):
    st.title("Dashboard: SUD Patient Insights")
    st.write("Overview of relapse risks and patient statistics.")

    st.subheader("Relapse Risk Distribution")
    relapse_counts = data['Relapse_Risk'].value_counts()
    st.bar_chart(relapse_counts)

    st.subheader("High-Risk Patients (Relapse Risk: High)")
    high_risk = data[data['Relapse_Risk'] == 'High']
    st.write(high_risk[['Patient_ID', 'Substance_Type', 'Treatment_Type']])

    st.subheader("Key Statistics")
    st.write(data.describe())

# Data Visualization Page
def data_visualization(data):
    st.title("Data Visualization")
    st.write("Explore visual trends in patient data.")

    st.subheader("Average Heart Rate by Relapse Risk")
    avg_heart_rate = data.groupby('Relapse_Risk')['Heart_Rate'].mean().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=avg_heart_rate, x='Relapse_Risk', y='Heart_Rate', ax=ax)
    ax.set_title("Average Heart Rate by Relapse Risk")
    st.pyplot(fig)

    st.subheader("Activity Levels by Relapse Risk")
    avg_activity = data.groupby('Relapse_Risk')[['X_accel', 'Y_accel', 'Z_accel']].mean().reset_index()
    fig, ax = plt.subplots()
    avg_activity.set_index('Relapse_Risk').plot(kind='bar', stacked=True, ax=ax)
    ax.set_title("Average Activity Levels by Relapse Risk")
    st.pyplot(fig)

    st.subheader("Filter Data")
    relapse_risk_filter = st.selectbox("Select Relapse Risk Level", options=data['Relapse_Risk'].unique())
    filtered_data = data[data['Relapse_Risk'] == relapse_risk_filter]
    st.write(filtered_data)

# ML Prediction Prototype
def ml_prediction_prototype():
    st.title("ML Prediction: Relapse Risk")
    st.write("Enter patient details to simulate a relapse risk prediction.")

    with st.form("prediction_form"):
        age = st.number_input("Age", min_value=0, max_value=120, value=30)
        gender = st.selectbox("Gender", ["Male", "Female"])
        substance_type = st.selectbox("Substance Type", ["Alcohol", "Cannabis", "Opioids", "Cocaine", "Methamphetamine", "Polysubstance"])
        treatment_type = st.selectbox("Treatment Type", ["Residential Rehab", "Detox", "Counseling", "Medication-Assisted Treatment (MAT)"])
        support_system = st.selectbox("Support System", ["Strong", "Moderate", "Weak"])
        treatment_outcome = st.selectbox("Treatment Outcome", ["Ongoing", "Recovered", "Relapsed"])
        submit = st.form_submit_button("Predict Relapse Risk")

    if submit:
        with st.spinner("Generating prediction..."):
            if treatment_outcome == "Ongoing" or support_system == "Weak" or substance_type in ["Cocaine", "Methamphetamine"]:
                predicted_risk = "High"
                confidence = 85
            elif treatment_outcome == "Relapsed" or age > 50:
                predicted_risk = "Medium"
                confidence = 65
            else:
                predicted_risk = "Low"
                confidence = 95

        st.subheader("Prediction Result")
        st.write(f"**Predicted Relapse Risk:** {predicted_risk}")
        st.write(f"**Confidence:** {confidence}%")

# Function to generate a case report using Google Generative AI
def generate_case_report(patient_id, notes):
    try:
        # Refined prompt for case report generation
        prompt = f"""
        Generate a detailed case report for a Substance Use Disorder (SUD) patient.
        Patient ID: {patient_id}.
        Case notes:
        {notes}
        Include the following sections:
        1. Patient Overview
        2. Diagnosis
        3. Treatment Plan
        4. Medication Dosage and Instructions (if applicable)
        5. Recommendations and Referrals
        6. Follow-Up Plan
        Format the report for professional documentation.
        """

        # Use Google Generative AI's GenerativeModel
        model = genai.GenerativeModel('gemini-pro')  # Ensure the correct model is specified
        response = model.generate_content(prompt)

        # Extract the response text
        report = response.text
        return report
    except Exception as e:
        st.error(f"Error generating report: {e}")
        return "Sorry, I couldn't process your request."

# Case Management page updated with Google Generative AI integration and transcription
def case_management(data):
    st.title("Case Management")
    st.write("Manage and monitor patient cases with AI-generated reports and multilingual transcription.")

    # Upload audio file
    st.subheader("Upload Audio File")
    audio_file = st.file_uploader("Upload a patient conversation (audio file)", type=["wav", "mp3"])

    transcription = ""
    if audio_file:
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)
            try:
                transcription = recognizer.recognize_google(audio_data, language="en-US")  # Change language as needed
                st.success("Transcription completed successfully.")
                st.text_area("Transcription", transcription, height=200)
            except Exception as e:
                st.error(f"Error in transcription: {e}")

    # Patient ID and additional notes
    st.subheader("Patient Details")
    patient_id = st.text_input("Enter Patient ID", placeholder="E.g., PID12345")
    notes = st.text_area("Enter Additional Notes", placeholder="E.g., Patient has shown improvement...")

    # Generate the report
    if st.button("Generate AI Report"):
        if not patient_id:
            st.error("Patient ID is required to generate a report.")
        else:
            combined_notes = f"{notes}\n\nTranscription:\n{transcription}" if transcription else notes

            # Generate the case report
            report = generate_case_report(patient_id, combined_notes)
            st.subheader("Generated Case Report")
            st.write(report)

# Navigation
page = st.sidebar.selectbox("Select a Page", ["Dashboard", "Data Visualization", "ML Prediction", "Case Management"])

data = load_and_preprocess_data()

if page == "Dashboard":
    dashboard(data)
elif page == "Data Visualization":
    data_visualization(data)
elif page == "ML Prediction":
    ml_prediction_prototype()
elif page == "Case Management":
    case_management(data)
