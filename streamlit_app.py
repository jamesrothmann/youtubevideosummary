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
        
    # Create a list to store the paragraphs
    paragraphs = []
    
    # Initialize a temporary list to store the current paragraph
    current_paragraph = ""
    
    # Loop through the transcript text and add it to the current paragraph
    # until the paragraph has 4000 characters or less
    for character in transcript_text:
        if len(current_paragraph) + len(character) >= 2000:
            # Add the current paragraph to the list of paragraphs
            paragraphs.append(current_paragraph)
            
            # Reset the current paragraph
            current_paragraph = ""
        else:
            # Add the character to the current paragraph
            current_paragraph += character
            
    # If the transcript is less than 4000 characters, return the whole text as a single paragraph
    if len(paragraphs) == 0:
        return [transcript_text]
    else:
        return paragraphs



    

def gpt3_summarize(paragraph):
    # Concatenate the sentences in the paragraph into a single string
    paragraph_text = " ".join(paragraph)

    # Use GPT-3 to summarize the paragraph
    summary = openai.Completion.create(
        engine="text-curie-001",
        prompt=f"{paragraph_text} TL;DR:",
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        best_of=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Return the summary text
    return summary["choices"][0]["text"]

url_input = st.text_input("Enter YouTube URL:")

if st.button("Summarize Video"):
    # Extract the video ID from the URL
    video_id = extract_video_id(url_input)
    
    # Fetch the transcript using youtube-transcript-api
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    
    # Check if the transcript is None
    if transcript is None:
        # If the transcript is None, display a message saying that the transcript is not available
        st.write("Transcript not available")
    else:
        # If the transcript is not None, split the transcript into paragraphs of 800-1200 words
        paragraphs = split_transcript(transcript)

        # Use GPT-3 to summarize each paragraph
        summaries = []
        for paragraph in paragraphs:
            summaries.append(gpt3_summarize(paragraph))

        # Display the summaries
        for summary in summaries:
            st.write(summary)
            st.write(paragraph)
            
            st.write(summaries)
