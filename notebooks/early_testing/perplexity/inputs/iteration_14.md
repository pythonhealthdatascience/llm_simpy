create two classes for the Exponential and Normal distributions

The constructor of each class should accept the distribution parameters, and an random seed (default=None).  The constructor should create an instance of a numpy random Generator using the random seed.  The class should provide a function called "sample" that 


Update the CCUModel class and add five instances of numpy random Generator objects. These will be used by the patient generator functions to sample the next inter-arrival time.  As these objects are created they are passed their own random seed. These are stored in the Experiment class with the default value "none".



The objects should be given appropriate names and the generator and treatment functions should be updated to sample from the correct distributions.

