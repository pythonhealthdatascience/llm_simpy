Correct the three python scripts below to use the correct versions of `audit_rehab_occupancy` and `audit_rehab_occupancy`.  Always pass env. Set first_interval equal to warm_up.
Rename run_length to results_collection_period and run the model for the experiments results_collection_period + warm_up

show the three edited scripts separately.

### Script 1

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

### Script 2

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


### Script 3

```python
# Combine the two scripts into a single script following the specified steps

# Create an instance of the Experiment class with default parameters and trace set to False
default_experiment_params = Experiment()

# Create the simulation environment
env = simpy.Environment()

# Create an instance of RehabilitationUnit
rehab_unit = RehabilitationUnit(env, default_experiment_params)

# Create an instance of AcuteStrokeUnit. Pass the RehabilitationUnit as a parameter
acu_experiment = AcuteStrokeUnit(env, default_experiment_params, rehab_unit)

# Initialise the patient generators in AcuteStrokeUnit as simpy processes
env.process(acu_experiment.stroke_patient_generator())
env.process(acu_experiment.tia_patient_generator())
env.process(acu_experiment.neuro_patient_generator())
env.process(acu_experiment.other_patient_generator())

# Initialise the patient generators in RehabilitationUnit as simpy processes
env.process(rehab_unit.stroke_patient_generator())
env.process(rehab_unit.neuro_patient_generator())
env.process(rehab_unit.other_patient_generator())

# Initialise the audit of rehab occupancy as a simpy process. Use an interval of 1 day.
env.process(audit_rehab_occupancy(env, 1, rehab_unit, default_experiment_params))

# Initialise the audit of AcuteStrokeUnit occupancy as a simpy process. Use an interval of 1 day.
env.process(audit_acute_occupancy(1, acu_experiment, default_experiment_params))

# Run the model for the default run length in the experiment * 50
env.run(until=default_experiment_params.run_length * 50)

# Calculate occupancy frequencies of both AcuteStrokeUnit and rehab occupancy
relative_freq_asu, cumulative_freq_asu, unique_vals_asu = calculate_occupancy_frequencies(default_experiment_params.asu_occupancy)
relative_freq_rehab, cumulative_freq_rehab, unique_vals_rehab = calculate_occupancy_frequencies(default_experiment_params.rehab_occupancy)

# Calculate probability of delay for both AcuteStrokeUnit and rehab
prob_delay_asu = calculate_prob_delay(relative_freq_asu, cumulative_freq_asu)
prob_delay_rehab = calculate_prob_delay(relative_freq_rehab, cumulative_freq_rehab)

# Display probability of delay plot for both AcuteStrokeUnit and rehab unit with appropriate x_label values
prob_delay_plot(prob_delay_asu, unique_vals_asu, x_label="No. of people in Acute Stroke Unit")
prob_delay_plot(prob_delay_rehab, unique_vals_rehab, x_label="No. of people in Rehab Unit")

```
