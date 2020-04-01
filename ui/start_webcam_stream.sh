#!/bin/bash
ffmpeg -stream_loop -1 -re -i ../posenet/gt/jumping_jack/01.mp4 -map 0:v -f v4l2 /dev/video0
