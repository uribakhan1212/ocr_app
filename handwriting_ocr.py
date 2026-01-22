"""
Specialized OCR engine for handwritten text
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import easyocr
import streamlit as st
from typing import List, Dict, Optional

class HandwritingOCREngine:
    """Specialized OCR engine optimized for handwritten text"""
    
    def __init__(self, languages: List[str] = ['en']):
        try:
            self.reader = easyocr.Reader(languages, gpu=False)
        except Exception as e:
            st.error(f"Failed to initialize EasyOCR for handwriting: {str(e)}")
            self.reader = None
    
    def preprocess_for_handwriting(self, image: Image.Image) -> np.ndarray:
        """Specialized preprocessing for handwritten text"""
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Enhance contrast for handwriting
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.3)
        
        # Apply slight blur to smooth handwriting
        image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # Convert to OpenCV format
        img_array = np.array(image)
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        
        # Apply morphological operations to connect broken characters
        kernel = np.ones((2, 2), np.uint8)
        gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 10
        )
        
        return thresh
    
    def extract_handwritten_text(self, image: Image.Image) -> List[Dict]:
        """Extract handwritten text with optimized settings"""
        if self.reader is None:
            return []
        
        try:
            # Preprocess image for handwriting
            processed_img = self.preprocess_for_handwriting(image)
            
            # Use EasyOCR with handwriting-optimized parameters
            results = self.reader.readtext(
                processed_img,
                detail=1,        # Return coordinates
                paragraph=False,  # Don't group paragraphs for handwriting
                width_ths=0.5,   # Lower threshold for handwriting spacing
                height_ths=0.5,  # Lower threshold for handwriting spacing
                text_threshold=0.1,  # Very low text threshold
                low_text=0.1,    # Low text threshold
                link_threshold=0.1,  # Low link threshold
                canvas_size=2560,  # Larger canvas for better resolution
                mag_ratio=1.5    # Magnification ratio
            )
            
            text_blocks = []
            for (bbox, text, confidence) in results:
                # Very low confidence threshold for handwriting
                if confidence > 0.05 and len(text.strip()) > 0:
                    # Calculate bounding box center
                    x_center = (bbox[0][0] + bbox[2][0]) / 2
                    y_center = (bbox[0][1] + bbox[2][1]) / 2
                    
                    text_blocks.append({
                        'text': text.strip(),
                        'bbox': bbox,
                        'x_center': x_center,
                        'y_center': y_center,
                        'confidence': confidence
                    })
            
            return text_blocks
            
        except Exception as e:
            st.error(f"Handwriting OCR error: {str(e)}")
            return []
    
    def extract_with_multiple_attempts(self, image: Image.Image) -> List[Dict]:
        """Try multiple preprocessing approaches for handwriting"""
        all_results = []
        
        # Attempt 1: Standard preprocessing
        results1 = self.extract_handwritten_text(image)
        all_results.extend(results1)
        
        # Attempt 2: Higher contrast
        try:
            enhanced = ImageEnhance.Contrast(image).enhance(2.0)
            results2 = self.extract_handwritten_text(enhanced)
            all_results.extend(results2)
        except:
            pass
        
        # Attempt 3: Inverted colors (for dark backgrounds)
        try:
            from PIL import ImageOps
            inverted = ImageOps.invert(image.convert('RGB'))
            results3 = self.extract_handwritten_text(inverted)
            all_results.extend(results3)
        except:
            pass
        
        # Remove duplicates and keep highest confidence
        unique_results = {}
        for result in all_results:
            text = result['text']
            if text not in unique_results or result['confidence'] > unique_results[text]['confidence']:
                unique_results[text] = result
        
        return list(unique_results.values())

def create_handwriting_engine() -> Optional[HandwritingOCREngine]:
    """Create a handwriting OCR engine"""
    try:
        return HandwritingOCREngine()
    except Exception as e:
        st.error(f"Failed to create handwriting OCR engine: {str(e)}")
        return None