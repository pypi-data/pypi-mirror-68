"""
Configure Python package
https://packaging.python.org/tutorials/packaging-projects/

python setup.py sdist bdist_wheel
twine upload dist/* --skip-existing
"""

import setuptools

with open('README.md') as file:
    readme = file.read()

setuptools.setup(
    name="ufmetadata",
    description="Urban Flows Observatory (Sheffield) metadata tools",
    version="0.0.2",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Joe Heffer",
    author_email="j.heffer@sheffield.ac.uk",
    url='https://github.com/Joe-Heffer-Shef/ufmetadata',
)
