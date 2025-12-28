"""
Collage maker module for creating photo collages
"""

from PIL import Image
import math
import logging
from typing import List, Tuple

logger = logging.getLogger(__name__)


class CollageMaker:
    """
    Creates collages from processed images
    """
    
    def __init__(self, width=3000, columns=4, spacing=10, background_color=(255, 255, 255)):
        """
        Initialize collage maker
        
        Args:
            width: Width of final collage in pixels
            columns: Number of columns in the collage grid
            spacing: Spacing between images in pixels
            background_color: Background color as RGB tuple
        """
        self.width = width
        self.columns = columns
        self.spacing = spacing
        self.background_color = background_color
        logger.info(f"Initialized CollageMaker: width={width}, columns={columns}")
    
    def calculate_layout(self, num_images: int) -> Tuple[int, int]:
        """
        Calculate grid layout (rows, columns)
        
        Args:
            num_images: Number of images to arrange
            
        Returns:
            Tuple of (rows, columns)
        """
        rows = math.ceil(num_images / self.columns)
        return (rows, self.columns)
    
    def resize_images_uniform(self, images: List[Image.Image]) -> List[Image.Image]:
        """
        Resize all images to uniform size based on collage layout
        
        Args:
            images: List of PIL Images
            
        Returns:
            List of resized PIL Images
        """
        if not images:
            return []
        
        # Calculate cell size based on collage width and spacing
        cell_width = (self.width - (self.columns + 1) * self.spacing) // self.columns
        
        # Find the average aspect ratio
        aspect_ratios = [img.width / img.height for img in images]
        avg_aspect_ratio = sum(aspect_ratios) / len(aspect_ratios)
        
        # Calculate cell height based on average aspect ratio
        cell_height = int(cell_width / avg_aspect_ratio)
        
        # Resize all images to cell size
        resized_images = []
        for img in images:
            # Resize maintaining aspect ratio, then crop/pad to fit cell
            img_aspect = img.width / img.height
            
            if img_aspect > avg_aspect_ratio:
                # Image is wider, fit by height
                new_height = cell_height
                new_width = int(cell_height * img_aspect)
            else:
                # Image is taller, fit by width
                new_width = cell_width
                new_height = int(cell_width / img_aspect)
            
            resized = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Crop to cell size
            left = (new_width - cell_width) // 2
            top = (new_height - cell_height) // 2
            right = left + cell_width
            bottom = top + cell_height
            
            cropped = resized.crop((left, top, right, bottom))
            resized_images.append(cropped)
        
        logger.info(f"Resized {len(images)} images to {cell_width}x{cell_height}")
        return resized_images
    
    def create_collage(self, image_paths: List[str], output_path: str) -> str:
        """
        Create collage from list of image paths
        
        Args:
            image_paths: List of paths to images
            output_path: Path where collage will be saved
            
        Returns:
            Path to saved collage
        """
        if not image_paths:
            logger.warning("No images provided for collage")
            return None
        
        # Load images
        images = []
        for path in image_paths:
            try:
                img = Image.open(path)
                images.append(img)
            except Exception as e:
                logger.error(f"Failed to load image {path}: {e}")
        
        if not images:
            logger.error("No valid images loaded")
            return None
        
        logger.info(f"Loaded {len(images)} images for collage")
        
        # Resize images uniformly
        resized_images = self.resize_images_uniform(images)
        
        # Calculate layout
        rows, cols = self.calculate_layout(len(resized_images))
        
        # Calculate collage dimensions
        cell_width = resized_images[0].width
        cell_height = resized_images[0].height
        
        collage_width = cols * cell_width + (cols + 1) * self.spacing
        collage_height = rows * cell_height + (rows + 1) * self.spacing
        
        # Create blank collage
        collage = Image.new('RGB', (collage_width, collage_height), self.background_color)
        
        # Place images in grid
        for idx, img in enumerate(resized_images):
            row = idx // cols
            col = idx % cols
            
            x = col * cell_width + (col + 1) * self.spacing
            y = row * cell_height + (row + 1) * self.spacing
            
            collage.paste(img, (x, y))
        
        # Save collage
        collage.save(output_path, quality=95)
        logger.info(f"Collage saved to {output_path} ({collage_width}x{collage_height})")
        
        return output_path
    
    def create_collage_adaptive(self, image_paths: List[str], output_path: str) -> str:
        """
        Create collage with adaptive layout that maintains original aspect ratios
        
        Args:
            image_paths: List of paths to images
            output_path: Path where collage will be saved
            
        Returns:
            Path to saved collage
        """
        if not image_paths:
            logger.warning("No images provided for collage")
            return None
        
        # Load images
        images = []
        for path in image_paths:
            try:
                img = Image.open(path)
                images.append(img)
            except Exception as e:
                logger.error(f"Failed to load image {path}: {e}")
        
        if not images:
            logger.error("No valid images loaded")
            return None
        
        logger.info(f"Loaded {len(images)} images for adaptive collage")
        
        # Calculate target height for each row
        rows = math.ceil(len(images) / self.columns)
        images_per_row = []
        
        for i in range(rows):
            start_idx = i * self.columns
            end_idx = min((i + 1) * self.columns, len(images))
            images_per_row.append(images[start_idx:end_idx])
        
        # Process each row
        collage_rows = []
        available_width = self.width - (self.columns + 1) * self.spacing
        
        for row_images in images_per_row:
            # Calculate scaling to fit row width
            total_aspect_ratio = sum(img.width / img.height for img in row_images)
            row_height = int(available_width / total_aspect_ratio)
            
            # Resize images in this row
            row_resized = []
            for img in row_images:
                aspect_ratio = img.width / img.height
                new_width = int(row_height * aspect_ratio)
                resized = img.resize((new_width, row_height), Image.LANCZOS)
                row_resized.append(resized)
            
            # Create row image
            row_width = sum(img.width for img in row_resized) + (len(row_resized) + 1) * self.spacing
            row_img = Image.new('RGB', (row_width, row_height), self.background_color)
            
            x_offset = self.spacing
            for img in row_resized:
                row_img.paste(img, (x_offset, 0))
                x_offset += img.width + self.spacing
            
            collage_rows.append(row_img)
        
        # Combine rows into final collage
        collage_height = sum(img.height for img in collage_rows) + (len(collage_rows) + 1) * self.spacing
        collage = Image.new('RGB', (self.width, collage_height), self.background_color)
        
        y_offset = self.spacing
        for row_img in collage_rows:
            x_offset = (self.width - row_img.width) // 2  # Center the row
            collage.paste(row_img, (x_offset, y_offset))
            y_offset += row_img.height + self.spacing
        
        # Save collage
        collage.save(output_path, quality=95)
        logger.info(f"Adaptive collage saved to {output_path} ({self.width}x{collage_height})")
        
        return output_path
