"""
Image processing module - keeps images at original size
"""

import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)


class ImageProcessor:
    """
    Image processor that keeps images at their original size
    """
    
    def __init__(self):
        """
        Initialize image processor
        """
        logger.info("Initialized ImageProcessor - keeping original image sizes")
    
    def process_image(self, image: np.ndarray) -> np.ndarray:
        """
        Process image: return as-is (no resizing or cropping)
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Original image unchanged
        """
        h, w = image.shape[:2]
        logger.debug(f"Processing image at original size: {w}x{h}")
        return image
