import flask
import json

import video_code

app = flask.Flask(__name__)

@app.route('/get_gif/')
def get_gif():
    """Pulls a random GIF link. SLOW!!!"""
    link, source_link = video_code.everything()
    return json.dumps({'link': flask.request.url_root + link, 'source': source_link})

@app.route('/videos/<path:path>')
def get_video(path):
    return flask.send_from_directory('videos', path)

@app.route('/statics/<path:path>')
def statics(path):
    return flask.send_from_directory('statics', path)

@app.route('/')
def main():
    return flask.render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
