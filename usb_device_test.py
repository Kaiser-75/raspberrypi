import subprocess
import time

def devices():
    # Loop through video device indices from 0 to 32
    for i in range(33):  
        device = f'/dev/video{i}'
        print(f'Testing {device}...')
        command = ['ffplay', '-f', 'v4l2', '-video_size', '640x480', '-i', device]
        
        try:
            subprocess.run(command, check=True)
            print(f'Successfully opened {device}. Press Ctrl+C to stop.')
            time.sleep(5)  
            
        except subprocess.CalledProcessError:
            print(f'Failed to open {device}. Moving to the next device...')
        
        except KeyboardInterrupt:
            print('Exiting...')
            break

if __name__ == '__main__':
    devices()
