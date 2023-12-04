modify the code as follows: 

Create a new generator function in the CCUModel class called "warmup_complete". It should be scheduled by simpy to run only once at the end of the warm up period.  The logic of the function should set the patient count to zero. 

At the end of the simulation run add the patient coun to the pandas dataframe.
Add the result to the pandas dataframe.

Show all of the model code: this includes all patient generator functions in the CCUModel class and all code in the Experiment class.