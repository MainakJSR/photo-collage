# Photo Processing & Collage Maker

A Python-based photo processing pipeline that enhances images and creates beautiful collages while preserving original image dimensions.

## Features

- ✨ **Image Enhancement**: Automatically improves brightness, contrast, sharpness, and color saturation
- 📸 **No Cropping/Resizing**: Keeps images at their original size and aspect ratio
- 🖼️ **Flexible Collage Layout**: Creates collages with 1-5 images per row based on image dimensions
- 📅 **EXIF Date Sorting**: Automatically sorts images by creation date from EXIF data
- 🔢 **Sequential Naming**: Renames processed images sequentially (1.jpg, 2.jpg, etc.)
- 📊 **Detailed Logging**: Tracks all processing steps with comprehensive logging

## Project Structure

```
Photos-3-001/
├── main.py                 # Main entry point - orchestrates the pipeline
├── config.py              # Configuration settings
├── image_processor.py     # Keeps images at original size (no resizing)
├── image_enhancer.py      # Enhances image quality (brightness, contrast, etc.)
├── collage_maker.py       # Creates flexible collages with EXIF sorting
├── requirements.txt       # Python dependencies
├── setup.sh              # Setup script for environment
├── input/                # Place your original photos here
├── processed/            # Enhanced images (renamed sequentially)
├── output/               # Final collages
└── photo_processing.log  # Detailed processing log
```

## Installation

### Prerequisites

- Python 3.8 or higher
- Virtual environment (recommended)

### Setup

1. **Clone or navigate to the project directory**:
   ```bash
   cd /path/to/Photos-3-001
   ```

2. **Run the setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   Or manually:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Dependencies

- `opencv-python` - Image processing
- `Pillow` - Image manipulation and EXIF handling
- `numpy` - Numerical operations

## Usage

### Basic Workflow

1. **Add your photos** to the `input/` directory
   ```bash
   cp /path/to/your/photos/*.jpg input/
   ```

2. **Run the pipeline**:
   ```bash
   source .venv/bin/activate  # Activate virtual environment
   python main.py
   ```

3. **Check the results**:
   - Enhanced images: `processed/` (renamed 1.jpg, 2.jpg, etc.)
   - Final collage: `output/collage_YYYYMMDD_HHMMSS.jpg`

### What Happens During Processing

1. **Image Loading**: Scans `input/` directory for supported formats (.jpg, .jpeg, .png)
2. **Enhancement**: Applies brightness, contrast, sharpness, and color adjustments
3. **Saving**: Saves enhanced images to `processed/` directory
4. **EXIF Sorting**: Reads creation dates from EXIF data and sorts images chronologically
5. **Sequential Naming**: Renames files as 1.jpg, 2.jpg, etc. based on date order
6. **Collage Creation**: Arranges images in flexible rows (1-5 images per row)
7. **Output**: Saves final collage to `output/` directory

### EXIF Date Handling

If an image doesn't have EXIF date information, you'll be prompted:
```
Enter date for 'IMG_1234.jpg' (DD-MM-YYYY or press Enter to use file date):
```

- Enter date in `DD-MM-YYYY` format (e.g., `15-08-2021`)
- Press Enter to use the file's modification date

## Configuration

Edit `config.py` to customize processing settings:

### Directory Paths

```python
INPUT_DIR = os.path.join(BASE_DIR, "input")      # Source images
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")  # Enhanced images
OUTPUT_DIR = os.path.join(BASE_DIR, "output")    # Final collages
```

### Image Enhancement Settings

```python
ENHANCE_BRIGHTNESS = True
BRIGHTNESS_FACTOR = 1.1    # 1.0 = no change, >1.0 = brighter, <1.0 = darker

ENHANCE_CONTRAST = True
CONTRAST_FACTOR = 1.2      # 1.0 = no change, >1.0 = more contrast

ENHANCE_SHARPNESS = True
SHARPNESS_FACTOR = 1.3     # 1.0 = no change, >1.0 = sharper

ENHANCE_COLOR = True
COLOR_FACTOR = 1.1         # 1.0 = no change, >1.0 = more saturated
```

### Collage Settings

```python
COLLAGE_WIDTH = 6000       # Target width in pixels (reference only)
COLLAGE_COLUMNS = 5        # Max images per row (1-5)
COLLAGE_SPACING = 20       # Spacing between images in pixels
COLLAGE_BACKGROUND_COLOR = (255, 255, 255)  # RGB tuple (white)
```

### Supported Image Formats

```python
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
```

### Logging

```python
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR
```

## How It Works

### Image Processing (No Resizing!)

The `ImageProcessor` class keeps images at their **original size**:
- No cropping
- No resizing
- Maintains original aspect ratios
- Only enhancement is applied

### Image Enhancement

