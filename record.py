#!/usr/bin/python3
import logging
import subprocess
import datetime
from pathlib import Path

class VideoRecorder:
    def __init__(self):
        self.video_processes = []
        self.video_sec = 60
        self.video_dir = Path(__file__).parent  # Save in the code directory

    def record_video(self):
        utc_now = datetime.datetime.utcnow()

        # List of camera devices to record from
        camera_devices = ['/dev/video0', '/dev/video4', '/dev/video8']

        for index, camera in enumerate(camera_devices):
            video_file = utc_now.strftime(f'video{index}-%Y-%m-%d-%H-%M-%S.mp4')
            logging.info('Start recording of ' + video_file)

            # Record video using ffmpeg
            process = subprocess.Popen(
                utc_now.strftime(f'ffmpeg -an -f v4l2 '
                + '-framerate 15 -video_size 720x480 '
                + f'-i {camera} -codec:v h264_omx -b:v 1000k -an -t '
                + str(self.video_sec) + ' '
                + str(self.video_dir / video_file)).split()
            )
            self.video_processes.append((process, video_file))

        print('Recording video from all cameras...')
        for process, video_file in self.video_processes:
            process.wait()  # Wait for each recording process to finish

            if (self.video_dir / video_file).exists():
                file_size = (self.video_dir / video_file).stat().st_size
                logging.info('Size of recording {} is {}'.format(video_file, file_size))
            else:
                logging.error('Video recording failed {}'.format(video_file))

    def start(self):
        logging.info("Starting video recording...")
        self.record_video()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    video_recorder = VideoRecorder()
    video_recorder.start()
