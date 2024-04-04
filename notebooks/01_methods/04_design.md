# Model design

## Simpy models

All generated models were built in `simpy` {cite:p}`simpy`: a process-based DES package implemented in Python that is available under a permissive MIT license. DES models are built by defining Python generator functions and logic to request and return resources. The `simpy` is lightweight and provides a full event scheduling engine. Statistical distributions for sampling, common random number streams, output analysis tools, user interfaces, and model animation are not included. The implementation of all of these tools are available in the general and scientific Python stack. For example, `numpy` and `pandas` for sampling and output analysis, and `matplotlib` for visualising results.

For those unfamiliar with `simpy`, a simple simulation model of a urgent care call centre is presented below. This is based on introductory tutorial material published elsewhere {cite:p}`monksharper_simpy_tutorial, monks2023improving`. In the interest of space we have removed docstrings and comments from the code.  The model consists of three parts. First is patient generator function `arrivals_generator` that generates inter-arrival times following an exponential distribution. Second a `service` function where patient processes request call operator resources and when available samples a call duration from a triangular distribution.  A simulated trace is provided as the model runs.  The final part of the code is a script to run the model. It creates a `simpy` environment (that holds the DES engine), the call operator resources, schedules the patient generator function, and starts the simulation run for a user specified run length. See {cite}`monksharper_simpy_tutorial` for a full tutorial.

```python
import simpy
import numpy as np
import itertools

def service(identifier, operators, env):
    start_wait = env.now

    with operators.request() as req:
        yield req

        waiting_time = env.now - start_wait
        print(f'operator answered call {identifier} at ' \
              + f'{env.now:.3f}')

        call_duration = np.random.triangular(left=5.0, mode=7.0,
                                             right=10.0)
        
        yield env.timeout(call_duration)

        print(f'call {identifier} ended {env.now:.3f}; ' \
              + f'waiting time was {waiting_time:.3f}')


def arrivals_generator(env, operators):
    for caller_count in itertools.count(start=1):

        inter_arrival_time = np.random.exponential(60/100)
        yield env.timeout(inter_arrival_time)

        print(f'call arrives at: {env.now:.3f}')

        env.process(service(caller_count, operators, env))


if __name__ == '__main__':
    RUN_LENGTH = 100
    N_OPERATORS = 13
    
    env = simpy.Environment()
    operators = simpy.Resource(env, capacity=N_OPERATORS)
    
    env.process(arrivals_generator(env, operators))
    env.run(until=RUN_LENGTH)
    print(f'end of run. simulation clock time = {env.now}')
```


## Code organisation, standards, and best practice

To optimise organisation and usability of the `simpy` simulation model we adopted the approach of {cite:p}`monks2023improving`. 

1. A model logic is separated from parameters using an `Experiment` class.
2. 

## General approach to model building

| **Aim** | **Description**                               | **Example additions to model**                                                                                |
|---------|-----------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| 1       | Arrival processes and logic                   | Single and multiple classes of patients                                                                       |
| 2       | Initial queuing logic and activities (delays) | Reneging, patient class dependent length of stay in a ward                                                    |
| 3       | Separation of parameters from model logic     | A configurable Experiment class to hold all model parameters                                                  |
| 4       | Simulated trace control                       | Functionality to hide and display simulated events                                                            |
| 4       | Patient routing                               | Sampling to determine post ward destinations and activities                                                   |
| 5       | Additional queuing and activities             | Additional treatment in a different hospital/ward                                                             |
| 6       | Results collection                            | Audit and calculate ward occupancy, bed utilisation, waiting times etc.                                       |
| 7       | Warm-up period                                | Split the model run length into warm-up and results collection, reset all KPIs, introduce auditing processes. |
| 8       | Multiple replications                         | Multiple unique runs of the model                                                                             |
| 9       | Output analysis procedures                    | Charts and summary tables                                                                                     |
| 10      | Common random numbers                         | Allocate unique random number stream to each distribution                                                     |
| 11      | User interface                                | A web browser based interface for the model.                                                                  |



## References

```{bibliography}
:filter: docname in docnames