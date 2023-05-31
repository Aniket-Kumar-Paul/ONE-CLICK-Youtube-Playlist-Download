from pytube import Playlist
from pytube.exceptions import AgeRestrictedError, VideoPrivate
from tqdm import tqdm
import re
from http.client import IncompleteRead

def replace_special_characters(input_string):
    pattern = r'[^a-zA-Z0-9_]'
    replaced_string = re.sub(pattern, ' ', input_string)
    return replaced_string

link = input("Enter Youtube Video Playlist Link: ")
yt_playlist = Playlist(link)
total_videos = len(yt_playlist.videos)
print("Total number of videos:", total_videos)

with tqdm(total=len(yt_playlist.videos), desc="Downloading", unit="video") as pbar:
    for i, video in enumerate(yt_playlist.videos):
        title = replace_special_characters(video.title)
        print("\nDownloading:", (i + 1), title)
        
        try:
            # Get the stream
            stream = video.streams.get_by_resolution("720p")

            # Get the total file size
            file_size = stream.filesize

            # Download the video
            stream.download(filename=str(i + 1) + "_" + title + ".mp4")
            
            print(f'{i + 1}/{total_videos} videos downloaded')
        except AgeRestrictedError:
            print("Skipping age-restricted video:", title)
        except IncompleteRead:
            # Try again
            continue
        except VideoPrivate:
            print("Skipping private video", title)
        pbar.update(1)
        
print("\nAll videos are downloaded.")
