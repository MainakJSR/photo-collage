"""
Configuration file for the photo processing project
"""

import os

# Directory paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "input")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Image processing settings
CROP_SHAPE = "rectangle"  # Options: "square", "rectangle"
ASPECT_RATIO = (4, 3)  # For rectangle mode (width, height)
TARGET_SIZE = (800, 600)  # Target size for processed images

# Enhancement settings
ENHANCE_BRIGHTNESS = False  # Set to False to disable enhancement
BRIGHTNESS_FACTOR = 1.1  # 1.0 = no change, >1.0 = brighter
ENHANCE_CONTRAST = False  # Set to False to disable enhancement
CONTRAST_FACTOR = 1.2
ENHANCE_SHARPNESS = False  # Set to False to disable enhancement
SHARPNESS_FACTOR = 1.3
ENHANCE_COLOR = False  # Set to False to disable enhancement
COLOR_FACTOR = 1.1

# Collage settings
COLLAGE_WIDTH = 6000  # Width of final collage in pixels (increased to fit more images)
COLLAGE_COLUMNS = 5  # Maximum number of images per row (1-5)
COLLAGE_SPACING = 20  # Spacing between images in pixels
COLLAGE_BACKGROUND_COLOR = (255, 255, 255)  # White background

# Supported image formats
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']

# Logging
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR
