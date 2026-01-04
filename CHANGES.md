# Recent Changes Summary

## Date Handling Improvements

### Filename Date Extraction
The system now automatically extracts dates from filenames using these patterns:
- YYYYMMDD (e.g., 20231215)
- YYYY-MM-DD or YYYY_MM_DD
- DDMMYYYY (e.g., 15122023)
- DD-MM-YYYY or DD_MM_YYYY
- IMG_YYYYMMDD (e.g., IMG_20231215)
- YYYYMMDD_HHMMSS (e.g., 20231215_143000)
- IMG-YYYYMMDD-WA format (e.g., IMG-20161028-WA0005)

### Date Priority Order
1. EXIF data from image (DateTimeOriginal, DateTime, or DateTimeDigitized)
2. Date extracted from filename
3. User input (if prompted)
4. File modification date (fallback)

### User Interaction
- Only prompts for date when BOTH EXIF and filename date are missing
- User can press Enter to use file modification date
- Date format: DD-MM-YYYY (e.g., 15-08-2021)

## Image Compression Improvements

### Size-based Compression
Images are automatically compressed based on total image count:
- **≤ 20 images**: Max 1 MB per image, Quality 80
- **21-50 images**: Max 700 KB per image, Quality 70
- **51-70 images**: Max 500 KB per image, Quality 60
- **71-100 images**: Max 300 KB per image, Quality 50
- **> 100 images**: Error - too many images

### EXIF Preservation
- Original EXIF data is preserved during image processing
- EXIF data is maintained through compression
- Collage images also maintain metadata

## Collage Output

### Two Versions Created
1. **High Quality**: ~25 MB, Quality 75
2. **Compressed**: < 5 MB, Quality 11

### Square Layout
- Automatically arranges images in rows to create near-square aspect ratio
- Maximum 5 images per row
- Intelligent row distribution based on image count

## File Size Reduction
- Original 67 MB → 25 MB (high quality)
- Original 67 MB → < 5 MB (compressed version)
- 60% reduction in standard version
- 92% reduction in compressed version
