from setuptools import setup, find_packages
import os
import shutil

def copy_skin_tone_file():
    """Copy skin_tone.py to the package directory during installation."""
    source = os.path.join('Python', 'skin_tone.py')
    dest_dir = 'skin_tone_analyzer'
    dest = os.path.join(dest_dir, 'skin_tone.py')
    
    print(f"Copying {source} to {dest}")
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copy2(source, dest)
    return [dest]

# Ensure the file is copied
if os.path.exists('Python/skin_tone.py'):
    copied_files = copy_skin_tone_file()
else:
    raise FileNotFoundError("skin_tone.py not found in Python directory")

setup(
    name="skin_tone_analyzer",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'skin_tone_analyzer': ['*.py'],
    },
    data_files=[
        ('skin_tone_analyzer', copied_files),
    ],
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