import streamlit as st
from moviepy.video.io.VideoFileClip import VideoFileClip
import os
import subprocess

# Function to download TikTok video
def download_tiktok_video(url):
    download_path = './downloads'
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    
    try:
        command = f'tiktok-scraper video {url} -d -p {download_path}'
        subprocess.run(command, shell=True, check=True)
        video_files = [f for f in os.listdir(download_path) if f.endswith(".mp4")]
        if video_files:
            video_file_path = os.path.join(download_path, video_files[0])
            return video_file_path
        else:
            return None
    except Exception as e:
        return f"Error: {e}"

# Function to crop the video
def crop_video(video_path, start_time, end_time, output_path):
    try:
        video = VideoFileClip(video_path)
        cropped_video = video.subclip(start_time, end_time)
        cropped_video.write_videofile(output_path, codec="libx264")
        return output_path
    except Exception as e:
        return f"Error: {e}"

# Streamlit Interface
st.title("TikTok Video Downloader with Cropping Feature")

# User input for TikTok URL
tiktok_url = st.text_input("Enter the TikTok video URL")

# Inputs for cropping times
start_time = st.number_input("Start time for cropping (in seconds)", min_value=0, value=0)
end_time = st.number_input("End time for cropping (in seconds)", min_value=1, value=10)

# Download and crop the video
if st.button("Download and Crop"):
    if tiktok_url:
        video_file = download_tiktok_video(tiktok_url)
        
        if video_file:
            st.success(f"Video downloaded successfully: {video_file}")
            
            # Create cropped video path
            cropped_video_path = './downloads/cropped_video.mp4'
            
            # Crop the video
            result = crop_video(video_file, start_time, end_time, cropped_video_path)
            
            if os.path.exists(cropped_video_path):
                st.success(f"Cropped video saved: {cropped_video_path}")
                st.video(cropped_video_path)
            else:
                st.error(f"Failed to crop the video: {result}")
        else:
            st.error(f"Failed to download video: {video_file}")
    else:
        st.error("Please enter a valid TikTok URL")

# Clear button
if st.button("Clear"):
    if os.path.exists('./downloads'):
        for file in os.listdir('./downloads'):
            os.remove(os.path.join('./downloads', file))
    st.success("Downloads folder cleared.")
