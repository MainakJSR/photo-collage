# Photo Processing and Collage Creator

A Python-based photo processing pipeline that performs face detection, intelligent cropping, image enhancement, and creates beautiful collages from your photos.

## Features

- **Face Detection**: Automatically detect faces in photos using OpenCV or face_recognition library
- **Intelligent Cropping**: Crop photos to focus on detected faces with configurable padding
- **Flexible Aspect Ratios**: Support for both square and rectangular crops
- **Image Enhancement**: 
  - Brightness adjustment
  - Contrast enhancement
  - Sharpness enhancement
  - Color saturation boost
  - Optional denoising
- **Collage Creation**: Generate beautiful photo collages with customizable layouts
- **All Open Source**: Uses only open-source Python libraries

## Project Structure

```
Photos-3-001/
├── input/              # Place your original photos here
├── processed/          # Processed photos (cropped & enhanced)
├── output/             # Final collages
├── config.py           # Configuration settings
├── face_detector.py    # Face detection module
├── image_processor.py  # Image cropping and resizing
├── image_enhancer.py   # Image enhancement module
├── collage_maker.py    # Collage creation module
├── main.py             # Main pipeline script
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd /home/mainak1/Documents/Risabh/Photos-3-001
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   **Note**: Installing `dlib` and `face-recognition` may require additional system dependencies:
   
   - **Ubuntu/Debian:**
     ```bash
     sudo apt-get install build-essential cmake
     sudo apt-get install libopenblas-dev liblapack-dev
     ```
   
   - **macOS:**
     ```bash
     brew install cmake
     ```

## Usage

### Basic Usage

1. **Place your photos in the `input` folder**

2. **Run the pipeline:**
   ```bash
   python main.py
   ```

3. **Find your results:**
   - Processed photos: `processed/` folder
   - Final collage: `output/` folder

### Configuration

Edit `config.py` to customize the processing:

#### Face Detection Settings
```python
FACE_DETECTION_METHOD = "opencv"  # or "face_recognition"
MIN_FACE_SIZE = (30, 30)         # Minimum face size to detect
FACE_PADDING = 50                # Pixels around detected face
```

#### Cropping Settings
```python
CROP_SHAPE = "rectangle"         # "square" or "rectangle"
ASPECT_RATIO = (4, 3)            # For rectangle mode
TARGET_SIZE = (800, 600)         # Output image size
```

#### Enhancement Settings
```python
ENHANCE_BRIGHTNESS = True
BRIGHTNESS_FACTOR = 1.1          # 1.0 = no change
ENHANCE_CONTRAST = True
CONTRAST_FACTOR = 1.2
ENHANCE_SHARPNESS = True
SHARPNESS_FACTOR = 1.3
ENHANCE_COLOR = True
COLOR_FACTOR = 1.1
```

#### Collage Settings
```python
COLLAGE_WIDTH = 3000             # Width in pixels
COLLAGE_COLUMNS = 4              # Number of columns
COLLAGE_SPACING = 10             # Spacing between images
```

## How It Works

1. **Face Detection**: The system scans each photo and detects faces using either OpenCV's Haar Cascade or the face_recognition library

2. **Intelligent Cropping**: Based on detected faces, the image is cropped to focus on the important areas with configurable padding

3. **Enhancement**: Each photo is enhanced for better quality:
   - Brightness and contrast adjustments
   - Sharpness enhancement
   - Color saturation boost

4. **Collage Creation**: All processed photos are arranged into a beautiful grid-based collage

## Advanced Usage

### Using Different Face Detection Methods

The project supports two face detection methods:

- **OpenCV** (default): Faster, good for most cases
- **face_recognition**: More accurate, slower

Change in `config.py`:
```python
FACE_DETECTION_METHOD = "face_recognition"
```

### Custom Image Processing

You can import and use individual modules in your own scripts:

```python
from face_detector import FaceDetector
from image_processor import ImageProcessor
from image_enhancer import ImageEnhancer
from collage_maker import CollageMaker

# Initialize components
detector = FaceDetector(method="opencv")
processor = ImageProcessor(crop_shape="square")
enhancer = ImageEnhancer(brightness_factor=1.2)
collage = CollageMaker(columns=3)

# Use them in your code...
```

## Troubleshooting

### Import Errors
If you see import errors for `cv2`, `PIL`, or other packages, make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### No Faces Detected
- Try adjusting `MIN_FACE_SIZE` in config.py
- Switch to `face_recognition` method for better accuracy
- Ensure photos have visible faces

### Memory Issues
If processing large batches of high-resolution images:
- Reduce `TARGET_SIZE` in config.py
- Process images in smaller batches
- Reduce `COLLAGE_WIDTH`

## Future Enhancements (Phase 2)

- **Google Photos Integration**: Direct import from Google Photos
- **Batch Processing**: Process multiple folders
- **Custom Templates**: Different collage layouts
- **Web Interface**: User-friendly web UI
- **Cloud Processing**: Process in the cloud

## Dependencies

- **opencv-python**: Computer vision and face detection
- **opencv-contrib-python**: Additional OpenCV modules
- **Pillow**: Image processing and enhancement
- **numpy**: Numerical operations
- **face-recognition**: Advanced face detection
- **dlib**: Machine learning toolkit

## License

This project uses open-source libraries. Please refer to individual library licenses for more information.

## Contributing

Feel free to submit issues, feature requests, or pull requests!

## Author

Created as a photo processing and collage creation tool using open-source Python libraries.

---

**Enjoy creating beautiful photo collages!** 📸✨
