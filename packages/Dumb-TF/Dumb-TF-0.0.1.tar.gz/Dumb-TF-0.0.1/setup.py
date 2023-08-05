import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Dumb-TF",
    version="0.0.1",
    author="Siddharth Panda",
    author_email="siddharth.pandathedancer@gmail.com",
    description="A deep learning library for dumb people",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sidray-Infinity/DumbTF",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
