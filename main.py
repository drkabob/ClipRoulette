import flask

import video_code

app = flask.Flask(__name__)

@app.route('/get_gif/')
def get_gif():
    """Pulls a random GIF link. SLOW!!!"""
    link = flask.request.url_root + video_code.everything()
    return link

@app.route('/videos/<path:path>')
def get_video(path):
    return flask.send_from_directory('videos', path)

@app.route('/static/<path:path>')
def static(path):
    return flask.send_from_directory('static', path)

@app.route('/')
def main():
    pass

if __name__ == '__main__':
    app.run(debug=True)
