# 4. Experimentation

## 4.1 Initialisation

The model is a non-terminating system. It has a default warm-up of 720 hours

## 4.2 Run length

The time units used in the model are hours and a results collection period of 8640 hours.

## 4.3 Estimation approach

Multiple independent replications are employed to account for lack of independence. Common random numbers are employed between scenarios.  A total of 5 replications are run for each experiment, but this number can be varied. 

> In Griffith's et al. 100,000 replications were employed.  This was excessive for our recreation of the model and hence we use a much smaller number of replications in our notebooks.  The original model did not appear to use Common Random Numbers. Our implementation includes CRN and it is likely that less replication is needed to compare experiments. 

