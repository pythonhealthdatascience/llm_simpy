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


## Recreation plan and best practice code organisation

The number of modelling iterations needed to recreate the models was not known in advance. Instead we read the articles reporting the model designs and constructed a general plan that ordered and batched iterations into 12 aims of model recreation. {numref}`table-model-building` details the ordered aims of the model recreation process along with a description and examples of changes to the model that could be expected.  Our aims took us from modelling of arrivals of patients and patient classes (e.g. types of stroke, or unplanned emergencies versus elective patients) through to user interface allowing for basic experimentation. We believe this mirrors how recreation of a DES model would take place regardless of it an LLM was used. 

## General approach to model building


```{table} Ordered aims of the model recreation process
:name: table-model-building
| **Aim** | **Description**                               | **Example additions to model**                                                                                |
|---------|-----------------------------------------------|---------------------------------------------------------------------------------------------------------------|
| 1       | Arrival processes and logic                   | Single and multiple classes of patients                                                                       |
| 2       | Initial queuing logic and activities (delays) | Reneging, patient class dependent length of stay in a ward                                                    |
| 3       | Separation of parameters from model logic     | A configurable Experiment class to hold all model parameters. See {cite}`monks2023improving`                  |
| 4       | Simulated trace control                       | Functionality to hide and display simulated events                                                            |
| 4       | Patient routing                               | Sampling to determine post ward destinations and activities                                                   |
| 5       | Additional queuing and activities             | Additional treatment in a different hospital/ward                                                             |
| 6       | Results collection                            | Audit and calculate ward occupancy, bed utilisation, waiting times etc.                                       |
| 7       | Warm-up period                                | Split the model run length into warm-up and results collection, reset all KPIs, introduce auditing processes. |
| 8       | Multiple replications                         | Multiple unique runs of the model. See {cite}`monks2023improving`                                             |
| 9       | Output analysis procedures                    | Charts and summary tables                                                                                     |
| 10      | Common random numbers                         | Allocate unique random number stream to each distribution                                                     |
| 11      | User interface                                | A web browser based interface for the model. See {cite}`monks2023improving`                                   |
| 12      | Final bug fixes                               | Patch any remaining bugs identified by a 2nd modeller                                   |
```
To optimise organisation and usability of the `simpy` simulation model we adopted the approach of {cite:p}`monks2023improving` in aims 3, 8 and 11.  The result is that model logic is separated from parameters using an `Experiment` class (used to setup "what-if" experiments).  The `Experiment` class is used in combination with a multiple replications wrapper function to generate results.  This simple organisation enables quick integration with Python web app frameworks such as `streamlit` to make models usable by a wider group of people.

To enable both repeatable replications and variance reduction between experiments, we chose to implement common random number (CRN) streams in our models; i.e. each random statistical distribution used for sampling has its own unique controllable pseudo random number stream {cite:p}`Davies2007`.  This is inline with case study 2 that used Simul8 that implements CRN. However, we note that case study 1 was implemented in VBA and it is unclear if CRN streams were implemented by the authors. We aimed to manage all random sampling through the `numpy.random` module and the PCG-64 pseudo-random number generator. For the pilot we followed a simple approach where the replication number was used to spawn $n$ independent random number streams.

Python code should follow coding standards such as PEP8 and PEP257.  For the pilot we chose to relax these standards to reduce the number of lines the LLMs had to generate (in terms of line wrapping and documentation). After all iterations were completed we used the tool `black` to autoformat the code to meet PEP8 standards.


## References

```{bibliography}
:filter: docname in docnames