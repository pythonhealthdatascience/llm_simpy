### Main command

Modify the model to sample a patients destination after they have left the acute stroke unit (ASU).

Show all of the model code: this includes all patient generator functions in the ASU class.

### General model logic

After patients have arrived the model immediately samples their destination after the ASU. Destinations are:

1. Rehab
2. ESD 
3. Other

Create a variable called "post_asu_destination". This variable is used to record the sampled destination of the patient.

### Simulation inputs

The sampling distribution are specific to the patient type.

Stroke = Discrete Empirical: 24, 13, 63
TIA = Discrete Empirical: 1, 1, 98
Complex-neurological = Discrete Empirical: 11, 5, 84
Other = Discrete Empirical 5, 10, 85


