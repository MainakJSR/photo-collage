"""
Main script for photo processing pipeline
"""

import os
import cv2
import logging
from datetime import datetime
from pathlib import Path
from typing import List

import config
from face_detector import FaceDetector
from image_processor import ImageProcessor
from image_enhancer import ImageEnhancer
from collage_maker import CollageMaker


# Setup logging
def setup_logging():
    """Configure logging for the application"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format=log_format,
        handlers=[
            logging.FileHandler('photo_processing.log'),
            logging.StreamHandler()
        ]
    )


def get_image_files(directory: str) -> List[str]:
    """
    Get all image files from directory
    
    Args:
        directory: Path to directory containing images
        
    Returns:
        List of image file paths
    """
    image_files = []
    
    if not os.path.exists(directory):
        logging.error(f"Directory does not exist: {directory}")
        return image_files
    
    for filename in os.listdir(directory):
        if any(filename.endswith(ext) for ext in config.SUPPORTED_FORMATS):
            image_files.append(os.path.join(directory, filename))
    
    logging.info(f"Found {len(image_files)} images in {directory}")
    return sorted(image_files)


def process_single_image(image_path: str, face_detector: FaceDetector, 
                        image_processor: ImageProcessor, image_enhancer: ImageEnhancer,
                        output_dir: str) -> str:
    """
    Process a single image through the pipeline
    
    Args:
        image_path: Path to input image
        face_detector: FaceDetector instance
        image_processor: ImageProcessor instance
        image_enhancer: ImageEnhancer instance
        output_dir: Directory to save processed image
        
    Returns:
        Path to processed image, or None if processing failed
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Processing: {os.path.basename(image_path)}")
    
    try:
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            logger.error(f"Failed to load image: {image_path}")
            return None
        
        # Detect faces
        faces = face_detector.detect_faces(image)
        
        # Get bounding box
        bbox = face_detector.get_face_bounding_box(
            faces, 
            image.shape[:2], 
            padding=config.FACE_PADDING
        )
        
        # Process image (crop and resize)
        processed = image_processor.process_image(image, bbox)
        
        # Enhance image
        enhanced = image_enhancer.enhance(
            processed,
            apply_denoising=False,
            gamma=1.0
        )
        
        # Save processed image
        output_filename = os.path.basename(image_path)
        output_path = os.path.join(output_dir, output_filename)
        cv2.imwrite(output_path, enhanced)
        
        logger.info(f"Saved processed image: {output_filename}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error processing {image_path}: {e}", exc_info=True)
        return None


def main():
    """Main function to orchestrate the photo processing pipeline"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("=" * 60)
    logger.info("Starting Photo Processing Pipeline")
    logger.info("=" * 60)
    
    # Create directories if they don't exist
    os.makedirs(config.INPUT_DIR, exist_ok=True)
    os.makedirs(config.PROCESSED_DIR, exist_ok=True)
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    
    # Initialize components
    logger.info("Initializing components...")
    
    face_detector = FaceDetector(
        method=config.FACE_DETECTION_METHOD,
        min_face_size=config.MIN_FACE_SIZE
    )
    
    image_processor = ImageProcessor(
        crop_shape=config.CROP_SHAPE,
        aspect_ratio=config.ASPECT_RATIO,
        target_size=config.TARGET_SIZE
    )
    
    image_enhancer = ImageEnhancer(
        brightness_factor=config.BRIGHTNESS_FACTOR if config.ENHANCE_BRIGHTNESS else 1.0,
        contrast_factor=config.CONTRAST_FACTOR if config.ENHANCE_CONTRAST else 1.0,
        sharpness_factor=config.SHARPNESS_FACTOR if config.ENHANCE_SHARPNESS else 1.0,
        color_factor=config.COLOR_FACTOR if config.ENHANCE_COLOR else 1.0
    )
    
    collage_maker = CollageMaker(
        width=config.COLLAGE_WIDTH,
        columns=config.COLLAGE_COLUMNS,
        spacing=config.COLLAGE_SPACING,
        background_color=config.COLLAGE_BACKGROUND_COLOR
    )
    
    # Get input images
    logger.info(f"Scanning input directory: {config.INPUT_DIR}")
    image_files = get_image_files(config.INPUT_DIR)
    
    if not image_files:
        logger.warning("No images found in input directory!")
        logger.info("Please place images in the 'input' folder and run again.")
        return
    
    # Process all images
    logger.info(f"Processing {len(image_files)} images...")
    processed_images = []
    
    for idx, image_path in enumerate(image_files, 1):
        logger.info(f"\n[{idx}/{len(image_files)}] Processing image...")
        processed_path = process_single_image(
            image_path,
            face_detector,
            image_processor,
            image_enhancer,
            config.PROCESSED_DIR
        )
        
        if processed_path:
            processed_images.append(processed_path)
    
    logger.info(f"\nSuccessfully processed {len(processed_images)}/{len(image_files)} images")
    
    # Create collage
    if processed_images:
        logger.info("\nCreating collage...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        collage_path = os.path.join(config.OUTPUT_DIR, f"collage_{timestamp}.jpg")
        
        result = collage_maker.create_collage(processed_images, collage_path)
        
        if result:
            logger.info(f"Collage created successfully: {collage_path}")
        else:
            logger.error("Failed to create collage")
    else:
        logger.warning("No processed images available for collage creation")
    
    logger.info("\n" + "=" * 60)
    logger.info("Photo Processing Pipeline Complete!")
    logger.info("=" * 60)
    logger.info(f"Processed images: {config.PROCESSED_DIR}")
    logger.info(f"Final collage: {config.OUTPUT_DIR}")


if __name__ == "__main__":
    main()
