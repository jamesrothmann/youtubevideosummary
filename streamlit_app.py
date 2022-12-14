import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse
import openai

# Create a text input field for the GPT-3 API key
api_key_input = st.text_input("Enter GPT-3 API key:")

# Set the OpenAI API key
openai.api_key = api_key_input

def extract_video_id(url):
    # Parse the URL using urlparse()
    parsed_url = urlparse(url)
    
    # Extract the query string from the parsed URL
    query_string = parsed_url.query
    
    # Split the query string into key-value pairs
    query_pairs = query_string.split('&')
    
    # Loop through the query pairs and find the `v` parameter
    for query_pair in query_pairs:
        key, value = query_pair.split('=')
        if key == 'v':
            return value
        
        
def split_transcript(transcript):
    # Concatenate the transcript text into a single string
    transcript_text = ""
    for line in transcript:
        transcript_text += line['text']
        
    # Split the transcript text into sentences
    sentences = transcript_text.split('.')

    # Create a list to store the paragraphs
    paragraphs = []
    
    # Initialize a temporary list to store the current paragraph
    current_paragraph = []
    
    # Loop through the sentences and add them to the current paragraph
    # until the paragraph has between 800 and 1200 words
    for sentence in sentences:
        if len(current_paragraph) + len(sentence) >= 800 and len(current_paragraph) + len(sentence) <= 1200:
            # Add the sentence to the current paragraph
            current_paragraph.append(sentence)
            
            # Add the current paragraph to the list of paragraphs
            paragraphs.append(" ".join(current_paragraph))
            
            # Reset the current paragraph
            current_paragraph = []
        else:
            # Add the sentence to the current paragraph
            current_paragraph.append(sentence)
            
    # If the transcript is less than 800 words, return the whole text as a single paragraph
    if len(paragraphs) == 0:
        return [transcript_text]
    else:
        return paragraphs


    

def gpt3_summarize(paragraph):
    # Use GPT-3 to summarize the paragraph
    summary = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"TL;DR: {paragraph}",
        max_tokens=1024,
        temperature=0.5,
    )
    
    # Return the summary text
    return summary.text    

url_input = st.text_input("Enter YouTube URL:")

if st.button("Summarize Video"):
    # Extract the video ID from the URL
    video_id = extract_video_id(url_input)
    
    # Fetch the transcript using youtube-transcript-api
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    
    # Split the transcript into paragraphs of 800-1200 words
    paragraphs = split_transcript(transcript)
    
    # Use GPT-3 to summarize each paragraph
    summaries = []
    for paragraph in paragraphs:
        summaries.append(gpt3_summarize(paragraph))
        
    # Display the summaries
    for summary in summaries:
        st.write(summary)
