"""
Test script for handwriting OCR functionality
"""

import sys
import traceback
from PIL import Image
import numpy as np

def test_handwriting_ocr():
    """Test the handwriting OCR engine"""
    print("🧪 Testing Handwriting OCR Engine...")
    
    try:
        # Import the handwriting engine
        from handwriting_ocr import create_handwriting_engine
        
        # Create engine
        engine = create_handwriting_engine()
        if engine is None:
            print("❌ Failed to create handwriting engine")
            return False
        
        print("✅ Handwriting OCR engine created successfully")
        
        # Create a simple test image (white background)
        img_array = np.ones((200, 600, 3), dtype=np.uint8) * 255
        test_image = Image.fromarray(img_array)
        
        # Test the engine (should return empty results for blank image)
        results = engine.extract_handwritten_text(test_image)
        print(f"✅ Engine processing works (found {len(results)} text blocks in blank image)")
        
        return True
        
    except Exception as e:
        print(f"❌ Handwriting OCR test failed: {e}")
        traceback.print_exc()
        return False

def test_pillow_fix():
    """Test the Pillow compatibility fix"""
    print("\n🧪 Testing Pillow Compatibility...")
    
    try:
        import pillow_fix
        from PIL import Image
        
        # Test if ANTIALIAS attribute exists
        if hasattr(Image, 'ANTIALIAS'):
            print("✅ Image.ANTIALIAS is available")
        else:
            print("❌ Image.ANTIALIAS not available")
            return False
        
        # Create a test image and try resizing
        img_array = np.ones((100, 100, 3), dtype=np.uint8) * 255
        test_image = Image.fromarray(img_array)
        
        # Try resizing with ANTIALIAS
        resized = test_image.resize((50, 50), Image.ANTIALIAS)
        print("✅ Image resizing with ANTIALIAS works")
        
        return True
        
    except Exception as e:
        print(f"❌ Pillow compatibility test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🔍 Testing Handwriting OCR Setup\n")
    
    all_passed = True
    
    # Test Pillow fix
    if not test_pillow_fix():
        all_passed = False
    
    # Test handwriting OCR
    if not test_handwriting_ocr():
        all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 All handwriting tests passed!")
        print("\n💡 Tips for better handwriting recognition:")
        print("• Use high-resolution images (300+ DPI)")
        print("• Ensure good contrast (dark text on light background)")
        print("• Make sure handwriting is clear and legible")
        print("• Avoid skewed or rotated images")
        print("• Try the 'Mixed' mode for documents with both printed and handwritten text")
    else:
        print("❌ Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    main()