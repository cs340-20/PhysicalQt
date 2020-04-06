#!/bin/bash

apt-get update

# opencv
apt-get install -y libsm6 libxext6 libxrender-dev
pip install opencv-python

apt install -y libgl1-mesa-glx

# upgrade pip
pip install --upgrade pip

# pyqt5
#pip install PyQt5
apt-get install -y python3-pyqt5

# yaml
pip install pyyaml

# scipy
pip install scipy

apt-get update
