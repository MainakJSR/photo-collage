#!/bin/bash

# Photo Processing Pipeline Setup Script

echo "=========================================="
echo "Photo Processing Pipeline Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
echo "Found Python $python_version"

if [ ! $(python3 -c "import sys; print(sys.version_info >= (3, 7))") = "True" ]; then
    echo "Error: Python 3.7 or higher is required"
    exit 1
fi

echo ""
echo "Creating virtual environment..."
python3 -m venv venv

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Upgrading pip..."
pip install --upgrade pip

echo ""
echo "Installing dependencies..."
echo "Note: This may take several minutes, especially for dlib and face-recognition"
echo ""

# Install numpy first (required by other packages)
pip install numpy

# Install OpenCV
echo "Installing OpenCV..."
pip install opencv-python opencv-contrib-python

# Install Pillow
echo "Installing Pillow..."
pip install Pillow

# Try to install dlib and face-recognition
echo ""
echo "Installing face-recognition (this may take a while)..."
echo "If this fails, you can still use the project with OpenCV face detection"
pip install dlib face-recognition || echo "Warning: face-recognition installation failed. You can still use OpenCV method."

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To use the photo processor:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Place your photos in the 'input' folder"
echo "3. Run: python main.py"
echo ""
echo "Your photos are already in the input folder!"
echo "You can run the pipeline right now with: python main.py"
echo ""
