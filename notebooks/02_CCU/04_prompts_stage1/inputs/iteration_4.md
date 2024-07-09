modify the code as follows

the model should include a user settable warm up period. This defaults to 1 month.

model run length should be renamed results collection period and have the default value of 12 months.  

The total run length of the model is the warm up period plus the results collection period.

the Experiment class should also accept a parameter for the warm up period

Show all of the model code: this includes all patient generator functions in the CCModel class and all code in the Experiment class.