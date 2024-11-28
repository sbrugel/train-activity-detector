# train-activity-detector

A computer vision project which, given a YouTube railcam livestream link, automatically detects train movement. I made this to capture highlights of these streams, which (as you might have figured) most of the time see no activity.

![demonstration gif](demo.gif)

## Files
**main.py**: The entry point of the program, this continuously records 5-minute "segments" of livestream data for processing using `yt-dlp` and `ffmpeg`. Once this period is over, it saves the resulting mp4, restarts the process, and hands over the saved video to the next script:

**detect_stream.py**: Here we input an mp4 file and threshold for motion detection, and we use `opencv` to determine where object motion occurs. Where sufficient motion is detected (based on percentage of pixels that have changed color), the program saves the frames where it occurs along with a heatmap showing where the program detected motion.

## Setup
You will need to [download ffmpeg](https://www.ffmpeg.org/download.html) from here, and ensure it can be run from a terminal.

Make sure to run `pip install -r requirements.txt` before doing anything else!

Create three folders: `data`, `out`, `sns`

Input a YouTube livestream URL into the constant of the same name in `main.py`. For starters, try out the [Deshler camera](https://www.youtube.com/watch?v=Y28qU7UsFko) or [Kearney camera](https://www.youtube.com/watch?v=23tmCNeFh7A)

Input a threshold from 0 to 1 into the constant of the same name in `main.py`. Small numbers work best. For those two examples, 0.02 should be sufficient, but feel free to tweak it a bit.

Run `python main.py` continuously in a terminal

That's it!

## Notes

This has been tested on Windows and Linux (and as such, it probably also works on MacOS), however the process of running the program varies greatly between the two systems.

**Linux:** Running `main.py` should work out of the box.

**Windows:** Due to Windows systems not being POSIX compliant, I ended up having trouble getting multithreading in `main.py` to function correctly, as sending a signal to gracefully exit the `ffmpeg` process that records the livestream ends up signalling the entire main python thread to terminate for some reason. You will have to run `main.py` in a loop through some other means (probably through a batch/shell file) and run `detect_stream.py` through there. Most likely, I will update the project to handle this out of the box

**MacOS:** I do not have acces to a Mac machine, but considering it is POSIX compliant like Linux is, it should work fine. No guarantees.

While this will capture almost all train activity, sometimes the program may capture non-train related activity (likely due to lighting changes or excessive unrelated activity such as moving cars) but this happens infrequently.