### Main command

Modify the RehabilitationUnit class to sample a patients destination after they have left the rehabilitation unit (ASU).

Show all of the RehabilitationUnit class code: this includes all patient generator functions

### General model logic

After patients have arrived the model immediately samples their destination after the ASU. Destinations are:

1. ESD 
2. Other

Create a variable called "post_rehab_destination". This variable is used to record the sampled destination of the patient.

### Simulation inputs

The sampling distribution are specific to the patient type.

Stroke = Discrete Empirical: 40, 60
TIA = Discrete Empirical: 0, 100
Complex-neurological = Discrete Empirical: 9, 91
Other = Discrete Empirical 13, 88


