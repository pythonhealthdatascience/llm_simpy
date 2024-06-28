# Prompt Engineering 

## Prompts versus academic article write-up

Our early 


## Common tokens

In a health care simulation study, stakeholders and modellers may use multiple terms to refer to the same concept.  For example, in the terms treatment time, treatment duration, and length of stay may be used interchangeably in a conversation or in a written article.  We aimed to make our prompts as specific as possible in order to obtain the iteration of the model that met our design. We therefore attempted to use a common token throughout an individual prompt and across iterations. 

## Initial prompt

In both cases our initial cases were designed to generate a simple working simulation model in `simpy` that generated patient arrivals only. Our hypothesis is that the level of detail and scope could then be expanded in further iterations.  Our initial prompt was one of the most detailed provided. We broke it down into four sections. 

* *Main command*: that specified the context (e.g. a Critical Unit DES model), programming language, simulation package and that this was a code generating task.
* *General model logic*: including time units, arrival sources, model boundaries and run length.
* *Simulation inputs*: for the first iteration this was always inter-arrivals distributions and parameters.
* *Simulation methodology*: underlying sampling tools and how this should be implemented.

Below we include the initial prompts from the two case studies.

```{note}
There is no need to include the titles in the prompt. However, for clarity we chose to include them in our prompts to the LLM.
```

**Critical Care Unit Model Prompt 1**

```markdown
### Main command

Code a discrete-event simulation model of a critical care unit (CCU) in python 3.10 and simpy 4. 

Please code the full model specified. Do not return a simplified version. Show all code.

### General model logic

All time units in the model are in hours.

Each patient in the model has a unique identifier.  The first patient to arrive has an identifier of 0. For each subsequent patient increment the identifier by 1.

Patients to arrive at the CCU from five different sources: Accident and Emergency, the Wards, Emergency surgery, other hospitals, or the X-Ray department. 
Each source had a different inter-arrival time distribution.    
After patients arrive they immediately leave the model.

All patient types must have their own generator function

The model should print out useful information after each event.

the model should include a user settable run length. This defaults to 12 months.


### Simulation inputs

the interarrival time distributions and parameters of patients are dependent on patient type. For each distribution time is measured in hours.

Accident and Emergency = Exponential: 22.72
the Wards = Exponential: 26.0
Emergency surgery = Exponential: 37.0
other hospitals = Exponential: 47.2
the X-Ray department = Exponential: 575.0 


### simulation methodology

numpy should be use for sampling.

each interarrival distribution should have its own numpy.random.Generator object.
```

**Stroke + Rehab Model Prompt 1**

```markdown
### Main command

Code a discrete-event simulation model of an Acute Stroke Unit (ACU) in python 3.10 and simpy 4. 

Please code the full model specified. Do not return a simplified version. Show all code.

### General model logic

All time units in the model are in days.

The model should count the total number of patient arrivals.  The first patient to arrive has an identifier of 0. For each subsequent patient increment the identifier by 1.  
The model should also maintain counts of the number of patients broken down by their type.

Patients to arrive at the ACU from four different sources: Stroke, TIA, Complex Neurological, or Other. 
Each source had a different inter-arrival time distribution.  
After patients arrive they immediately leave the model.

All patient types must have their own generator function.

The model should print out useful information after each event.

The model should include a user settable run length. This defaults to 5 years.


### Simulation inputs

the interarrival time distributions and parameters of patients are dependent on patient type. For each distribution time is measured in days.

Stroke = Exponential: 1.2
TIA = Exponential: 9.3
Complex Neurological = Exponential: 3.6
Other = Exponential: 3.2


### simulation methodology

numpy should be use for sampling.

each interarrival distribution should have its own numpy.random.Generator object.
```


## Refactoring prompts

Within an iteration, we occasionally made use subsequent short prompts to the refactor (another term is "nudge") the code closer to our requirements or expectations.  For example, if the code generated made was a set of functions when we preferred classes.  For example:

```markdown
re-factor the coding into a CCU class.

```

## One-shot prompt engineering

When refactoring of code was judged to be complex we chose to provide a short example of the refactoring in the prompt for the LLM to mimic (so called 1-short prompt engineering).  
An exert from a prompt given to the LLM from the Stroke + Rehab model is shown below where we are refactoring the code to use random sampling that following best practice.  The LLM must modify the code in multiple methods and also count from 0 to the number of random streams implemented.  We therefore provide an example of how this should be implemented.

```markdown
modify the acute_treatment functions in `AcuteStrokeUnit` class. Do not modify the acute_treatment functions.

code that uses `numpy.random`, must be replaced with a call to a unique stream in the `Experiment` list `streams`. Select the stream using a hard coded integer. Start from zero and increment by 1 each time to allocate a unique number to each stream.  E.g. in `stroke_acute_treatment` the first instance of `length_of_stay = np.random.lognormal(mean=mu, sigma=sigma)` becomes `length_of_stay = self.experiment.streams[0](mean=mu, sigma=sigma)`; the second instance uses index 1 and the third uses index 2.
```

## Numbered steps

Many simple functions in programming are a series of steps to be followed by the Python interpreter.  Where they were very clear we specified them as a number ordered list of natural language instructions that the LLM could follow. The below illustrate such a prompt applied to creating an initial iteration of a streamlit inteface for the Stroke+Rehab model

```markdown
write python code that creates an interactive user interface using the package streamlit.

The interface should include a main window.

The main window contains a button labelled “Simulate”. After the button is pressed the following logic is implemented:

1. display a spinner with the text “please wait for results”.

2. run the python code included below

3. display a streamlit table for df_acute and df_rehab results

4. display all plots.  Plotting functions return a tuple of figure, axis.

All classes and functions should be imported from a module called `stroke_rehab_model`

```

## Restrictive clauses in prompts

We appended restrictive clauses to our prompts to avoid changes to parts of the code that were not part of our design. For example, when specifying a modification to the treatment of patients we could append "Do not modify the patient_generator functions at all" to ensure these were not modified in the same way. Similarly if we were interested in refactoring the Experiment class to add new variables we might specify "only modify the Experiment class" or "do not modify the CCU class" to avoid small changes to the design between iterations.  




