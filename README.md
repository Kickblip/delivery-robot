## Setting up the pi

#### Update packages on your Raspberry Pi OS.
```sudo apt-get update```

#### Check your Python version. You should have Python 3.7 or later.
```python3 --version```

#### Install virtualenv and upgrade pip.
```python3 -m pip install --user --upgrade pip```

```python3 -m pip install --user virtualenv```

#### Create a Python virtual environment for the TFLite models (optional but strongly recommended)
```python3 -m venv ~/tflite```

#### Run this command whenever you open a new Terminal window/tab to activate the environment.
```source ~/tflite/bin/activate```

#### Clone the repository with the TFLite Raspberry Pi models and pathing code (test data not included).
```git clone https://github.com/Kickblip/delivery-robot```

```cd delivery-robot```

#### Note: to pull changes from github repo use

```git pull origin main``` in ```~/delivery-robot```

#### Install required dependencies
```sh setup.sh```

#### Run the object detection model

```python detect.py```

**IMPORTANT**: If you SSH to the Pi, make sure that:
 1. There is a display connected to the Pi.
 2. Run `export DISPLAY=:0` before proceed to make the object_detection window appear on the display.

## Common issues

```ImportError: libcblas.so.3: cannot open shared object file: No such file or directory```

you can fix this by installing an OpenCV dependency that is missing on your Raspberry Pi.

```sudo apt-get install libatlas-base-dev```

## Speed up model inference (optional)

If you want to significantly speed up the inference time, you can attach an
[Coral USB Accelerator](https://coral.withgoogle.com/products/accelerator)—a USB
accessory that adds the
[Edge TPU ML accelerator](https://coral.withgoogle.com/docs/edgetpu/faq/) to any
Linux-based system.

If you have a Coral USB Accelerator, you can run the model with it enabled:

1.  First, be sure you have completed the
    [USB Accelerator setup instructions](https://coral.withgoogle.com/docs/accelerator/get-started/).

2.  Run the object detection script using the EdgeTPU TFLite model and enable
    the EdgeTPU option.

```
python3 detect.py \
  --enableEdgeTPU
  --model efficientdet_lite0_edgetpu.tflite
```

You should see significantly faster inference speeds.

For more information about creating and running TensorFlow Lite models with
Coral devices, read
[TensorFlow models on the Edge TPU](https://coral.withgoogle.com/docs/edgetpu/models-intro/).
