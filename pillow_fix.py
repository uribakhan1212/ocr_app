"""
Compatibility fix for Pillow versions
"""

from PIL import Image

# Fix for newer Pillow versions where ANTIALIAS was deprecated
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

# Also fix BICUBIC if needed
if not hasattr(Image, 'BICUBIC'):
    Image.BICUBIC = Image.Resampling.BICUBIC if hasattr(Image, 'Resampling') else 3