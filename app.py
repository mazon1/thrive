import streamlit as st
from datetime import datetime

# Set page title
st.set_page_config(page_title="Supportive Community App", layout="wide")

# Header
st.title("Welcome to Your Safe Space")
st.write("Express yourself, connect with others, and share your journey in a supportive community.")

# Navigation
menu = st.sidebar.selectbox("Menu", ["Home", "Audio Sharing", "Community", "Profile", "Support Groups"])

if menu == "Home":
    st.header("Discover, Reflect, and Connect")
    st.write("Explore shared stories, daily check-ins, and more.")
    
    # Suggested posts
    st.subheader("Community Highlights")
    st.write("1. [Jane's Journey to Recovery](#)")
    st.write("2. [Tips for Overcoming Anxiety](#)")
    st.write("3. [How Peer Support Changed My Life](#)")

elif menu == "Audio Sharing":
    st.header("Audio Sharing")
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
    st.write("Follow others, join discussions, and build your network.")
    
    st.subheader("Your Network")
    st.write("**Following**: 20 | **Followers**: 15")

    st.subheader("Trending Stories")
    st.write("1. [Overcoming Relapse: John's Story](#)")
    st.write("2. [Anxiety Hacks from Sarah](#)")
    
    st.subheader("Find Friends")
    search = st.text_input("Search for community members:")
    if search:
        st.write(f"Results for {search}:")
        st.write("- [Alex Smith](#)")
        st.write("- [Chris Doe](#)")

elif menu == "Profile":
    st.header("Your Profile")
    st.write("Customize your experience and control your privacy.")

    # Profile Details
    name = st.text_input("Name", "Your Name")
    bio = st.text_area("Bio", "Share a bit about yourself.")
    st.checkbox("Make my profile private")
    st.button("Save Changes")

elif menu == "Support Groups":
    st.header("Join Support Groups")
    st.write("Connect in real-time with others.")
    st.write("Upcoming live sessions:")
    st.write("- [Mindfulness Monday: Coping Techniques](#) at 7 PM")
    st.write("- [Wellness Wednesday: Open Forum](#) at 6 PM")

    st.button("Join Live Session")
