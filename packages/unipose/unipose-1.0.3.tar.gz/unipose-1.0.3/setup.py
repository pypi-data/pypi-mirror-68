import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unipose", # Replace with your own username
    version="1.0.3",
    author="Julie Ganeshan",
    author_email="HeavenlyQueen@outlook.com",
    description="2D Pose in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sanjay-Ganeshan/UniPose",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    python_requires='>=3.7',
    dependency_links=['https://download.pytorch.org/whl/torch_stable.html'],
    install_requires=[
        "torch>=1.5.0",
        "torchvision>=0.6.0",
        "opencv-python>=4.2.0.34",
        "easydict>=1.9",
        "tqdm>=4.46.0",
        "numpy>=1.18.4"
    ],
    include_package_data=True
)