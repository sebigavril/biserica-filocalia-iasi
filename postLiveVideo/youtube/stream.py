#!/usr/bin/python

last_live_stream_published_at = ''

def is_stream_live(client):
    global last_live_stream_published_at
    print("Checking if stream is live...")

    live_streams = client.search().list(
        part="id,snippet",
        type="video",
        q="filocalia",
        channelId="UC1OBeVZRh8KiqGvKDzb50lg",
        eventType="live",
        # pageToken="2",
        maxResults=50
    ).execute()

    if len(live_streams['items']) > 0:
        published_at = live_streams['items'][0]['snippet']['publishedAt']
        if last_live_stream_published_at != published_at:
            print("Stream is live")
            last_live_stream_published_at = published_at
            return True
        else:
            print("Stream is not live")
            return False
    else:
        print("Stream is not live")
        return False
