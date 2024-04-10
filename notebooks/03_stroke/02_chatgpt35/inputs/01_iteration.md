### Main command

Code a discrete-event simulation model of an Acute Stroke Unit (ACU) in python 3.10 and simpy 4. 

Please code the full model specified. Do not return a simplified version. Show all code.

### General model logic

All time units in the model are in days.

The model should count the total number of patient arrivals.  The first patient to arrive has an identifier of 0. For each subsequent patient increment the identifier by 1.  The model should also maintain counts of the number of patients broken down by their type.

Patients to arrive at the ACU from four different sources: Stroke, TIA, Complex Neurological, or Other. Each source had a different inter-arrival time distribution.  After patients arrive they immediately leave the model.

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