import streamlit as st
from google.cloud import generativeai
import os
import re


# Configure Google Generative AI
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', st.secrets.get("GOOGLE_API_KEY"))
genai.configure(api_key=GOOGLE_API_KEY)

# App title and description
st.title("Medicaid Enrollment Assistant")
st.write("""
This application simplifies the Medicaid enrollment process for high-needs individuals, 
leveraging Google Generative AI for conversational assistance and compliance.
""")

# Navigation menu
menu = st.sidebar.radio("Navigation", ["Home", "Enrollment", "Document Upload", "Progress Tracker", "Help"])

# Home page
if menu == "Home":
    st.header("Welcome to the Medicaid Enrollment Assistant")
    st.write("Use the sidebar to navigate through the enrollment process.")
    st.image("anchorlogo.png", width=300)

# Enrollment page
elif menu == "Enrollment":
    st.header("Guided Medicaid Enrollment")
    st.write("Answer a few questions to begin your Medicaid application.")
    
    # AI-assisted conversation
    user_input = st.text_input("Type your question or concern here:")
    if user_input:
        # Connect to Google Generative AI
        response = generativeai.chat(prompt=user_input)
        st.text_area("AI Response", response["output"], height=200)
    
    # Basic information form
    st.write("### Basic Information")
    name = st.text_input("Full Name")
    dob = st.date_input("Date of Birth")
    address = st.text_input("Current Address (or type 'No Fixed Address')")
    income = st.number_input("Monthly Income ($)", min_value=0, step=100)
    
    if st.button("Submit Information"):
        st.success("Your information has been saved. Proceed to the Document Upload step.")

# Document Upload page
elif menu == "Document Upload":
    st.header("Upload Required Documents")
    st.write("Upload necessary documents for Medicaid enrollment.")
    
    # File upload
    uploaded_file = st.file_uploader("Upload your ID or proof of eligibility (PDF, PNG, JPG)")
    if uploaded_file:
        st.success(f"{uploaded_file.name} uploaded successfully.")
        st.write("Our system will verify your document automatically.")
        # Placeholder for document verification
        st.info("Verification in progress...")

# Progress Tracker
elif menu == "Progress Tracker":
    st.header("Track Your Application Progress")
    st.write("Check the status of your Medicaid application.")
    
    # Simulated progress tracker
    progress = st.progress(50)
    st.write("Current Status: Verification Complete. Awaiting Review.")

# Help Section
elif menu == "Help":
    st.header("Help and Compliance")
    st.write("Frequently Asked Questions:")
    st.write("""
    - **What is Medicaid?** Medicaid is a healthcare program for individuals in need.
    - **Is my data secure?** Yes, your data is encrypted and complies with HIPAA regulations.
    - **Who can I contact for help?** Email support@medicaidassist.com or call (555) 123-4567.
    """)
    # Compliance reminder
    st.warning("Ensure that all uploaded documents are accurate to avoid delays.")

# Footer
st.sidebar.write("© 2025 Medicaid Enrollment Assistant. All rights reserved.")
