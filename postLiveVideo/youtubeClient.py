#!/usr/bin/python

import httplib2
import os
import sys

from apiclient.discovery import build
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