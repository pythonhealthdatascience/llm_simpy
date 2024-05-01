### Main command

Modify the model to add in three new `rehab_treatment` methods to the `RehabilitationUnit` class each patient type i.e. Stroke, Complex Neurological, and other.  Prefix the method names with the patient type e.g. `stroke_rehab_treatment`

Show only the RehabilitationUnit class code: this includes all patient generator functions

### General model logic

Add the following logic

1. After a patient has been generated call `rehab_treatment` as a simpy process. Pass the patient type.  Do not use the yield statement when calling this method. 
2. sample a post rehab destination. The options are ESD or Other. Store the result in `post_rehab_destination`
3. sample a length of stay (measured in days) for treatment of patients. store the result in `length_of_stay`
4. yield a simpy timeout equal to the length of stay for treatment
5. Print out information detailing the completion of a patient treatment.

### Simulation inputs

The sampling distribution for post_rehab_destination is specific to the patient type.

Stroke = Discrete Empirical: 40, 60
Complex-neurological = Discrete Empirical: 9, 91
Other = Discrete Empirical 12, 88

the length of stay (measured in days) for treatment of patients in the RehabilitationUnit follow source specific distributions

if patient type = Stroke and post_rehab_destination = ESD then Lognormal: mean 30.3 and standard deviation 23.1

if patient type = Stroke and post_rehab_destination = Other then Lognormal: mean 28.4 and standard deviation 27.2

if patient type = Complex Neurological then Lognormal: mean 27.6 and standard deviation 28.4

if patient type = Other then Lognormal: mean 16.1 and standard deviation 14.1

