## Testing

Following each iteration of model generation a two step testing procedure was employed.  

#### Step 1: visual inspection of the code.

Our initial approach was to use the Jupyter Lab IDE to visually inspect the generated model and check for obvious logical bugs, unused code or package imports, outdated Python libraries, fabricated functionality (e.g. functions that do not exist) etc.  However, during the initial model creation phase we found that visual inspection became too difficult when a modification of existing code took place. In iteration 11 of case 2, we enhanced the code inspection process by including the use of a Python library called `nbdime` that provided a highlighted difference between two versions of the same notebook. This enhancement meant that we did not miss any modification that unexpectedly removed code or modified existing code from prior iterations. Our process was therefore updated to include:

1. Copy the prior iteration of the notebook;
2. Replace any existing functions, classes or scripts with new versions generated in the iteration;
3. Add in cells to hold new functions, classes, or scripts;
4. Generate highlighted difference between the new notebook and the prior iteration.

#### Step 2: classical verification of the simulation model. 

We designed and conducted a series of experiments with the model.  These included

1. extreme value tests (e.g limiting arrival types, zero or extreme lengths of stay)
2. varying parameters such as run lengths/warm-up periods
3. data collection and post run processing
4. basic unit test that any equations produce expected values.
5. Testing of individual components within the model (for example, in case 2 testing the Acute Stroke Unit separate from the Rehabilitation Ward).
6. Visual inspection of charts or plots produced.
7. Inspection of summary statistics of performance measures.

In each iteration of the model we reran prior model testing and if required added new tests.