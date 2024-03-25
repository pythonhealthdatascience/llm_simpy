modify the `multiple_replications` function

before the model is run call the Experiment `setup_stream` method and pass in the current replication number as an argument.

Show the full multiple_replications function code.

```python

def multiple_replications(experiment_instance, num_replications=5):
    rep_results = []
    for _ in range(num_replications):
        rep_results.append(single_run(experiment_instance))
    return rep_results
```