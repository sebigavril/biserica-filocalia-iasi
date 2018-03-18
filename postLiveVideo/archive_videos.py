#!/usr/bin/python

import youtubeClient

import time

channelId                   = 'UC1OBeVZRh8KiqGvKDzb50lg'
videoTitle                  = 'Biserica Filocalia Iași - LIVE'
videoTitleQuery             = '"' + videoTitle + '"'
servicesArchivePlaylistId   = 'PLqjc0RLa-aohm6nmOVdQ37SUtbKag5daJ'

def get_last_live_video_ids(client):
    channel = client\
                .channels()\
                .list(
                    part='contentDetails',
                    mine=True)\
                .execute()

    uploads_playlist_id = channel['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    uploads = client\
                .playlistItems()\
                .list(
                    part='snippet,contentDetails,status',
                    playlistId=uploads_playlist_id,
                    maxResults=50)\
                .execute()

    former_live_uploads = [item for item in uploads['items'] if item['snippet']['title'] == videoTitle and item['status']['privacyStatus'] == 'unlisted']
    former_live_uploads.sort(key=lambda item: item['snippet']['publishedAt'])
    return [item['snippet']['resourceId']['videoId'] for item in former_live_uploads]

def get_old_archive_videos(client):
    archive = client \
        .playlistItems() \
        .list(
        part='snippet,contentDetails,status',
        playlistId=servicesArchivePlaylistId,
        maxResults=50) \
        .execute()

    videos = archive['items']
    videos = [item for item in videos if item['status']['privacyStatus'] != 'private']
    videos.sort(key=lambda item2: item2['snippet']['publishedAt'], reverse = True)
    return videos[10:] # always keep first 10 videos


def update_video(client, video_id):
    video = client\
        .videos()\
        .list(
            id=video_id,
            part='liveStreamingDetails')\
        .execute()

    video_start_time_string = video['items'][0]['liveStreamingDetails']['actualStartTime']
    video_start_time = time.strptime(video_start_time_string, "%Y-%m-%dT%H:%M:%S.%fZ")

    title = time.strftime("%Y.%m.%d", video_start_time)
    if video_start_time.tm_wday == 6:       # Sunday
        title = title + " Program duminică"

    body = {
        'id': video_id,
        'snippet': {
            'categoryId': '29',
            'title': title,
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    client\
        .videos()\
        .update(
            body=body,
            part='snippet,status')\
        .execute()

def update_video_privacy(client, video):
    print ('Making video ' + video['snippet']['title'] + ' private')
    body = {
        'id': video['snippet']['resourceId']['videoId'],
        'snippet': {
            'categoryId': '29',
            'title': video['snippet']['title']
        },
        'status': {
            'privacyStatus': 'private'
        }
    }
    client \
        .videos() \
        .update(
        body=body,
        part='snippet,status') \
        .execute()

def add_video_to_services_archive_playlist(client, video_id):
    body = {
        'snippet': {
            'playlistId': servicesArchivePlaylistId,
            'resourceId': {
                'kind': 'youtube#video',
                'videoId': video_id
            }
        }
    }
    res = client \
            .playlistItems() \
            .insert(
                body=body,
                part='snippet')\
            .execute()
    return res

def archive_last_live_event(client):
    print("Getting the live events...")
    video_ids = get_last_live_video_ids(client)
    print("Getting the id of the last live events - " + ', '.join(video_ids))

    for video_id in video_ids:
        print("Updating video title for " + video_id + "...")
        update_video(client, video_id)
        print("Moving video for " + video_id + " to archive playlist...")
        add_video_to_services_archive_playlist(client, video_id)
        print("DONE")

def make_archive_private(client):
    print("Getting the last videos in the archive...")
    videos = get_old_archive_videos(client)
    print("Getting the last videos in the archive - " + ', '.join([item['snippet']['resourceId']['videoId'] for item in videos]))
    print("Making them private ...")
    [update_video_privacy(client, video) for video in videos]
    print("DONE")


print("Creating youtube client...")
client = youtubeClient.get_authenticated_service()
print("Creating youtube client - DONE")
archive_last_live_event(client)
make_archive_private(client)