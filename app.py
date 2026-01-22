import streamlit as st
from PIL import Image
import pandas as pd
import io
import time
from typing import List, Dict, Optional

# Import custom modules
from config import STREAMLIT_CONFIG, MAX_FILE_SIZE_MB, ALLOWED_EXTENSIONS
from utils import (
    enhance_image_quality, resize_image_if_needed, validate_image,
    display_processing_stats, clean_text
)
from ocr_engine import OCREngineFactory, get_best_ocr_engine
from document_generator import WordDocumentGenerator

# Configure page
st.set_page_config(**STREAMLIT_CONFIG)

class ImageToWordConverter:
    """Main converter class that orchestrates the conversion process"""
    
    def __init__(self, ocr_engine_type: str = "easyocr"):
        self.ocr_engine = OCREngineFactory.create_engine(ocr_engine_type)
        if self.ocr_engine is None:
            self.ocr_engine = get_best_ocr_engine()
    
    def process_image(self, image: Image.Image, 
                     enhance_quality: bool = True,
                     detect_tables: bool = True) -> Dict:
        """Process image and extract all content"""
        start_time = time.time()
        
        # Enhance image quality if requested
        if enhance_quality:
            image = enhance_image_quality(image)
            image = resize_image_if_needed(image)
        
        # Extract text with positions
        text_blocks = self.ocr_engine.extract_text_with_positions(image)
        
        if not text_blocks:
            return {
                'text_blocks': [],
                'formatted_text': '',
                'tables': [],
                'processing_time': time.time() - start_time,
                'success': False,
                'error': 'No text detected in image'
            }
        
        # Format text maintaining structure
        formatted_text = self._format_text_structure(text_blocks)
        
        # Detect tables if requested
        tables = []
        if detect_tables:
            tables = self._detect_tables(text_blocks)
        
        processing_time = time.time() - start_time
        
        return {
            'text_blocks': text_blocks,
            'formatted_text': formatted_text,
            'tables': tables,
            'processing_time': processing_time,
            'success': True,
            'error': None
        }
    
    def _format_text_structure(self, text_blocks: List[Dict]) -> str:
        """Format text maintaining structure and paragraphs"""
        if not text_blocks:
            return ""
        
        formatted_text = ""
        current_paragraph = []
        last_y = None
        line_height_threshold = 30
        
        for block in text_blocks:
            text = clean_text(block['text'])
            y_pos = block['y_center']
            
            # Check if this is a new paragraph (significant vertical gap)
            if last_y is not None and abs(y_pos - last_y) > line_height_threshold:
                if current_paragraph:
                    formatted_text += " ".join(current_paragraph) + "\n\n"
                    current_paragraph = []
            
            current_paragraph.append(text)
            last_y = y_pos
        
        # Add the last paragraph
        if current_paragraph:
            formatted_text += " ".join(current_paragraph)
        
        return formatted_text.strip()
    
    def _detect_tables(self, text_blocks: List[Dict]) -> List[List[str]]:
        """Detect and extract table-like structures"""
        # Group text blocks by similar y-coordinates (rows)
        rows = []
        current_row = []
        current_y = None
        y_threshold = 20  # pixels
        
        for block in text_blocks:
            if current_y is None or abs(block['y_center'] - current_y) < y_threshold:
                current_row.append(block)
                current_y = block['y_center'] if current_y is None else current_y
            else:
                if current_row:
                    rows.append(sorted(current_row, key=lambda x: x['x_center']))
                current_row = [block]
                current_y = block['y_center']
        
        if current_row:
            rows.append(sorted(current_row, key=lambda x: x['x_center']))
        
        # Convert to table format if multiple columns detected
        tables = []
        for row in rows:
            if len(row) > 1:  # Potential table row
                table_row = [clean_text(block['text']) for block in row]
                tables.append(table_row)
        
        return tables if len(tables) > 1 else []
    
    def create_word_document(self, 
                           text_content: str,
                           tables: List[List[str]],
                           original_image: Optional[Image.Image] = None,
                           text_blocks: Optional[List[Dict]] = None) -> bytes:
        """Create Word document from extracted content"""
        generator = WordDocumentGenerator()
        return generator.create_complete_document(
            text_content=text_content,
            tables=tables,
            original_image=original_image,
            text_blocks=text_blocks
        )

