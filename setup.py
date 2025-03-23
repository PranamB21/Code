from setuptools import setup, find_packages
import os

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