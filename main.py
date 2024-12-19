import logging
from threading import Thread
from video import VideoRecorder
import subprocess

def run_health():
    """
    Runs the health monitoring script as a subprocess.
    """
    logging.info("Starting health monitoring.")
    process = subprocess.Popen(["python3", "health.py"])
    return process

def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize VideoRecorder
    recorder = VideoRecorder(duration=60, framerate=15, resolution="720x480")

    # Start health monitoring and video recording
    try:
        health_process = run_health()

        # Start video recording in a separate thread
        video_thread = Thread(target=recorder.start_recording)
        video_thread.start()

        # Wait for video recording to complete
        video_thread.join()
        recorder.wait_for_completion()

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        # Stop the health monitoring process
        if health_process and health_process.poll() is None:
            logging.info("Stopping health monitoring.")
            health_process.terminate()
            health_process.wait()

        logging.info("All processes stopped.")

if __name__ == "__main__":
    main()
