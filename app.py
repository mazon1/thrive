import streamlit as st
from datetime import datetime
import google.generativeai as genai
import random

# Set page title
st.set_page_config(page_title="Supportive Community App", layout="wide")

# Initialize Google Generative AI API (Replace 'your_api_key_here' with an actual API key)
genai.configure(api_key="your_api_key_here")

# Synthetic data generator for patient stories
def generate_synthetic_story():
    emotions = ["hopeful", "anxious", "grateful", "struggling"]
    events = [
        "attended a support group", 
        "shared their story for the first time", 
        "received positive feedback from followers",
        "reached a milestone in their recovery"
    ]
    return f"Today, I am feeling {random.choice(emotions)}. I {random.choice(events)} and it has made a difference in my journey."

# Header
st.title("Welcome to Your Safe Space")
st.image("SafeSpace.PNG", use_container_width=True)
st.write("Express yourself, connect with others, and share your journey in a supportive community.")

# Navigation
menu = st.sidebar.selectbox("Menu", ["Home", "Audio Sharing", "Community", "Profile", "Support Groups", "Case Management"])

if menu == "Home":
    st.header("Discover, Reflect, and Connect")
    st.write("Explore shared stories, daily check-ins, and more.")
    
    # Suggested posts
    st.subheader("Community Highlights")
    for _ in range(3):
        st.write(f"- {generate_synthetic_story()}")

elif menu == "Audio Sharing":
    st.header("Audio Sharing")
    st.image("mic.jpg", use_container_width=True)
    st.write("Record and share your journey or keep it private.")

    # Audio recording section
    audio_option = st.radio("Choose your audio recording option:", ["Record Now", "Upload Audio"])
    
    if audio_option == "Record Now":
        st.info("This feature will require microphone access.")
        st.button("Start Recording")
        st.button("Stop Recording")
        st.write("[Recording Saved]")
    elif audio_option == "Upload Audio":
        uploaded_file = st.file_uploader("Upload your audio file", type=["mp3", "wav"])
        if uploaded_file:
            st.success("Audio uploaded successfully!")

    # Share or Save Option
    share_option = st.radio("What would you like to do with this recording?", ["Keep Private", "Share with Community"])
    if share_option == "Share with Community":
        st.text_area("Add a description or context to your audio log:")
        st.button("Post Audio")
        st.success("Your audio has been shared!")

elif menu == "Community":
    st.header("Community")
    st.image("SafeSpace.PNG", use_container_width=True)
    st.write("Follow others, join discussions, and build your network.")
    
    st.subheader("Your Network")
    st.write("**Following**: 20 | **Followers**: 15")

    st.subheader("Trending Stories")
    for _ in range(3):
        st.write(f"- {generate_synthetic_story()}")
    
    st.subheader("Find Friends")
    search = st.text_input("Search for community members:")
    if search:
        st.write(f"Results for {search}:")
        st.write("- [Alex Smith](#)")
        st.write("- [Chris Doe](#)")

elif menu == "Profile":
    st.header("Your Profile")
    st.image("SafeSpace.PNG", use_container_width=True)
    st.write("Customize your experience and control your privacy.")

    # Profile Details
    name = st.text_input("Name", "Your Name")
    bio = st.text_area("Bio", "Share a bit about yourself.")
    st.checkbox("Make my profile private")
    st.button("Save Changes")

elif menu == "Support Groups":
    st.header("Join Support Groups")
    st.image("SafeSpace.PNG", use_column_width=True)
    st.write("Connect in real-time with others.")
    st.write("Upcoming live sessions:")
    st.write("- [Mindfulness Monday: Coping Techniques](#) at 7 PM")
    st.write("- [Wellness Wednesday: Open Forum](#) at 6 PM")

    st.button("Join Live Session")

elif menu == "Case Management":
    st.header("Case Management Dashboard")
    st.image("SafeSpace.PNG", use_column_width=True)
    st.write("Manage and monitor patient cases efficiently.")

    # Example Case List
    st.subheader("Current Cases")
    st.table({
        "Patient ID": ["P001", "P002", "P003"],
        "Status": ["In Progress", "Completed", "Pending"],
        "Last Update": ["2024-12-01", "2024-11-15", "2024-12-03"]
    })

    # Add Notes Section
    st.subheader("Add Case Notes")
    patient_id = st.selectbox("Select Patient ID", ["P001", "P002", "P003"])
    notes = st.text_area("Enter case notes here:")
    if st.button("Save Notes"):
        st.success("Notes saved successfully for patient {}!".format(patient_id))

# Footer
st.write("---")
st.write("Powered by Streamlit and Google Generative AI")
