#!/bin/bash

pip3 install --user -r requirements.txt

mkdir data
mkdir tmp

cd data
git clone https://github.com/pjreddie/darknet.git
cd darknet
make

# execute in the ./darkent directory
wget https://pjreddie.com/media/files/darknet19.weights
wget https://pjreddie.com/media/files/yolov3-tiny.weights
