#!/usr/bin/env python3
"""
Installation script for spaCy and required language model.
"""

import subprocess
import sys

def install_spacy():
    """Install spaCy and the English language model."""
    print("Installing spaCy...")
    
    try:
        # Install spaCy
        subprocess.check_call([sys.executable, "-m", "pip", "install", "spacy>=3.4.0"])
        print("✓ spaCy installed successfully")
        
        # Download English language model
        print("Downloading English language model...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✓ English language model downloaded successfully")
        
        print("\nInstallation complete! You can now run the semantic breaks tool with spaCy integration.")
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Installation failed: {e}")
        print("\nYou can install manually with:")
        print("pip install spacy>=3.4.0")
        print("python -m spacy download en_core_web_sm")
        
    except Exception as e:
        print(f"✗ Unexpected error: {e}")

if __name__ == "__main__":
    install_spacy()