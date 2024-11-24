import cv2
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import imageio
import time
import subprocess
import shlex
import yt_dlp

CHANGE_THRESHOLD = 100
DETECTION_THRESHOLD = 0.02

prev_frame = None
current_frame = None

def get_stream_url(youtube_url):
    ydl_opts = {"format": "best"}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        return info_dict["url"]

def trains_detected(prev_frame, current_frame):
    # reduce prev_frame to 25% size
    pframe = cv2.resize(prev_frame, (0, 0), fx=0.25, fy=0.25)
    cframe = cv2.resize(current_frame, (0, 0), fx=0.25, fy=0.25)

    diff = cv2.absdiff(pframe, cframe) # calculate the difference between the previous frame and the current frame
    change_magnitude = np.sum(diff, axis=2) # sum the differences across the color channels to create a single channel diff matrix
    change_mask = (change_magnitude > CHANGE_THRESHOLD).astype(np.uint8) # threshold the diff matrix to create a binary mask

    # visualize with Seaborn
    sns.set_theme(style="white")

    # make two 16, 9 subplots
    fig, axs = plt.subplots(1, 2, figsize=(32, 9))

    # put the change_mask on the left subplot
    sns.heatmap(change_mask, cmap='coolwarm', cbar=True, ax=axs[0])

    # put the full current_frame on the right subplot - convert from BGR to RGB
    cframe_disp = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
    axs[1].imshow(cframe_disp)

    # set title of the plot
    axs[0].set_title('Color Change Magnitude')
    axs[1].set_title('Current Frame - TRAIN DETECTED' if np.mean(change_mask) > DETECTION_THRESHOLD else 'Current Frame')
    
    file_name = None
    if np.mean(change_mask) > DETECTION_THRESHOLD:
        file_name = ("./sns/color_change_heatmap_" + str(time.time()) + ".png")
        plt.tight_layout()
        plt.savefig(file_name, dpi=50)
        plt.close()

    return (np.mean(change_mask) > DETECTION_THRESHOLD, file_name)

if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/live/Y28qU7UsFko?si=ykoRwgKPjGkGoBU6"  # Replace with the actual YouTube URL
    stream_url = get_stream_url(youtube_url)
    print("Stream URL fetched.", stream_url)

    i = 0
    imgs_to_gif = []

    while True:
        i += 1
        full_cmd = 'ffmpeg -y -i ' + stream_url + ' -frames:v 1 -q:v 2 ./out/frame' + str(i) + '.jpg'
        subprocess.run(shlex.split(full_cmd))

        # obtain current_frame from frame.jpg
        current_frame = cv2.imread('./out/frame' + str(i) + '.jpg')

        if prev_frame is not None:
            detected, heatmap_file = trains_detected(prev_frame, current_frame)
            
            if not detected:
                # delete the oldest picture in the folder
                subprocess.run(shlex.split('rm ./out/frame' + str(i - 1) + '.jpg'))

                if len(imgs_to_gif) > 0:
                    # create a gif of all images in the 'sns' folder, comparing the current frame against the heatmap of color change magnitude vs the previous frame
                    with imageio.get_writer('./sns_' + str(time.time()) + '.gif', mode='I', loop=0, duration=1) as writer:
                        for filename in imgs_to_gif:
                            image = imageio.imread(filename)
                            writer.append_data(image)

                    print('gif created')

                    # delete all the images in the folder
                    subprocess.run(shlex.split('rm ./sns/*.png'))

                    imgs_to_gif = []
            else:
                imgs_to_gif.append(heatmap_file)

        prev_frame = current_frame

        # wait for 1 second
        time.sleep(5)