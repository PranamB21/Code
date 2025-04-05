import os
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from .skin_tone import process_image, detect_skin_tone, recommend_colors, create_color_preview
    logger.info("Successfully imported skin_tone module")
except ImportError as e:
    logger.error(f"Error importing from skin_tone: {e}")
    logger.error(f"Current directory: {os.getcwd()}")
    logger.error(f"Package directory: {os.path.dirname(os.path.abspath(__file__))}")
    logger.error(f"Directory contents: {os.listdir(os.path.dirname(os.path.abspath(__file__)))}")
    raise

__all__ = ['process_image', 'detect_skin_tone', 'recommend_colors', 'create_color_preview'] 