[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-360+/)
[![PyPI version fury.io](https://badge.fury.io/py/treat-sim.svg)](https://pypi.org/project/treat-sim/)
[![ORCID: Harper](https://img.shields.io/badge/ORCID-0000--0001--5274--5037-brightgreen)](https://orcid.org/0000-0001-5274-5037)
[![ORCID: Monks](https://img.shields.io/badge/ORCID-0000--0003--2631--4481-brightgreen)](https://orcid.org/0000-0003-2631-4481)

# Using Large Language Models to support researchers reproduce and reuse unpublished health care discrete-event simulation computer models: a feasibility and pilot study in Python

## Authors

* Thomas Monks [![ORCID: Monks](https://img.shields.io/badge/ORCID-0000--0003--2631--4481-brightgreen)](https://orcid.org/0000-0003-2631-4481)
* Alison Harper [![ORCID: Harper](https://img.shields.io/badge/ORCID-0000--0001--5274--5037-brightgreen)](https://orcid.org/0000-0001-5274-5037)

* Navonil Mustafee [![ORCID: Harper](https://img.shields.io/badge/ORCID-0000--0001--5274--5037-brightgreen)](https://orcid.org/0000-0002-2204-8924)

## Creating the virtual environment

The project uses `conda` to manage dependencies. Navigate your terminal to the directory containing the code

```
conda env create -f binder/environment.yml
```

This will create a conda virtual environment called `gen_simpy`. To activate:

```
conda activate gen_simpy
```

## Building the Juypter Book

One in the `gen_simpy` environment navigate to the top level directory of the code repository in your terminal and issue the following command:

```
jb buid .
```

This will build the HTML book locally on your machine.  The terminal will display a URL link that you can use to point your browser at the HTML.
