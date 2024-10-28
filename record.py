import subprocess
import time

# Define the video devices and output files
cameras = {
    '/dev/video0': 'camera_0.mp4',
    '/dev/video4': 'camera_4.mp4',
    '/dev/video8': 'camera_8.mp4',
}


def record_videos():
    processes = []

    try:
        for device, output_file in cameras.items():
            command = [
                'ffmpeg',
                '-f', 'v4l2',
                '-video_size', '640x480',
                '-i', device,
                '-t', '60',  # Record for 60 seconds
                output_file
            ]
            print(f'Starting recording from {device} to {output_file}...')
            
            processes.append(subprocess.Popen(command))

        # Wait for all processes to finish
        for process in processes:
            process.wait()

        print('record success')

    except Exception as e:
        print(f'Error')
        for process in processes:
            process.terminate()

if __name__ == '__main__':
    record_videos()
