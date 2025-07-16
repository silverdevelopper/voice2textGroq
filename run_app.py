#!/usr/bin/env python3
"""
Script to install dependencies and run the Groq Audio Transcription app
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies using uv"""
    print("Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "uv", "sync"], check=True)
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True

def run_app():
    """Run the Gradio app"""
    print("Starting Groq Audio Transcription app...")
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running app: {e}")

if __name__ == "__main__":
    # Check if .env file exists
    if not os.path.exists(".env"):
        print("⚠️  Warning: No .env file found!")
        print("Please create a .env file with your GROQ_API_KEY")
        print("Example: GROQ_API_KEY=your_api_key_here")
        print()
    
  
        # Run the app
    run_app()
