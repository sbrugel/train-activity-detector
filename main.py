
import os
import psutil
import queue
import signal
import subprocess
import sys
import threading
import time

URL = 'https://www.youtube.com/watch?v=Y28qU7UsFko'
THRESHOLD = 0.02

def download_stream(url):
    """
    Download the current hour of the livestream, then return the output filename
    """
    try:
        print('beginning recording')
        output_name = 'live-' + str(time.time()) + '.mp4'

        command = ['yt-dlp', url, '-o', output_name]
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # sleep for 1 minute
        for i in range(60):
            print(i)
            time.sleep(1)

        # Check if we're on Windows
        if psutil.WINDOWS:
            process.send_signal(signal.CTRL_C_EVENT)
        else:
            process.send_signal(signal.SIGINT)
        print('a')
        result_queue.put(output_name)
    except KeyboardInterrupt:
        pass # Windows is dumb and a CTRL_C_EVENT kills the parent instead regardless, this prevents that from happening

def process_saved_video(video_file):
    for i in range(10):
        print('in this thread', video_file)
        time.sleep(2)
    #subprocess.run(['python', 'detect_stream.py', 'live-' + time.time() + '.mp4'])
    print('thread complete')

if __name__ == '__main__':
    result_queue = queue.Queue()

    # download the stream
    dl_thread = threading.Thread(target=download_stream, args=(URL,))
    dl_thread.start()

    # wait for this to finish, then get the resulting filename
    dl_thread.join()
    output_name = result_queue.get()

    while True:
        # process previous video
        process_thread = threading.Thread(target=process_saved_video, args=(output_name,))
        process_thread.start()

        # download the stream
        dl_thread = threading.Thread(target=download_stream, args=(URL,))
        dl_thread.start()

        # wait for this to finish, then get the resulting filename
        dl_thread.join()
        output_name = result_queue.get()