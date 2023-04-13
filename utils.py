"""Utility functions to display the pose detection results."""

import cv2
import numpy as np
from tflite_support.task import processor
import RPi.GPIO as GPIO

_MARGIN = 10  # pixels
_ROW_SIZE = 10  # pixels
_FONT_SIZE = 1
_FONT_THICKNESS = 1
_TEXT_COLOR = (48, 219, 117)  # green-ish color
_TARGET_COLOR = (0, 225, 255) # yellow
_OBSTACLE_COLOR = (0, 0, 255) # red


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

  objectDetected = None;
  
  # Defining the dimensions of the hotzone - 640x480
  dx = 64 
  x = 320 - dx
  y = 0
  width, height = dx*2, 480

  # Draw the hotzone rectangle in yellow
  cv2.rectangle(image, (x, y), (x + width, y + height), _TARGET_COLOR, 3)

  for detection in detection_result.detections:

    # If the detection is not a human, skip it
    if (detection.categories[0].category_name != 'person'):
        continue
    

    # X and Y coordinates of the bounding box
    bbox = detection.bounding_box

    # Parameters to determine if the rover should stop
    WITHIN_X = bbox.origin_x < x + width and bbox.origin_x + bbox.width > x
    WITHIN_Y = bbox.origin_y < y + height and bbox.origin_y + bbox.height > y
    IS_PERSON = detection.categories[0].category_name == 'person'
    IS_HIGH_CONFIDENCE = detection.categories[0].score > 0.35
    IS_LARGE_AREA = bbox.width * bbox.height > 10000

    # If the detection meets all the above parameters, set the objectDetected flag to true
    if (WITHIN_X and WITHIN_Y and IS_PERSON and IS_HIGH_CONFIDENCE and IS_LARGE_AREA):
      
      objectDetected = True

      # Draw a red rectangle around detected people
      start_point = bbox.origin_x, bbox.origin_y
      end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
      cv2.rectangle(image, start_point, end_point, _OBSTACLE_COLOR, 3)
      # Draw some text too
      category = detection.categories[0]
      category_name = category.category_name
      probability = round(category.score, 2)
      result_text = category_name + ' (' + str(probability) + ')'
      text_location = (_MARGIN + bbox.origin_x,
                      _MARGIN + _ROW_SIZE + bbox.origin_y)
      cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                  _FONT_SIZE, _OBSTACLE_COLOR, _FONT_THICKNESS)



    else:
      
      # People who aren't in the hotzone get green rectangles
      start_point = bbox.origin_x, bbox.origin_y
      end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
      cv2.rectangle(image, start_point, end_point, _TEXT_COLOR, 3)

      # They also get text and scores
      category = detection.categories[0]
      category_name = category.category_name
      probability = round(category.score, 2)
      result_text = category_name + ' (' + str(probability) + ')'
      text_location = (_MARGIN + bbox.origin_x,
                      _MARGIN + _ROW_SIZE + bbox.origin_y)
      cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                  _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS)


    # If there are no values in the detection_result, then there is no obstacle
    if (len(detection_result.detections) == 0):
      objectDetected = False
      

  if (objectDetected == True):
    # Check the flag and set the GPIO pin to high if there is an obstacle
    # GPIO 17 is a signal pin that connects to the relay switch
    GPIO.output(17,GPIO.HIGH)

  else:
    # If the flag is false, then there is no obstacle
    # If there is no obstacle, then the GPIO pin is set to low
    GPIO.output(17,GPIO.LOW)

# Return the image with the bounding boxes
  return image
