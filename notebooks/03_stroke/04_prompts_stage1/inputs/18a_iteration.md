Modify the script to run the model as follows:

1. create an experiment
2. create an instance of a simpy environment
3. create an instance RehabilitationUnit
4. initialise the patient generators as simpy processes
5. initialise the audit of rehab occupancy as a simpy process. Use an interval of 1 day.
6. run the model for the default run length in the experiment * 10
7. use `calculate_occupancy_frequencies` to calculate occupancy frequencies of the rehab occupancy
8. use `occupancy_plot` to display an occupancy plot for the rehab unit. The x axis should be labelled "No. of people in rehab"
9. use `calculate_prob_delay` to calculate the probability of delay for rehab
10. use `prob_delay_plot` to display a prob of delay plot for rehab. The x label is "No. rehab beds available"

```python
def calculate_occupancy_frequencies(data):
    unique_values, counts = np.unique(data, return_counts=True)
    relative_frequency = counts / len(data)
    cumulative_frequency = np.cumsum(relative_frequency)
    return relative_frequency, cumulative_frequency, unique_values


def occupancy_plot(relative_frequency, unique_values, x_label="No. people in ASU", fig_size=(12, 5)):
    fig, ax = plt.subplots(figsize=fig_size)
    ax.bar(unique_values, relative_frequency, align='center', alpha=0.7)
    ax.set_xticks(np.arange(0, 31, 1))
    ax.set_xlabel(x_label)
    ax.set_ylabel('Relative Frequency')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.title('Occupancy Relative Frequency Distribution')
    plt.show()
    return fig, ax

def calculate_prob_delay(relative_frequencies, cumulative_frequencies):
    prob_delay = np.array(relative_frequencies) / np.array(cumulative_frequencies)
    return prob_delay

def prob_delay_plot(prob_delay, unique_values, x_label="No. acute beds available", fig_size=(12, 5)):
    fig, ax = plt.subplots(figsize=fig_size)
    ax.step(unique_values, prob_delay, where='post')
    ax.set_xticks(np.arange(0, 31, 1))
    ax.set_xlabel(x_label)
    ax.set_ylabel('Probability of Delay')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.title('Probability of Delay Distribution')
    plt.show()
    return fig, ax
```