def main():
    """Main Streamlit application"""
    st.title("📄 Image to Word Document Converter")
    st.markdown("""
    **Transform images containing text, tables, and graphics into editable Word documents**
    
    This application uses advanced OCR technology to extract text while preserving formatting and structure.
    """)
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # OCR Engine selection
    available_engines = OCREngineFactory.get_available_engines()
    if not available_engines:
        st.error("No OCR engines available. Please install pytesseract or easyocr.")
        return
    
    engine_options = {
        'easyocr': 'EasyOCR (Recommended)',
        'tesseract': 'Tesseract OCR'
    }
    
    selected_engine = st.sidebar.selectbox(
        "Select OCR Engine",
        options=available_engines,
        format_func=lambda x: engine_options.get(x, x),
        help="EasyOCR generally provides better accuracy for complex layouts"
    )
    
    # Processing options
    st.sidebar.subheader("🔧 Processing Options")
    enhance_quality = st.sidebar.checkbox("Enhance Image Quality", value=True, 
                                         help="Apply image enhancement for better OCR results")
    detect_tables = st.sidebar.checkbox("Detect Tables", value=True,
                                       help="Automatically detect and extract table structures")
    include_original_image = st.sidebar.checkbox("Include Original Image", value=True,
                                                help="Include the original image in the Word document")
    include_confidence = st.sidebar.checkbox("Include Confidence Scores", value=True,
                                           help="Add OCR confidence statistics to the document")
    
    # File size limit info
    st.sidebar.info(f"📁 Maximum file size: {MAX_FILE_SIZE_MB}MB")
    st.sidebar.info(f"📋 Supported formats: {', '.join(ALLOWED_EXTENSIONS)}")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Upload Image")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=ALLOWED_EXTENSIONS,
            help="Upload an image containing text, tables, or graphics"
        )
        
        if uploaded_file is not None:
            # Validate image
            is_valid, message = validate_image(uploaded_file)
            
            if not is_valid:
                st.error(f"❌ {message}")
                return
            
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="📷 Uploaded Image", use_column_width=True)
            
            # Image info
            file_size_mb = uploaded_file.size / (1024 * 1024)
            st.info(f"📊 Image: {image.size[0]} × {image.size[1]} pixels | Size: {file_size_mb:.2f} MB")
    
    with col2:
        st.header("🔄 Processing Results")
        
        if uploaded_file is not None:
            # Process button
            if st.button("🚀 Convert to Word Document", type="primary"):
                with st.spinner("🔍 Processing image... This may take a few moments."):
                    try:
                        # Initialize converter
                        converter = ImageToWordConverter(selected_engine)
                        
                        # Process image
                        result = converter.process_image(
                            image, 
                            enhance_quality=enhance_quality,
                            detect_tables=detect_tables
                        )
                        
                        if not result['success']:
                            st.warning(f"⚠️ {result['error']}")
                            st.info("💡 Try adjusting the image quality or using a different OCR engine.")
                            return
                        
                        # Display results
                        text_blocks = result['text_blocks']
                        formatted_text = result['formatted_text']
                        tables = result['tables']
                        processing_time = result['processing_time']
                        
                        # Show extracted text
                        st.subheader("📝 Extracted Text")
                        if formatted_text:
                            st.text_area("Text Content", formatted_text, height=200, 
                                       help="This is the extracted text that will be included in the Word document")
                        else:
                            st.warning("No text content extracted.")
                        
                        # Show tables if found
                        if tables:
                            st.subheader("📊 Detected Tables")
                            for i, table in enumerate(tables[:3]):  # Show first 3 tables
                                st.write(f"**Table {i+1}:**")
                                try:
                                    # Create DataFrame for better display
                                    if len(table) > 1:
                                        df = pd.DataFrame(table[1:], columns=table[0])
                                    else:
                                        df = pd.DataFrame(table)
                                    st.dataframe(df, use_container_width=True)
                                except:
                                    # Fallback to simple table display
                                    for row in table:
                                        st.write(" | ".join(row))
                                st.write("")
                        
                        # Generate Word document
                        st.subheader("📄 Generate Document")
                        
                        with st.spinner("📝 Creating Word document..."):
                            doc_bytes = converter.create_word_document(
                                text_content=formatted_text,
                                tables=tables,
                                original_image=image if include_original_image else None,
                                text_blocks=text_blocks if include_confidence else None
                            )
                        
                        # Download button
                        filename = f"extracted_document_{uploaded_file.name.split('.')[0]}.docx"
                        st.download_button(
                            label="📥 Download Word Document",
                            data=doc_bytes,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            help="Click to download the generated Word document"
                        )
                        
                        # Processing statistics
                        st.subheader("📈 Processing Statistics")
                        display_processing_stats(text_blocks, tables, processing_time)
                        
                        # Success message
                        st.success("✅ Document generated successfully!")
                        
                    except Exception as e:
                        st.error(f"❌ An error occurred during processing: {str(e)}")
                        st.info("💡 Please try with a different image or check the image quality.")
                        
                        # Debug info for developers
                        with st.expander("🔧 Debug Information"):
                            st.code(str(e))
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Built with ❤️ using Streamlit | Powered by EasyOCR & Tesseract</p>
        <p><small>For best results, use high-quality images with clear text</small></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()