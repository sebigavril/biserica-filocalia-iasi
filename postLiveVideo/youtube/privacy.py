#!/usr/bin/python

from . import constants

def __get_old_archive_videos(client):
    archive = client \
        .playlistItems() \
        .list(
        part='snippet,contentDetails,status',
        playlistId=constants.servicesArchivePlaylistId,
        maxResults=50) \
        .execute()

    videos = archive['items']
    videos = [item for item in videos if item['status']['privacyStatus'] != 'private']
    videos.sort(key=lambda item2: item2['snippet']['publishedAt'], reverse = True)
    return videos[10:] # always keep first 10 videos

def __update_video_privacy(client, video):
    print ('Making video ' + video['snippet']['title'] + ' private')
    body = {
        'id': video['snippet']['resourceId']['videoId'],
        'snippet': {
            'categoryId': '29',
            'title': video['snippet']['title']
        },
        'status': {
            'privacyStatus': 'private',
            'embeddable': 'true'
        }
    }
    client \
        .videos() \
        .update(
        body=body,
        part='snippet,status') \
        .execute()


def make_archive_private(client):
    print("Getting the last videos in the archive...")
    videos = __get_old_archive_videos(client)
    print("Found " + str(len(videos)) + " videos in the archive that need to made private: " + ', '.join([item['snippet']['resourceId']['videoId'] for item in videos]))
    print("Making them private ...")
    [__update_video_privacy(client, video) for video in videos]
    print("DONE")