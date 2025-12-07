#!/usr/bin/env python3
"""
Hostel Management System - Standalone Runner
This script automatically detects available dependencies and runs the application.
"""

import sys
import subprocess
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_and_install_dependencies():
    """Check for required dependencies and install if missing"""
    required_packages = {
        'pandas': 'pandas'
    }
    
    optional_packages = {
        'mysql.connector': 'mysql-connector-python',
        'reportlab': 'reportlab'
    }
    
    print("Checking dependencies...")
    
    # Check required packages
    for module, package in required_packages.items():
        try:
            __import__(module)
            print(f"✓ {package} is available")
        except ImportError:
            print(f"✗ {package} not found. Installing...")
            if install_package(package):
                print(f"✓ {package} installed successfully")
            else:
                print(f"✗ Failed to install {package}")
                return False
    
    # Check optional packages
    for module, package in optional_packages.items():
        try:
            if module == 'mysql.connector':
                import mysql.connector
            else:
                __import__(module)
            print(f"✓ {package} is available")
        except ImportError:
            print(f"⚠ {package} not found (optional - will use CSV storage)")
    
    return True

def run_application():
    """Run the tkinter application"""
    print("\nStarting Hostel Management System...")
    print("Default credentials:")
    print("  Admin: admin / admin123")
    print("  Student: student1 / student123")
    print("\nPress Ctrl+C to stop the application.\n")
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\nApplication stopped.")
    except Exception as e:
        print(f"Error running application: {e}")

def main():
    """Main function"""
    print("=" * 50)
    print("Hostel Management System")
    print("=" * 50)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check and install dependencies
    if check_and_install_dependencies():
        run_application()
    else:
        print("Failed to install required dependencies. Please install manually:")
        print("pip install pandas")

if __name__ == "__main__":
    main()