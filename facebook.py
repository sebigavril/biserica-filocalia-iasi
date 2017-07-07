import json
import os
import requests
import time

def getStreamUrl():
    pageId = os.environ.get("FILOCALIA_FB_PAGE_ID")
    token  = os.environ.get("FILOCALIA_FB_TOKEN")

    if pageId is None:
        raise Exception("No env variable FILOCALIA_FB_PAGE_ID found!")
    if token  is None:
        raise Exception("No env variable FILOCALIA_FB_TOKEN found!")

    r = requests.post(
        "https://graph.facebook.com/v2.9/" + str(pageId) + "/live_videos"
        + "?access_token=" + str(token)
        + "&title=Test Live Video"
        + "&description=This is a test for a live video on " + time.strftime("%a, %d %b %Y"))

    j = json.loads(r.text)
    return j["stream_url"]
