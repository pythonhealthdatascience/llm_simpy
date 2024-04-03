# Testing

Following each iteration of model generation a four step testing procedure was employed.  

## Step 1: visual inspection of the code.

Our initial approach was to use the Jupyter Lab IDE to visually inspect the generated model and check for obvious logical bugs, unused code or package imports, outdated Python libraries, fabricated functionality (e.g. functions that do not exist) etc.  However, during the initial model creation phase we found that visual inspection became too difficult when a modification of existing code took place. In iteration 11 of case 2, we enhanced the code inspection process by including the use of a Python library called [`nbdime`](https://nbdime.readthedocs.io/en/latest/) that provided a highlighted difference between two versions of the same notebook. An example of a difference is illustrated in Figure 3. On the left hand side of Figure 3 we see the version of the code in the prior iteration. Modified lines are highlighted in red.  One the right hand side of Figure 3 we have the current iterations version of the model. Modified lines are highlighted in green. the function `audit_rehab_occupancy` is an entirely new function added to the code base.  This enhancement meant that we did not miss any modification that unexpectedly removed code or modified existing code from prior iterations. Our process was therefore updated to include:

1. Copy the prior iteration of the notebook;
2. Replace any existing functions, classes or scripts with new versions generated in the iteration;
3. Add in cells to hold new functions, classes, or scripts;
4. Generate highlighted difference between the new notebook and the prior iteration.

```{figure} ../../images/diff_example.png
---
name: diff_fig
---
Example of differencing two iterations of the generated model
```

## Step 2: classical verification of the simulation model. 

We designed and conducted a series of experiments with the model.  These included

1. extreme value tests (e.g limiting arrival types, zero or extreme lengths of stay)
2. varying parameters such as run lengths/warm-up periods
3. data collection and post run processing
4. basic unit test that any equations produce expected values.
5. Testing of individual components within the model (for example, in case 2 testing the Acute Stroke Unit separate from the Rehabilitation Ward).
6. Visual inspection of charts or plots produced.
7. Inspection of summary statistics of performance measures.

In each iteration of the model we reran prior model testing and if required added new tests.


## Step 3: Creation of automated and manual tests

After the completion of a model we stored all generated code in a dedicated python module. We then refactored tests created in step 2 into two sets of tests that were easy to run and included with the full models.  These were split into automated and manual tests.  The automated tests worked with the python package `pytest`. These tests have simple quantitative pass/fail criteria. The `pytest` software automatically detects and runs all automated tests and reports successes and failures to a user.  The manual tests involve visual inspect (e.g. inspecting the simulated trace, and charts).  

## Step 4: Testing by a second modeller

The final step in testing was conducted by the second modeller. The modeller was provided with

1. The journal articles describing the two simulation models.
2. The python module(s) containing all model code for the two case studies.
3. The set of automated and manual tests.
4. Jupyter notebooks that contained a (human created) python script for running the models/user interfaces and detailed usage instructions.
5. All prompts (in sequence) used to generate code and all Jupyter notebooks containing the iterations of the model/testing.
   
The second modeller reviewed all of this information and attempted to run the models and tests. We used this phase to identify:

* Missed errors in the model recreation (either by LLM or user).
* Typos/mistakes/copy paste errors in iteration notebooks.
* Additional formal testing that should be conducted.
* Improvements that were needed in model documentation.

The outcome of these step would then be fixed/implemented before proceeding to phase 2 in our experimental procedure.


