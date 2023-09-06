# A youtube playlist downloader that imports the mp4 files into a google drive folder to be acessed by my iPhone to download and watch on my commute offline.
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pytube import Playlist
import os

# playlist link
link = "INSERT_YOUTUBE_PLAYLIST_LINK_HERE"
# output path for downloaded videos
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

# uploads a normal sized video (pydrive limits uploads at 100 MB)
def upload_to_drive(drive, local_path):
    file_name = os.path.basename(local_path)
    # copy the folder ID at the end of the desired Google Drive Folder URL. Exclude https://drive.google.com/drive/u/0/folders/
    drive_file = drive.CreateFile({'title': file_name, 'parents': [{'id': "INSERT_DRIVE_FOLDER_ID_HERE"}]}) 
    print(f"Starting the upload of {file_name} to your Google Drive")
    try:
        drive_file.SetContentFile(local_path)  # Set the content of the file
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
            upload_to_drive(drive, video_path)
            os.remove(video_path)  # Remove local file after upload
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    download_and_upload_playlist()
