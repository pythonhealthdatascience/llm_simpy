### Main command

Add a class representing the process at a Rehabilitation Unit (RU) called `RehabilitationUnit`

### General model logic

The RehabilitationUnit class should count the total number of patient arrivals.  The first patient to arrive has an identifier of 0. For each subsequent patient increment the identifier by 1.  The model should also maintain counts of the number of patients broken down by their type.

Patients to arrive at the RU from three different sources: Stroke, Complex Neurological, or Other. Each source had a different inter-arrival time distribution.  After patients arrive they immediately leave the model.

All patient types must have their own generator function.

The model should print out useful information after each event.

### Simulation inputs

the interarrival time distributions and parameters of patients are dependent on patient type. For each distribution time is measured in days.

Stroke = Exponential: 21.8
Complex Neurological = Exponential: 31.7
Other = Exponential: 28.6

Add three class member variables for the mean of each distribution. For example `self.stroke_iat_external`