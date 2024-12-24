import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression

# Set page configuration
st.set_page_config(page_title="SUD Patient Analysis", page_icon="📊", layout="wide")

# Data Loading and Preprocessing
@st.cache_data
def load_and_preprocess_data():
    # Load data from GitHub
    github_base_url = "https://raw.githubusercontent.com/your-github-username/your-repo-name/main/"
    sud_patient_data_url = github_base_url + "Synthetic_SUD_Patient_Data.csv"
    har_data_url = github_base_url + "Synthetic_HAR_Data_for_SUD_Patients2.csv"
    
    # Read the data
    sud_df = pd.read_csv(sud_patient_data_url)
    har_df = pd.read_csv(har_data_url)
    
    # Merge datasets if necessary
    combined_df = pd.merge(sud_df, har_df, on="PATIENT_ID", how="inner")

    return combined_df

# Pages
def dashboard(data):
    st.title("Dashboard: SUD Patient Insights")
    st.write("Overview of relapse risks and patient statistics.")

    # Relapse Risk Distribution
    st.subheader("Relapse Risk Distribution")
    relapse_counts = data['RELAPSE_RISK'].value_counts()
    st.bar_chart(relapse_counts)

    # High-Risk Patients
    st.subheader("High-Risk Patients (Relapse Risk: High)")
    high_risk = data[data['RELAPSE_RISK'] == 'High']
    st.write(high_risk[['PATIENT_ID', 'SUBSTANCE_TYPE', 'TREATMENT_TYPE']])

    # Key Statistics
    st.subheader("Key Statistics")
    st.write(data.describe())

def data_visualization(data):
    st.title("Data Visualization")
    st.write("Explore visual trends in patient data.")

    # Average Heart Rate by Relapse Risk
    st.subheader("Average Heart Rate by Relapse Risk")
    avg_heart_rate = data.groupby('RELAPSE_RISK')['AVG_HEART_RATE'].mean().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=avg_heart_rate, x='RELAPSE_RISK', y='AVG_HEART_RATE', ax=ax)
    ax.set_title("Average Heart Rate by Relapse Risk")
    st.pyplot(fig)

    # Activity Level Visualization
    st.subheader("Average Activity Levels by Relapse Risk")
    avg_activity = data.groupby('RELAPSE_RISK')[['AVG_X_ACCEL', 'AVG_Y_ACCEL', 'AVG_Z_ACCEL']].mean().reset_index()
    fig, ax = plt.subplots()
    avg_activity.set_index('RELAPSE_RISK').plot(kind='bar', stacked=True, ax=ax)
    ax.set_title("Average Activity Levels by Relapse Risk")
    st.pyplot(fig)

    # Filter and display data
    st.subheader("Filter Data")
    relapse_risk_filter = st.selectbox("Select Relapse Risk Level", options=data['RELAPSE_RISK'].unique())
    filtered_data = data[data['RELAPSE_RISK'] == relapse_risk_filter]
    st.write(filtered_data)

def ml_prediction(model, encoder):
    st.title("ML Prediction: Relapse Risk")
    st.write("Enter patient details to predict relapse risks.")

    with st.form("prediction_form"):
        age = st.number_input("Age", min_value=0, max_value=120, value=30)
        gender = st.selectbox("Gender", ["Male", "Female"])
        substance_type = st.selectbox("Substance Type", ["Alcohol", "Cannabis", "Opioids", "Cocaine", "Methamphetamine", "Polysubstance"])
        treatment_type = st.selectbox("Treatment Type", ["Residential Rehab", "Detox", "Counseling", "Medication-Assisted Treatment (MAT)"])
        support_system = st.selectbox("Support System", ["Strong", "Moderate", "Weak"])
        submit = st.form_submit_button("Predict Relapse Risk")

        if submit:
            input_data = pd.DataFrame({
                "Age": [age],
                "Gender": [gender],
                "Substance_Type": [substance_type],
                "Treatment_Type": [treatment_type],
                "Support_System": [support_system]
            })
            encoded_input = encoder.transform(input_data)
            prediction = model.predict(encoded_input)
            st.write(f"Predicted Relapse Risk: **{prediction[0]}**")

def case_management(data):
    st.title("Case Management")
    st.write("Manage and monitor patient cases.")
    patient_id = st.text_input("Enter Patient ID")
    notes = st.text_area("Add Case Notes")
    if st.button("Save Notes"):
        st.success(f"Notes saved for patient {patient_id}!")

# Navigation
page = st.sidebar.selectbox("Select a Page", ["Dashboard", "Data Visualization", "ML Prediction", "Case Management"])

# Load data
data = load_and_preprocess_data()

# Display the selected page
if page == "Dashboard":
    dashboard(data)
elif page == "Data Visualization":
    data_visualization(data)
elif page == "ML Prediction":
    # Load a dummy encoder and model for demo
    encoder = OneHotEncoder(handle_unknown='ignore')
    model = LogisticRegression()
    ml_prediction(model, encoder)
elif page == "Case Management":
    case_management(data)
