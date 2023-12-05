modify CCUModel.run so that it returns the pandas dataframe instead of printing it out.

organise the code so that multiple replications of the model can be run (e.g. default = 5). 

This should be implemented as a separate function called "multiple_replications". The functions logic of each replication is as follows:

1. create a new instance of the model
2. reset the performance measures held in Experiment to their original values
3. run the model
4. store the results of the replication for later use

After all multiple replications have been completed return the stored results and summarise these in a pandas dataframe.