"""
Example script showing how to use individual modules
"""

import cv2
from face_detector import FaceDetector
from image_processor import ImageProcessor
from image_enhancer import ImageEnhancer

# Example 1: Face Detection
print("Example 1: Face Detection")
print("-" * 40)

detector = FaceDetector(method="opencv")
image = cv2.imread("input/IMG_1269.JPG")

if image is not None:
    faces = detector.detect_faces(image)
    print(f"Detected {len(faces)} face(s)")
    
    # Draw rectangles around faces
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Save result
    cv2.imwrite("output/example_face_detection.jpg", image)
    print("Saved: output/example_face_detection.jpg")
else:
    print("Could not load example image")

print()

# Example 2: Image Processing
print("Example 2: Image Cropping")
print("-" * 40)

processor = ImageProcessor(crop_shape="square", target_size=(500, 500))
image = cv2.imread("input/IMG_1269.JPG")

if image is not None:
    # Use a sample bounding box
    bbox = (100, 100, 400, 400)
    cropped = processor.process_image(image, bbox)
    
    cv2.imwrite("output/example_cropped.jpg", cropped)
    print(f"Cropped image to {cropped.shape}")
    print("Saved: output/example_cropped.jpg")

print()

# Example 3: Image Enhancement
print("Example 3: Image Enhancement")
print("-" * 40)

enhancer = ImageEnhancer(
    brightness_factor=1.2,
    contrast_factor=1.3,
    sharpness_factor=1.5,
    color_factor=1.1
)

image = cv2.imread("input/IMG_1269.JPG")

if image is not None:
    enhanced = enhancer.enhance(image)
    
    cv2.imwrite("output/example_enhanced.jpg", enhanced)
    print("Enhanced image with improved brightness, contrast, and sharpness")
    print("Saved: output/example_enhanced.jpg")

print()
print("=" * 40)
print("Examples complete! Check the output folder.")
