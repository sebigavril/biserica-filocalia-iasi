#!/usr/bin/python

import httplib2
import locale
import os
import sys
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

def get_authenticated_service():
    clientSecretsFile = os.environ.get("FILOCALIA_YT_CLIENT_SECRETS_FILE")
    if clientSecretsFile is None:
        raise Exception("No env variable FILOCALIA_YT_CLIENT_SECRETS_FILE found!")

    flow = flow_from_clientsecrets(
        str(clientSecretsFile),
        scope="https://www.googleapis.com/auth/youtube",
        message="No client_secrets file found! To get one, create an OAuth 2.0 client ID and download it from the google console. ")

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, argparser.parse_args())

    return build(
        "youtube",
        "v3",
        http=credentials.authorize(httplib2.Http()))

def getPersistendBroazdcast(youtube):
    res = youtube.liveBroadcasts().list(
        part="id,snippet,contentDetails,status",
        broadcastStatus="all",
        broadcastType="persistent"
    ).execute()

    item = res["items"][0]
    snippet = res["items"][0]["snippet"]

    return item["id"]

def updateBroadcast(youtube, broadcast_id):
    locale.setlocale(locale.LC_TIME, "ro_RO")
    title = "Test - " + time.strftime("%A, %d %B %Y")
    description = "This is a test for a live video"

    res = youtube.liveBroadcasts().update(
        part="snippet,contentDetails",
        body=dict(
            id=broadcast_id,
            contentDetails=dict(
                enableEmbed=True,
                enableDvr=True,
                recordFromStart=True,
                enableContentEncryption=False,
                startWithSlate=False,
                monitorStream=dict(
                    enableMonitorStream=False
                )
            ),
        snippet=dict(
            title=title,
            description=description
            )
        )
    ).execute()

    return res["contentDetails"]["boundStreamId"]

def getStreamName(youtube, streamId):
    res = youtube.liveStreams().list(
        part="id,cdn",
        id=streamId
    ).execute()

    ingestionInfo = res["items"][0]["cdn"]["ingestionInfo"]

    return ingestionInfo["ingestionAddress"] + "/" + ingestionInfo["streamName"]

def getStreamUrl():
    youtube = get_authenticated_service()
    broadcast_id = getPersistendBroadcast(youtube)
    streamId = updateBroadcast(youtube, broadcast_id)
    streamName = getStreamName(youtube, streamId)

    return streamName
