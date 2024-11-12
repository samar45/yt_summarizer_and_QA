import os
import google.generativeai as genai
from dotenv import load_dotenv
from src.main import *
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import re
import streamlit as st

# Load API key
load_dotenv()
API_KEY = os.getenv("API_KEY")
genai.configure(api_key=API_KEY)

# Streamlit UI Styling
st.set_page_config(page_title="YouTube Video Summarizer & FAQ Generator", layout="wide")

# Input for YouTube URL
st.title("YouTube Video Summarizer & FAQ Generator")
url = st.text_input("Enter YouTube video URL:")

if url:
    # Extract video ID from URL
    pattern = r"(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=|embed/|v/|.+/|)([\w-]{11})"
    match = re.search(pattern, url)
    video_id = match.group(1) if match else None

    # Fetch transcript
    transcript_paragraph = fetch_and_translate_transcript(video_id)

    # Create two columns for displaying summary and transcript side by side
    col1, col2 = st.columns(2)

    with col1:
        # Transcript Summary
        st.subheader("Transcript Summary")
        summary = summarize_text(transcript_paragraph)
        st.write(summary)

    with col2:
        # Generate FAQs
        st.subheader("Frequently Asked Questions")
        faq = generate_faq(transcript_paragraph)
        st.write(faq)

    # User question input for Q&A
    question = st.text_input("Ask a question about the video:")
    get_answer = st.button("Get Answer")

    if question and get_answer:
        # Generate answer only when the "Get Answer" button is clicked
        answer = question_text(transcript_paragraph, question)
        st.subheader("Answer")
        st.write(answer)
