"""
Test script to verify the installation and basic functionality
"""

import sys
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✅ Streamlit")
    except ImportError as e:
        print(f"❌ Streamlit: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ PIL (Pillow)")
    except ImportError as e:
        print(f"❌ PIL: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ Pandas")
    except ImportError as e:
        print(f"❌ Pandas: {e}")
        return False
    
    try:
        import cv2
        print("✅ OpenCV")
    except ImportError as e:
        print(f"❌ OpenCV: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy")
    except ImportError as e:
        print(f"❌ NumPy: {e}")
        return False
    
    try:
        from docx import Document
        print("✅ python-docx")
    except ImportError as e:
        print(f"❌ python-docx: {e}")
        return False
    
    try:
        import pytesseract
        print("✅ pytesseract")
    except ImportError as e:
        print(f"❌ pytesseract: {e}")
        return False
    
    try:
        import easyocr
        print("✅ EasyOCR")
    except ImportError as e:
        print(f"❌ EasyOCR: {e}")
        return False
    
    return True

def test_custom_modules():
    """Test if custom modules can be imported"""
    print("\nTesting custom modules...")
    
    try:
        from config import STREAMLIT_CONFIG
        print("✅ config.py")
    except ImportError as e:
        print(f"❌ config.py: {e}")
        return False
    
    try:
        from utils import enhance_image_quality
        print("✅ utils.py")
    except ImportError as e:
        print(f"❌ utils.py: {e}")
        return False
    
    try:
        from ocr_engine import OCREngineFactory
        print("✅ ocr_engine.py")
    except ImportError as e:
        print(f"❌ ocr_engine.py: {e}")
        return False
    
    try:
        from document_generator import WordDocumentGenerator
        print("✅ document_generator.py")
    except ImportError as e:
        print(f"❌ document_generator.py: {e}")
        return False
    
    return True

def test_ocr_engines():
    """Test OCR engines availability"""
    print("\nTesting OCR engines...")
    
    # Test Tesseract
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract OCR v{version}")
    except Exception as e:
        print(f"❌ Tesseract OCR: {e}")
    
    # Test EasyOCR
    try:
        import easyocr
        reader = easyocr.Reader(['en'], gpu=False)
        print("✅ EasyOCR initialized successfully")
    except Exception as e:
        print(f"❌ EasyOCR: {e}")

def test_basic_functionality():
    """Test basic functionality with a simple example"""
    print("\nTesting basic functionality...")
    
    try:
        from PIL import Image
        import numpy as np
        from ocr_engine import OCREngineFactory
        
        # Create a simple test image with text
        img_array = np.ones((100, 300, 3), dtype=np.uint8) * 255
        test_image = Image.fromarray(img_array)
        
        # Try to create an OCR engine
        available_engines = OCREngineFactory.get_available_engines()
        if available_engines:
            engine = OCREngineFactory.create_engine(available_engines[0])
            print(f"✅ OCR engine created: {available_engines[0]}")
        else:
            print("❌ No OCR engines available")
            return False
        
        # Test document generation
        from document_generator import WordDocumentGenerator
        generator = WordDocumentGenerator()
        doc_bytes = generator.create_complete_document(
            text_content="Test content",
            tables=[],
            original_image=None,
            text_blocks=None
        )
        print("✅ Document generation works")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Image to Word Converter Installation\n")
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test custom modules
    if not test_custom_modules():
        all_passed = False
    
    # Test OCR engines
    test_ocr_engines()
    
    # Test basic functionality
    if not test_basic_functionality():
        all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check the installation.")
        print("\nTo fix issues:")
        print("1. Run: python install_dependencies.py")
        print("2. Install missing packages manually")
        print("3. Check Tesseract installation")

if __name__ == "__main__":
    main()