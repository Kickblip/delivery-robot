#!/bin/bash

# get most recent version of code
git pull origin main

# activate virtual environment
source ~/tflite/bin/activate

# ensure connected display is set as default
export DISPLAY=:0

# cd into the project dir
cd delivery-robot

# run the model
python3 detect.py
