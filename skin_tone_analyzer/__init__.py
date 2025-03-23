import os
import sys

# Get the absolute path of the package directory
package_dir = os.path.dirname(os.path.abspath(__file__))
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

try:
    from .skin_tone import process_image, detect_skin_tone, recommend_colors, create_color_preview
except ImportError as e:
    print(f"Error importing from skin_tone: {e}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Package directory: {package_dir}")
    print(f"Python path: {sys.path}")
    raise

__all__ = ['process_image', 'detect_skin_tone', 'recommend_colors', 'create_color_preview'] 