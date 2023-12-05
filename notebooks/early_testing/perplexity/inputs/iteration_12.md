create a function called "multiple_replications". This should be standalone and separate from the CCUModel class. The function accepts an instance of Experiment and the number of replications (default=5) as parameters. The functions logic of each replication is as follows:

1. create a new instance of the model
2. reset the performance measures held in Experiment to their original values
3. run the model
4. store the returned results of the replication for later use

After all multiple replications have been completed return the stored results and summarise these in a pandas dataframe.