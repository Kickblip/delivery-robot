#!/bin/bash

# Update packages on your Raspberry Pi OS.
sudo apt-get update

# Check your Python version. You should have Python 3.7 or later.
python3 --version

# Install virtualenv and upgrade pip.
python3 -m pip install --user --upgrade pip
python3 -m pip install --user virtualenv

# Create a Python virtual environment
python3 -m venv ~/tflite

# Run this command whenever you open a new Terminal window/tab to activate the environment.
source ~/tflite/bin/activate

# Install Python dependencies
python3 -m pip install pip --upgrade
python3 -m pip install -r requirements.txt
