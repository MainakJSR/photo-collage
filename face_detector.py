"""
Face detection module using OpenCV and face_recognition library
"""

import cv2
import face_recognition
import numpy as np
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)


class FaceDetector:
    """
    Face detector class supporting multiple detection methods
    """
    
    def __init__(self, method="opencv", min_face_size=(30, 30)):
        """
        Initialize face detector
        
        Args:
            method: Detection method ("opencv" or "face_recognition")
            min_face_size: Minimum size of face to detect (width, height)
        """
        self.method = method
        self.min_face_size = min_face_size
        
        if method == "opencv":
            # Load OpenCV's pre-trained Haar Cascade
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            logger.info("Initialized OpenCV face detector")
        elif method == "face_recognition":
            logger.info("Initialized face_recognition detector")
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def detect_faces_opencv(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces using OpenCV Haar Cascade
        
        Args:
            image: Input image as numpy array (BGR format)
            
        Returns:
            List of face rectangles as (x, y, width, height)
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=self.min_face_size,
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # Convert to list of tuples
        return [(int(x), int(y), int(w), int(h)) for x, y, w, h in faces]
    
    def detect_faces_face_recognition(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces using face_recognition library (HOG-based)
        
        Args:
            image: Input image as numpy array (BGR format)
            
        Returns:
            List of face rectangles as (x, y, width, height)
        """
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Detect faces
        face_locations = face_recognition.face_locations(rgb_image, model="hog")
        
        # Convert from (top, right, bottom, left) to (x, y, width, height)
        faces = []
        for top, right, bottom, left in face_locations:
            x = left
            y = top
            width = right - left
            height = bottom - top
            
            # Filter by minimum size
            if width >= self.min_face_size[0] and height >= self.min_face_size[1]:
                faces.append((x, y, width, height))
        
        return faces
    
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """
        Detect faces in image using configured method
        
        Args:
            image: Input image as numpy array (BGR format)
            
        Returns:
            List of face rectangles as (x, y, width, height)
        """
        if self.method == "opencv":
            faces = self.detect_faces_opencv(image)
        elif self.method == "face_recognition":
            faces = self.detect_faces_face_recognition(image)
        else:
            raise ValueError(f"Unknown method: {self.method}")
        
        logger.info(f"Detected {len(faces)} face(s)")
        return faces
    
    def get_face_bounding_box(self, faces: List[Tuple[int, int, int, int]], 
                              image_shape: Tuple[int, int],
                              padding: int = 50) -> Tuple[int, int, int, int]:
        """
        Get bounding box that encompasses all detected faces with padding
        
        Args:
            faces: List of face rectangles as (x, y, width, height)
            image_shape: Shape of image as (height, width)
            padding: Padding around faces in pixels
            
        Returns:
            Bounding box as (x, y, width, height)
        """
        if not faces:
            # No faces detected, return entire image
            return (0, 0, image_shape[1], image_shape[0])
        
        # Find min/max coordinates
        min_x = min(x for x, y, w, h in faces)
        min_y = min(y for x, y, w, h in faces)
        max_x = max(x + w for x, y, w, h in faces)
        max_y = max(y + h for x, y, w, h in faces)
        
        # Add padding
        min_x = max(0, min_x - padding)
        min_y = max(0, min_y - padding)
        max_x = min(image_shape[1], max_x + padding)
        max_y = min(image_shape[0], max_y + padding)
        
        width = max_x - min_x
        height = max_y - min_y
        
        return (min_x, min_y, width, height)
