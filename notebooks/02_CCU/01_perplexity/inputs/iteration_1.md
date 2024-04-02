### Main command

Modify the model to add in an unplanned admissions treatment process.

Show the full code listing.  Do not hide any functions or classes.

### General model logic

The model includes a resource: critical care beds.

After patients have arrived they follow the unplanned admissions process. In the unplanned admissions process patients request and wait for a critical care bed resource to become available in a FIFO queue, and undergo treatment.  Following treatment the patient is recorded as "discharged", but the bed is not released until intensive cleaning has taken place.  

The model should print out useful information after each event.

### Simulation inputs

the length of stay (measured in hours) for treatment of patients in the CCU follow source specific distributions

Accident and Emergency: Lognormal: mean 128.79 and standard deviation 267.51
the Wards = Lognormal: mean 177.89 and standard deviation 276.54
Emergency surgery = Lognormal: mean 140.15 and standard deviation 218.02
other hospitals = Lognormal: mean 212.86 and standard deviation 457.67
the X-Ray department = Lognormal: mean 87.53 and standard deviation 108.67

The mean and standard deviation of the Lognormal distributions must be converted to the mean and standard deviation of the underlying normal distribution.

There are 24 critical care beds in the model.  These are shared across all types of patient.

Intensive cleaning takes a fixed amount of time: 5 hours.


