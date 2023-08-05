import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chattest",
    version="0.0.10",
    author="simon",
    author_email="simon@gmail.com",
    description="Chat test.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jshmSimon/chattest",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
