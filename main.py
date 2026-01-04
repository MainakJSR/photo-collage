"""
Main script for photo processing pipeline
"""

import os
import cv2
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Tuple
from PIL import Image
from PIL.ExifTags import TAGS

import config
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
    return image_files


def get_compression_settings(image_count: int) -> Tuple[int, int]:
    """
    Determine compression quality and max file size based on image count
    
    Args:
        image_count: Total number of images to process
        
    Returns:
        Tuple of (quality, max_size_kb)
        
    Raises:
        ValueError: If image count exceeds 100
    """
    if image_count > 100:
        raise ValueError(f"Too many images ({image_count})! Maximum supported is 100 images.")
    elif image_count > 70:
        return (50, 300)  # quality 50, max 300KB
    elif image_count > 50:
        return (60, 500)  # quality 60, max 500KB
    elif image_count > 20:
        return (70, 700)  # quality 70, max 700KB
    else:
        return (80, 1024)  # quality 80, max 1MB
    

def compress_image_to_target(image_path: str, target_size_kb: int, initial_quality: int) -> None:
    """
    Compress image to target file size
    
    Args:
        image_path: Path to image file
        target_size_kb: Target maximum file size in KB
        initial_quality: Initial JPEG quality to try
    """
    logger = logging.getLogger(__name__)
    
    # Load with PIL for better compression control
    img = Image.open(image_path)
    
    # Preserve EXIF data
    exif = img.info.get('exif', None)
    
    # Convert to RGB if necessary
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGB')
    
    quality = initial_quality
    
    # Try compression with decreasing quality until target size is met
    while quality > 10:
        if exif:
            img.save(image_path, 'JPEG', quality=quality, optimize=True, exif=exif)
        else:
            img.save(image_path, 'JPEG', quality=quality, optimize=True)
        
        file_size_kb = os.path.getsize(image_path) / 1024
        
        if file_size_kb <= target_size_kb:
            logger.debug(f"Compressed to {file_size_kb:.1f}KB at quality {quality}")
            break
        
        quality -= 5
    
    final_size_kb = os.path.getsize(image_path) / 1024
    if final_size_kb > target_size_kb:
        logger.warning(f"Could not compress below {target_size_kb}KB. Final size: {final_size_kb:.1f}KB")


def process_single_image(image_path: str, 
                        image_processor: ImageProcessor, image_enhancer: ImageEnhancer,
                        output_dir: str, quality: int, max_size_kb: int) -> str:
    """
    Process a single image through the pipeline
    
    Args:
        image_path: Path to input image
        image_processor: ImageProcessor instance
        image_enhancer: ImageEnhancer instance
        output_dir: Directory to save processed image
        quality: JPEG quality for compression
        max_size_kb: Maximum file size in KB
        
    Returns:
        Path to processed image, or None if processing failed
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Processing: {os.path.basename(image_path)}")
    
    try:
        # Try to read EXIF from original image
        original_exif = None
        try:
            original_img = Image.open(image_path)
            original_exif = original_img.info.get('exif', None)
        except:
            pass
        
        # Load image with OpenCV
        image = cv2.imread(image_path)
        if image is None:
            logger.error(f"Failed to load image: {image_path}")
            return None
        
        # Process image (resize only, no cropping)
        processed = image_processor.process_image(image)
        
        # Enhance image
        enhanced = image_enhancer.enhance(
            processed,
            apply_denoising=False,
            gamma=1.0
        )
        
        # Save processed image with initial quality
        output_filename = os.path.basename(image_path)
        # Ensure output is .jpg for compression
        if not output_filename.lower().endswith(('.jpg', '.jpeg')):
            output_filename = os.path.splitext(output_filename)[0] + '.jpg'
        output_path = os.path.join(output_dir, output_filename)
        
        # Save with OpenCV first
        cv2.imwrite(output_path, enhanced)
        
        # Re-open with PIL to add EXIF and compress
        img_pil = Image.open(output_path)
        if img_pil.mode in ('RGBA', 'LA', 'P'):
            img_pil = img_pil.convert('RGB')
        
        # Save with EXIF if available
        if original_exif:
            img_pil.save(output_path, 'JPEG', quality=quality, optimize=True, exif=original_exif)
        else:
            img_pil.save(output_path, 'JPEG', quality=quality, optimize=True)
        
        # Compress to target size
        compress_image_to_target(output_path, max_size_kb, quality)
        
        file_size_kb = os.path.getsize(output_path) / 1024
        logger.info(f"Saved processed image: {output_filename} ({file_size_kb:.1f}KB)")
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
    os.makedirs(config.OUTPUT_DIR, exist_ok=True)
    
    # Clear and recreate processed directory
    import shutil
    if os.path.exists(config.PROCESSED_DIR):
        logger.info(f"Clearing processed directory: {config.PROCESSED_DIR}")
        shutil.rmtree(config.PROCESSED_DIR)
    os.makedirs(config.PROCESSED_DIR, exist_ok=True)
    logger.info("Processed directory is ready")
    
    # Initialize components
    logger.info("Initializing components...")
    
    image_processor = ImageProcessor()
    
    image_enhancer = ImageEnhancer(
        brightness_factor=config.BRIGHTNESS_FACTOR if config.ENHANCE_BRIGHTNESS else 1.0,
        contrast_factor=config.CONTRAST_FACTOR if config.ENHANCE_CONTRAST else 1.0,
        sharpness_factor=config.SHARPNESS_FACTOR if config.ENHANCE_SHARPNESS else 1.0,
        color_factor=config.COLOR_FACTOR if config.ENHANCE_COLOR else 1.0
    )
    
    collage_maker = CollageMaker(
        width=config.COLLAGE_WIDTH,
        max_columns=config.COLLAGE_COLUMNS,
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
    
    # Determine compression settings based on image count
    try:
        quality, max_size_kb = get_compression_settings(len(image_files))
        logger.info(f"Image count: {len(image_files)}")
        logger.info(f"Compression settings: Quality={quality}, Max size={max_size_kb}KB per image")
    except ValueError as e:
        logger.error(str(e))
        logger.error("Please reduce the number of images to 100 or less.")
        return
    
    # Process all images
    logger.info(f"Processing {len(image_files)} images...")
    processed_images = []
    
    for idx, image_path in enumerate(image_files, 1):
        logger.info(f"\n[{idx}/{len(image_files)}] Processing image...")
        processed_path = process_single_image(
            image_path,
            image_processor,
            image_enhancer,
            config.PROCESSED_DIR,
            quality,
            max_size_kb
        )
        
        if processed_path:
            processed_images.append(processed_path)
    
    logger.info(f"\nSuccessfully processed {len(processed_images)}/{len(image_files)} images")
    
    # Create collage
    if processed_images:
        logger.info("\nCreating collage...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        collage_path = os.path.join(config.OUTPUT_DIR, f"collage_{timestamp}.jpg")
        
        result = collage_maker.create_collage(processed_images, collage_path, config.INPUT_DIR)
        
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
