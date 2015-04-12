import requests
from bs4 import BeautifulSoup
import configparser
import string
import random
import subprocess

import ffmpeg

# Etc.
DEVNULL = open("/dev/null", "w")
PATH = "./"

# Set up config so we can get basic data
config = configparser.ConfigParser()
config.read(PATH + "gif.cfg")

# YouTube related
YT_USERNAME = config.get("YouTube", "username")
YT_PASSWORD = config.get("YouTube", "password")

# Random string generator
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def get_random_youtube_link():
    """Gets a random YouTube link"""
    r = requests.get('http://randomyoutube.net/')
    soup = BeautifulSoup(r.text)
    return soup.body.find('div', {'class': 'col-md-3'}).p.a['href']

def get_random_start_stop(video_length):
    """Returns a random starting and stopping timecode given a video's length"""
    start = random.randrange(int(video_length))
    stop = min(video_length, start + random.randint(5, 10))

    start = '{}:{}'.format(start // 60, start % 60)
    stop = '{}:{}'.format(stop // 60, stop % 60)

    # Parse the time
    starts = [int(x) for x in start.split(":")[::-1]]
    stops = [int(x) for x in stop.split(":")[::-1]]

    diff = []

    for i in range(0, len(starts)):
        diff.append(stops[i] - starts[i])

        if diff[i] < 0:
            stops[i+1] -= 1
            diff[i] += 60

        if diff[0] > 15:
            raise Exception("Length too long.")

        for i in range(1, len(diff)):
            if diff[i] > 0:
                raise Excpetion("Length too long.")

    reverse_diff = diff[::-1]

    tosend = ""
    for d in reverse_diff:
        tosend += str(d) + ":"

    tosend = tosend[0:len(tosend)-1]

    return start, tosend

def make_short(youtube_link, token):
    """Takes a YouTube link, an optional random token, and start and stop strings and
    generates a short video out of them. Returns the locations of the video."""
    place = PATH + "tmp/" + token
    # Download the video
    subprocess.check_call([
        "youtube-dl", "-o", place + "-vid", "-f", "5", "--max-filesize",
        "40m", "-u", YT_USERNAME, "-p", YT_PASSWORD, youtube_link],
        stdout=DEVNULL, stderr=subprocess.STDOUT)

    length = ffmpeg.get_video_length(place + '-vid')

    start, stop = get_random_start_stop(length)

    out = 'videos/{}.mp4'.format(token)
    ffmpeg.convert_video(place + '-vid', out, 'h264', 'aac', '480', ffmpeg.get_rotation(place + '-vid'), start, stop)
    return out

def everything(retries=10):
    try:
        source_link = get_random_youtube_link()
        return make_short(source_link, id_generator()), source_link
    except Exception as e:
        if retries > 0:
            return everything(retries-1)
        else:
            raise e

