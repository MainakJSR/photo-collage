# Photo Processing Pipeline Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PHOTO PROCESSING PIPELINE                       │
└─────────────────────────────────────────────────────────────────────┘

INPUT FOLDER                        PROCESSING STAGES                    OUTPUT
═══════════                         ═════════════════                    ══════

  📁 input/                    ┌─────────────────────────┐
    ├── photo1.jpg             │   1. FACE DETECTION     │
    ├── photo2.jpg    ────────>│   • OpenCV / face_rec   │
    ├── photo3.jpg             │   • Find all faces      │
    └── ...                    │   • Get bounding box    │
                               └───────────┬─────────────┘
                                          │
                                          ▼
                               ┌─────────────────────────┐
                               │  2. INTELLIGENT CROP    │
                               │   • Focus on faces      │
                               │   • Add padding         │
                               │   • Square/Rectangle    │
                               └───────────┬─────────────┘
                                          │
                                          ▼
                               ┌─────────────────────────┐
                               │   3. IMAGE ENHANCE      │
                               │   • Brightness ↑        │
                               │   • Contrast ↑          │
                               │   • Sharpness ↑         │
                               │   • Color saturation ↑  │
                               └───────────┬─────────────┘
                                          │
                                          ▼
  📁 processed/                ┌─────────────────────────┐         📁 output/
    ├── photo1.jpg  <──────────│   4. SAVE PROCESSED     │
    ├── photo2.jpg             │   • Resized to target   │         ┌────────────┐
    ├── photo3.jpg             │   • Enhanced quality    │         │            │
    └── ...                    └───────────┬─────────────┘         │  COLLAGE   │
                                          │                         │            │
                                          ▼                         │  ┌──┬──┐  │
                               ┌─────────────────────────┐         │  │ 1│ 2│  │
                               │   5. CREATE COLLAGE     │ ───────>│  ├──┼──┤  │
                               │   • Grid layout         │         │  │ 3│ 4│  │
                               │   • Auto arrange        │         │  └──┴──┘  │
                               │   • High quality        │         │            │
                               └─────────────────────────┘         └────────────┘
                                                                   collage_*.jpg


═══════════════════════════════════════════════════════════════════════════

TECHNOLOGY STACK
────────────────

┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  Face Detection    │  OpenCV Haar Cascade (fast)                   │
│                    │  face_recognition / dlib (accurate)           │
│                                                                     │
│  Image Processing  │  OpenCV (cv2) - cropping, resizing            │
│                    │  NumPy - array operations                     │
│                                                                     │
│  Enhancement       │  PIL / Pillow - brightness, contrast, color   │
│                    │  OpenCV - denoising, gamma correction         │
│                                                                     │
│  Collage           │  PIL / Pillow - image composition             │
│                    │  Python - layout algorithms                   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════

CONFIGURATION OPTIONS (config.py)
──────────────────────────────────

┌───────────────────┬──────────────────────────────────────────────────┐
│ Category          │ Options                                          │
├───────────────────┼──────────────────────────────────────────────────┤
│ Face Detection    │ • Method: opencv / face_recognition              │
│                   │ • Min face size: (width, height)                 │
│                   │ • Padding: pixels around face                    │
├───────────────────┼──────────────────────────────────────────────────┤
│ Cropping          │ • Shape: square / rectangle                      │
│                   │ • Aspect ratio: (4, 3), (16, 9), etc.            │
│                   │ • Target size: output dimensions                 │
├───────────────────┼──────────────────────────────────────────────────┤
│ Enhancement       │ • Brightness factor: 1.1 (10% brighter)          │
│                   │ • Contrast factor: 1.2 (20% more contrast)       │
│                   │ • Sharpness factor: 1.3 (30% sharper)            │
│                   │ • Color factor: 1.1 (10% more saturated)         │
├───────────────────┼──────────────────────────────────────────────────┤
│ Collage           │ • Width: total width in pixels                   │
│                   │ • Columns: number of columns in grid             │
│                   │ • Spacing: pixels between images                 │
│                   │ • Background: RGB color tuple                    │
└───────────────────┴──────────────────────────────────────────────────┘


═══════════════════════════════════════════════════════════════════════════

USAGE EXAMPLES
──────────────

1. Basic Usage (Full Pipeline):
   $ python main.py
   
   → Processes all images in input/
   → Saves enhanced photos to processed/
   → Creates collage in output/

2. Custom Configuration:
   Edit config.py, then run:
   $ python main.py

3. Individual Module Usage:
   $ python example_usage.py
   
   → Demonstrates each module separately
   → Useful for custom workflows

4. Setup (First Time):
   $ ./setup.sh
   
   → Creates virtual environment
   → Installs all dependencies
   → Ready to run!


═══════════════════════════════════════════════════════════════════════════

FILE STRUCTURE
──────────────

Photos-3-001/
│
├── Core Modules (Python)
│   ├── main.py              # Main pipeline orchestrator
│   ├── config.py            # Configuration settings
│   ├── face_detector.py     # Face detection logic
│   ├── image_processor.py   # Cropping & resizing
│   ├── image_enhancer.py    # Image enhancement
│   └── collage_maker.py     # Collage generation
│
├── Documentation
│   ├── README.md            # User guide
│   ├── PROJECT_SUMMARY.md   # Technical overview
│   └── WORKFLOW.md          # This file
│
├── Setup & Examples
│   ├── requirements.txt     # Python dependencies
│   ├── setup.sh            # Automated setup script
│   └── example_usage.py    # Usage examples
│
├── Data Directories
│   ├── input/              # 📥 Place original photos here
│   ├── processed/          # 💾 Enhanced photos saved here
│   └── output/             # 📤 Final collages saved here
│
└── Version Control
    ├── .git/               # Git repository
    └── .gitignore          # Git ignore rules


═══════════════════════════════════════════════════════════════════════════

NEXT STEPS
──────────

1. Install Dependencies:
   ./setup.sh

2. Activate Environment:
   source venv/bin/activate

3. Run Pipeline:
   python main.py

4. Check Results:
   - processed/ folder: Enhanced individual photos
   - output/ folder: Final collage

5. Customize (Optional):
   Edit config.py to adjust settings

6. Phase 2 Features:
   - Google Photos integration
   - Web interface
   - Custom templates
   - Batch processing


═══════════════════════════════════════════════════════════════════════════

TROUBLESHOOTING
───────────────

❌ Import errors for cv2, PIL, numpy?
   → Run: pip install -r requirements.txt

❌ No faces detected?
   → Try: FACE_DETECTION_METHOD = "face_recognition" in config.py
   → Adjust: MIN_FACE_SIZE in config.py

❌ Memory issues with large images?
   → Reduce: TARGET_SIZE in config.py
   → Reduce: COLLAGE_WIDTH in config.py

❌ face_recognition install fails?
   → Use OpenCV method instead (works fine!)
   → Or install system dependencies (see README.md)


═══════════════════════════════════════════════════════════════════════════
