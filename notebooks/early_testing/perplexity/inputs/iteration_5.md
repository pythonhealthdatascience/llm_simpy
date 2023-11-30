modify the code as follows:

The code should calculate performance measures at the end of the simulation run.  

The following measures should be calculated.

1. The number of elective operations cancelled. 

The code should only collect statistics on this performance measure if the simulation time has exceeded the warm-up period.

After the performance measures are calculated the results should outputted in a pandas dataframe.

Show all of the model code: this includes all patient generator functions in the CCModel class and all code in the Experiment class.





2. The total time critical care beds were in use represented as a percentage of the (number of beds multiplied by the results collection period). 
3. The mean time an unplanned admission had to wait for a critical care bed to be available.