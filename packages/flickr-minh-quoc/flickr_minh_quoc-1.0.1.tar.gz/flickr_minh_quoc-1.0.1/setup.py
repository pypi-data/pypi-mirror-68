from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

__author__ = "Minh Quoc"
__version__ = "1.0.1"
__email__ = "minh.nong@f4.intek.edu.vn"


setup(
    install_requires=[
        "certifi==2020.4.5.1",
        "chardet==3.0.4",
        "idna==2.9",
        "langdetect==1.0.8",
        "requests==2.23.0",
        "six==1.14.0",
        "urllib3==1.25.9",
    ],
    name="flickr_minh_quoc",  # Replace with your own username
    version=__version__,
    author=__author__,
    author_email=__email__,
    description="A useful tool to mirror flickr photo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/intek-training-jsc/flickr-mirroring-nvqMinh29101992/",
    packages=["flickr_pkg"],
    entry_points={
        "console_scripts": [
            "mirror_flickr=flickr_pkg.__main__:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
