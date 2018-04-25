import locale
import json
import os
import requests

def postLiveStream():
    print ("Posting live video to facebook...")
    pageId = "175350919147927"
    token  = os.environ.get("FILOCALIA_FB_TOKEN")

    if token  is None:
        raise Exception("No env variable FILOCALIA_FB_TOKEN found!")

    locale.setlocale(locale.LC_TIME, "ro_RO")

    r = requests.post(
        "https://graph.facebook.com/v2.10/" + str(pageId) + "/feed"
        + "?access_token=" + str(token)
        + "&link=https://www.youtube.com/watch?v=ArBFs_1togo"
        + "&message=Suntem LIVE! Acceseaza https://www.youtube.com/watch?v=ArBFs_1togo pentru a ne urmari sau www.bisericafilocalia.ro/media/arhiva-video-youtube pentru ")

    j = json.loads(r.text)
    print(j)
    print ("Posting live video to facebook - DONE")
