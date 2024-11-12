# Import necessary libraries
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
API_KEY = os.environ['API_KEY']  # Retrieve API key from environment
genai.configure(api_key=API_KEY)  # Configure Google Generative AI with the API key

# Import YouTube Transcript API and regex library
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import re

# Define the YouTube video URL and extract the video ID using regex
url = ""
pattern = r"(?:https?://)?(?:www\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=|embed/|v/|.+/|)([\w-]{11})"
match = re.search(pattern, url)
video_id = match.group(1) if match else None
print(video_id)  # Print the extracted video ID for confirmation

# Supported languages and their ISO codes
supported_languages = {
    "English": "en",
    "Japanese": "ja",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-Hans",
    "Chinese (Traditional)": "zh-Hant",
    "Korean": "ko",
    "Russian": "ru",
    "Portuguese": "pt",
    "Italian": "it",
    "Dutch": "nl",
    "Arabic": "ar",
    "Hindi": "hi",
    "Swedish": "sv",
    "Norwegian": "no",
    "Danish": "da",
    "Finnish": "fi",
    "Greek": "el",
    "Polish": "pl",
}

# Function to fetch and translate the transcript from YouTube
def fetch_and_translate_transcript(video_id):
    transcript_paragraph = ""
    try:
        # Get available transcripts (manual and auto-generated) for the video
        transcript_info = YouTubeTranscriptApi.list_transcripts(video_id)

        # Check if an English transcript is available or translate if needed
        for transcript in transcript_info:
            language_code = transcript.language_code

            if language_code == "en":
                # Fetch English transcript directly if available
                entries = transcript.fetch()
                transcript_paragraph += " ".join([entry['text'] for entry in entries])
                break  # Exit after fetching the English transcript

            elif language_code in supported_languages.values():
                # If in a supported language, translate to English
                translated_transcript = transcript.translate('en').fetch()
                transcript_paragraph += " ".join([entry['text'] for entry in translated_transcript])
                break  # Exit after fetching the translated transcript

    except TranscriptsDisabled:
        print("Transcripts are disabled for this video.")
    except Exception as e:
        print("An error occurred:", e)

    return transcript_paragraph



# Function to summarize the transcript using Google Generative AI
def summarize_text(transcript_paragraph):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = (
        f"Identify the main topic of the content and summarize the text in details "
        f"Text: {transcript_paragraph}"
    )
    response = model.generate_content([prompt])
    return response.text  # Return the generated summary

# Generate the summary of the transcript



# Function to generate FAQs based on the transcript content
def generate_faq(transcript_paragraph):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([f"""
    The following text is a transcript of a YouTube Video: {transcript_paragraph}

    Generate 5 frequently asked questions (FAQs) related to these topics answer should precise.
    """])
    return response.text


# Accept a question input from the user

# question = input("Enter your question: ")
# print(question)

# Function to answer user questions based on the transcript content
def question_text(transcript_paragraph,question):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([
        f"Please answer the following question based on the provided text : {transcript_paragraph}. Question: {question}.",
    ])
    response_text = response.text
    cleaned_text = response_text.replace('\n', '')  # Clean up response
    return cleaned_text

# Generate an answer based on user question
