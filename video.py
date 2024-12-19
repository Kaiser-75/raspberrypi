import subprocess
import logging
import datetime
from pathlib import Path
import threading
import time

class VideoRecorder:
    def __init__(self, duration=60, framerate=15, resolution="720x480", base_dir="/home/pi/Documents/"):
        """
        Initializes the video recorder with default parameters.
        :param duration: Recording duration for each video in seconds.
        :param framerate: Frame rate for the recordings.
        :param resolution: Resolution of the recordings.
        :param base_dir: Directory to save recorded videos.
        """
        self.duration = duration
        self.framerate = framerate
        self.resolution = resolution
        self.video_dir = Path(base_dir)
        self.cameras = [
            ("/dev/video0", "video0"),
            ("/dev/video4", "video1"),
            ("/dev/video8", "video2")
        ]
        self.running = False
        self.threads = []

        # Ensure the base directory exists
        self.video_dir.mkdir(parents=True, exist_ok=True)

    def record_camera(self, device, file_prefix):
        """
        Records a single video from a camera using ffmpeg.
        """
        utc_now = datetime.datetime.utcnow()
        video_file = self.video_dir / utc_now.strftime(f"{file_prefix}-%Y-%m-%d-%H-%M-%S.mp4")
        logging.info(f"Starting recording for device: {device} -> {video_file}")
        cmd = [
            "ffmpeg",
            "-f", "v4l2",
            "-framerate", str(self.framerate),
            "-video_size", self.resolution,
            "-i", device,
            "-t", str(self.duration),
            "-c:v", "libx264",
            "-preset", "ultrafast",
            str(video_file)
        ]
        subprocess.run(cmd)
        logging.info(f"Completed recording for device: {device} -> {video_file}")

    def continuous_recording(self, device, file_prefix):
        """
        Continuously records videos for a single camera in 60-second chunks.
        """
        while self.running:
            try:
                self.record_camera(device, file_prefix)
            except Exception as e:
                logging.error(f"Error recording from device {device}: {e}")
            time.sleep(1)  # Short delay before starting the next recording

    def start_recording(self):
        """
        Starts continuous recording for all cameras.
        """
        self.running = True
        logging.info("Starting continuous video recording.")
        self.threads = [
            threading.Thread(target=self.continuous_recording, args=(device, file_prefix))
            for device, file_prefix in self.cameras
        ]
        for thread in self.threads:
            thread.start()

    def stop_recording(self):
        """
        Stops all recording processes.
        """
        self.running = False
        logging.info("Stopping video recording.")
        for thread in self.threads:
            thread.join()
        logging.info("All recording threads have stopped.")
