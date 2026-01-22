"""
Simple script to run the Image to Word Converter application
"""

import subprocess
import sys
import os

def check_streamlit():
    """Check if Streamlit is installed"""
    try:
        import streamlit
        return True
    except ImportError:
        return False

def install_requirements():
    """Install requirements if needed"""
    print("Installing requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def run_app():
    """Run the Streamlit application"""
    print("🚀 Starting Image to Word Converter...")
    print("📱 The application will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("\n⚠️  To stop the application, press Ctrl+C in this terminal\n")
    
    try:
        subprocess.run(["streamlit", "run", "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to run the application: {e}")
        print("\n💡 Try running manually:")
        print("streamlit run app.py")
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")

def main():
    """Main function"""
    print("📄 Image to Word Converter - Startup Script")
    print("=" * 50)
    
    # Check if app.py exists
    if not os.path.exists("app.py"):
        print("❌ app.py not found in current directory")
        print("Please run this script from the project directory")
        return
    
    # Check Streamlit installation
    if not check_streamlit():
        print("❌ Streamlit not found. Installing requirements...")
        if not install_requirements():
            print("❌ Failed to install requirements")
            print("Please run: pip install -r requirements.txt")
            return
    
    # Run the application
    run_app()

if __name__ == "__main__":
    main()