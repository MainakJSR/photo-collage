"""
Image processing module for cropping and trimming based on face detection
"""

import cv2
import numpy as np
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class ImageProcessor:
    """
    Image processor for cropping images based on face detection
    """
    
    def __init__(self, crop_shape="rectangle", aspect_ratio=(4, 3), target_size=(800, 600)):
        """
        Initialize image processor
        
        Args:
            crop_shape: Shape of crop ("square" or "rectangle")
            aspect_ratio: Desired aspect ratio as (width, height) for rectangle
            target_size: Target size for output images (width, height)
        """
        self.crop_shape = crop_shape
        self.aspect_ratio = aspect_ratio
        self.target_size = target_size
        logger.info(f"Initialized ImageProcessor with shape={crop_shape}, aspect_ratio={aspect_ratio}")
    
    def crop_to_square(self, image: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
        """
        Crop image to square containing the bounding box
        
        Args:
            image: Input image as numpy array
            bbox: Bounding box as (x, y, width, height)
            
        Returns:
            Cropped square image
        """
        x, y, width, height = bbox
        img_h, img_w = image.shape[:2]
        
        # Calculate center of bounding box
        center_x = x + width // 2
        center_y = y + height // 2
        
        # Use the larger dimension as the square size
        size = max(width, height)
        
        # Calculate square boundaries
        half_size = size // 2
        x1 = max(0, center_x - half_size)
        y1 = max(0, center_y - half_size)
        x2 = min(img_w, center_x + half_size)
        y2 = min(img_h, center_y + half_size)
        
        # Adjust if we hit image boundaries
        if x2 - x1 < size:
            if x1 == 0:
                x2 = min(img_w, x1 + size)
            else:
                x1 = max(0, x2 - size)
        
        if y2 - y1 < size:
            if y1 == 0:
                y2 = min(img_h, y1 + size)
            else:
                y1 = max(0, y2 - size)
        
        cropped = image[y1:y2, x1:x2]
        logger.debug(f"Cropped to square: {cropped.shape}")
        return cropped
    
    def crop_to_rectangle(self, image: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
        """
        Crop image to rectangle with specified aspect ratio containing the bounding box
        
        Args:
            image: Input image as numpy array
            bbox: Bounding box as (x, y, width, height)
            
        Returns:
            Cropped rectangular image
        """
        x, y, width, height = bbox
        img_h, img_w = image.shape[:2]
        
        # Calculate center of bounding box
        center_x = x + width // 2
        center_y = y + height // 2
        
        # Calculate dimensions based on aspect ratio
        aspect_w, aspect_h = self.aspect_ratio
        
        # Start with bbox dimensions and expand to match aspect ratio
        if width / height > aspect_w / aspect_h:
            # Width is limiting factor
            crop_width = width
            crop_height = int(width * aspect_h / aspect_w)
        else:
            # Height is limiting factor
            crop_height = height
            crop_width = int(height * aspect_w / aspect_h)
        
        # Calculate crop boundaries
        half_w = crop_width // 2
        half_h = crop_height // 2
        
        x1 = max(0, center_x - half_w)
        y1 = max(0, center_y - half_h)
        x2 = min(img_w, center_x + half_w)
        y2 = min(img_h, center_y + half_h)
        
        # Adjust if we hit image boundaries
        if x2 - x1 < crop_width:
            if x1 == 0:
                x2 = min(img_w, x1 + crop_width)
            else:
                x1 = max(0, x2 - crop_width)
        
        if y2 - y1 < crop_height:
            if y1 == 0:
                y2 = min(img_h, y1 + crop_height)
            else:
                y1 = max(0, y2 - crop_height)
        
        cropped = image[y1:y2, x1:x2]
        logger.debug(f"Cropped to rectangle: {cropped.shape}")
        return cropped
    
    def crop_image(self, image: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
        """
        Crop image based on configured shape
        
        Args:
            image: Input image as numpy array
            bbox: Bounding box as (x, y, width, height)
            
        Returns:
            Cropped image
        """
        if self.crop_shape == "square":
            return self.crop_to_square(image, bbox)
        elif self.crop_shape == "rectangle":
            return self.crop_to_rectangle(image, bbox)
        else:
            raise ValueError(f"Unknown crop shape: {self.crop_shape}")
    
    def resize_image(self, image: np.ndarray) -> np.ndarray:
        """
        Resize image to target size while maintaining aspect ratio
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Resized image
        """
        h, w = image.shape[:2]
        target_w, target_h = self.target_size
        
        # Calculate scaling factor to fit within target size
        scale = min(target_w / w, target_h / h)
        
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        logger.debug(f"Resized from {(w, h)} to {(new_w, new_h)}")
        return resized
    
    def process_image(self, image: np.ndarray, bbox: Tuple[int, int, int, int]) -> np.ndarray:
        """
        Process image: crop and resize
        
        Args:
            image: Input image as numpy array
            bbox: Bounding box for cropping as (x, y, width, height)
            
        Returns:
            Processed image
        """
        # Crop image
        cropped = self.crop_image(image, bbox)
        
        # Resize to target size
        resized = self.resize_image(cropped)
        
        return resized
