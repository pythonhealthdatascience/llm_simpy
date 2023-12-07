### Main command

Code a discrete-event simulation model of a critical care unit (CCU) in python 3.10 and simpy 4. 

Please code the full model specified. Do not return a simplified version. Show all code.

### General model logic

All time units in the model are in hours.

Each patient in the model has a unique identifier.  The first patient to arrive has an identifier of 0. For each subsequent patient increment the identifer by 1.

Patients to arrive at the CCU from five different sources: Accident and Emergency, the Wards, Emergency surgery, other hospitals, or the X-Ray department. Each source had a different inter-arrival time distribution.    After patients arrive they immediately leave the model.

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