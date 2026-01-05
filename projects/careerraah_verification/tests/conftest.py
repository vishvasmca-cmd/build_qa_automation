"""Pytest configuration for CareerRaah verification tests"""
import sys
import os

# Add project root to path so 'pages' module can be imported
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
