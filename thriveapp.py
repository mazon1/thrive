import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder
import pickle

# Set page configuration
st.set_page_config(page_title="SUD Patient Analysis", page_icon="📊", layout="wide")

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

# Load the trained model and encoder
@st.cache_resource
def load_model_and_encoder():
    # Load the retrained model and encoder
    with open("logistic_regression_retrained.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    with open("encoder_retrained.pkl", "rb") as encoder_file:
        encoder = pickle.load(encoder_file)
    return model, encoder

# Pages
def dashboard(data):
    st.title("Dashboard: SUD Patient Insights")
    st.write("Overview of relapse risks and patient statistics.")

    # Relapse Risk Distribution
    st.subheader("Relapse Risk Distribution")
    relapse_counts = data['Relapse_Risk'].value_counts()
    st.bar_chart(relapse_counts)

    # High-Risk Patients
    st.subheader("High-Risk Patients (Relapse Risk: High)")
    high_risk = data[data['Relapse_Risk'] == 'High']
    st.write(high_risk[['Patient_ID', 'Substance_Type', 'Treatment_Type']])

    # Key Statistics
    st.subheader("Key Statistics")
    st.write(data.describe())

def data_visualization(data):
    st.title("Data Visualization")
    st.write("Explore visual trends in patient data.")

    # Average Heart Rate by Relapse Risk
    st.subheader("Average Heart Rate by Relapse Risk")
    avg_heart_rate = data.groupby('Relapse_Risk')['Heart_Rate'].mean().reset_index()
    fig, ax = plt.subplots()
    sns.barplot(data=avg_heart_rate, x='Relapse_Risk', y='Heart_Rate', ax=ax)
    ax.set_title("Average Heart Rate by Relapse Risk")
    st.pyplot(fig)

    # Activity Level Visualization
    st.subheader("Average Activity Levels by Relapse Risk")
    avg_activity = data.groupby('Relapse_Risk')[['X_accel', 'Y_accel', 'Z_accel']].mean().reset_index()
    fig, ax = plt.subplots()
    avg_activity.set_index('Relapse_Risk').plot(kind='bar', stacked=True, ax=ax)
    ax.set_title("Average Activity Levels by Relapse Risk")
    st.pyplot(fig)

    # Filter and display data
    st.subheader("Filter Data")
    relapse_risk_filter = st.selectbox("Select Relapse Risk Level", options=data['Relapse_Risk'].unique())
    filtered_data = data[data['Relapse_Risk'] == relapse_risk_filter]
    st.write(filtered_data)

def ml_prediction():
    st.title("ML Prediction: Relapse Risk")
    st.write("Enter patient details to predict relapse risks.")

    # User input form
    with st.form("prediction_form"):
        age = st.number_input("Age", min_value=0, max_value=120, value=30)
        gender = st.selectbox("Gender", ["Male", "Female"])
        substance_type = st.selectbox("Substance Type", ["Alcohol", "Cannabis", "Opioids", "Cocaine", "Methamphetamine", "Polysubstance"])
        treatment_type = st.selectbox("Treatment Type", ["Residential Rehab", "Detox", "Counseling", "Medication-Assisted Treatment (MAT)"])
        support_system = st.selectbox("Support System", ["Strong", "Moderate", "Weak"])
        treatment_outcome = st.selectbox("Treatment Outcome", ["Ongoing", "Recovered", "Relapsed"])
        submit = st.form_submit_button("Predict Relapse Risk")

        if submit:
            try:
                # Create input data DataFrame
                input_data = pd.DataFrame({
                    "Age": [age],
                    "Gender": [gender],
                    "Substance_Type": [substance_type],
                    "Treatment_Type": [treatment_type],
                    "Support_System": [support_system],
                    "Treatment_Outcome": [treatment_outcome]
                })

                # Load the model, encoder, and feature order
                with open("logistic_regression_retrained.pkl", "rb") as model_file:
                    model = pickle.load(model_file)
                with open("encoder_retrained.pkl", "rb") as encoder_file:
                    encoder = pickle.load(encoder_file)
                with open("feature_order.pkl", "rb") as feature_file:
                    feature_order = pickle.load(feature_file)

                # Identify categorical and numerical columns
                categorical_cols = ["Gender", "Substance_Type", "Treatment_Type", "Support_System", "Treatment_Outcome"]
                numerical_cols = ["Age"]

                # Encode categorical features
                encoded_categorical = encoder.transform(input_data[categorical_cols]).toarray()
                numerical_features = input_data[numerical_cols].values

                # Combine numerical and encoded categorical features
                final_input = pd.concat(
                    [
                        pd.DataFrame(numerical_features, columns=numerical_cols),
                        pd.DataFrame(encoded_categorical, columns=encoder.get_feature_names_out(categorical_cols))
                    ],
                    axis=1
                )

                # Align columns with the feature order from training
                final_input = final_input.reindex(columns=feature_order, fill_value=0)

                # Make prediction
                prediction = model.predict(final_input)[0]
                prediction_proba = model.predict_proba(final_input)[0]

                # Display results
                st.subheader("Prediction Result")
                st.write(f"**Predicted Relapse Risk:** {prediction}")
                st.write(f"**Confidence:** {prediction_proba.max() * 100:.2f}%")  # Assuming class 1 is "Relapse"

            except Exception as e:
                st.error("An error occurred during prediction. Please check your inputs or contact support.")
                st.error(f"Details: {e}")


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
    ml_prediction()
elif page == "Case Management":
    case_management(data)
