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



create a function called `mean_results(rep_results)` where `rep_results` is a numpy array. The function should return the mean of the columns in rep_results.


create a function called `summary_table(mean_pdelay, min_beds, max_beds, bed_type)`. 
1. Slice `mean_pdelay` between `min_beds` and `max_beds`.
2. Creates a pandas dataframe. The first column is the slice of `mean_pdelay` (2dp) the second column is 1 / the slice of `mean_pdelay` (to 2dp).  Round the 2nd column down to nearest integer.
3. The column names are "p(delay)" and "1 in every n patients delayed".
4. The index should start at min_beds and end at max_beds.  Its name is "No. " + `bed_type` + " beds"
5.  Return the dataframe
