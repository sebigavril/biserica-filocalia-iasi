#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit

import facebook
import youtube
import postLiveVideo

app = Flask(__name__)
app.secret_key = 'session-secret'
socketio = SocketIO(app, async_mode=None, manage_session = False)

thread_lock = Lock()
commonSession = {
    'status': 'off',
    'urls': {
        'facebookStreamUrl': '',
        'youtubeStreamUrl': ''
    }
}

@app.route('/')
def index():
    session['status'] = commonSession['status']
    session['urls'] = {}
    session['urls']['facebookStreamUrl'] = commonSession['urls']['facebookStreamUrl']
    session['urls']['youtubeStreamUrl'] = commonSession['urls']['youtubeStreamUrl']
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('start_stream_client_event', namespace='/stream')
def start_stream(message):
    global commonSession
    if commonSession['status'] == "off":
        commonSession['status'] = "starting"

        with thread_lock:
            socketio.start_background_task(target=__status_thread)
            socketio.start_background_task(target=__get_facebook_stream_url)
            socketio.start_background_task(target=__get_youtube_stream_url)
            socketio.start_background_task(target=__start_nginx)

@socketio.on('stop_stream_client_event', namespace='/stream')
def stop_stream():
    global commonSession
    commonSession['status'] = "off"
    commonSession['urls']['facebookStreamUrl'] = ""
    commonSession['urls']['youtubeStreamUrl'] = ""
    socketio.emit('facebook_status_server_event',
                  {'status': ""},
                  namespace='/stream')
    socketio.emit('youtube_status_server_event',
                  {'status': ""},
                  namespace='/stream')
    socketio.emit('stream_status_server_event',
                  {'status': 'off'},
                  namespace='/stream')

def __status_thread():
    global commonSession
    count = 0
    while commonSession['status'] == "starting":
        count += 1
        prefix = '.' * (count % 4)
        socketio.emit('stream_status_server_event',
                      {'status': 'waiting' + prefix},
                      namespace='/stream')
        socketio.sleep(1)

def __get_facebook_stream_url():
    global commonSession
    if commonSession['status'] == "starting":
        facebookStreamUrl = facebook.getStreamUrl()
        if commonSession['status'] == "starting":
            commonSession['urls']['facebookStreamUrl'] = facebookStreamUrl
            socketio.emit('facebook_status_server_event',
                          {'status': facebookStreamUrl},
                          namespace='/stream')

def __get_youtube_stream_url():
    global commonSession
    if commonSession['status'] == "starting":
        youtubeStreamUrl = youtube.getStreamUrl()
        if commonSession['status'] == "starting":
            commonSession['urls']['youtubeStreamUrl'] = youtubeStreamUrl
            socketio.emit('youtube_status_server_event',
                          {'status': youtubeStreamUrl},
                          namespace='/stream')

def __start_nginx():
    global commonSession
    while commonSession['status'] == "starting" and (commonSession['urls']['facebookStreamUrl'] == "" or commonSession['urls']['youtubeStreamUrl'] == ""):
        socketio.sleep(1)
    if commonSession['status'] == "starting":
        res = postLiveVideo.postLiveVideo(commonSession['urls']['facebookStreamUrl'], commonSession['urls']['youtubeStreamUrl'])
        if res and commonSession['status'] == "starting":
            commonSession['status'] = "on"
            socketio.sleep(1)
            socketio.emit('stream_status_server_event',
                          {'status': 'on'},
                          namespace='/stream')


if __name__ == '__main__':
    socketio.run(app, debug=True)
