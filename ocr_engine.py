"""
OCR Engine implementations for text extraction
"""

import pytesseract
import easyocr
import cv2
import numpy as np
from PIL import Image
from typing import List, Dict, Tuple, Optional
import streamlit as st
from abc import ABC, abstractmethod

class OCREngine(ABC):
    """Abstract base class for OCR engines"""
    
    @abstractmethod
    def extract_text_with_positions(self, image: Image.Image) -> List[Dict]:
        """Extract text with bounding box positions"""
        pass
    
    @abstractmethod
    def extract_text_simple(self, image: Image.Image) -> str:
        """Extract text as simple string"""
        pass

class TesseractEngine(OCREngine):
    """Tesseract OCR engine implementation"""
    
    def __init__(self, config: str = '--oem 3 --psm 6'):
        self.config = config
        
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess image for Tesseract"""
        # Convert PIL to OpenCV format
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Apply adaptive thresholding
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        return thresh
    
    def extract_text_with_positions(self, image: Image.Image) -> List[Dict]:
        """Extract text with bounding boxes using Tesseract"""
        try:
            processed_img = self.preprocess_image(image)
            
            # Get detailed data from Tesseract
            data = pytesseract.image_to_data(
                processed_img, 
                config=self.config, 
                output_type=pytesseract.Output.DICT
            )
            
            text_blocks = []
            n_boxes = len(data['text'])
            
            for i in range(n_boxes):
                text = data['text'][i].strip()
                confidence = int(data['conf'][i])
                
                if text and confidence > 30:  # Filter low confidence results
                    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                    
                    # Create bounding box in EasyOCR format for consistency
                    bbox = [
                        [x, y],
                        [x + w, y],
                        [x + w, y + h],
                        [x, y + h]
                    ]
                    
                    text_blocks.append({
                        'text': text,
                        'bbox': bbox,
                        'x_center': x + w/2,
                        'y_center': y + h/2,
                        'confidence': confidence / 100.0  # Normalize to 0-1
                    })
            
            return text_blocks
            
        except Exception as e:
            st.error(f"Tesseract OCR error: {str(e)}")
            return []
    
    def extract_text_simple(self, image: Image.Image) -> str:
        """Extract text as simple string using Tesseract"""
        try:
            processed_img = self.preprocess_image(image)
            text = pytesseract.image_to_string(processed_img, config=self.config)
            return text.strip()
        except Exception as e:
            st.error(f"Tesseract OCR error: {str(e)}")
            return ""

class EasyOCREngine(OCREngine):
    """EasyOCR engine implementation"""
    
    def __init__(self, languages: List[str] = ['en']):
        try:
            self.reader = easyocr.Reader(languages, gpu=False)  # Set gpu=True if CUDA available
        except Exception as e:
            st.error(f"Failed to initialize EasyOCR: {str(e)}")
            self.reader = None
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess image for EasyOCR"""
        # Convert PIL to OpenCV format
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        
        # EasyOCR works well with minimal preprocessing
        # Apply slight denoising
        if len(img_array.shape) == 3:
            denoised = cv2.fastNlMeansDenoisingColored(img_array, None, 10, 10, 7, 21)
        else:
            denoised = cv2.fastNlMeansDenoising(img_array, None, 10, 7, 21)
        
        return denoised
    
    def extract_text_with_positions(self, image: Image.Image) -> List[Dict]:
        """Extract text with bounding boxes using EasyOCR"""
        if self.reader is None:
            return []
        
        try:
            processed_img = self.preprocess_image(image)
            
            # Use EasyOCR to extract text
            results = self.reader.readtext(processed_img)
            
            text_blocks = []
            for (bbox, text, confidence) in results:
                if confidence > 0.3:  # Filter low confidence results
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
            st.error(f"EasyOCR error: {str(e)}")
            return []
    
    def extract_text_simple(self, image: Image.Image) -> str:
        """Extract text as simple string using EasyOCR"""
        if self.reader is None:
            return ""
        
        try:
            text_blocks = self.extract_text_with_positions(image)
            # Sort by position and join
            text_blocks.sort(key=lambda x: (x['y_center'], x['x_center']))
            return ' '.join([block['text'] for block in text_blocks])
        except Exception as e:
            st.error(f"EasyOCR error: {str(e)}")
            return ""

class OCREngineFactory:
    """Factory class to create OCR engines"""
    
    @staticmethod
    def create_engine(engine_type: str, **kwargs) -> Optional[OCREngine]:
        """Create OCR engine based on type"""
        if engine_type.lower() == 'tesseract':
            return TesseractEngine(kwargs.get('config', '--oem 3 --psm 6'))
        elif engine_type.lower() == 'easyocr':
            return EasyOCREngine(kwargs.get('languages', ['en']))
        else:
            raise ValueError(f"Unknown OCR engine type: {engine_type}")
    
    @staticmethod
    def get_available_engines() -> List[str]:
        """Get list of available OCR engines"""
        engines = []
        
        # Check Tesseract availability
        try:
            pytesseract.get_tesseract_version()
            engines.append('tesseract')
        except:
            pass
        
        # Check EasyOCR availability
        try:
            import easyocr
            engines.append('easyocr')
        except:
            pass
        
        return engines

def get_best_ocr_engine() -> OCREngine:
    """Get the best available OCR engine"""
    available_engines = OCREngineFactory.get_available_engines()
    
    # Prefer EasyOCR for better accuracy
    if 'easyocr' in available_engines:
        return OCREngineFactory.create_engine('easyocr')
    elif 'tesseract' in available_engines:
        return OCREngineFactory.create_engine('tesseract')
    else:
        raise RuntimeError("No OCR engines available. Please install pytesseract or easyocr.")