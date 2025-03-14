[![Licence: MIT](https://img.shields.io/badge/Licence-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/-Python_≥_3.10-306998?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-360+/)

# Using Large Language Models to support researchers reproduce and reuse unpublished health care discrete-event simulation computer models: a feasibility and pilot study in Python

## Authors

* Thomas Monks &nbsp;&nbsp; [![ORCID: Monks](https://img.shields.io/badge/ORCID-0000--0003--2631--4481-brightgreen)](https://orcid.org/0000-0003-2631-4481)

* Alison Harper &nbsp;&nbsp; [![ORCID: Harper](https://img.shields.io/badge/ORCID-0000--0001--5274--5037-brightgreen)](https://orcid.org/0000-0001-5274-5037)

* Amy Heather &nbsp;&nbsp; [![ORCID: Heather](https://img.shields.io/badge/ORCID-0000--0002--6596--3479-brightgreen)](https://orcid.org/0000-0002-6596-3479)

* Navonil Mustafee &nbsp;&nbsp; [![ORCID: Mustafee](https://img.shields.io/badge/ORCID-0000--0002--2204--8924-brightgreen)](https://orcid.org/0000-0002-2204-8924)

## Creating the environment

The project uses `conda` to manage dependencies. Navigate your terminal to the directory containing the code

```
conda env create -f binder/environment.yml
```

This will create a conda environment called `gen_simpy`. To activate:

```
conda activate gen_simpy
```

## Building the Juypter Book

Once in the `gen_simpy` environment, navigate to the top level directory of the code repository in your terminal and issue the following command:

```
jb build .
```

This will build the HTML book locally on your machine.  The terminal will display a URL link that you can use to point your browser at the HTML.

## Citation

Please cite this repository as:

> Thomas Monks, Alison Harper, Amy Heather, and Navonil Mustafee. **Using Large Language Models to support researchers reproduce and reuse unpublished health care discrete-event simulation computer models: a feasibility and pilot study in Python**. <https://github.com/pythonhealthdatascience/llm_simpy>.

A `CITATION.cff` file is also provided.

<!--TODO: Archive repository on Zenodo, and cite that -->

## Funding

<!--TODO: Add funding statement-->