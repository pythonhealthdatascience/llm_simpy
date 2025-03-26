[![Licence: MIT](https://img.shields.io/badge/Licence-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/-Python_≥_3.10-306998?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-360+/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15090961.svg)](https://doi.org/10.5281/zenodo.15090961)

<!--TODO: Add DOI badge-->

# Research Compendium: Replicating Simulations in Python using Generative AI

This repository serves as a **research compendium** for the paper:

> Monks, T., Harper, A., & Heather, A. (2025). **Unlocking the Potential of Past Research: Using Generative AI to Reconstruct Healthcare Simulation Models**. Work in progress. <!--TODO: Add URL-->

A research compendium is collection of all the digital materials relevant to the study. In this case, it includes a description of the aims and models, as well the STRESS reports for each model, the full model code and testing, logs of all the prompts used and experiences working with the LLMs, analysis of the results, and more!

This has been structured into a book which is hosted on GitHub pages and can be viewed at: https://pythonhealthdatascience.github.io/llm_simpy

<br>

## 👥 Authors

* Thomas Monks &nbsp;&nbsp; [![ORCID: Monks](https://img.shields.io/badge/ORCID-0000--0003--2631--4481-brightgreen)](https://orcid.org/0000-0003-2631-4481)

* Alison Harper &nbsp;&nbsp; [![ORCID: Harper](https://img.shields.io/badge/ORCID-0000--0001--5274--5037-brightgreen)](https://orcid.org/0000-0001-5274-5037)

* Amy Heather &nbsp;&nbsp; [![ORCID: Heather](https://img.shields.io/badge/ORCID-0000--0002--6596--3479-brightgreen)](https://orcid.org/0000-0002-6596-3479)

<br>

## 🌐 Creating the environment

The project uses `conda` to manage dependencies. Navigate your terminal to the directory containing the code

```
conda env create -f binder/environment.yml
```

This will create a conda environment called `gen_simpy`. To activate:

```
conda activate gen_simpy
```

<br>

## 🖥️ Viewing the jupyter book locally

Once in the `gen_simpy` environment, navigate to the top level directory of the code repository in your terminal and issue the following command:

```
jb build .
```

This will build the HTML book locally on your machine.  The terminal will display a URL link that you can use to point your browser at the HTML.

<br>

## 📝 Citation

Please cite the archived repository:

> TBC. <!--TODO: Add Zenodo citation-->

You can also cite this GitHub repository as:

> Thomas Monks, Alison Harper, and Amy Heather. **Using Large Language Models to support researchers reproduce and reuse unpublished health care discrete-event simulation computer models: a feasibility and pilot study in Python**. <https://github.com/pythonhealthdatascience/llm_simpy>.

```bibtex
@software{llm_simpy,
  author       = {Monks, Thomas and
                  Harper, Alison and
                  Heather, Amy},
  title        = {Using Large Language Models to support researchers
                   reproduce and reuse unpublished health care
                   discrete-event simulation computer models: a
                   feasibility and pilot study in Python
                  },
  month        = mar,
  year         = 2025,
  publisher    = {Zenodo},
  version      = {v0.1.0},
  doi          = {10.5281/zenodo.15090961},
  url          = {https://doi.org/10.5281/zenodo.15090961},
}
```

A `CITATION.cff` file is also provided.




<br>

## Funding

This project was developed as part of the project STARS: Sharing Tools and Artefacts for Reproducible Simulations. It is supported by the Medical Research Council [grant number [MR/Z503915/1](https://gtr.ukri.org/projects?ref=MR%2FZ503915%2F1)].