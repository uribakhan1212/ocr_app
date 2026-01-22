"""
Configuration settings for the Image to Word Converter application
"""

import os
from pathlib import Path

# Application settings
APP_NAME = "Image to Word Converter"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Convert images containing text, tables, and graphics into editable Word documents"

# File upload settings
MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp']

# OCR settings
DEFAULT_OCR_ENGINE = "easyocr"
TESSERACT_CONFIG = '--oem 3 --psm 6'
EASYOCR_LANGUAGES = ['en']
MIN_CONFIDENCE_THRESHOLD = 0.5

# Image processing settings
IMAGE_PREPROCESSING = {
    'denoise': True,
    'adaptive_threshold': True,
    'dpi_enhancement': True,
    'contrast_enhancement': True
}

# Table detection settings
TABLE_DETECTION = {
    'y_threshold': 20,  # pixels for row grouping
    'min_columns': 2,   # minimum columns to consider as table
    'min_rows': 2       # minimum rows to consider as table
}

# Document generation settings
DOCUMENT_SETTINGS = {
    'default_font': 'Calibri',
    'default_font_size': 11,
    'image_width_inches': 6,
    'paragraph_spacing': 1.15
}

# Paths
BASE_DIR = Path(__file__).parent
TEMP_DIR = BASE_DIR / "temp"
MODELS_DIR = BASE_DIR / "models"

# Create directories if they don't exist
TEMP_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# Streamlit configuration
STREAMLIT_CONFIG = {
    'page_title': APP_NAME,
    'page_icon': '📄',
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}