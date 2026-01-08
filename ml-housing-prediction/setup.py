"""
Setup script for the ML Housing Prediction project.
Initializes the project with data generation and model training.
"""

import os
import sys
import subprocess

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"  {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False)
        if result.returncode != 0:
            print(f"❌ Error running: {description}")
            return False
        print(f"✓ {description} completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main setup function."""
    print("\n" + "="*60)
    print("  ML Housing Prediction - Project Setup")
    print("="*60)
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ required")
        return False
    
    print(f"✓ Python {sys.version.split()[0]} detected")
    
    # Step 1: Install dependencies
    if not run_command(
        "pip install -r requirements.txt",
        "Installing dependencies"
    ):
        return False
    
    # Step 2: Generate data
    if not run_command(
        "python data/generate_data.py",
        "Generating housing dataset"
    ):
        return False
    
    # Step 3: Train model
    if not run_command(
        "python -m src.train_model",
        "Training ML model"
    ):
        return False
    
    print("\n" + "="*60)
    print("  ✓ Setup completed successfully!")
    print("="*60)
    print("\nNext steps:")
    print("  1. Test predictions: python -m src.predict")
    print("  2. Start API:        python app.py")
    print("  3. View API docs:    http://localhost:5000/api/docs")
    print("\n")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
