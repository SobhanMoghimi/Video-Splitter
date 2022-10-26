# Video-Splitter
A python code using FFmpeg to slice long videos into desired splits.


## Running The Code:

To run the code try shell commands:


`python Video-Splitter.py -s [seconds] --root [path to root folder of videos]`

After running the command, a 'out' folder in the root directory will be made, and the splitted videos will be saved there.

### Stop FFmpeg from showing output
To stop the FFmpeg outputs, just add the extra argument `-e '-loglevel quiet'`.


### Same Video Length
For some purposes we need the same length of videos, and if our last piece is not the same as other pieces it may crash our project. To ignore the last piece and not using it, just add the argument `--equal-len`

## Issue With FFmpeg
Some videos aren't correctly splitted after being used by ffmpeg. To solve this problem we should pass the video codecs using -v option in our code. For most mp4 and avi videos we can use h264 codec. Thus running the command `python Video-Splitter.py -s [seconds] --root [path to root folder of videos] -v h264` can help solving the issue.

