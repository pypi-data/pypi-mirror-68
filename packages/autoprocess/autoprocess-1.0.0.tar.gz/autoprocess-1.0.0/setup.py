
from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="autoprocess",
    version="1.0.0",
    description="A Python package for cleaning, making transformation of data and variables, making visualization of varibale. All this automated script will do all such mannual work. This is very helpful for such people having vary basic knowledge of python",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/roshanfande/autoprocess",
    author="Roshan Fande",
    
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["autoprocess"],
    include_package_data=True,
    #install_requires=["requests"],

)