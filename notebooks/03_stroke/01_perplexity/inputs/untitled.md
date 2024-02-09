### Main command

Modify the model to add in an acute stroke unit (ASU) treatment process.

Show the full code listing.  Do not hide any functions or classes.

### General model logic

After patients have arrived they immediately follow the ASU treatment process. Following treatment the patient is recorded as "discharged".

The model should print out useful information after each event.

### Simulation inputs

the length of stay (measured in days) for treatment of patients in the ASU follow source specific distributions

Stroke: Lognormal: mean 128.79 and standard deviation 267.51
TIA = Lognormal: mean 177.89 and standard deviation 276.54
Complex Neurological  = Lognormal: mean 140.15 and standard deviation 218.02
Other = Lognormal: mean 212.86 and standard deviation 457.67

The mean and standard deviation of the Lognormal distributions must be converted to the mean and standard deviation of the underlying normal distribution.

There are 24 critical care beds in the model.  These are shared across all types of patient.

Intensive cleaning takes a fixed amount of time: 5 hours.


