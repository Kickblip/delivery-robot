# get most recent version of code
git pull origin main

# activate virtual environment
source ~/tflite/bin/activate

# ensure connected display is set as default
export DISPLAY=:0

# run the model
python3 detect.py