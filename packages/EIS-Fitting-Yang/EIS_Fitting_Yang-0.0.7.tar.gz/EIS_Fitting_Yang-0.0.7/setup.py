import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EIS_Fitting_Yang", # Replace with your own username
    version="0.0.7",
    author="Tianrang Yang",
    author_email="tianrangyang@gmail.com",
    description="CNLS fitting for EIS spectra",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=" ",
    packages=['EIS_Fitting_Yang'],
    install_requires=[
        'numpy',
        'pandas',
        'mpmath',
        'matplotlib',
        'lmfit'
        
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
