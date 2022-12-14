import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi

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
