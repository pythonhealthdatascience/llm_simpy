modify the code as follows: 

For both unplanned and elective admissions, after a patient has completed treatment, if the simulation time has exceeded the warm-up period, the patient's treatment time should be added to a running total.

Add in a new performance measure that is calculated at the end of the simulation run called "bed utilization". This is calculated as follows:

* The total treatment time divided by (the number of beds multiplied by the results collection period).   This is a percentage.

Add the result to the pandas dataframe.

Show all of the model code: this includes all patient generator functions in the CCUModel class and all code in the Experiment class.