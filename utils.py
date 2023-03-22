# Copyright 2021 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utility functions to display the pose detection results."""

import cv2
import numpy as np
from tflite_support.task import processor
import handler
import RPi.GPIO as GPIO

_MARGIN = 10  # pixels
_ROW_SIZE = 10  # pixels
_FONT_SIZE = 1
_FONT_THICKNESS = 1
_TEXT_COLOR = (48, 219, 117)  # green-ish color
_TARGET_COLOR = (0, 225, 255) # yellow
_OBSTACLE_COLOR = (0, 0, 255) # red

objectDetected = False

def visualize(
    image: np.ndarray,
    detection_result: processor.DetectionResult,
) -> np.ndarray:
  """Draws bounding boxes on the input image and return it.

  Args:
    image: The input RGB image.
    detection_result: The list of all "Detection" entities to be visualize.

  Returns:
    Image with bounding boxes.
  """


  # Define the rectangle parameters - 640x480
  x, y = 224, 0
  width, height = 192, 480

  # Draw the rectangle
  cv2.rectangle(image, (x, y), (x + width, y + height), _TARGET_COLOR, 3)

  for detection in detection_result.detections:

    bbox = detection.bounding_box

    # if the detected object is within the rectangle, draw a red rectangle and handle the detection
    WITHIN_X = bbox.origin_x < x + width and bbox.origin_x + bbox.width > x
    WITHIN_Y = bbox.origin_y < y + height and bbox.origin_y + bbox.height > y
    IS_PERSON = detection.categories[0].category_name == 'person'
    IS_HIGH_CONFIDENCE = detection.categories[0].score > 0.35
    IS_LARGE_AREA = bbox.width * bbox.height > 10000

    if (WITHIN_X and WITHIN_Y and IS_PERSON and IS_HIGH_CONFIDENCE and IS_LARGE_AREA):
      
      objectDetected = True

      # draw a red rectangle around the detected object
      start_point = bbox.origin_x, bbox.origin_y
      end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
      cv2.rectangle(image, start_point, end_point, _OBSTACLE_COLOR, 3)
      # draw text
      category = detection.categories[0]
      category_name = category.category_name
      probability = round(category.score, 2)
      result_text = category_name + ' (' + str(probability) + ')'
      text_location = (_MARGIN + bbox.origin_x,
                      _MARGIN + _ROW_SIZE + bbox.origin_y)
      cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                  _FONT_SIZE, _OBSTACLE_COLOR, _FONT_THICKNESS)
      





    else:
      objectDetected = False

      # Draw bounding_box
      start_point = bbox.origin_x, bbox.origin_y
      end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
      cv2.rectangle(image, start_point, end_point, _TEXT_COLOR, 3)

      # Draw label and score
      category = detection.categories[0]
      category_name = category.category_name
      probability = round(category.score, 2)
      result_text = category_name + ' (' + str(probability) + ')'
      text_location = (_MARGIN + bbox.origin_x,
                      _MARGIN + _ROW_SIZE + bbox.origin_y)
      cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                  _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS)
      
    # Handle the detection
    # handler.handleObstacle(objectDetected)


  if (objectDetected == True):
    print("obstacle detected")
    GPIO.output(17,GPIO.HIGH)
  else:
    print("no obstacle detected")
    GPIO.output(17,GPIO.LOW)

  return image
