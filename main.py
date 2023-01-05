import re
import config
from datetime import timedelta
from googleapiclient.discovery import build

#YouTube API key
api_key = config.api_key

youtube = build('youtube', 'v3', developerKey=api_key)

#Add user input
print("Please input a public YouTube Playlist ID:")
print()
print("If you need an example copy and paste this one: PLvII-M6kZPhSIKpa9QreVNfxbSFdIewQl")
print()
inputPlaylist = (input())

#get the digit values by H/M/S
hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

total_seconds = 0

#Make a while loop to grab videos from the playlist until the playlist runs out.
nextPageToken = None
while True:
    pl_request = youtube.playlistItems().list(
        part="contentDetails, snippet",
        playlistId=inputPlaylist,
        maxResults=50,
        pageToken=nextPageToken
        )
    pl_response = pl_request.execute()

    #Gets video IDs
    vid_ids = []
    for item in pl_response["items"]:
        vid_ids.append(item['contentDetails']['videoId'])

    vid_request = youtube.videos().list(
        part="contentDetails",
        id=','.join(vid_ids)
    )

    #From video response gets digit before hours, minutes, seconds
    vid_response = vid_request.execute()

    #Video response contenDetails duration
    for item in vid_response['items']:
        vid_duration = item['contentDetails']['duration']

        hours = hours_pattern.search(vid_duration)
        minutes = minutes_pattern.search(vid_duration)
        seconds = seconds_pattern.search(vid_duration)

    #Ternary conditional hours, minutes, seconds
        hours = int(hours.group(1)) if hours else 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

    #Using from datetime import timedelta
        video_seconds = timedelta(
            hours = hours,
            minutes = minutes,
            seconds = seconds
        ).total_seconds()

        total_seconds += video_seconds

        #Old way of just displaying old videos seconds count
        #print(video_seconds)
        #print()

    nextPageToken = pl_response.get('nextPageToken')

    if not nextPageToken:
        break

#total_seconds
#print(total_seconds)
#total_seconds = int(total_seconds)

#use divmod to turn seconds into hours, minutes, seconds
total_seconds = int(total_seconds)

minutes, seconds = divmod(total_seconds, 60)
hours, minutes = divmod(minutes, 60)

print('The playlist is')
print(f'{hours}:{minutes}:{seconds}')

if hours >= 1:
    print("This is going to take a long time, you might want to get a snack.")
else:
    print("Ah less than an hour, that's not bad.")
