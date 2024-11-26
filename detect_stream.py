import cv2
import imageio
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import shlex
import subprocess
import sys
import time
import yt_dlp

# cli arguments
if len(sys.argv) != 3:
    print("Usage: python detect_stream.py <mp4 video name> <threshold, from 0 to 1>")
    sys.exit(1)
    
CHANGE_THRESHOLD = 100
vid_name = sys.argv[1]
DETECTION_THRESHOLD = float(sys.argv[2])

prev_frame = None
current_frame = None

if __name__ == "__main__":
    print('loading video...')
    cap = cv2.VideoCapture('./data/live.mp4')
    print('video loaded')
    ret, prev_frame = cap.read() # read in the first frame

    # reduce prev_frame to 25% size
    prev_frame = cv2.resize(prev_frame, (0, 0), fx=0.25, fy=0.25)

    frame_count = 0 # the current frame number
    frame_start = None # start of train activity, if applicable
    frame_end = None # end of train activity, if applicable

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            cap.release()
            break 

        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        diff = cv2.absdiff(prev_frame, frame) # calculate the difference between the previous frame and the current frame
        change_magnitude = np.sum(diff, axis=2) # sum the differences across the color channels to create a single channel diff matrix
        change_mask = (change_magnitude > CHANGE_THRESHOLD).astype(np.uint8) # threshold the diff matrix to create a binary mask

        train_found = np.mean(change_mask) > 0.02

        # print percentage of pixels in change_mask that are 1
        print('percentage of pixels that changed:', np.mean(change_mask) * 100, '%', train_found)

        if train_found:
            if frame_start is None:
                frame_start = frame_count
            # visualize with Seaborn
            sns.set_theme(style="white")
            
            # make two 16, 9 subplots
            fig, axs = plt.subplots(1, 2, figsize=(32, 9))

            # put the change_mask on the left subplot
            sns.heatmap(change_mask, cmap='coolwarm', cbar=True, ax=axs[0])

            # put the full current_frame on the right subplot - convert from BGR to RGB
            cframe_disp = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            axs[1].imshow(cframe_disp)

            # set title of the plot
            axs[0].set_title('Color Change Magnitude')
            axs[1].set_title('Current Frame - TRAIN DETECTED' if train_found else 'Current Frame')
            
            file_name = ("./sns/color_change_heatmap_" + str(frame_count) + ".png")
            plt.savefig(file_name, dpi=100)
            plt.close()
        else:
            if frame_start is not None:
                frame_end = frame_count
                print('Train activity from frame', frame_start, 'to frame', frame_end)
                frame_start = None
                frame_end = None

        print('done with frame', frame_count)

        prev_frame = frame

        frame_count += 150 # advance this many frames, i.e. at 30 fps, this advances one second
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)

    cap.release()

    # delete the video file
    subprocess.run(shlex.split('rm ' + vid_name))