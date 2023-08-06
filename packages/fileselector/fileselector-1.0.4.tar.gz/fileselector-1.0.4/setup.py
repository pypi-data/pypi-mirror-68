from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="fileselector",
    version="1.0.4",
    description="A Python package that prints all files in a specified folder whick can be selected by the user.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="",
    author="TheAPEX, Greg M",
    author_email="greg@ap3x.xyz",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["fileselector"],
    include_package_data=True,
    install_requires=["colorama"]
)