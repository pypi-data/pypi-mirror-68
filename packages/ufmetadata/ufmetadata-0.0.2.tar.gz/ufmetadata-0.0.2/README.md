# Urban Flows Observatory metadata tools

These are tools and classes to help work with metadata in the [Urban Flows Observatory](https://urbanflows.ac.uk/).

* [ufmetadata](https://github.com/Joe-Heffer-Shef/ufmetadata) on Github
* [ufmetadata](https://pypi.org/project/ufmetadata/) on PyPi

## Installation

### Using Python virtual environments

Create a `venv`:

```bash
$ python -m venv my_environment
$ pip install ufmetadata
```

### Using Conda

Create a Conda environment and use pip to install the package from the repository:

```bash
$ conda env create --name my_environment --file environment.yml
```

...where `environment.yml` contains:

```yaml
name: my_environment
channels:
  - defaults
dependencies:
  - python
  - pip
  - pip:
    - ufmetadata
```

## Usage

To view the documentation in Python:

```python
import ufmetadata.assets

help(ufmetadata.assets.Site)
help(ufmetadata.assets.Sensor)
```
