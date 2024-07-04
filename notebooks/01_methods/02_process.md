# Procedure overview

Our experimental procedure followed three phases: an *initial recreation phase*, a *replication phase*, a *comparison phase*. All phases used, and added to, a *prompt database*. Figure 2 illustrates the general sequence of activities followed in the experiment.  

In phase 1, we created a prompt database that contained a record of all prompts given to the LLM and for what purpose. We then proceeded to recreate case study 1 and then, when complete, recreate case study 2.  Where appropriate we reused or adapted prompts from case study 1 when recreating the model for case study 2.  All case study 2 prompts were stored in the database in sequence of use.

In phase 2, a second modeller repeated the experiment. I.e. they attempted to recreate the models using the original sequence of prompts. Given the stochastic nature of LLM output (i.e. the same input prompt may not produce the same output), we allowed for re-engineering of prompts in the replication phase. This might be a direct modification to original prompt or an additional follow up prompt to modify output to the desired code.  

In phase 3, we compared the artefacts generated and experience of working with the LLM to create the simpy models in phase 1 and 2.  

```{figure} ../../images/llm_study_process_info_graphic.png
---
height: 500px
name: experiment_fig
---
General sequence of activities in model recreation experiment.
```