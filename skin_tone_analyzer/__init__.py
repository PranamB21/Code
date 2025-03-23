import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute path of the package directory
package_dir = os.path.dirname(os.path.abspath(__file__))
logger.info(f"Package directory: {package_dir}")

# Log current working directory and Python path
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Python path: {sys.path}")

# Add the package directory to Python path if not already there
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)
    logger.info(f"Added {package_dir} to Python path")

# Verify file exists
skin_tone_path = os.path.join(package_dir, 'skin_tone.py')
logger.info(f"Looking for skin_tone.py at: {skin_tone_path}")

if not os.path.exists(skin_tone_path):
    logger.error(f"skin_tone.py not found at {skin_tone_path}")
    logger.error(f"Directory contents: {os.listdir(package_dir)}")
    logger.error(f"Parent directory contents: {os.listdir(os.path.dirname(package_dir))}")
    raise FileNotFoundError(f"skin_tone.py not found at {skin_tone_path}")

try:
    # Try to import the module
    from .skin_tone import process_image, detect_skin_tone, recommend_colors, create_color_preview
    logger.info("Successfully imported skin_tone module")
except ImportError as e:
    logger.error(f"Error importing from skin_tone: {e}")
    logger.error(f"Current directory: {os.getcwd()}")
    logger.error(f"Package directory: {package_dir}")
    logger.error(f"Python path: {sys.path}")
    logger.error(f"Directory contents: {os.listdir(package_dir)}")
    raise

__all__ = ['process_image', 'detect_skin_tone', 'recommend_colors', 'create_color_preview'] 