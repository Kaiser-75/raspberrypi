#!/usr/bin/python3
import subprocess
import time

class VideoStreamer:
    def __init__(self):
        self.video_processes = []

    def stream_video(self):
        # List of camera devices to stream from
        camera_devices = ['/dev/video0', '/dev/video4', '/dev/video8']

        for camera in camera_devices:
            # Stream live from each camera using ffplay
            process = subprocess.Popen([
                'ffplay',
                '-f', 'v4l2',
                '-framerate', '15',
                '-video_size', '720x480',
                '-i', camera
            ])
            self.video_processes.append(process)
            time.sleep(1)  # Optional delay to avoid initialization issues

        print('Streaming live from all cameras...')

    def stop_streams(self):
        # Stop all streaming processes if needed
        for process in self.video_processes:
            process.terminate()
        self.video_processes.clear()

if __name__ == '__main__':
    streamer = VideoStreamer()
    try:
        streamer.stream_video()
        input("Press Enter to stop streaming...\n")  # Keeps the script running
    finally:
        streamer.stop_streams()
