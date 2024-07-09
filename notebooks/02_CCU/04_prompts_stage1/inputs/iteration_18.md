code a new function called "get_experiments".  The function should create six Experiment objects.  The experiments vary the number of critical care beds.  Starting at 23 and increasing to 28.  The function should return a dictionary containing an appropriate name for each experiment as the key and the Experiment object as the value.

code a new function called "run_all_experiments".  The function should accept a dictionary and the number of replications as parameters. The function should loop through each key value pair in the dictionary. On each iteration the following actions are performed:

1. Informs the user of the name of the current experiment
1. Create an instance of the CCUModel using the current experiment
2. Call the multiple_replications function
3. Summarise the results of the experiment using the "results_summary" function.
4. Store the summary dataframe in a dictionary.

Return the summary.

code a new function called "summary_of_experiments". The function should accept a dictionary containing a summaries of multiple experiments. The function should combined the summaries into an overall dataframe.  The columns of the dataframe should be the name of the experiments.  

Return the dataframe.

only show the code for these three functions.
