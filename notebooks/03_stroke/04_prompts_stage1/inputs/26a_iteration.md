modify all patient_generator functions in the `AcuteStrokeUnit` class. Do not modify the acute_treatment functions.

code that uses `numpy.random`, must be replaced with a call to a unique stream in the `Experiment` list `streams`. Select the stream using a hard coded integer. Start from 6 and increment by 1 each time to allocate a unique number to each stream.  E.g. in `stroke_patient_generator` the first instance of `interarrival_time = np.random.exponential(self.experiment.stroke_interarrival_mean)` becomes `interarrival_time = self.experiment.streams[6](self.experiment.stroke_interarrival_mean)`; the call to choice will then use index 7.  Do not add new parameters to any methods.

Show the full AcuteStrokeUnit including all patient generator and treatment functions.  

