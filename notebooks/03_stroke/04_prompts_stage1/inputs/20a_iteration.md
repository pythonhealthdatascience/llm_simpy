Combine the two scripts below create a new single script that follows these steps:

1. create an instance of `Experiment`
2. create an instance of a simpy environment
3. create an instance RehabilitationUnit 
4. create an instance of AcuteStrokeUnit. Pass the RehabilitationUnit as a parameter
5. initialise the four methods postfixed with "generator" in AcuteStrokeUnit  as simpy processes
6. initialise the three methods postfixed with "generator" in RehabilitationUnit  simpy processes
7. initialise the audit of rehab occupancy as a simpy process. Use an interval of 1 day.  Pass in env
8. initialise the audit of the AcuteStrokeUnit occupancy as a simpy process. Use an interval of 1 day.
9. run the model for the default run length in the experiment * 50
10. use `calculate_occupancy_frequencies` to calculate occupancy frequencies of both the AcuteStrokeUnit and the rehab occupancy
11. use `calculate_prob_delay` to calculate the probability of delay for AcuteStrokeUnit and rehab  
12. use `prob_delay_plot` to display a prob of delay plot for AcuteStrokeUnit and rehab.  Use appropriate x_label values for the AcuteStrokeUnit and rehab unit

Only show the code in the script. Do no modify the functions or classes used.

```python
# Create an instance of the Experiment class with default parameters and trace set to False
default_experiment_params = Experiment()

# Create the simulation environment and AcuteStrokeUnit instance with the Experiment parameters
env = simpy.Environment()

## MODIFIED BY TESTER
#  create instance of RU, but we do not run the model at this stage
rehab_unit = RehabilitationUnit(env, default_experiment_params)
##

acu_experiment = AcuteStrokeUnit(env, default_experiment_params, rehab_unit)

# Start the patient generators for each type of patient in the AcuteStrokeUnit instance
env.process(acu_experiment.stroke_patient_generator())
env.process(acu_experiment.tia_patient_generator())
env.process(acu_experiment.neuro_patient_generator())
env.process(acu_experiment.other_patient_generator())

# Start the audit_acute_occupancy generator function to record ASU occupancy at intervals
env.process(audit_acute_occupancy(1, acu_experiment, default_experiment_params))

# Run the simulation until the specified run length in the Experiment parameters
# modified by tester - run length * 10
env.run(until=default_experiment_params.run_length * 10)

# Calculate occupancy frequencies and plot the relative frequency distribution
relative_freq, cumulative_freq, unique_vals = calculate_occupancy_frequencies(default_experiment_params.asu_occupancy)

# Calculate probability of delay and plot the step chart
prob_delay = calculate_prob_delay(relative_freq, cumulative_freq)
prob_delay_plot(prob_delay, unique_vals)
```

```python
# 1. Create an experiment
experiment = Experiment()

# 2. Create an instance of a simpy environment
env = simpy.Environment()

# 3. Create an instance of RehabilitationUnit
rehab_unit = RehabilitationUnit(env, experiment)

# 4. Initialize the patient generators as simpy processes
env.process(rehab_unit.stroke_patient_generator())
env.process(rehab_unit.neuro_patient_generator())
env.process(rehab_unit.other_patient_generator())

# 5. Initialize the audit of rehab occupancy as a simpy process with an interval of 1 day
env.process(audit_rehab_occupancy(env, 1, rehab_unit, experiment))

# 6. Run the model for the default run length in the experiment * 10
env.run(until=experiment.run_length * 10)

# 7. Calculate occupancy frequencies of the rehab occupancy
relative_frequency, cumulative_frequency, unique_values = calculate_occupancy_frequencies(experiment.rehab_occupancy)

# 8. Display an occupancy plot for the rehab unit
occupancy_plot(relative_frequency, unique_values, x_label="No. of people in rehab")

# 9. Calculate the probability of delay for rehab
prob_delay = calculate_prob_delay(relative_frequency, cumulative_frequency)

# 10. Display a probability of delay plot for rehab
prob_delay_plot(prob_delay, unique_values, x_label="No. rehab beds available")

```