# Model recreation

The study will follow an iterative approach to model recreation in line with the principal of parsimony. We will gradually add detail to the model in small increments as this mirrors how modellers code models.  Figure 1 illustrates this process for a traditional *manual* approach to recreating a simulation model from the literature without the aid of an LLM versus incorporating an LLM.

```{figure} ../../images/iterative_model_recreation.png
---
height: 500px
name: methods_fig
---
The iterative process for recreating a model from a textual description: with and without a LLM.
```

## Testing of a generated model

Following each iteration of model generation a two step procedure will be employed.  We will gradually build tests up as more detail is added to the generated model and also perform regression (repeating prior tests) as new logic and functionality is added.

### Step 1: visual inspection of the code.

We will use the Visual Studio Code IDE to visually inspect the generated model and check for obvious logical bugs, unused code or package imports, outdated Python libraries, fabricated functionality etc. 

### Step 2: classical verification of the simulation model. 

We will design and conduct extreme value tests, vary parameters such as run lengths/warm-up periods, deterministic runs, and unit test that any equations produce expected values.  