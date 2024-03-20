# Experiment

## Sequence

Our experimental setup was made-up of a *initial recreation phase*, a *replication phase* and a *prompt database*. Figure 2 illustrates the sequence of activities followed in the experiment.  

In the initial recreation phase we created a prompt database that contains a record of all prompts given to an LLM and for what purpose. We then proceeded to recreate case study 1 and then, when complete, recreate case study 2.  Where appropriate we reused or adapted prompts from case study 1 when recreating the model for case study 2.  All case study 2 prompts were stored the database in sequence of use.

In the replication stage a second modeller attempted to recreate the models using the original sequence of prompts. Given the stochastic nature of LLM output (i.e. the same input prompt may not produce the same output), we allowed for re-engineering of prompts in the replication phase. This might be a direct modification to original prompt or an additional follow up prompt to modify output to the desired code.  

```{figure} ../../images/diagram_experiment_process.png
---
height: 500px
name: experiment_fig
---
Sequence of activities in model recreation experiment.
```









