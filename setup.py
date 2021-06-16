import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="py-steamcmd-wrapper",  # Replace with your own username
    version="1.0.6",
    author="Wouter Mellema",
    author_email="info@woutermellema.nl",
    description="Python wrapper for SteamCMD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wmellema/pysteamcmdwrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires='>=3.6',
    install_requires=['requests'],
)
