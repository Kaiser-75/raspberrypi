#!/usr/bin/python3
import logging
import subprocess
import datetime
from pathlib import Path

class VideoStreamer:
    def __init__(self):
        self.video_processes = []
        self.video_dir = Path(__file__).parent  # Save in the code directory

    def stream_video(self):
        # List of camera devices to stream from
        camera_devices = ['/dev/video0', '/dev/video4', '/dev/video8']

        # Example RTMP URL for streaming (modify this as needed)
        rtmp_url = 'rtmp://your.streaming.server/live'  # Replace with your RTMP server URL

        for index, camera in enumerate(camera_devices):
            # Construct the stream URL for each camera
            stream_url = f'{rtmp_url}/camera{index}'
            logging.info(f'Start streaming from {camera} to {stream_url}')

            # Stream video using ffmpeg
            process = subprocess.Popen(
                [
                    'ffmpeg',
                    '-an', 
                    '-f', 'v4l2',
                    '-framerate', '15',
                    '-video_size', '720x480',
                    '-i', camera,
                    '-codec:v', 'h264_omx',
                    '-b:v', '1000k',
                    '-f', 'flv',  # Format for RTMP
                    stream_url
                ]
            )
            self.video_processes.append(process)

        print('Streaming video from all cameras...')

        # Wait for each streaming process to finish (optional)
        for process in self.video_processes:
            process.wait()  # This line can be removed if you want to run indefinitely

    def start(self):
        logging.info("Starting video streaming...")
        self.stream_video()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    video_streamer = VideoStreamer()
    video_streamer.start()
