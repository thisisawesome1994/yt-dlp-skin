import requests
import feedparser
import subprocess
import os
from datetime import datetime

def get_channel_info(channel_id):
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(requests.get(rss_url).content)
    channel_name = feed.feed.title
    video_entries = feed.entries
    return channel_name, video_entries

def read_downloaded_urls(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            return set(line.strip() for line in file)
    return set()

def main():
    channel_ids_file = 'channel_ids.txt'
    output_file = 'urls.txt'
    downloaded_file = 'downloaded.dat'
    
    downloaded_urls = read_downloaded_urls(downloaded_file)
    
    try:
        with open(channel_ids_file, 'r') as file:
            channel_ids = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"File '{channel_ids_file}' not found.")
        return

    all_channel_info = {}
    for channel_id in channel_ids:
        try:
            channel_name, video_entries = get_channel_info(channel_id)
            all_channel_info[channel_id] = {'name': channel_name, 'entries': video_entries}
        except Exception as e:
            print(f"Error fetching information for channel {channel_id}: {e}")

    for channel_id, info in all_channel_info.items():
        channel_name = info['name']
        video_entries = info['entries']
        channel_directory_name = f"{channel_id} - {channel_name}"

        for entry in video_entries:
            video_url = entry.link
            if video_url in downloaded_urls:
                print(f"Skipping already downloaded video: {video_url}")
                continue
            
            publication_date = datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%S%z")
            year = publication_date.year
            year_directory = os.path.join(str(year), channel_directory_name)

            if not os.path.exists(year_directory):
                os.makedirs(year_directory)

            with open(output_file, 'w') as file:
                file.write(f"{video_url}\n")

            # Run yt-dlp command with output directory
            try:
                subprocess.run(["./yt-dlp.exe", "-f", "mp4", "--batch-file", output_file, "-o", f"{year_directory}/%(title)s.%(ext)s"], check=True)
                print(f"yt-dlp command executed successfully for channel {channel_id}.")
                
                # Save downloaded URL to downloaded.dat
                with open(downloaded_file, 'a') as downloaded:
                    downloaded.write(f"{video_url}\n")
                downloaded_urls.add(video_url)
            except subprocess.CalledProcessError as e:
                print(f"Error executing yt-dlp command for channel {channel_id}: {e}")
            except FileNotFoundError:
                print("yt-dlp.exe not found. Please ensure yt-dlp.exe is in the current directory.")

            # Delete urls.txt after the download
            try:
                if os.path.exists(output_file):
                    os.remove(output_file)
                    print(f"'{output_file}' has been deleted.")
            except Exception as e:
                print(f"Error deleting file '{output_file}': {e}")

if __name__ == "__main__":
    main()
