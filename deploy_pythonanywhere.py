#!/usr/bin/env python
"""
Deployment script for PythonAnywhere
This script helps set up the environment for PythonAnywhere deployment
"""

import os
import sys

def setup_environment():
    """Setup the environment for PythonAnywhere deployment"""
    print("Setting up PythonAnywhere deployment environment...")
    
    # Create a .pythonanywhere file to indicate this is a PythonAnywhere deployment
    with open('.pythonanywhere', 'w') as f:
        f.write('PYTHONANYWHERE_DEPLOYMENT')
    
    print("Environment setup complete!")

if __name__ == "__main__":
    setup_environment()