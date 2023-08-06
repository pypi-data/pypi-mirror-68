
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JoeLiu-RF Refactoring",
    version="1.0.6",
    author="Joe Liu",
    author_email="angrybirdliu@gmail.com",
    description="RF Refactoring package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JoeLiu1321/RF-Refactoring",
    packages=["rfrefactoring"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['robotframework']
)