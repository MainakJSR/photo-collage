"""
Configuration file for the photo processing project
"""

import os

# Directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Face detection settings
FACE_DETECTION_METHOD = "opencv"  # Options: "opencv", "face_recognition"
MIN_FACE_SIZE = (30, 30)  # Minimum face size to detect
FACE_PADDING = 50  # Pixels to add around detected face

# Image processing settings
CROP_SHAPE = "rectangle"  # Options: "square", "rectangle"
ASPECT_RATIO = (4, 3)  # For rectangle mode (width, height)
TARGET_SIZE = (800, 600)  # Target size for processed images

# Enhancement settings
ENHANCE_BRIGHTNESS = True
BRIGHTNESS_FACTOR = 1.1  # 1.0 = no change, >1.0 = brighter
ENHANCE_CONTRAST = True
CONTRAST_FACTOR = 1.2
ENHANCE_SHARPNESS = True
SHARPNESS_FACTOR = 1.3
ENHANCE_COLOR = True
COLOR_FACTOR = 1.1

# Collage settings
COLLAGE_WIDTH = 3000  # Width of final collage in pixels
COLLAGE_COLUMNS = 4  # Number of columns in collage
COLLAGE_SPACING = 10  # Spacing between images in pixels
COLLAGE_BACKGROUND_COLOR = (255, 255, 255)  # White background

# Supported image formats
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']

# Logging
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR
