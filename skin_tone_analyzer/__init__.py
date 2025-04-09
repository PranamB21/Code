import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the absolute path of the package directory
package_dir = os.path.dirname(os.path.abspath(__file__))

# Add package directory to Python path
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

try:
    from .skin_tone import process_image, detect_skin_tone, recommend_colors, create_color_preview
    logger.info("Successfully imported skin_tone module")
except ImportError as e:
    logger.error(f"Error importing from skin_tone: {e}")
    raise

__all__ = ['process_image', 'detect_skin_tone', 'recommend_colors', 'create_color_preview'] 