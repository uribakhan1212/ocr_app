"""
Utility functions for the Image to Word Converter application
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance
import streamlit as st
from typing import Tuple, Optional
import tempfile
import os

def enhance_image_quality(image: Image.Image) -> Image.Image:
    """
    Enhance image quality for better OCR results
    """
    # Convert to RGB if necessary
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.2)
    
    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(1.1)
    
    return image

def resize_image_if_needed(image: Image.Image, max_dimension: int = 2000) -> Image.Image:
    """
    Resize image if it's too large while maintaining aspect ratio
    """
    width, height = image.size
    
    if max(width, height) > max_dimension:
        if width > height:
            new_width = max_dimension
            new_height = int((height * max_dimension) / width)
        else:
            new_height = max_dimension
            new_width = int((width * max_dimension) / height)
        
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return image

def validate_image(uploaded_file) -> Tuple[bool, str]:
    """
    Validate uploaded image file
    """
    if uploaded_file is None:
        return False, "No file uploaded"
    
    # Check file size (10MB limit)
    if uploaded_file.size > 10 * 1024 * 1024:
        return False, "File size exceeds 10MB limit"
    
    # Check file type
    allowed_types = ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp', 'image/tiff']
    if uploaded_file.type not in allowed_types:
        return False, f"Unsupported file type: {uploaded_file.type}"
    
    try:
        # Try to open the image
        image = Image.open(uploaded_file)
        image.verify()
        return True, "Valid image file"
    except Exception as e:
        return False, f"Invalid image file: {str(e)}"

def create_download_link(doc_buffer, filename: str) -> str:
    """
    Create a download link for the Word document
    """
    import base64
    
    b64 = base64.b64encode(doc_buffer.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}" download="{filename}">Download Word Document</a>'
    return href

def display_processing_stats(text_blocks: list, tables: list, processing_time: float):
    """
    Display processing statistics in Streamlit
    """
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Text Blocks", len(text_blocks))
    
    with col2:
        total_words = sum(len(block['text'].split()) for block in text_blocks)
        st.metric("Total Words", total_words)
    
    with col3:
        st.metric("Tables Found", len(tables))
    
    with col4:
        st.metric("Processing Time", f"{processing_time:.2f}s")

def clean_text(text: str) -> str:
    """
    Clean and normalize extracted text
    """
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    # Fix common OCR errors
    replacements = {
        '|': 'I',
        '0': 'O',  # Only in specific contexts
        '5': 'S',  # Only in specific contexts
        '1': 'l',  # Only in specific contexts
    }
    
    # Apply replacements cautiously
    # This is a simplified approach - in production, you'd want more sophisticated text correction
    
    return text.strip()

def save_temp_image(image: Image.Image, suffix: str = '.png') -> str:
    """
    Save image to temporary file and return path
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        image.save(tmp_file.name, 'PNG')
        return tmp_file.name

def cleanup_temp_file(filepath: str):
    """
    Clean up temporary file
    """
    try:
        if os.path.exists(filepath):
            os.unlink(filepath)
    except Exception:
        pass  # Ignore cleanup errors

def format_confidence_score(confidence: float) -> str:
    """
    Format confidence score for display
    """
    return f"{confidence * 100:.1f}%"

def detect_text_orientation(image: Image.Image) -> float:
    """
    Detect text orientation in image
    Returns rotation angle in degrees
    """
    # Convert PIL to OpenCV format
    img_array = np.array(image)
    if len(img_array.shape) == 3:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    
    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    # Detect lines using Hough transform
    lines = cv2.HoughLines(edges, 1, np.pi/180, threshold=100)
    
    if lines is not None:
        angles = []
        for rho, theta in lines[:10]:  # Consider only first 10 lines
            angle = theta * 180 / np.pi
            angles.append(angle)
        
        # Find the most common angle
        if angles:
            return np.median(angles)
    
    return 0.0  # No rotation needed