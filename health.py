#!/usr/bin/python3

"""
Monitors storage health in the /home/pi/Documents/ directory and logs relevant information.
"""

import logging
import shutil
import time

class HealthMonitor:
    def __init__(self, log_interval=5.0, check_path="/home/pi/Documents"):
        """
        Initializes the health monitor.
        """
        self.log_interval = log_interval
        self.check_path = check_path
        self.running = False

    def check_storage(self):
        """
        Checks the available and used storage on the specified path.
        Logs a warning if storage is running low.
        """
        total, used, free = shutil.disk_usage(self.check_path)
        logging.info(
            f"Storage Check - Total: {total // (2**30)} GB, Used: {used // (2**30)} GB, Free: {free // (2**30)} GB"
        )
        if free < 1 * (2**30):
            logging.warning("Warning: Less than 1 GB of storage remaining!")

    def start(self):
        """
        Starts the health monitoring process.
        """
        self.running = True
        logging.info("Health monitoring started.")
        while self.running:
            try:
                self.check_storage()
                time.sleep(self.log_interval)
            except Exception as e:
                logging.error(f"Error during health monitoring: {e}")

    def stop(self):
        """
        Stops the health monitoring process.
        """
        self.running = False
        logging.info("Health monitoring stopped.")

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize and start health monitoring
    health_monitor = HealthMonitor(log_interval=5.0)
    try:
        health_monitor.start()
    except KeyboardInterrupt:
        health_monitor.stop()
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
