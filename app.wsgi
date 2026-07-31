import sys
import os

# Add the project directory to the sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.main import app as application
