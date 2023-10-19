# MeTube Freemium

MeTube Freemium is a Python script that allows you to download YouTube videos from a playlist and upload them to your Google Drive, making them accessible for offline viewing. This is especially useful for creating your offline video library for commutes or other situations.

## Prerequisites

- Python 3.x
- PyDrive2 library (`pip install pydrive2`)
- PyTube library (`pip install pytube`)
- A Google account

## Installation

1. **Clone this repository:**

    ```bash
    git clone https://github.com/yourusername/metube-freemium.git
    cd metube-freemium
    ```

2. **Install the required libraries:**

    ```bash
    pip install pydrive2 pytube
    ```

3. **Set up Google Drive API:**

    - Go to [Google Cloud Console](https://console.cloud.google.com/).
    - Create a Desktop App OAuth 2.0 client ID.
    - Download the `client_secrets.json` file and place it in the project directory.

## Usage

1. **Run the script:**

    ```bash
    python main.py
    ```

2. **Enter the YouTube playlist link and Google Drive folder ID.**

3. **The script will start downloading the videos from the playlist and then will upload them to Google Drive.**

## Project Structure

- `main.py`: The main script to download and upload videos.
- `client_secrets.json`: Google Drive API credentials file (you need to create this).
- `Downloads/`: The folder where downloaded videos are temporarily stored.
