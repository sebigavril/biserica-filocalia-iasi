#!/usr/bin/python

import time

from . import constants

def archive_last_live_event(client):
    print("Getting the live events...")
    video_ids = __get_last_live_video_ids(client)
    print("Found " + str(len(video_ids)) + " live videos not yet archived: " + ', '.join(video_ids))

    for video_id in video_ids:
        print("Updating video title for " + video_id + "...")
        __update_video(client, video_id)
        print("Moving video for " + video_id + " to archive playlist...")
        __add_video_to_services_archive_playlist(client, video_id)
        print("DONE")

def __get_last_live_video_ids(client):
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

    former_live_uploads = [item for item in uploads['items'] if item['snippet']['title'] == 'Biserica Filocalia Iași - LIVE' and item['status']['privacyStatus'] == 'unlisted']
    former_live_uploads.sort(key=lambda item: item['snippet']['publishedAt'])
    return [item['snippet']['resourceId']['videoId'] for item in former_live_uploads]

def __update_video(client, video_id):
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
            'privacyStatus': 'public',
            'embeddable': 'true'
        }
    }

    client\
        .videos()\
        .update(
            body=body,
            part='snippet,status')\
        .execute()

def __add_video_to_services_archive_playlist(client, video_id):
    body = {
        'snippet': {
            'playlistId': constants.servicesArchivePlaylistId,
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