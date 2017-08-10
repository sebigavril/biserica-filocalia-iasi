import locale
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

    locale.setlocale(locale.LC_TIME, "ro_RO")
    title = "Test - " + time.strftime("%A, %d %B %Y")
    description = "This is a test for a live video"

    r = requests.post(
        "https://graph.facebook.com/v2.9/" + str(pageId) + "/live_videos"
        + "?access_token=" + str(token)
        + "&title=" + title
        + "&description=" + description)

    j = json.loads(r.text)
    return j["stream_url"]
