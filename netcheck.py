#!/usr/bin/env python3
"""
NetCheck - Main Entry Point
Cross-platform network diagnostic tool
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from netcheck.cli import main

if __name__ == '__main__':
    main()
