create a function called "multiple_replications". This should be standalone and separate from the CCUModel class. The function accepts an instance of Experiment and the number of replications (default=5) as parameters. The functions logic of each replication is as follows:

1. create a new instance of the model
2. reset the performance measures held in Experiment to their original values
3. run the model and store the results returned in a 
4. store the returned results of the replication for later use.
5. create a new column in the results that represent the replication number.  This should be the index of the results table.

After all multiple replications have been completed concatenate all results into a single dataframe. The first column of the dataframe should be an integer representing the replication number. The function returns the results.
