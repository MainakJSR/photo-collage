╔═══════════════════════════════════════════════════════════════════════════╗
║                    PHOTO PROCESSING PIPELINE                              ║
║                         QUICK REFERENCE                                   ║
╚═══════════════════════════════════════════════════════════════════════════╝

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🚀 QUICK START                                                         ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  1. Setup (first time only):
     $ ./setup.sh

  2. Activate environment:
     $ source venv/bin/activate

  3. Run pipeline:
     $ python main.py

  ✅ Your 22 photos are already in the input/ folder!

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  📁 DIRECTORY STRUCTURE                                                 ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  input/         📥 Place original photos here (22 photos ready!)
  processed/     💾 Enhanced photos saved here automatically
  output/        📤 Final collages saved here

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🔧 KEY FILES                                                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  main.py              Run the complete pipeline
  config.py            Customize all settings here
  example_usage.py     See how to use individual modules
  setup.sh             Install dependencies automatically

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  ⚙️  COMMON SETTINGS (edit config.py)                                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  Face Detection Method:
  FACE_DETECTION_METHOD = "opencv"           # Fast, good quality
  FACE_DETECTION_METHOD = "face_recognition" # Slower, more accurate

  Crop Shape:
  CROP_SHAPE = "square"                      # Instagram-style
  CROP_SHAPE = "rectangle"                   # Custom aspect ratio

  Enhancement (1.0 = no change):
  BRIGHTNESS_FACTOR = 1.1                    # 10% brighter
  CONTRAST_FACTOR = 1.2                      # 20% more contrast
  SHARPNESS_FACTOR = 1.3                     # 30% sharper

  Collage Layout:
  COLLAGE_COLUMNS = 4                        # Number of columns
  COLLAGE_WIDTH = 3000                       # Width in pixels

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🔍 WHAT HAPPENS WHEN YOU RUN                                           ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  For each photo:
    1. ✅ Detects faces
    2. ✅ Crops around faces
    3. ✅ Enhances quality (brighter, sharper, more vibrant)
    4. ✅ Saves to processed/ folder

  Finally:
    5. ✅ Creates beautiful collage
    6. ✅ Saves to output/ folder with timestamp

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🛠️  COMMANDS                                                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  # Full pipeline
  python main.py

  # See examples
  python example_usage.py

  # Install/reinstall dependencies
  pip install -r requirements.txt

  # Check git history
  git log --oneline

  # View photos
  ls -l input/
  ls -l processed/
  ls -l output/

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  📚 DOCUMENTATION                                                       ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  README.md           Complete user guide
  PROJECT_SUMMARY.md  Technical overview
  WORKFLOW.md         Visual workflow diagram
  QUICKREF.md         This quick reference

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🐛 TROUBLESHOOTING                                                     ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  Problem: Import errors (cv2, PIL, numpy not found)
  Solution: pip install -r requirements.txt

  Problem: No faces detected
  Solution: Edit config.py, try face_recognition method

  Problem: face_recognition install fails
  Solution: Use opencv method (works great!)

  Problem: Images too large / memory issues
  Solution: Reduce TARGET_SIZE and COLLAGE_WIDTH in config.py

  Problem: Photos in wrong folder
  Solution: Move to input/ folder: mv *.jpg input/

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  📦 PYTHON MODULES                                                      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  face_detector.py      FaceDetector class
  image_processor.py    ImageProcessor class
  image_enhancer.py     ImageEnhancer class
  collage_maker.py      CollageMaker class

  Each can be imported and used independently!

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  💡 TIPS                                                                ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  ✨ Start with default settings, adjust as needed
  ✨ Check photo_processing.log for detailed information
  ✨ Processed photos are kept - safe to re-run
  ✨ Each collage has unique timestamp - won't overwrite
  ✨ Use example_usage.py to test individual features
  ✨ All settings in one place: config.py

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🎯 FEATURES                                                            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  ✅ Automatic face detection
  ✅ Intelligent cropping
  ✅ Professional enhancement
  ✅ Beautiful collages
  ✅ Configurable settings
  ✅ Batch processing
  ✅ Multiple detection methods
  ✅ All open source
  ✅ Full git version control
  ✅ Comprehensive documentation

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🚀 PHASE 2 (Future)                                                    ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

  📱 Google Photos integration
  🌐 Web interface
  🎨 Custom collage templates
  ☁️  Cloud deployment
  👥 Face grouping
  🎬 Video support

╔═══════════════════════════════════════════════════════════════════════════╗
║                    Ready to create amazing collages!                      ║
║                            Run: python main.py                            ║
╚═══════════════════════════════════════════════════════════════════════════╝
