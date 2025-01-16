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
providing guided steps for provisional Medicaid, document preparation, and full enrollment.
""")

# Navigation menu
menu = st.sidebar.radio("Navigation", ["Home", "Provisional Medicaid", "Document Hub", "Full Enrollment", "Progress Tracker", "Help"])

# Home page
if menu == "Home":
    st.header("Welcome to the Medicaid Enrollment Assistant")
    st.write("Use the sidebar to navigate through the enrollment process.")
    st.image("anchorlogo.PNG", width=300)

# Provisional Medicaid page
elif menu == "Provisional Medicaid":
    st.header("Provisional Medicaid Application")
    st.write("Get temporary Medicaid coverage with a simplified application process.")
    
    # Basic provisional form
    name = st.text_input("Full Name")
    dob = st.date_input("Date of Birth")
    address = st.text_input("Current Address (or type 'No Fixed Address')")
    income = st.number_input("Monthly Income ($)", min_value=0, step=100)

    if st.button("Submit Provisional Application"):
        st.success("Your provisional Medicaid application has been submitted. Coverage will be available shortly.")
        st.info("Next Steps: Gather the required documents for full enrollment.")

# Document Hub page
elif menu == "Document Hub":
    st.header("Document Hub")
    st.write("Prepare and upload the required documents for your Medicaid application.")
    
    # Dynamic document templates
    st.write("### Generate a Document Template")
    template_type = st.selectbox("Select Template Type", ["Address Waiver Letter", "Income Verification Letter"])
    if st.button("Generate Template"):
        if template_type == "Address Waiver Letter":
            st.text_area("Template", "To whom it may concern:\n\nI currently do not have a fixed address. Please accept this letter as a declaration of my living situation.\n\nSincerely,\n[Your Name]")
        elif template_type == "Income Verification Letter":
            st.text_area("Template", "To whom it may concern:\n\nI currently earn an informal income of approximately $[amount] per month. Please accept this letter as verification of my income.\n\nSincerely,\n[Your Name]")
    
    # Document upload
    st.write("### Upload Documents")
    uploaded_files = st.file_uploader("Upload necessary documents (PDF, PNG, JPG)", accept_multiple_files=True)
    if uploaded_files:
        st.success(f"{len(uploaded_files)} document(s) uploaded successfully.")
        st.info("Our team will verify your documents shortly.")

# Full Enrollment page
elif menu == "Full Enrollment":
    st.header("Full Medicaid Enrollment")
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
    medical_conditions = st.text_area("Describe any medical conditions (if applicable)", key="conditions")

    if st.button("Submit Full Application"):
        st.success("Your full Medicaid application has been submitted.")
        st.info("Track your application status in the Progress Tracker.")

# Progress Tracker page
elif menu == "Progress Tracker":
    st.header("Track Your Application Progress")
    st.write("Check the status of your Medicaid application.")

    # Simulated progress tracker
    progress = st.progress(70)
    st.write("Current Status: Full Application Submitted. Awaiting Review.")

# Help Section
elif menu == "Help":
    st.header("Help and Support")
    st.write("Frequently Asked Questions:")
    st.write("""
    - **What is Medicaid?** Medicaid is a healthcare program for individuals in need.
    - **What is Provisional Medicaid?** Temporary coverage based on initial eligibility.
    - **Is my data secure?** Yes, your data is encrypted and complies with HIPAA regulations.
    - **Who can I contact for help?** Email support@medicaidassist.com or call (555) 123-4567.
    """)
    st.warning("Ensure all submitted documents are accurate to avoid delays.")

# Footer
st.sidebar.write("© 2025 Medicaid Enrollment Assistant. All rights reserved.")
