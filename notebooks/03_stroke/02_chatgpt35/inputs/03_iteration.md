### Main command

Modify the model to add in four new `acute_treatment` methods to the ASU class each patient type i.e. Stroke, TIA, Complex Neurological, and other.  Prefix the method names with the patient type e.g. `stroke_acute_treatment`

Show all of the model code: this includes all patient generator functions in the ASU class.

### General model logic

Add the following logic

1. After a patient has been generated call `acute_treatment` as a simpy process. Pass the patient type to the method.  Do not use the yield statement when calling this method.
2. sample a length of stay (measured in days) for treatment of patients
3. yield a simpy timeout equal to the length of stay for treatment

The model should print out useful information after each event.

### Simulation inputs

the length of stay (measured in days) for treatment of patients in the ASU follow source specific distributions

if patient type = Stroke and post_asu_destination = Rehab then Lognormal: mean 7.4 and standard deviation 8.6

if patient type = Stroke and post_asu_destination = ESD then Lognormal: mean 4.6 and standard deviation 4.8

if patient type = Stroke and post_asu_destination = Other then Lognormal: mean 7.0 and standard deviation 8.7

if patient type = TIA then Lognormal: mean 1.8 and standard deviation 5.0

if patient type = Complex Neurological then Lognormal: mean 4.0 and standard deviation 5.0

if patient type = Other then Lognormal: mean 3.8 and standard deviation 5.2

The mean and standard deviation of the Lognormal distributions must be converted to the mean and standard deviation of the underlying normal distribution.


