### Main command

Modify the model to add in an elective admissions treatment process.

Show the full code listing for the model.  Do not exclude any functions or classes.

### general simulation logic

Add a new arrival source to the CCU: Elective surgery

Elective surgery patients are modelled as a separate process from the unplanned admissions, but share the critical care bed resources. 

As an elective patient arrives to the CCU a check is made on the number of critical care beds available.  There are two outcomes from this check

Outcome 1: the number of beds in use is equal to the total number of beds available. In this case the elective patient leaves the model immediately. This is called a "cancelled operation" event and should be reported to the user.

Outcome 2. the number of beds in use is less than the total number of beds available. In this case the elective patient requests a critical care bed, is treated, and is then discharged. Before the bed is released for another patient there is an additional delay for intensive cleaning of the area and the bed.

### simulation inputs

the interarrival time of elective surgery patients has a normal distribution with mean 17.91 and standard deviation 3.16.

the treatment time of elective surgery patients is exponential mean: 57.34