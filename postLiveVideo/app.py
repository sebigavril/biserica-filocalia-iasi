#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit

import facebook
import youtube

app = Flask(__name__)
app.secret_key = 'session-secret'
socketio = SocketIO(app, async_mode=None)
streaming = False
thread_lock = Lock()

@app.route('/')
def index():
    session['streaming'] = streaming
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('start_stream_client_event', namespace='/stream')
def start_stream(message):
    emit('start_stream_confirmation_server_event', message)
    __start_nginx()

@socketio.on('stop_stream_client_event', namespace='/stream')
def stop_stream():
    global streaming
    streaming = False
    session['streaming'] = streaming

def __start_nginx():
    global streaming
    with thread_lock:
        if not streaming:
            streaming = True
            session['streaming'] = streaming
            socketio.start_background_task(target=__status_thread)
            socketio.start_background_task(target=__facebook_thread)

def __status_thread():
    global streaming
    count = 0
    while streaming:
        if count > 0:
            socketio.sleep(1)
        count += 1
        prefix = '.' * (count % 4)
        socketio.emit('stream_status_server_event',
                      {'status': 'Waiting for stream to start' + prefix},
                      namespace='/stream')

def __facebook_thread():
    global streaming
    if streaming:
        facebookStreamUrl = facebook.getStreamUrl()
        socketio.emit('facebook_status_server_event',
                      {'status': "Facebook Stream: " + facebookStreamUrl},
                      namespace='/stream')

if __name__ == '__main__':
    socketio.run(app, debug=True)
