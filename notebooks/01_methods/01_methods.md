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

#### Step 1: visual inspection of the code.

Our initial approach was to use the Jupyter Lab IDE to visually inspect the generated model and check for obvious logical bugs, unused code or package imports, outdated Python libraries, fabricated functionality etc.  However, during the creation of the second case study model we found that visual inspection became too difficult when a modification of existing code took place. In iteration 11 of case 2, we enhanced this process by including the use of a python tool called `nbdime` that provided a highlighted difference between two versions of the same notebook. This enhancement meant that we did not miss any modification that unexpectedly removed code or modified existing from prior iterations. Our process was therefore updated to include:

1. Copy the prior iteration of the notebook
2. Replace any existing functions, classes or scripts with new versions generated in the iteration
3. Add in cells to hold new functions, classes, or scripts
4. Generate highlighted difference between the new notebook and the prior iteration.

#### Step 2: classical verification of the simulation model. 

We designed and conducted a series of experiments with the model.  These included

1. extreme value tests (e.g limiting arrival types, zero or extreme lengths of stay)
2. vary parameters such as run lengths/warm-up periods
3. deterministic runs
4. basic unit test that any equations produce expected values.
5. Testing of individual components within the model (for example, in case 2 testing the Acute Stroke Unit separate from the Rehabilitation Ward).
6. Visual inspection of charts or plots produced.
7. Inspection of summary statistics of performance measures.

In each iteration of the model we reran prior model testing and if required added new tests.



