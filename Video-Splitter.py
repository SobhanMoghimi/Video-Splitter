from __future__ import print_function

import csv
import json
import math
import os
import time
import shlex
import subprocess
from optparse import OptionParser

def get_video_length(filename):
    output = subprocess.check_output(("ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                      "default=noprint_wrappers=1:nokey=1", filename)).strip()
    video_length = int(float(output))
    print("Video length in seconds: " + str(video_length))

    return video_length


def ceildiv(a, b):
    return int(math.ceil(a / float(b)))
def floordiv(a, b):
    return int(math.floor(a / float(b)))

def split_by_seconds(filename, split_length, vcodec="copy", acodec="copy",
                     is_equal_len=False, extra="", video_length=None, **kwargs):
    if split_length and split_length <= 0:
        print("Split length can't be 0")
        raise SystemExit

    if not video_length:
        video_length = get_video_length(filename)
        
    if not is_equal_len:
        split_count = ceildiv(video_length, split_length)
    else:
        split_count = floordiv(video_length, split_length)
        if (video_length < split_length):
            return filename
    split_cmd = ["ffmpeg", "-i", filename, "-vcodec", vcodec, "-acodec", acodec] + shlex.split(extra)        
    try:
        filebase_list = filename.split('/')
        filefolder = '/'.join(filebase_list[:-1])
        filebase = filefolder+'/out/'+".".join((filebase_list[-1]).split(".")[:-1])
        print(filebase)
        fileext = filename.split(".")[-1]
    except IndexError as e:
        raise IndexError("No . in filename. Error: " + str(e))
    for n in range(0, split_count):
        split_args = []
        if n == 0:
            split_start = 0
        else:
            split_start = split_length * n

        split_args += ["-ss", str(split_start), "-t", str(split_length),
                       filebase + "-" + str(n + 1) + "-of-" +
                       str(split_count) + "." + fileext]
        print("About to run: " + " ".join(split_cmd + split_args))
        subprocess.check_output(split_cmd + split_args)
    return "success"
       	
        
        
def main():
    
    # Argument Parser, Made for running the code in command-line
    parser = OptionParser()
    
    parser.add_option("-f", "--file",
                      dest="filename",
                      help="File to split, for example sample.avi",
                      type="string",
                      action="store"
                      )
    
    parser.add_option("-s", "--split-size",
                      dest="split_length",
                      help="Split or chunk size in seconds, for example 10",
                      type="int",
                      action="store"
                      )
                      
    parser.add_option("-r", "--root",
                      dest="root_dir",
                      help="Root directory of videos, where they are saved",
                      type="string",
                      action="store"
                      )

    parser.add_option("-v", "--vcodec",
                      dest="vcodec",
                      help="Video codec to use. ",
                      type="string",
                      default="copy",
                      action="store"
                      )
    
    parser.add_option("-e", "--extra",
                      dest="extra",
                      help="Extra options for ffmpeg, e.g. '-e -threads 8'. ",
                      type="string",
                      default="",
                      action="store"
                      )
#     parser.add_option("-q", "--quiet",
#                       action="store_true", 
#                       dest="is_quiet", 
#                       default=False,
#                       help="don't print status messages to stdout")
    
    parser.add_option('--equal-len',
                      action="store_true", 
                      dest="is_equal_len", 
                      default=False,
                      help="ignore the last split if it's less than desired seconds")
    
    # getting the arguments
    (options, args) = parser.parse_args()
    
    #bailout function in case of errors
    def bailout():
        parser.print_help()
        raise SystemExit

        
        
    # We Set the root directory. If it is not mentioned,
    # The Current Directory will be set.
    video_length = None
    print(options.root_dir)
    root_dir = options.root_dir
    if root_dir == '':
        root_dir = os.getcwd()
   
    # Tuple of video formats to check in directory.
    video_formats = ('WEBM', 'MPG', 'MP2',
                 'MPEG', 'MPE', 'MPV',
                 'OGG', 'MP4', 'M4P',
                 'M4V', 'AVI', 'WMV',
                 'MOV', 'QT', 'FLV',
                 'SWF', 'AVCHD')
    
    # Looping through files of our directory to trim the videos
    # Note: The "out" folder should be made before the code
    # The unsuccessful_videos is for the videos that are smaller than the given size in --equal-len mode!
    unsuccessful_videos = []
    for file in os.listdir(root_dir):
        fileext = file.split(".")[-1]
        print(fileext,' , ',file)
        if (fileext.upper() in video_formats):
            res = split_by_seconds(root_dir+'/'+file, 
                             options.split_length, 
                             vcodec = options.vcodec, 
                             is_equal_len = options.is_equal_len, 
                             extra = options.extra)
            if(res != "success"):
            	unsuccessful_videos.append(res)
    print( '\033[93m' + "Warning: Below videos are smaller than the desired size for --equal-len and not processed." + '\033[0m')
    time.sleep(2)
    for st in unsuccessful_videos:
    	print('\033[94m'+st+'\033[0m')
    	time.sleep(0.05)


       

    
    
if __name__ == '__main__':
    main()
