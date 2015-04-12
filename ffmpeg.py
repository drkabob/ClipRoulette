# A script for handling ffmpeg via Python
# ~Nathan Hakkakzadeh

import subprocess

# Constants
SECONDS_IN_MINUTE = 60
SECONDS_IN_HOUR = 60 * 60

DEVNULL = open("/dev/null", "w")

# ffmpeg exception class
# Something went wrong with ffmpeg. Shit.
# Has a method which shows you the ffmpeg output
class FFmpegException(Exception):
    
    def __init__(self, value, output):
        self.output = output
        self.value = value

    def __str__(self):
        return repr(value)

    # Method for returning the ffmpeg output
    def ffmpeg_output(self):
        return self.output


# Get video length via ffprobe
# Give it a file location and it will give you time in seconds
def get_video_length(filename):
    result = subprocess.Popen(["ffprobe", "-print_format", "ini", filename],
    stdout = subprocess.PIPE, stderr = subprocess.STDOUT)

    lines = result.stdout.readlines()

    # Find the duration in the output...
    for line in lines:
        line = line.decode("utf-8")
        if "Duration: " in line:
            # Convert into a number
            line = line.strip().lstrip("Duration: ")
            times = line.split(":")
            seconds = times[2].split(",")[0]
            total_time = 0
            total_time += float(times[0]) * SECONDS_IN_HOUR
            total_time += float(times[1]) * SECONDS_IN_MINUTE
            total_time += float(seconds)
            return total_time
    
    # We didn't find anything throw an error
    raise FFmpegException("Unable to find duration", lines)

# Get whether or not the video is rotated via ffprobe
# Give it a file location and it will tell you whether or not it is rotated
def get_rotation(filename):
    result = subprocess.Popen(["ffprobe", "-print_format", "ini", filename],
    stdout = subprocess.PIPE, stderr = subprocess.STDOUT)

    lines = result.stdout.readlines()
    
    # Find the rotate in the output...
    for line in lines:
        line = line.decode("utf-8")
        if "rotate" in line:
            # See if it is rotated by 90 degrees
            if "90" in line:
                return True
            else:
                return False
    
    return False

# Convert a video to a certain format
# Give it a resolution and a format to output to
def convert_video(source_location, output_location, vid_encoding=None, audio_encoding=None, width=None, rotate=False, start_time=None, length_code=None, mute=False):
    # Start assembling command list
    command = ["ffmpeg", "-i", source_location]

    # Go through the arguments and if they are defined, add them
    if vid_encoding is not None:
        command.append("-vcodec")
        command.append(vid_encoding)
    
    if audio_encoding is not None:
        command.append("-acodec")
        command.append(audio_encoding)
    
    # This needs to be here... then we continue with the arugments
    command.append("-strict")
    command.append("-2")

    if width is not None or rotate:
        command.append("-vf")
    if width is not None:
        parameter = "scale=" + width + ":trunc(ow/a/2)*2"
        
        if rotate:
            parameter += ",transpose=1"

        command.append(parameter)
    
    if rotate:
        if width is None:
            command.append("transpose=1")

        command.append("-metadata:s:v:0")
        command.append("rotate=0")

    if start_time is not None and length_code is not None:
        command.append("-ss")
        command.append(start_time)
        command.append("-t")
        command.append(length_code)

    if mute:
        command.append("-an")

    
    # Finally add the output_location
    command.append(output_location)

    # And call the command
    subprocess.check_call(command, stdout=DEVNULL, stderr=DEVNULL)
