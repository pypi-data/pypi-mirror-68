from setuptools import setup

with open("./README.md", "r") as fh:
	long_description = fh.read()

setup(name = "Multi_Layer_NN_Package",
    version = "0.1.2",
    description = "A Multy Layer Neural Network Class",
    author = "Andreas Probst",
    packages = ["Multi_Layer_NN"],
    author_email = "andreaspadprobst@gmail.com",
    zip_safe = False,
    long_description = long_description,
    long_description_content_type = "text/markdown",
    install_requires = [
	"matplotlib >= 2.2.5",
	"numpy >= 1.16.6",],
    )
