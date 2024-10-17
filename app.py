import streamlit as st
import yt_dlp
import os
from moviepy.editor import VideoFileClip

# Set up the app title and description
st.title("TikTok Video Downloader & Cropper")
st.markdown("This tool allows you to download TikTok videos and crop them according to the start and end time you specify.")

# Function to download TikTok video
def download_video(url):
    download_path = './downloads'
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    ydl_opts = {
        'outtmpl': download_path + '/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict.get('title', None)
            file_path = ydl.prepare_filename(info_dict)
            ydl.download([url])
            return f"Downloaded successfully: {title}", file_path
    except Exception as e:
        return f"Error: {e}", None

# Function to crop video
def crop_video(file_path, start_time, end_time):
    try:
        clip = VideoFileClip(file_path)
        cropped_clip = clip.subclip(start_time, end_time)
        cropped_file = file_path.replace(".mp4", "_cropped.mp4")
        cropped_clip.write_videofile(cropped_file, codec="libx264")
        return cropped_file
    except Exception as e:
        return f"Error: {e}"

# Main function to handle both download and crop
def download_and_crop(url, start_time, end_time):
    status, video_file = download_video(url)
    if video_file:
        cropped_file = crop_video(video_file, start_time, end_time)
        if os.path.exists(cropped_file):
            return f"Download and cropping successful!", cropped_file
    return status, None

# Input fields in the Streamlit interface
url = st.text_input("Enter TikTok video URL:", "")
start_time = st.number_input("Start Time (seconds)", min_value=0, value=0)
end_time = st.number_input("End Time (seconds)", min_value=1, value=10)

# Button to download and crop the video
if st.button("Download and Crop Video"):
    if url:
        with st.spinner('Downloading and cropping...'):
            status, cropped_video = download_and_crop(url, start_time, end_time)
            if cropped_video:
                st.success(status)
                st.video(cropped_video)
                with open(cropped_video, "rb") as file:
                    st.download_button(
                        label="Download Cropped Video",
                        data=file,
                        file_name=os.path.basename(cropped_video),
                        mime="video/mp4"
                    )
            else:
                st.error(status)
    else:
        st.warning("Please enter a TikTok video URL.")

# Footer
st.markdown("---")
st.markdown("**Developed by [Your Name]**")
st.markdown("For any queries or issues, feel free to contact me.")
