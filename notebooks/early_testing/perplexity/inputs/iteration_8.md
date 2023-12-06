modify the code as follows: 

Add in a new performance measure that is calculated at the end of the simulation run called "bed occupancy". This is calculated by multiplying the bed utilization by the number of critical care beds.

Add the result to the pandas dataframe.

add a new parameter to Experiment called "trace". The default value of "trace" is False.  If "trace" is True the model will print out simulated events such as admissions, discharges, or cancellations.   The model will always print out the performance at the end of the simulated run.