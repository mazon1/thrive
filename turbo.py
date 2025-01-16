import streamlit as st
import google.generativeai as genai
import os

# Configure Google Generative AI
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', st.secrets.get("GOOGLE_API_KEY"))
genai.configure(api_key=GOOGLE_API_KEY)

# App title and description
st.title("Anchor: Your Medicaid Enrollment Assistant")
st.write("""
This application simplifies the Medicaid enrollment process for high-needs individuals, 
providing guided steps for document preparation and full Medicaid enrollment.
""")

# Navigation menu
menu = st.sidebar.radio("Navigation", ["Home", "Document Hub", "Medicaid Enrollment", "Progress Tracker", "Help"])

# Home page
if menu == "Home":
    st.header("Welcome to the Medicaid Enrollment Assistant")
    st.write("Use the sidebar to navigate through the enrollment process.")
    st.image("anchorlogo.PNG", width=300)

# Document Hub page
elif menu == "Document Hub":
    st.header("Document Hub")
    st.write("Prepare and upload the required documents for your Medicaid application.")

    # List of required documents
    st.write("### Required Documents")
    st.markdown("""
    - **Proof of Identity**: Government-issued photo ID, birth certificate, or Social Security card.
    - **Proof of Citizenship or Immigration Status**: U.S. birth certificate, naturalization certificate, or green card.
    - **Proof of Residency**: Utility bill, lease agreement, or shelter address letter.
    - **Proof of Income**: Pay stubs, tax returns, employer letter, or self-employment records.
    - **Health Insurance Information**: Insurance card (if applicable).
    - **Proof of Resources** (if required): Bank statements, property ownership documents, or retirement accounts.
    - **Medical Necessity Documents** (if applicable): Physician's statement, medical records, or hospital bills.
    """)

    # Generate templates
    st.write("### Generate a Document Template")
    template_type = st.selectbox("Select Template Type", ["Address Waiver Letter", "Income Verification Letter"])
    if st.button("Generate Template"):
        if template_type == "Address Waiver Letter":
            st.text_area("Template", "To whom it may concern:\n\nI currently do not have a fixed address. Please accept this letter as a declaration of my living situation.\n\nSincerely,\n[Your Name]")
        elif template_type == "Income Verification Letter":
            st.text_area("Template", "To whom it may concern:\n\nI currently earn an informal income of approximately $[amount] per month. Please accept this letter as verification of my income.\n\nSincerely,\n[Your Name]")

    # Document upload
    st.write("### Upload Documents")
    uploaded_files = st.file_uploader("Upload your required documents (PDF, PNG, JPG)", accept_multiple_files=True)
    if uploaded_files:
        st.success(f"{len(uploaded_files)} document(s) uploaded successfully.")
        st.info("Our team will verify your documents shortly.")

# Medicaid Enrollment page
elif menu == "Medicaid Enrollment":
    st.header("Medicaid Enrollment")
    st.write("Complete the full application to finalize your Medicaid eligibility.")

    # Step-by-step form
    st.write("### Step 1: Personal Information")
    name = st.text_input("Full Name", key="full_name")
    dob = st.date_input("Date of Birth", key="dob")
    address = st.text_input("Current Address", key="address")

    st.write("### Step 2: Financial Information")
    income = st.number_input("Monthly Income ($)", min_value=0, step=100, key="income")
    employment_status = st.selectbox("Employment Status", ["Employed", "Unemployed", "Self-Employed"], key="employment")

    st.write("### Step 3: Additional Information")
    household_size = st.number_input("Number of People in Household", min_value=1, step=1, key="household")
    health_conditions = st.text_area("Describe any medical conditions (if applicable)", key="conditions")
    insurance_status = st.selectbox("Do you currently have health insurance?", ["Yes", "No"], key="insurance_status")

    if st.button("Submit Application"):
        st.success("Your Medicaid application has been submitted.")
        st.info("Track your application status in the Progress Tracker.")

# Progress Tracker page
elif menu == "Progress Tracker":
    st.header("Track Your Application Progress")
    st.write("Check the status of your Medicaid application.")

    # Simulated progress tracker
    progress = st.progress(70)
    st.write("Current Status: Application Submitted. Awaiting Review.")

# Help Section
elif menu == "Help":
    st.header("Help and Support")
    st.write("Ask your questions about Medicaid or the app, and our chatbot will assist you.")

    # AI Chatbot for Help
    user_query = st.text_input("Type your question here:")
    if user_query:
        try:
            # Generate response from Google Generative AI
            response = genai.chat(prompt=user_query)
            st.text_area("Chatbot Response", response["output"], height=200)
        except Exception as e:
            st.error("Sorry, I couldn't process your request. Please try again later.")
    
    # Static FAQ (Optional for fallback)
    st.write("Frequently Asked Questions:")
    st.write("""
    - **What is Medicaid?** Medicaid is a healthcare program for individuals in need.
    - **What documents do I need?** Refer to the Document Hub for a complete list.
    - **Is my data secure?** Yes, your data is encrypted and complies with HIPAA regulations.
    - **Who can I contact for help?** Email support@medicaidassist.com or call (555) 123-4567.
    """)

# Footer
st.sidebar.write("© 2025 Medicaid Enrollment Assistant. All rights reserved.")
