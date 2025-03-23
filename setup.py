from setuptools import setup, find_packages
import os
import shutil

# Get the absolute path of the package directory
package_dir = os.path.dirname(os.path.abspath(__file__))
python_dir = os.path.join(package_dir, 'Python')
skin_tone_analyzer_dir = os.path.join(package_dir, 'skin_tone_analyzer')

# Ensure skin_tone_analyzer directory exists
os.makedirs(skin_tone_analyzer_dir, exist_ok=True)

# Copy skin_tone.py if it doesn't exist in skin_tone_analyzer
source_file = os.path.join(python_dir, 'skin_tone.py')
target_file = os.path.join(skin_tone_analyzer_dir, 'skin_tone.py')
if os.path.exists(source_file) and not os.path.exists(target_file):
    shutil.copy2(source_file, target_file)
    print(f"Copied {source_file} to {target_file}")

setup(
    name="skin_tone_analyzer",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'skin_tone_analyzer': ['*.py'],
    },
    install_requires=[
        'flask==2.0.1',
        'Werkzeug==2.0.3',
        'gunicorn==20.1.0',
        'matplotlib==3.7.1',
        'numpy==1.24.3',
        'opencv-python-headless==4.8.0.76',
        'Pillow==9.5.0'
    ],
    python_requires='>=3.11',
    zip_safe=False,
    package_dir={'': '.'},
) 