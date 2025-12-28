"""
Image enhancement module using PIL and OpenCV
"""

from PIL import Image, ImageEnhance
import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)


class ImageEnhancer:
    """
    Image enhancer for improving photo quality
    """
    
    def __init__(self, brightness_factor=1.0, contrast_factor=1.0, 
                 sharpness_factor=1.0, color_factor=1.0):
        """
        Initialize image enhancer
        
        Args:
            brightness_factor: Brightness adjustment (1.0 = no change)
            contrast_factor: Contrast adjustment (1.0 = no change)
            sharpness_factor: Sharpness adjustment (1.0 = no change)
            color_factor: Color saturation adjustment (1.0 = no change)
        """
        self.brightness_factor = brightness_factor
        self.contrast_factor = contrast_factor
        self.sharpness_factor = sharpness_factor
        self.color_factor = color_factor
        logger.info("Initialized ImageEnhancer")
    
    def enhance_with_pil(self, image_array: np.ndarray) -> np.ndarray:
        """
        Enhance image using PIL ImageEnhance
        
        Args:
            image_array: Input image as numpy array (BGR format)
            
        Returns:
            Enhanced image as numpy array (BGR format)
        """
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(rgb_image)
        
        # Apply brightness enhancement
        if self.brightness_factor != 1.0:
            enhancer = ImageEnhance.Brightness(pil_image)
            pil_image = enhancer.enhance(self.brightness_factor)
            logger.debug(f"Applied brightness factor: {self.brightness_factor}")
        
        # Apply contrast enhancement
        if self.contrast_factor != 1.0:
            enhancer = ImageEnhance.Contrast(pil_image)
            pil_image = enhancer.enhance(self.contrast_factor)
            logger.debug(f"Applied contrast factor: {self.contrast_factor}")
        
        # Apply sharpness enhancement
        if self.sharpness_factor != 1.0:
            enhancer = ImageEnhance.Sharpness(pil_image)
            pil_image = enhancer.enhance(self.sharpness_factor)
            logger.debug(f"Applied sharpness factor: {self.sharpness_factor}")
        
        # Apply color saturation enhancement
        if self.color_factor != 1.0:
            enhancer = ImageEnhance.Color(pil_image)
            pil_image = enhancer.enhance(self.color_factor)
            logger.debug(f"Applied color factor: {self.color_factor}")
        
        # Convert back to numpy array (RGB)
        enhanced_rgb = np.array(pil_image)
        
        # Convert RGB back to BGR for OpenCV
        enhanced_bgr = cv2.cvtColor(enhanced_rgb, cv2.COLOR_RGB2BGR)
        
        return enhanced_bgr
    
    def denoise(self, image: np.ndarray) -> np.ndarray:
        """
        Apply denoising to image using OpenCV
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Denoised image
        """
        # Use Non-local Means Denoising
        denoised = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
        logger.debug("Applied denoising")
        return denoised
    
    def adjust_gamma(self, image: np.ndarray, gamma=1.0) -> np.ndarray:
        """
        Adjust gamma (brightness curve) of image
        
        Args:
            image: Input image as numpy array
            gamma: Gamma value (< 1.0 = brighter, > 1.0 = darker)
            
        Returns:
            Gamma-adjusted image
        """
        if gamma == 1.0:
            return image
        
        # Build lookup table
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255
                         for i in np.arange(0, 256)]).astype("uint8")
        
        # Apply gamma correction
        adjusted = cv2.LUT(image, table)
        logger.debug(f"Applied gamma adjustment: {gamma}")
        return adjusted
    
    def enhance(self, image: np.ndarray, apply_denoising=False, gamma=1.0) -> np.ndarray:
        """
        Apply all enhancements to image
        
        Args:
            image: Input image as numpy array (BGR format)
            apply_denoising: Whether to apply denoising
            gamma: Gamma adjustment value
            
        Returns:
            Enhanced image as numpy array (BGR format)
        """
        enhanced = image.copy()
        
        # Apply PIL-based enhancements
        enhanced = self.enhance_with_pil(enhanced)
        
        # Apply optional denoising
        if apply_denoising:
            enhanced = self.denoise(enhanced)
        
        # Apply gamma adjustment
        if gamma != 1.0:
            enhanced = self.adjust_gamma(enhanced, gamma)
        
        logger.info("Image enhancement complete")
        return enhanced
