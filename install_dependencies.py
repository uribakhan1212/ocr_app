"""
Installation script for system dependencies
"""

import subprocess
import sys
import platform
import os

def install_tesseract():
    """Install Tesseract OCR based on the operating system"""
    system = platform.system().lower()
    
    print("Installing Tesseract OCR...")
    
    if system == "windows":
        print("For Windows:")
        print("1. Download Tesseract installer from: https://github.com/UB-Mannheim/tesseract/wiki")
        print("2. Install Tesseract and add it to your PATH")
        print("3. Or use chocolatey: choco install tesseract")
        
    elif system == "darwin":  # macOS
        try:
            subprocess.run(["brew", "install", "tesseract"], check=True)
            print("✅ Tesseract installed successfully via Homebrew")
        except subprocess.CalledProcessError:
            print("❌ Failed to install via Homebrew")
            print("Please install Homebrew first: https://brew.sh/")
            print("Then run: brew install tesseract")
            
    elif system == "linux":
        try:
            # Try apt-get first (Ubuntu/Debian)
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "tesseract-ocr"], check=True)
            print("✅ Tesseract installed successfully via apt-get")
        except subprocess.CalledProcessError:
            try:
                # Try yum (CentOS/RHEL)
                subprocess.run(["sudo", "yum", "install", "-y", "tesseract"], check=True)
                print("✅ Tesseract installed successfully via yum")
            except subprocess.CalledProcessError:
                print("❌ Failed to install Tesseract automatically")
                print("Please install manually using your package manager")

def install_python_packages():
    """Install Python packages from requirements.txt"""
    print("Installing Python packages...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Python packages installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python packages: {e}")
        return False
    
    return True

def verify_installation():
    """Verify that all dependencies are installed correctly"""
    print("\nVerifying installation...")
    
    # Check Python packages
    required_packages = [
        'streamlit', 'pytesseract', 'PIL', 'docx', 'pandas', 
        'cv2', 'numpy', 'easyocr'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            elif package == 'cv2':
                import cv2
            elif package == 'docx':
                import docx
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    # Check Tesseract
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        print("✅ Tesseract OCR")
    except Exception as e:
        print(f"❌ Tesseract OCR: {e}")
        missing_packages.append("tesseract")
    
    if missing_packages:
        print(f"\n❌ Missing dependencies: {', '.join(missing_packages)}")
        return False
    else:
        print("\n✅ All dependencies installed successfully!")
        return True

def main():
    """Main installation function"""
    print("🚀 Setting up Image to Word Converter dependencies...\n")
    
    # Install Python packages
    if not install_python_packages():
        print("❌ Failed to install Python packages. Please check your internet connection and try again.")
        return
    
    # Install Tesseract
    install_tesseract()
    
    # Verify installation
    if verify_installation():
        print("\n🎉 Setup complete! You can now run the application with:")
        print("streamlit run app.py")
    else:
        print("\n⚠️ Some dependencies are missing. Please install them manually and run this script again.")

if __name__ == "__main__":
    main()