import cv2
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

THRESHOLD = 100
FPS = 60

def detect_trains():
    print('loading video...')
    cap = cv2.VideoCapture('./data/train3.mp4')
    print('video loaded')
    ret, prev_frame = cap.read() # read in the first frame

    # reduce prev_frame to 50% size
    prev_frame = cv2.resize(prev_frame, (0, 0), fx=0.25, fy=0.25)

    frame_count = 0
    for i in range(frame_count):
        ret, frame = cap.read()
    while cap.isOpened():
        frame_count += 300
        for i in range(300):
            ret, frame = cap.read()
        frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        if not ret:
            break 

        diff = cv2.absdiff(prev_frame, frame) # calculate the difference between the previous frame and the current frame
        change_magnitude = np.sum(diff, axis=2) # sum the differences across the color channels to create a single channel diff matrix
        change_mask = (change_magnitude > THRESHOLD).astype(np.uint8) # threshold the diff matrix to create a binary mask

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
        axs[1].set_title('Current Frame - TRAIN DETECTED' if np.mean(change_mask) > 0.02 else 'Current Frame')
        
        file_name = ("./sns/color_change_heatmap_" + str(frame_count) + ".png")
        plt.savefig(file_name, dpi=100)
        plt.close()

        print('done with frame', frame_count)

        # print percentage of pixels in change_mask that are 1
        print('percentage of pixels that changed:', np.mean(change_mask) * 100, '%')

        prev_frame = frame

        # print(prev_gray)
        # print('====')
        # print(gray)
        # break

detect_trains()