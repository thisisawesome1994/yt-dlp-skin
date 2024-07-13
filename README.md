# yt-dlp-skin
YT-DLP Skin

# YouTube Channel Video Downloader

This script downloads videos from specified YouTube channels using their RSS feeds. It organizes the downloaded videos by year and channel, avoids re-downloading videos, and reruns every day to check for new videos.

## Features

- Fetches video URLs from YouTube channel RSS feeds.
- Organizes downloaded videos into directories by year and channel.
- Avoids re-downloading videos using a `downloaded.dat` file.
- Runs every 24 hours to check for new videos.

## Requirements

- `requests` library
- `feedparser` library
- `yt-dlp` executable

You can install the required Python libraries using:
```sh
pip install requests feedparser
```

Ensure yt-dlp.exe is in the same directory as the script. You can download it from yt-dlp's GitHub page.

Usage
1. Setup Channel IDs

Create a file named channel_ids.txt in the same directory as the script. Add the YouTube channel IDs, each on a new line.

```
UCCWLtpQNoq7gbiHqssF4rPg
```

2. Run the Script

Execute the script with:
```
./app.exe
```

The script will:

* Create directories for each year and channel.
* Download videos into these directories.
* Skip already downloaded videos.
* Append the URLs of downloaded videos to downloaded.dat.
* Sleep for 24 hours and then rerun to check for new videos.

Directory Structure
The script organizes videos as follows:

```
root_directory/
├── 2024/
│   ├── UCLXo7UDZvByw2ixzpQCufnA - Channel Name/
│   │   ├── Video Title 1.mp4
│   │   └── Video Title 2.mp4
│   └── UC_x5XG1OV2P6uZZ5FSM9Ttw - Channel Name/
│       ├── Video Title 1.mp4
│       └── Video Title 2.mp4
└── downloaded.dat
```

Notes
The script should be run in a directory where yt-dlp.exe is present.
The script creates a urls.txt file for temporary storage of video URLs during each run, which is deleted after each download session.
The downloaded.dat file is used to track downloaded videos and prevent re-downloading.


