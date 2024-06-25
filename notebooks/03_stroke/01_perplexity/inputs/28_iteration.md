write python code that creates an interactive user interface using the package streamlit.

The interface should include a main window.

The main window contains a button labelled “Simulate”. After the button is pressed the following logic is implemented:

1. display a spinner with the text “please wait for results”.

2. run the python code included below

3. display a streamlit table for df_acute and df_rehab results

4. display all plots.  Plotting functions return a tuple of figure, axis.

All classes and functions should be imported from a module called `stroke_rehab_model`


```python
# Create an instance of Experiment  (default params, default warm-up and rcp).
experiment = Experiment()

# run multiple replications
rep_results = multiple_replications(experiment, 100)

# combine results and take the mean 
pd_asu, pd_rehab = combine_pdelay_results(rep_results)
rel_asu, rel_rehab = combine_occup_results(rep_results)
mean_pd_asu, mean_pd_rehab = mean_results(pd_asu), mean_results(pd_rehab)
mean_rel_asu, mean_rel_rehab = mean_results(rel_asu), mean_results(rel_rehab)

# prob delay plots 
prob_delay_plot(mean_pd_asu, np.arange(0, 30))
prob_delay_plot(mean_pd_rehab, np.arange(0, 30), "No. rehab beds available")

# prob occupancy plots
occupancy_plot(mean_rel_asu, np.arange(0, 30))
occupancy_plot(mean_rel_rehab, np.arange(0, 30), "No. people in rehab")

## tabular results
# acute
df_acute = summary_table(mean_pd_asu, 9, 14, "acute")
df_rehab = summary_table(mean_pd_rehab, 10, 16, "rehab")
```