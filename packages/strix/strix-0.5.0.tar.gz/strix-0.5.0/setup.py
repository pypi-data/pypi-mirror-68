import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="strix",
    version="0.5.0",
    author="HFM3",
    # author_email="author@example.com",
    description="A Python Package for field-based GIS work",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/HFM3/strix',
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
        "Programming Language :: Python :: 3.8",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
    ],
    python_requires='>=3.8',
)

# https://github.com/pypa/sampleproject/blob/master/setup.py
