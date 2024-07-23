# 5. Implementation

## 5.1 Software or programming language

The simulation model was developed using python 3.10 and simpy 4.1.1.  Simpy details are here: [https://simpy.readthedocs.io/en/latest/](https://simpy.readthedocs.io/en/latest/)

A [conda virtual environment](https://github.com/pythonhealthdatascience/llm_simpy/blob/main/binder/environment.yml) is provided to manage versions on a local machine.

## 5.2 Random sampling 

All sampling uses [`numpy.random.Generator`](https://numpy.org/doc/stable/reference/random/generator.html).  A `numpy` generator object implements the Permuted Congruential Generator 64-bit (PCG64; period = $2^{128}$; maximum number of streams = $2^{63}$).

Repeatable experiments and common random number streams are used in the model.  A simple method is used to create streams are creating using multiple seeds. This does not guarantee, that streams are non overlapping.

## 5.3 Model execution

`simpy` implements a process based simulation worldview.

## 5.4 System Specification

The model was coded by [Perplexity.AI](https://www.perplexity.ai/) between Janurary 2024 and July 2024. It was run on Intel i7-1195G7 CPU with 16GB RAM running Ubuntu 20.04 Linux.