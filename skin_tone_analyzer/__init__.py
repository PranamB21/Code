import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute path of the package directory
package_dir = os.path.dirname(os.path.abspath(__file__))
logger.info(f"Package directory: {package_dir}")

# Add the package directory to Python path if not already there
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)
    logger.info(f"Added {package_dir} to Python path")

# Log current Python path
logger.info(f"Python path: {sys.path}")

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