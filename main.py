import flask
import json
import os
import random

import video_code

app = flask.Flask(__name__)

@app.route('/get_gif/')
def get_gif():
    """Pulls a random GIF link. SLOW!!!"""
    link, source_link = video_code.everything()
    return json.dumps({'link': flask.request.url_root + link, 'source': source_link})

@app.route('/get_old_gif/')
def get_old_gif():
    """Pulls a random GIF link. FAST!!!"""
    link, source_link = 'videos/' + random.choice(os.listdir('videos')), ""
    return json.dumps({'link': flask.request.url_root + link, 'source': source_link, 'inner': flask.request.url_root + 'video/' + link.lstrip('videos/').rstrip('.mp4')})

@app.route('/video/<vid_id>')
def video(vid_id):
    return flask.render_template('video.html', link=flask.request.url_root + 'videos/' + vid_id + '.mp4')

@app.route('/videos/<path:path>')
def get_video(path):
    return flask.send_from_directory('videos', path)

@app.route('/statics/<path:path>')
def statics(path):
    return flask.send_from_directory('statics', path)

@app.route('/')
def main():
    return flask.render_template('index_new.html')

if __name__ == '__main__':
    app.run(debug=True)
