# coding: utf-8
"""
@author: Nelson Zhao
@date:   2020/5/10 7:27 PM
@email:  dutzhaoyeyu@163.com
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="deepforecast",
    version="0.0.2",
    author="Nelson Zhao",
    author_email="dutzhaoyeyu@163.com",
    description="An easy-to-use deep model for time series forecast",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NELSONZHAO/DeepForecast",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)