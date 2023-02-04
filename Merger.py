import streamlit as st
from moviepy.editor import *
import requests
import logging

logging.info('App Started')
st.set_page_config(page_title='SVCET Marks',page_icon=':wave:', layout='centered')
st.title("Video Merger")

def MovMerge(N,Ext):
    logging.info('Merging '+N+' Videos') 
    # List of video clips
    clips = [VideoFileClip("Video{}.{}".format(i,Ext) for i in range(0,N))]

    # Merge the clips into a single video
    final_clip = concatenate_videos(clips)

    # Save the final video
    final_clip.write_videofile("final_video."+Ext)
    logging.info('Merged')

def AnonF(Ext):
    logging.info('Uploading') 
    # Define the API endpoint for uploading a file to anonfiles
    url = "https://api.anonfiles.com/upload"

    # Define the file to be uploaded
    file = {"file": ("final_video."+Ext,open("final_video."+Ext, "rb"))}

    # Make a POST request to the API endpoint
    response = requests.post(url, files=file)

    # Get the URL of the uploaded video from the response
    response_json = response.json()
    uploaded_video_url = response_json["data"]["file"]["url"]["full"]
    logging.info('Uploading '+uploaded_video_url) 
    # Print the URL of the uploaded video
    st.write(uploaded_video_url)

InputLink=st.text_input("Enter Links")
Ext=st.text_input("Ext")
Task=st.button('Merge',key='submit') 
Links=InputLink.split(",")
N=len(Links)

if Task:
    for i in range(0,N):
        # Set the chunk size (in bytes)
        chunk_size = 1024

        # Make a GET request to the direct download link
        response = requests.get(Links[i], stream=True)

        # Check if the request was successful
        if response.status_code == 200:
        # Write the contents of the response to a local file, chunk by chunk
            with open("Video{}.{}".format(i,Ext), "wb") as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
            print("File downloaded successfully")
        else:
            print("Failed to download file")
    MovMerge(N,Ext)
    AnonF(Ext)

