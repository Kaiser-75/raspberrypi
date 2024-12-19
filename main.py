import logging
import subprocess
import signal
import sys
from video import VideoRecorder

def run_health():
    """
    Runs the health monitoring script as a subprocess.
    """
    logging.info("Starting health monitoring.")
    process = subprocess.Popen(["python3", "health.py"])
    return process

def stop_all(recorder, health_process):
    """
    Stops the video recorder and health monitoring process.
    """
    logging.info("Stopping all processes.")
    recorder.stop_recording()
    if health_process and health_process.poll() is None:
        health_process.terminate()
        health_process.wait()
    logging.info("All processes stopped.")

def signal_handler(sig, frame, recorder, health_process):
    """
    Handles termination signals (e.g., Ctrl+C) to stop all processes gracefully.
    """
    stop_all(recorder, health_process)
    sys.exit(0)

def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize VideoRecorder
    recorder = VideoRecorder(duration=60, framerate=15, resolution="720x480")

    # Start health monitoring and video recording
    health_process = None
    try:
        health_process = run_health()
        signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, recorder, health_process))
        
        # Start continuous video recording
        recorder.start_recording()
        
        # Keep the main thread alive
        logging.info("Recording and health monitoring started. Press Ctrl+C to stop.")
        signal.pause()

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        stop_all(recorder, health_process)

if __name__ == "__main__":
    main()
