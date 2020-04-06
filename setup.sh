#!/bin/bash

apt-get update

# opencv
apt-get install -y libsm6 libxext6 libxrender-dev
pip install opencv-python

apt install -y libgl1-mesa-glx

# pyqt5
pip install pyqt5

# yaml
pip install pyyaml

apt-get update
