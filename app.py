import streamlit as st
import pandas as pd
import datetime

# Synthetic Data for Demonstration
story_data = []  # List to store stories
document_data = []  # List to store documents
provider_data = pd.DataFrame({
    "Provider": ["Community Health Center", "Mental Health Services", "Housing Support"],
    "Contact": ["chc@health.org", "mhs@mental.org", "hs@housing.org"],
    "Services": ["Primary Care, SUD Treatment", "Counseling, Therapy", "Housing Assistance"]
})

# App Configuration
st.set_page_config(page_title="Centralized Care Platform", layout="wide")
st.title("Centralized Care Platform")
st.sidebar.header("Navigation")

# Navigation Options
page = st.sidebar.selectbox("Choose a section", ["Home", "Storytelling", "Interoperability Dashboard", "Document Storage"])

if page == "Home":
    st.header("Welcome to the Centralized Care Platform")
    st.write("This platform is designed to support individuals in recovery with personalized storytelling, interoperable provider dashboards, and secure document storage.")

elif page == "Storytelling":
    st.header("Share Your Recovery Journey")

    # Input for Storytelling
    with st.form("story_form"):
        name = st.text_input("Your Name")
        story = st.text_area("Share your story")
        date = st.date_input("Date", value=datetime.date.today())
        submitted = st.form_submit_button("Submit")

    if submitted:
        story_data.append({"Name": name, "Story": story, "Date": date})
        st.success("Your story has been submitted!")

    # Display Existing Stories
    if story_data:
        st.subheader("Your Stories")
        for s in story_data:
            st.write(f"**{s['Name']}** on {s['Date']}: {s['Story']}")

elif page == "Interoperability Dashboard":
    st.header("Interoperability Dashboard")
    st.write("View and communicate with service providers.")

    # Display Provider Information
    st.table(provider_data)

    # Simulated API Example
    st.subheader("Send a Message to Providers")
    with st.form("message_form"):
        provider = st.selectbox("Choose a provider", provider_data["Provider"])
        message = st.text_area("Your Message")
        message_submitted = st.form_submit_button("Send")

    if message_submitted:
        st.success(f"Message sent to {provider}!")

elif page == "Document Storage":
    st.header("Document Storage")
    st.write("Upload and securely store important documents.")

    # Document Upload
    uploaded_file = st.file_uploader("Upload Document")
    if uploaded_file is not None:
        document_data.append({"File Name": uploaded_file.name, "Upload Date": datetime.date.today()})
        st.success("Document uploaded successfully!")

    # Display Stored Documents
    if document_data:
        st.subheader("Stored Documents")
        for doc in document_data:
            st.write(f"**{doc['File Name']}** uploaded on {doc['Upload Date']}")
