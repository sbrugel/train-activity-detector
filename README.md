# foamer-detector

A computer vision project which, given a YouTube railcam livestream link, automatically detects train movement. I made this to capture highlights of these streams, which (as you might have figured) most of the time see no activity.

![demonstration gif](demo.gif)

## Files
**detect_stream.py**: The main file which captures livestream activity. Given a YouTube stream link as input, the program captures the latest frame from the stream every 5 seconds (the minimum possible given how YouTube works), and saves gifs of train activity.

**detect_demo.py**: The testing version of the above. This takes in a local mp4 file of a train livestream recording, and simulates the above process, comparing frames every 5 seconds.

## Setup
You will need to [download ffmpeg](https://www.ffmpeg.org/download.html) from here, and ensure it can be run from a terminal.

Make sure to run `pip install -r requirements.txt` before doing anything else!

Create three folders: `data`, `out`, `sns`

Run `python detect_stream.py` continuously in a terminal

That's it!

## Notes

This has been tested only on Windows.

While this will capture almost all train activity, sometimes the program may capture non-train related activity (likely due to lighting changes or excessive unrelated activity such as moving cars) but this happens infrequently.

To reduce the chances of the above occurring: If you are using this on a Virtual Railfan camera, I recommend using it only on cameras that **are "static"/DO NOT rotate.** Examples include Cajon Pass, Deshler, and Kearney. I have not yet set up the program to handle camera changes.