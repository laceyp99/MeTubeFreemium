# A youtube playlist downloader that imports the mp4 files into a google drive folder to be acessed by my iPhone to download and watch on my commute offline.
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pytube import Playlist
import os
from io import BytesIO

# hard coded playlist link to my "Downloads" playlist I'll add all the vids I want to download to
link = "https://youtube.com/playlist?list=PLneyJW8_UXGHAUb6koeWhiViqgXXJTwcW&si=VliqH_la6KE90-Fd"
# hard coded output path for downloaded videos
script_directory = os.path.dirname(os.path.abspath(__file__))
downloads_directory = os.path.join(script_directory, 'Downloads')
        
if not os.path.exists(downloads_directory):
    os.makedirs(downloads_directory)

output_path = downloads_directory

# Go to https://console.cloud.google.com/apis/library/drive.googleapis.com and set up a Desktop App Credential and download the client_secrets.json file
# make sure to make your email a test user within the google cloud OAuth Consent screen
def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Creates local webserver and auto handles authentication.
    drive = GoogleDrive(gauth)
    return drive

# splits the large video into smaller chunks to then upload
def split_video(file_path, chunk_size):
    video_parts = []
    with open(file_path, 'rb') as video_file:
        while True:
            chunk = video_file.read(chunk_size)
            if not chunk:
                break
            video_parts.append(chunk)
    return video_parts

# uploads each split video part
def upload_split_video_parts(drive, video_parts, file_name):
    title = file_name[:-4]
    for idx, part in enumerate(video_parts, start=1):
        part_name = f"{title} part {idx}.mp4"
        
        # Create an in-memory BytesIO buffer for the content
        content_buffer = BytesIO(part)
        
        file = drive.CreateFile({'title': part_name, 'parents': [{'id': "16GQt75QiRHUyQpEkIT4uxE2cssk7X-8g"}]})
        
        # Set the content of the file to the BytesIO buffer
        file.content = content_buffer
        
        # Upload the file
        file.Upload()
        
        print(f"Uploaded {part_name} to Google Drive successfully")

# main upload function that calls the right function to upload based on the file size
def upload_large_video(drive, local_path):
    file_name = os.path.basename(local_path)
    file_size = os.path.getsize(local_path) / (1024 * 1024)
    
    if file_size <= 100:
        upload_to_drive(drive, local_path)
    else:
        chunk_size = 50 * 1024 * 1024  # 50 MB chunk size
        video_parts = split_video(local_path, chunk_size)
        upload_split_video_parts(drive, video_parts, file_name)

# uploads a normal sized video (pydrive limits uploads at 100 MB)
def upload_to_drive(drive, local_path):
    file_name = os.path.basename(local_path)
    file_size = os.path.getsize(local_path) / (1024 * 1024)  # Convert bytes to MB

    if file_size > 100:
        print(f"File {file_name} exceeds the maximum allowed file size of 100 MB. Skipping upload.")
        return

    drive_file = drive.CreateFile({'title': file_name, 'parents': [{'id': "16GQt75QiRHUyQpEkIT4uxE2cssk7X-8g"}]})
    drive_file.SetContentFile(local_path)
    print(f"Starting the upload of {file_name} to your Google Drive")
    try:
        drive_file.Upload()
        print(f"Upload of {file_name} successful")
    except Exception as e:
        print(f"Upload of {file_name} failed with error: {e}")

# the full download and uploading function
def download_and_upload_playlist():
    try:
        drive = authenticate_drive()

        playlist = Playlist(link)
        
        print(f"Total videos in playlist: {len(playlist)}")
        
        for idx, video in enumerate(playlist.videos, start=1):
            print(f"{idx}. {video.title}")
            video_path = video.streams.get_highest_resolution().download(output_path)
            print(f"Download of {video.title} complete")
            upload_large_video(drive, video_path)
            os.remove(video_path)  # Remove local file after upload
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_and_upload_playlist()