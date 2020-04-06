#!/bin/bash
# To make sure video0 is up and running:
sudo modprobe v4l2loopback
ffmpeg -stream_loop -1 -re -i ../posenet/gt/jumping_jack/01_2.mp4 -map 0:v -f v4l2 /dev/video0
