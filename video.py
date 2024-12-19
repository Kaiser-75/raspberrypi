import subprocess
import logging
import datetime
from pathlib import Path

class VideoRecorder:
    def __init__(self, duration=60, framerate=15, resolution="720x480", base_dir="/home/pi/Documents/"):
        """
        Initializes the video recorder with default parameters.
        """
        self.duration = duration
        self.framerate = framerate
        self.resolution = resolution
        self.processes = []
        self.video_dir = Path(base_dir)
        self.cameras = [
            ("/dev/video0", "video0"),
            ("/dev/video4", "video1"),
            ("/dev/video8", "video2")
        ]

        # Ensure the base directory exists
        self.video_dir.mkdir(parents=True, exist_ok=True)

    def record_camera(self, device, file_prefix):
        """
        Records video from a single camera using ffmpeg.
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
        return subprocess.Popen(cmd)

    def start_recording(self):
        """
        Starts recording from all cameras in separate processes.
        """
        logging.info("Starting video recording.")
        self.processes = [
            self.record_camera(device, file_prefix) for device, file_prefix in self.cameras
        ]

    def wait_for_completion(self):
        """
        Waits for all recording processes to complete.
        """
        for process in self.processes:
            process.wait()
        logging.info("Video recording completed.")