The `ImageEnhancer` class uses PIL (Pillow) to improve image quality:
- **Brightness**: Makes images lighter or darker
- **Contrast**: Enhances the difference between light and dark areas
- **Sharpness**: Increases edge definition and clarity
- **Color**: Adjusts color saturation

### Collage Layout

The `CollageMaker` class creates flexible collages:
- **Intelligent Row Arrangement**: Groups 1-5 images per row based on widths
- **No Image Resizing**: Uses original image dimensions
- **Vertical Centering**: Aligns images vertically within each row
- **Horizontal Centering**: Centers rows within the collage
- **EXIF Date Sorting**: Orders images chronologically
- **Sequential Naming**: Renames files 1, 2, 3, etc.

#### Row Layout Logic

- Images are arranged to fit within the target width
- Each row can contain 1-5 images
- Wide landscape photos get fewer images per row
- Portrait photos can fit more per row
- Images maintain their original dimensions

## Examples

### Example Output

**Input**: 21 photos of various sizes
**Output**: 
- 21 enhanced images in `processed/` (named 1.jpg through 21.jpg)
- 1 collage in `output/` (e.g., 6614x39676 pixels for 21 full-resolution photos)

### Sample Log Output

```
2025-12-29 11:00:26,746 - INFO - Starting Photo Processing Pipeline
2025-12-29 11:00:26,746 - INFO - Scanning input directory
2025-12-29 11:00:26,746 - INFO - Found 21 images
2025-12-29 11:00:26,746 - INFO - Processing 21 images...
2025-12-29 11:00:56,212 - INFO - Successfully processed 21/21 images
2025-12-29 11:00:56,212 - INFO - Creating collage...
2025-12-29 11:00:22,994 - INFO - Arranged 21 images into 10 rows
2025-12-29 11:00:26,631 - INFO - Collage saved (6614x39676)
2025-12-29 11:00:26,631 - INFO - Images kept at original size - NO resizing applied
```

## Troubleshooting

### No Images Found

**Issue**: "No images found in input directory"
**Solution**: 
- Check that images are in the `input/` folder
- Verify file extensions match `SUPPORTED_FORMATS` in config.py

### Memory Errors with Large Images

**Issue**: Out of memory when processing very large images
**Solution**:
- Process fewer images at once
- Increase system swap space
- Use smaller original images

### EXIF Date Not Found

**Issue**: "No EXIF date found for image"
**Solution**:
- Enter date manually when prompted (DD-MM-YYYY format)
- Or press Enter to use file modification date

### Collage Too Large

**Issue**: Collage file size is huge
**Solution**:
- Images are kept at original resolution - this is by design
- To reduce size, you can manually reduce input image resolution before processing

## Advanced Usage

### Custom Enhancement Factors

To disable specific enhancements, set factors to 1.0 or set flags to False:

```python
# config.py
ENHANCE_BRIGHTNESS = False  # Disable brightness adjustment
CONTRAST_FACTOR = 1.0       # No contrast change
```

### Batch Processing Multiple Folders

```bash
# Process multiple photo sets
for folder in folder1 folder2 folder3; do
    cp $folder/*.jpg input/
    python main.py
    mv output/*.jpg final_collages/$folder_collage.jpg
    rm input/*.jpg processed/*.jpg
done
```

### Running Without Prompts

To avoid EXIF date prompts, ensure all images have EXIF data, or modify the code to always use file dates.

## Technical Details

### Image Formats

- Input: JPEG, PNG
- Output: JPEG (quality=95)
- EXIF: Preserves date metadata for sorting

### Performance

- Processing time depends on:
  - Number of images
  - Image resolution
  - Enhancement settings
  - System specifications

Typical performance:
- ~20-30 images: 30-60 seconds
- Enhancement: ~1-2 seconds per image
- Collage creation: ~5-10 seconds

## Limitations

- **File Size**: Very large collages (>100MB) may have compatibility issues with some viewers
- **Memory**: Processing hundreds of high-resolution images may require significant RAM
- **EXIF Data**: Not all images contain EXIF dates (manual entry required)

## Contributing

To modify or extend the pipeline:

1. **Add new enhancement**: Edit `image_enhancer.py`
2. **Change layout logic**: Modify `collage_maker.py`
3. **Adjust workflow**: Update `main.py`
4. **Add settings**: Update `config.py`

## License

This project is provided as-is for personal use.

## Changelog

### Version 2.0 (Current)
- ✨ Added flexible collage layout (1-5 images per row)
- 🎯 Removed all image resizing/cropping - original sizes preserved
- 📅 Enhanced EXIF date sorting with user input fallback
- 🔢 Sequential file renaming based on chronological order
- 📝 Improved logging and error handling

### Version 1.0
- Initial release with face detection and cropping
- Fixed grid layout (4 columns)
- Image resizing to uniform size

---

**Created**: December 2025  
**Last Updated**: December 29, 2025
