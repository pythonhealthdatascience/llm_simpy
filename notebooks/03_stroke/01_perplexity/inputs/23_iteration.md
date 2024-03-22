create a function called `multiple_replications`. The function accepts an instance of `Experiment` and the number of replications (default=5) as parameters. The functions logic of each replication is as follows:

1. call `single_run` 
2. store the returned results of the replication for later use in a list called `rep_results`

after all replications are complete return `rep_results`


create a function called `combine_pdelay_results(rep_results)` where `rep_results` is a python list where each item is a dictionary.  The function logic is as follows:

Loop through `rep_results`:

1. select `prob_delay_asu` and `unique_vals_asu`.
2. find the minimum value in `unique_vals_asu` called `min_occupancy`
3. Create an new array of length 30 of all zeros.  Copy values from `prob_delay_asu` to the new array using `unique_vals_asu` as the index.
4. In the new array set all values whose array index is < `min_occupancy` to 1.0
5. store the results a new result list

Repeat for `prob_delay_rehab`,
Return the result lists as numpy arrays



create a function called `combine_occup_results(rep_results)` where `rep_results` is a python list where each item is a dictionary.  The function logic is as follows:

Loop through `rep_results`:

1. select `relative_freq_asu` and `unique_vals_asu`.
2. Create an new array of length 30 of all zeros.  Copy values from `relative_freq_asu` to the new array using `unique_vals_asu` as the index.
3. store the results a new result list

Repeat for `relative_freq_rehab`,
Return the result lists as numpy arrays



create a function called `mean_prob_delay(run_results) where run_results is a python list where each item is a dictionary.

Loop through run_results, select `prob_delay_asu`, each time stacking onto a new row to a numpy 2D array
Take the average of the columns in the numpy array. 
Repeat for `prob_delay_rehab`
Return the averages.


