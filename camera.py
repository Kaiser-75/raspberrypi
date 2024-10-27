#!/usr/bin/python3
import subprocess
import datetime
import logging
from pathlib import Path

class VideoRecorder:

    def __init__(self):
        self.video_sec = 60  # Duration to record in seconds
        self.video_dir = '/home/pi/videos/'  # Directory to save videos
        Path(self.video_dir).mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist

    def record_video(self):
        utc_now = datetime.datetime.utcnow()
        video_file = utc_now.strftime('video-%Y-%m-%d-%H-%M-%S.mp4')
        logging.info(f'Start recording: {video_file}')

        # Start recording from the USB camera connected to /dev/video0
        command = f'ffmpeg -f v4l2 -framerate 15 -video_size 720x480 -i /dev/video0 -codec:v h264_omx -b:v 1000k -t {self.video_sec} {self.video_dir}{video_file}'
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the recording to complete
        stdout, stderr = process.communicate()
        logging.info(stdout)
        logging.error(stderr)

        logging.info(f'Recording completed: {video_file}')

        # Check if the video file was created and log the file size
        if Path(self.video_dir + video_file).exists():
            file_size = Path(self.video_dir + video_file).stat().st_size
            logging.info(f'Video saved: {video_file}, size: {file_size} bytes')
        else:
            logging.error(f'Failed to record video: {video_file}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, filename='/home/pi/video_recorder.log', filemode='a', format='%(asctime)s - %(message)s')
    recorder = VideoRecorder()

    # Record a video
    recorder.record_video()
