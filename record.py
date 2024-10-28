import subprocess
import time

def record_camera(device, output_file, duration=60, framerate=15, resolution="320x240"):
    # Build the ffmpeg command
    cmd = [
        "ffmpeg",
        "-f", "v4l2",
        "-framerate", str(framerate),
        "-video_size", resolution,
        "-i", device,
        "-t", str(duration),
        "-c:v", "libx264",
        "-preset", "ultrafast",
        output_file
    ]
    return subprocess.Popen(cmd)

# Define the camera devices and output files
cameras = [
    ("/dev/video0", "cam0_output.mp4"),
    ("/dev/video4", "cam1_output.mp4"),
    ("/dev/video8", "cam2_output.mp4")
]

# Start recording from each camera
processes = [record_camera(device, output_file) for device, output_file in cameras]

# Wait for all processes to complete
for process in processes:
    process.wait()

print("Recording completed for all cameras.")
