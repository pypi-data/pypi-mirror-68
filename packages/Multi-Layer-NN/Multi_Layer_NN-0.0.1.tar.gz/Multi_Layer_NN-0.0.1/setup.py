from setuptools import setup

with open("./README.md", "r") as fh:
	long_description = fh.read()

setup(name = "Multi_Layer_NN",
    version = "0.0.1",
    description = "A Multy Layer Neural Network Class",
    author = "Andreas Probst",
    author_email = "andreaspadprobst@gmail.com",
    packages = ["Multi_Layer_NN"],
    zip_safe = False,
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license = "MIT",
    classifiers=[
    "License :: OSI Approved :: MIT License",],
    install_requires = [
	"matplotlib >= 2.2.5",
	"numpy >= 1.16.6",],
    )
