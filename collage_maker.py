"""
Collage maker module for creating photo collages with flexible layout
"""

from PIL import Image
from PIL.ExifTags import TAGS
import math
import logging
import os
from datetime import datetime
from typing import List, Tuple

logger = logging.getLogger(__name__)


class CollageMaker:
    """
    Creates collages from processed images with flexible layout (1-5 images per row)
    Images are NOT resized - they keep their original dimensions
    """
    
    def __init__(self, width=6000, max_columns=5, spacing=20, background_color=(255, 255, 255)):
        """
        Initialize collage maker
        
        Args:
            width: Target width of final collage in pixels (used as reference only)
            max_columns: Maximum number of images per row (1-5)
            spacing: Spacing between images in pixels
            background_color: Background color as RGB tuple
        """
        self.width = width
        self.max_columns = max_columns
        self.spacing = spacing
        self.background_color = background_color
        logger.info(f"Initialized CollageMaker: width={width}, max_columns={max_columns}")
    
    def arrange_images_in_rows(self, images: List[Image.Image]) -> List[List[Image.Image]]:
        """
        Arrange images into rows with 1-5 images per row based on dimensions
        
        Args:
            images: List of PIL Images at original size
            
        Returns:
            List of rows, where each row is a list of images
        """
        rows = []
        i = 0
        
        while i < len(images):
            remaining = len(images) - i
            
            if remaining == 1:
                # Single image gets its own row
                row_images = [images[i]]
                i += 1
            elif remaining == 2:
                # Two images per row
                row_images = images[i:i+2]
                i += 2
            else:
                # 3 or more images remaining - try to fit optimally
                # Check widths to decide how many fit well
                row_images = []
                accumulated_width = 0
                
                for j in range(min(self.max_columns, remaining)):
                    img = images[i + j]
                    accumulated_width += img.width + self.spacing
                    
                    # If adding this image would make row too wide, stop
                    if accumulated_width > self.width * 1.3 and j > 0:
                        break
                    row_images.append(img)
                
                # Ensure at least 1 image per row
                if not row_images:
                    row_images = [images[i]]
                
                i += len(row_images)
            
            rows.append(row_images)
        
        logger.info(f"Arranged {len(images)} images into {len(rows)} rows")
        return rows
    
    def get_image_date(self, image_path: str, input_dir: str = None) -> datetime:
        """
        Get the creation date from image EXIF data
        
        Args:
            image_path: Path to image file (processed)
            input_dir: Path to input directory to find original file with EXIF
            
        Returns:
            datetime object representing image creation date
        """
        # Try to find the original input file
        original_path = image_path
        if input_dir:
            filename = os.path.basename(image_path)
            potential_input = os.path.join(input_dir, filename)
            if os.path.exists(potential_input):
                original_path = potential_input
        
        try:
            img = Image.open(original_path)
            exif_data = img._getexif()
            
            if exif_data:
                # Try DateTimeOriginal first
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == 'DateTimeOriginal':
                        try:
                            dt = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                            if dt.year >= 1970:
                                logger.debug(f"{os.path.basename(image_path)}: Using DateTimeOriginal {value}")
                                return dt
                        except:
                            pass
                
                # Fallback to DateTime or DateTimeDigitized
                datetime_value = None
                digitized_value = None
                
                for tag_id, value in exif_data.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag == 'DateTime':
                        datetime_value = value
                    elif tag == 'DateTimeDigitized':
                        digitized_value = value
                
                if datetime_value:
                    try:
                        dt = datetime.strptime(datetime_value, '%Y:%m:%d %H:%M:%S')
                        if dt.year >= 1970:
                            logger.debug(f"{os.path.basename(image_path)}: Using DateTime {datetime_value}")
                            return dt
                    except:
                        pass
                
                if digitized_value:
                    try:
                        dt = datetime.strptime(digitized_value, '%Y:%m:%d %H:%M:%S')
                        if dt.year >= 1970:
                            logger.debug(f"{os.path.basename(image_path)}: Using DateTimeDigitized {digitized_value}")
                            return dt
                    except:
                        pass
        except Exception as e:
            logger.debug(f"Could not read EXIF from {original_path}: {e}")
        
        # No valid EXIF date found - ask user for input
        logger.warning(f"No EXIF date found for {os.path.basename(image_path)}")
        
        while True:
            try:
                user_input = input(f"Enter date for '{os.path.basename(image_path)}' (DD-MM-YYYY or press Enter to use file date): ").strip()
                
                if not user_input:
                    dt = datetime.fromtimestamp(os.path.getmtime(image_path))
                    logger.info(f"{os.path.basename(image_path)}: Using file date {dt.strftime('%d-%m-%Y')}")
                    return dt
                
                dt = datetime.strptime(user_input, '%d-%m-%Y')
                logger.info(f"{os.path.basename(image_path)}: Using user-provided date {user_input}")
                return dt
            except ValueError:
                print("Invalid format. Please use DD-MM-YYYY format (e.g., 15-08-2021)")
                continue
    
    def create_collage(self, image_paths: List[str], output_path: str, input_dir: str = None) -> str:
        """
        Create collage from list of image paths WITHOUT resizing images
        
        Args:
            image_paths: List of paths to processed images
            output_path: Path where collage will be saved
            input_dir: Path to input directory with original files (for EXIF data)
            
        Returns:
            Path to saved collage
        """
        if not image_paths:
            logger.warning("No images provided for collage")
            return None
        
        # Sort image paths by EXIF creation date (oldest first)
        image_paths_sorted = sorted(image_paths, key=lambda x: self.get_image_date(x, input_dir))
        logger.info(f"Sorted {len(image_paths_sorted)} images by EXIF date")
        
        # Rename files sequentially
        temp_paths = []
        directory = os.path.dirname(image_paths_sorted[0]) if image_paths_sorted else None
        
        if directory:
            for idx, path in enumerate(image_paths_sorted):
                temp_filename = f"temp_{idx}_{os.path.basename(path)}"
                temp_path = os.path.join(directory, temp_filename)
                try:
                    os.rename(path, temp_path)
                    temp_paths.append(temp_path)
                except Exception as e:
                    logger.error(f"Failed to rename {path} to temp: {e}")
                    temp_paths.append(path)
        
        # Rename from temp to final sequential names
        final_paths = []
        for idx, temp_path in enumerate(temp_paths, 1):
            extension = os.path.splitext(temp_path)[1]
            new_filename = f"{idx}{extension}"
            new_path = os.path.join(directory, new_filename)
            
            try:
                if os.path.exists(new_path):
                    os.remove(new_path)
                
                os.rename(temp_path, new_path)
                final_paths.append(new_path)
            except Exception as e:
                logger.error(f"Failed to rename {temp_path}: {e}")
                final_paths.append(temp_path)
        
        image_paths_sorted = final_paths
        logger.info(f"Renamed {len(image_paths_sorted)} files sequentially")
        
        # Load images at original size
        images = []
        for path in image_paths_sorted:
            try:
                img = Image.open(path)
                images.append(img)
            except Exception as e:
                logger.error(f"Failed to load image {path}: {e}")
        
        if not images:
            logger.error("No valid images loaded")
            return None
        
        logger.info(f"Loaded {len(images)} images for collage")
        
        # Arrange images into rows
        rows = self.arrange_images_in_rows(images)
        
        # Create collage rows WITHOUT resizing - use original image sizes
        collage_rows = []
        max_row_width = 0
        
        for row_images in rows:
            # Calculate row dimensions using original image heights
            row_height = max(img.height for img in row_images)
            
            # Calculate row width
            row_width = sum(img.width for img in row_images) + (len(row_images) + 1) * self.spacing
            row_img = Image.new('RGB', (row_width, row_height), self.background_color)
            
            # Paste images at original size
            x_offset = self.spacing
            for img in row_images:
                # Center vertically if image is shorter than row height
                y_offset = (row_height - img.height) // 2
                row_img.paste(img, (x_offset, y_offset))
                x_offset += img.width + self.spacing
            
            collage_rows.append(row_img)
            max_row_width = max(max_row_width, row_width)
        
        # Calculate total collage dimensions
        collage_width = max_row_width
        collage_height = sum(row.height for row in collage_rows) + (len(collage_rows) + 1) * self.spacing
        
        # Create final collage
        collage = Image.new('RGB', (collage_width, collage_height), self.background_color)
        
        # Paste rows into collage
        y_offset = self.spacing
        for row_img in collage_rows:
            # Center the row horizontally if it's narrower than the collage
            x_offset = (collage_width - row_img.width) // 2
            collage.paste(row_img, (x_offset, y_offset))
            y_offset += row_img.height + self.spacing
        
        # Save collage
        collage.save(output_path, quality=95)
        logger.info(f"Collage saved to {output_path} ({collage_width}x{collage_height})")
        logger.info(f"Images kept at original size - NO resizing applied")
        
        return output_path
