# 📄 Image to Word Document Converter

A powerful SaaS application that converts images containing text, tables, and graphics into editable Word documents using advanced OCR technology.

## ✨ Features

- **Advanced OCR**: Uses EasyOCR and Tesseract for high-accuracy text extraction
- **Table Detection**: Automatically detects and preserves table structures
- **Format Preservation**: Maintains text formatting, paragraphs, and layout
- **Multiple Formats**: Supports PNG, JPG, JPEG, BMP, TIFF, and WebP images
- **Professional Output**: Generates well-formatted Word documents with styling
- **Confidence Scoring**: Provides OCR confidence metrics for quality assessment
- **Image Enhancement**: Automatic image preprocessing for better results
- **User-Friendly Interface**: Clean, intuitive Streamlit web interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd image-to-word-converter
   ```

2. **Install dependencies automatically**
   ```bash
   python install_dependencies.py
   ```

   Or install manually:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR** (if not installed automatically):
   
   **Windows:**
   - Download from [GitHub Releases](https://github.com/UB-Mannheim/tesseract/wiki)
   - Or use Chocolatey: `choco install tesseract`
   
   **macOS:**
   ```bash
   brew install tesseract
   ```
   
   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt-get update
   sudo apt-get install tesseract-ocr
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## 📖 Usage

1. **Upload an Image**: Click "Choose an image file" and select your image
2. **Configure Settings**: Adjust OCR engine and processing options in the sidebar
3. **Process**: Click "Convert to Word Document" to start the conversion
4. **Review Results**: Check the extracted text and detected tables
5. **Download**: Click "Download Word Document" to get your converted file

### Supported Image Types

- PNG (.png)
- JPEG (.jpg, .jpeg)
- BMP (.bmp)
- TIFF (.tiff)
- WebP (.webp)

### Best Practices for Optimal Results

- Use high-resolution images (300 DPI or higher)
- Ensure good contrast between text and background
- Avoid blurry or skewed images
- For tables, ensure clear cell boundaries
- Keep file size under 10MB

## 🛠️ Configuration Options

### OCR Engines

- **EasyOCR (Recommended)**: Better accuracy for complex layouts and multiple languages
- **Tesseract OCR**: Fast processing, good for simple text documents

### Processing Options

- **Enhance Image Quality**: Applies preprocessing to improve OCR accuracy
- **Detect Tables**: Automatically identifies and extracts table structures
- **Include Original Image**: Embeds the source image in the Word document
- **Include Confidence Scores**: Adds OCR quality metrics to the document

## 📁 Project Structure

```
image-to-word-converter/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration settings
├── utils.py              # Utility functions
├── ocr_engine.py         # OCR engine implementations
├── document_generator.py # Word document generation
├── install_dependencies.py # Dependency installation script
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🔧 Technical Details

### OCR Technology

The application uses two OCR engines:

1. **EasyOCR**: Deep learning-based OCR with support for 80+ languages
2. **Tesseract**: Google's open-source OCR engine with excellent accuracy

### Image Processing Pipeline

1. **Image Enhancement**: Contrast and sharpness adjustment
2. **Preprocessing**: Noise reduction and adaptive thresholding
3. **Text Extraction**: OCR with position information
4. **Structure Analysis**: Paragraph and table detection
5. **Document Generation**: Professional Word document creation

### Table Detection Algorithm

- Groups text blocks by vertical position (rows)
- Identifies columns by horizontal alignment
- Validates table structure with minimum row/column requirements
- Preserves cell content and formatting

## 🎯 Use Cases

- **Document Digitization**: Convert scanned documents to editable format
- **Data Entry**: Extract information from forms and invoices
- **Academic Research**: Digitize printed materials and papers
- **Business Process**: Convert receipts, contracts, and reports
- **Accessibility**: Make printed content searchable and editable

## 🔍 Troubleshooting

### Common Issues

**"No OCR engines available"**
- Install Tesseract OCR or EasyOCR dependencies
- Run `python install_dependencies.py`

**"No text detected in image"**
- Check image quality and contrast
- Try image enhancement option
- Ensure text is clearly visible

**Poor OCR accuracy**
- Use higher resolution images
- Enable image enhancement
- Try different OCR engines
- Ensure good lighting in original image

**Large file processing slow**
- Resize images to reasonable dimensions
- Use JPEG format for photographs
- Enable image enhancement for better preprocessing

### Performance Tips

- Images larger than 2000px are automatically resized
- Use PNG for text documents, JPEG for photographs
- Enable GPU acceleration for EasyOCR (requires CUDA)
- Process images in batches for multiple files

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Development Setup

1. Fork the repository
2. Create a virtual environment
3. Install development dependencies
4. Make your changes
5. Test thoroughly
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [EasyOCR](https://github.com/JaidedAI/EasyOCR) for excellent OCR capabilities
- [Tesseract](https://github.com/tesseract-ocr/tesseract) for reliable text recognition
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [python-docx](https://python-docx.readthedocs.io/) for Word document generation

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Search existing issues in the repository
3. Create a new issue with detailed information
4. Include sample images and error messages

---

**Built with ❤️ using Python and Streamlit**