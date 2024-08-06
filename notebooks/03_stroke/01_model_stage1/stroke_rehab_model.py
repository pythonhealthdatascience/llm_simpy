"""A SimPy-based simulation model for analyzing patient flow in stroke care units.

This module simulates the patient flow through an Acute Stroke Unit (ASU) and a connected
Rehabilitation Unit to assist in capacity planning for acute and community stroke services.
It models patient arrivals, treatment durations, and transitions between units using
statistical distributions to provide insights into occupancy levels and potential delays.

Authors: LLM implemented by Perplexity.AI
Auto-formatted with `black` for PEP8 compliance.

Based on:
---------
Monks et al. A modelling tool for capacity planning in acute 
and community stroke services
https://link.springer.com/article/10.1186/s12913-016-1789-4

All functions and classes included in this module have been 
generated between Jan-Mar 2024 by the LLM implemented by Perplexity.AI 
https://www.perplexity.ai/

Auto-formatting:
----------------
After generation was complete We used `black` to autoformat the code
to PEP8 standards

Docstrings:
-----------
After auto-formatting the file was uploaded to Perplexity.AI and the 
following query was issued: 

'Write PEP257 compliant docstrings for all functions, classes and methods.  
Provide a brief description of the purpose of the code, document parameters, 
and return values'

All returned docstrings have been incorporated. This includes the initial
part of the module level docstring above.
"""

import simpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# External function to convert Lognormal moments to Normal moments
def normal_moments_from_lognormal(mean, std_dev):
    """Convert lognormal distribution moments to normal distribution moments.

    Parameters:
    - mean (float): The mean of the lognormal distribution.
    - std_dev (float): The standard deviation of the lognormal distribution.

    Returns:
    - tuple: A tuple containing the mean (mu) and standard deviation (sigma) of the
             corresponding normal distribution.
    """

    phi = np.sqrt(std_dev**2 + mean**2)
    mu = np.log(mean**2 / np.sqrt(std_dev**2 + mean**2))
    sigma = np.sqrt(np.log(phi**2 / mean**2))
    return mu, sigma


class Experiment:
    """A class to set up and run the simulation experiment for stroke patient flow.

    This class initializes the simulation parameters, including patient arrival rates,
    treatment durations, and post-treatment destinations. It also sets up the simulation
    environment and runs the simulation to collect occupancy data for analysis.

    Attributes:
    - Various parameters for initializing the simulation (see __init__ method).

    Methods:
    - reset_kpi: Clears the occupancy data lists.
    - setup_streams: Initializes random number streams for the simulation.
    """

    def __init__(
        self,
        stroke_mean=1.2,
        tia_mean=9.3,
        neuro_mean=3.6,
        other_mean=3.2,
        rehab_mean=7.4,
        rehab_std_dev=8.6,
        esd_mean=4.6,
        esd_std_dev=4.8,
        other_dest_mean=7.0,
        other_dest_std_dev=8.7,
        tia_dest_mean=1.8,
        tia_dest_std_dev=5.0,
        neuro_dest_mean=4.0,
        neuro_dest_std_dev=5.0,
        other_dest_mean_2=3.8,
        other_dest_std_dev_2=5.2,
        results_collection_period=1825,
        trace=False,
        rehab_stroke_iat=21.8,
        rehab_neuro_iat=31.7,
        rehab_other_iat=28.6,
        rehab_stroke_esd_mean=30.3,
        rehab_stroke_esd_std_dev=23.1,
        rehab_stroke_other_mean=28.4,
        rehab_stroke_other_std_dev=27.2,
        rehab_neuro_mean=27.6,
        rehab_neuro_std_dev=28.4,
        rehab_other_mean=16.1,
        rehab_other_std_dev=14.1,
        rehab_stroke_post_destination_prob=[0.4, 0.6],
        rehab_neuro_post_destination_prob=[0.09, 0.91],
        rehab_other_post_destination_prob=[0.12, 0.88],
        warm_up=1095,
        random_number_set=0,
    ):
        self.stroke_interarrival_mean = stroke_mean
        self.tia_interarrival_mean = tia_mean
        self.neuro_interarrival_mean = neuro_mean
        self.other_interarrival_mean = other_mean
        self.rehab_mean = rehab_mean
        self.rehab_std_dev = rehab_std_dev
        self.esd_mean = esd_mean
        self.esd_std_dev = esd_std_dev
        self.other_dest_mean = other_dest_mean
        self.other_dest_std_dev = other_dest_std_dev
        self.tia_dest_mean = tia_dest_mean
        self.tia_dest_std_dev = tia_dest_std_dev
        self.neuro_dest_mean = neuro_dest_mean
        self.neuro_dest_std_dev = neuro_dest_std_dev
        self.other_dest_mean_2 = other_dest_mean_2
        self.other_dest_std_dev_2 = other_dest_std_dev_2
        self.results_collection_period = results_collection_period
        self.warm_up = warm_up  # New member variable for warm-up period
        self.trace = trace
        self.asu_occupancy = []  # List to store ASU occupancy data
        self.rehab_occupancy = []  # List to store Rehabilitation Unit occupancy data

        # New parameters for RehabilitationUnit treatment distributions and probabilities
        self.rehab_stroke_iat = rehab_stroke_iat
        self.rehab_neuro_iat = rehab_neuro_iat
        self.rehab_other_iat = rehab_other_iat

        self.rehab_stroke_esd_mean = rehab_stroke_esd_mean
        self.rehab_stroke_esd_std_dev = rehab_stroke_esd_std_dev

        self.rehab_stroke_other_mean = rehab_stroke_other_mean
        self.rehab_stroke_other_std_dev = rehab_stroke_other_std_dev

        self.rehab_neuro_mean = rehab_neuro_mean
        self.rehab_neuro_std_dev = rehab_neuro_std_dev

        self.rehab_other_mean = rehab_other_mean
        self.rehab_other_std_dev = rehab_other_std_dev

        # Probabilities for post-rehab destination sampling
        # for each patient type in RehabilitationUnit
        self.rehab_stroke_post_destination_prob = rehab_stroke_post_destination_prob
        self.rehab_neuro_post_destination_prob = rehab_neuro_post_destination_prob
        self.rehab_other_post_destination_prob = rehab_other_post_destination_prob

        # Call the setup_streams method with the provided random_number_set parameter
        self.setup_streams(random_number_set)

    def reset_kpi(self):
        """Reset the key performance indicators (occupancy lists) to empty."""
        self.asu_occupancy.clear()
        self.rehab_occupancy.clear()

    def setup_streams(self, random_number_set):
        """Setup random number streams based on the provided seed.

        Parameters:
        - random_number_set (int): The seed for generating random number streams.
        """
        # Create an empty list to store random number generator objects
        self.streams = []

        # Create a numpy random default_rng generator
        # object using random_number_set as a seed.
        rng_seed_generator = np.random.default_rng(random_number_set)

        # Generate a list of 25 random integer seeds sampled from
        # a uniform distribution with lower bound 0 and upper bound
        # equal to the system's maximum 64-bit integer size.
        seeds = rng_seed_generator.integers(0, np.iinfo(np.int64).max, size=25)

        # Loop through the seeds and create a new numpy random default_rng
        # object for each seed and append it to the streams list.
        for seed in seeds:
            rng_obj = np.random.default_rng(seed)
            self.streams.append(rng_obj)


class AcuteStrokeUnit:
    """A class representing the Acute Stroke Unit in the simulation.

    This class models the arrival and acute treatment of stroke patients, tracking occupancy
    and simulating the duration of stay based on treatment type.

    Attributes:
    - env (simpy.Environment): The simulation environment.
    - experiment (Experiment): The experiment configuration.
    - rehab_unit (RehabilitationUnit): The connected Rehabilitation Unit.

    Methods:
    - stroke_acute_treatment, tia_acute_treatment, etc.: Simulate the treatment process.
    - stroke_patient_generator, tia_patient_generator, etc.: Generate patients over time.
    """

    def __init__(self, env, experiment, rehab_unit):
        """Initialize the Acute Stroke Unit with the simulation environment and parameters.

        Parameters:
        - env (simpy.Environment): The simulation environment.
        - experiment (Experiment): The experiment configuration.
        - rehab_unit (RehabilitationUnit): The connected Rehabilitation Unit.
        """
        self.env = env
        self.experiment = experiment
        self.rehab_unit = rehab_unit
        self.patient_count = 0
        self.occupancy = 0

    def stroke_acute_treatment(self, post_asu_destination):
        """Simulate the acute treatment process for a stroke patient.

        Parameters:
        - post_asu_destination (str): The destination of the patient after ASU treatment.

        The method simulates the treatment duration and updates occupancy accordingly.
        """
        if post_asu_destination == "Rehab":
            mu, sigma = normal_moments_from_lognormal(
                self.experiment.rehab_mean, self.experiment.rehab_std_dev
            )
            length_of_stay = self.experiment.streams[0].lognormal(mean=mu, sigma=sigma)
        elif post_asu_destination == "ESD":
            mu, sigma = normal_moments_from_lognormal(
                self.experiment.esd_mean, self.experiment.esd_std_dev
            )
            length_of_stay = self.experiment.streams[1].lognormal(mean=mu, sigma=sigma)
        else:
            mu, sigma = normal_moments_from_lognormal(
                self.experiment.other_dest_mean, self.experiment.other_dest_std_dev
            )
            length_of_stay = self.experiment.streams[2].lognormal(mean=mu, sigma=sigma)

        self.occupancy += 1  # Increment occupancy when a patient arrives
        yield self.env.timeout(length_of_stay)
        if self.experiment.trace:
            print(
                f"Stroke patient {self.patient_count} finished treatment at {self.env.now} days"
            )
        self.occupancy -= 1  # Decrement occupancy at the end of treatment
        if post_asu_destination == "Rehab":
            self.rehab_unit.occupancy += 1
            self.env.process(self.rehab_unit.stroke_rehab_treatment())

    def tia_acute_treatment(self, post_asu_destination):
        mu, sigma = normal_moments_from_lognormal(
            self.experiment.tia_dest_mean, self.experiment.tia_dest_std_dev
        )
        length_of_stay = self.experiment.streams[3].lognormal(mean=mu, sigma=sigma)

        self.occupancy += 1  # Increment occupancy when a patient arrives
        yield self.env.timeout(length_of_stay)
        if self.experiment.trace:
            print(
                f"TIA patient {self.patient_count} finished treatment at {self.env.now} days"
            )
        self.occupancy -= 1  # Decrement occupancy at the end of treatment
        if post_asu_destination == "Rehab":
            self.rehab_unit.occupancy += 1
            self.env.process(self.rehab_unit.tia_rehab_treatment())

    def neuro_acute_treatment(self, post_asu_destination):
        mu, sigma = normal_moments_from_lognormal(
            self.experiment.neuro_dest_mean, self.experiment.neuro_dest_std_dev
        )
        length_of_stay = self.experiment.streams[4].lognormal(mean=mu, sigma=sigma)

        self.occupancy += 1  # Increment occupancy when a patient arrives
        yield self.env.timeout(length_of_stay)
        if self.experiment.trace:
            print(
                f"Complex Neuro patient {self.patient_count} finished treatment at {self.env.now} days"
            )
        self.occupancy -= 1  # Decrement occupancy at the end of treatment
        if post_asu_destination == "Rehab":
            self.rehab_unit.occupancy += 1
            self.env.process(self.rehab_unit.neuro_rehab_treatment())

    def other_acute_treatment(self, post_asu_destination):
        mu, sigma = normal_moments_from_lognormal(
            self.experiment.other_dest_mean_2, self.experiment.other_dest_std_dev_2
        )
        length_of_stay = self.experiment.streams[5].lognormal(mean=mu, sigma=sigma)

        self.occupancy += 1  # Increment occupancy when a patient arrives
        yield self.env.timeout(length_of_stay)
        if self.experiment.trace:
            print(
                f"Other patient {self.patient_count} finished treatment at {self.env.now} days"
            )
        self.occupancy -= 1  # Decrement occupancy at the end of treatment
        if post_asu_destination == "Rehab":
            self.rehab_unit.occupancy += 1
            self.env.process(self.rehab_unit.other_rehab_treatment())

    def stroke_patient_generator(self):
        while True:
            interarrival_time = self.experiment.streams[6].exponential(
                self.experiment.stroke_interarrival_mean
            )
            yield self.env.timeout(interarrival_time)
            self.patient_count += 1
            post_asu_destination = self.experiment.streams[7].choice(
                ["Rehab", "ESD", "Other"], p=[0.24, 0.13, 0.63]
            )
            if self.experiment.trace:
                print(
                    f"Stroke patient {self.patient_count} arrived at {self.env.now} days and will go to {post_asu_destination}"
                )
            self.env.process(self.stroke_acute_treatment(post_asu_destination))

    def tia_patient_generator(self):
        while True:
            interarrival_time = self.experiment.streams[8].exponential(
                self.experiment.tia_interarrival_mean
            )
            yield self.env.timeout(interarrival_time)
            self.patient_count += 1
            post_asu_destination = self.experiment.streams[9].choice(
                ["Rehab", "ESD", "Other"], p=[0.01, 0.01, 0.98]
            )
            if self.experiment.trace:
                print(
                    f"TIA patient {self.patient_count} arrived at {self.env.now} days and will go to {post_asu_destination}"
                )
            self.env.process(self.tia_acute_treatment(post_asu_destination))

    def neuro_patient_generator(self):
        while True:
            interarrival_time = self.experiment.streams[10].exponential(
                self.experiment.neuro_interarrival_mean
            )
            yield self.env.timeout(interarrival_time)
            self.patient_count += 1
            post_asu_destination = self.experiment.streams[11].choice(
                ["Rehab", "ESD", "Other"], p=[0.11, 0.05, 0.84]
            )
            if self.experiment.trace:
                print(
                    f"Complex Neuro patient {self.patient_count} arrived at {self.env.now} days and will go to {post_asu_destination}"
                )
            self.env.process(self.neuro_acute_treatment(post_asu_destination))

    def other_patient_generator(self):
        while True:
            interarrival_time = self.experiment.streams[12].exponential(
                self.experiment.other_interarrival_mean
            )
            yield self.env.timeout(interarrival_time)
            self.patient_count += 1
            post_asu_destination = self.experiment.streams[13].choice(
                ["Rehab", "ESD", "Other"], p=[0.05, 0.10, 0.85]
            )
            if self.experiment.trace:
                print(
                    f"Other patient {self.patient_count} arrived at {self.env.now} days and will go to {post_asu_destination}"
                )
            self.env.process(self.other_acute_treatment(post_asu_destination))


class RehabilitationUnit:
    """A class representing the Rehabilitation Unit in the simulation.

    This class models the rehabilitation treatment of patients, tracking occupancy and
    simulating the duration of stay based on post-rehabilitation destinations.

    Attributes and methods are similar in purpose to those of the AcuteStrokeUnit class.
    """

    def __init__(self, env, experiment):
        self.env = env
        self.experiment = experiment
        self.patient_count = 0
        self.stroke_count = 0
        self.neuro_count = 0
        self.other_count = 0
        self.occupancy = 0

    def stroke_patient_generator(self):
        while True:
            interarrival_time = self.experiment.streams[14].exponential(
                self.experiment.rehab_stroke_iat
            )
            yield self.env.timeout(interarrival_time)
            self.patient_count += 1
            self.stroke_count += 1
            if self.experiment.trace:
                print(
                    f"Stroke patient {self.patient_count} arrived at Rehabilitation Unit at {self.env.now} days"
                )
            self.occupancy += 1
            self.env.process(self.stroke_rehab_treatment())

    def neuro_patient_generator(self):
        while True:
            interarrival_time = self.experiment.streams[15].exponential(
                self.experiment.rehab_neuro_iat
            )
            yield self.env.timeout(interarrival_time)
            self.patient_count += 1
            self.neuro_count += 1
            if self.experiment.trace:
                print(
                    f"Complex Neurological patient {self.patient_count} arrived at Rehabilitation Unit at {self.env.now} days"
                )
            self.occupancy += 1
            self.env.process(self.neuro_rehab_treatment())

    def other_patient_generator(self):
        while True:
            interarrival_time = self.experiment.streams[16].exponential(
                self.experiment.rehab_other_iat
            )
            yield self.env.timeout(interarrival_time)
            self.patient_count += 1
            self.other_count += 1
            if self.experiment.trace:
                print(
                    f"Other patient {self.patient_count} arrived at Rehabilitation Unit at {self.env.now} days"
                )
            self.occupancy += 1
            self.env.process(self.other_rehab_treatment())

    def tia_rehab_treatment(self):
        post_rehab_destination = self.experiment.streams[17].choice([0, 100])
        mu, sigma = normal_moments_from_lognormal(18.7, 23.5)

        length_of_stay = self.experiment.streams[18].lognormal(mean=mu, sigma=sigma)

        yield self.env.timeout(length_of_stay)

        if self.experiment.trace:
            print(
                f"TIA patient {self.patient_count} finished treatment at Rehabilitation Unit at {self.env.now} days"
            )

        self.occupancy -= 1

    def stroke_rehab_treatment(self):
        post_rehab_destination = self.experiment.streams[19].choice(
            ["ESD", "Other"], p=self.experiment.rehab_stroke_post_destination_prob
        )
        if post_rehab_destination == "ESD":
            mu, sigma = normal_moments_from_lognormal(
                self.experiment.rehab_stroke_esd_mean,
                self.experiment.rehab_stroke_esd_std_dev,
            )
        else:
            mu, sigma = normal_moments_from_lognormal(
                self.experiment.rehab_stroke_other_mean,
                self.experiment.rehab_stroke_other_std_dev,
            )

        length_of_stay = self.experiment.streams[20].lognormal(mean=mu, sigma=sigma)

        yield self.env.timeout(length_of_stay)

        if self.experiment.trace:
            print(
                f"Stroke patient {self.patient_count} finished treatment at Rehabilitation Unit at {self.env.now} days"
            )

        self.occupancy -= 1

    def neuro_rehab_treatment(self):
        post_rehab_destination = self.experiment.streams[21].choice(
            ["ESD", "Other"], p=self.experiment.rehab_neuro_post_destination_prob
        )
        mu, sigma = normal_moments_from_lognormal(
            self.experiment.rehab_neuro_mean, self.experiment.rehab_neuro_std_dev
        )

        length_of_stay = self.experiment.streams[22].lognormal(mean=mu, sigma=sigma)

        yield self.env.timeout(length_of_stay)

        if self.experiment.trace:
            print(
                f"Complex Neurological patient {self.patient_count} finished treatment at Rehabilitation Unit at {self.env.now} days"
            )

        self.occupancy -= 1

    def other_rehab_treatment(self):
        post_rehab_destination = self.experiment.streams[23].choice(
            ["ESD", "Other"], p=self.experiment.rehab_other_post_destination_prob
        )
        mu, sigma = normal_moments_from_lognormal(
            self.experiment.rehab_other_mean, self.experiment.rehab_other_std_dev
        )

        length_of_stay = self.experiment.streams[24].lognormal(mean=mu, sigma=sigma)

        yield self.env.timeout(length_of_stay)

        if self.experiment.trace:
            print(
                f"Other patient {self.patient_count} finished treatment at Rehabilitation Unit at {self.env.now} days"
            )

        self.occupancy -= 1


def audit_acute_occupancy(env, first_interval, audit_interval, asu, experiment):
    """Record the occupancy of the Acute Stroke Unit at regular intervals.

    Parameters:
    - env (simpy.Environment): The simulation environment.
    - first_interval (int): The initial delay before starting the audit.
    - audit_interval (int): The interval between occupancy recordings.
    - asu (AcuteStrokeUnit): The Acute Stroke Unit being audited.
    - experiment (Experiment): The experiment configuration.
    """
    yield env.timeout(first_interval)
    while True:
        experiment.asu_occupancy.append(asu.occupancy)
        yield env.timeout(audit_interval)


def audit_rehab_occupancy(env, first_interval, audit_interval, rehab_unit, experiment):
    """Record the occupancy of the Rehabilitation Unit at regular intervals."""
    yield env.timeout(first_interval)
    while True:
        experiment.rehab_occupancy.append(rehab_unit.occupancy)
        yield env.timeout(audit_interval)


def calculate_occupancy_frequencies(data):
    unique_values, counts = np.unique(data, return_counts=True)
    relative_frequency = counts / len(data)
    cumulative_frequency = np.cumsum(relative_frequency)
    return relative_frequency, cumulative_frequency, unique_values


def occupancy_plot(relative_frequency, unique_values, x_label="No. people in ASU", fig_size=(12, 5)):
    """Generate a plot of the occupancy relative frequency distribution.

    Parameters:
    - relative_frequency (numpy.ndarray): The relative frequencies of occupancy levels.
    - unique_values (numpy.ndarray): The unique occupancy levels observed.
    - x_label (str): The label for the x-axis.
    - fig_size (tuple): The size of the figure.

    Returns:
    - matplotlib.figure.Figure, matplotlib.axes.Axes: The figure and axes of the plot.
    """
    fig, ax = plt.subplots(figsize=fig_size)
    ax.bar(unique_values, relative_frequency, align='center', alpha=0.7)
    
    # Dynamically set x-axis ticks based on the range of unique values
    max_value = max(unique_values)
    tick_step = max(1, max_value // 10)  # Ensure at least 10 ticks, but not more than the number of unique values
    ax.set_xticks(np.arange(0, max_value + 1, tick_step))
    
    ax.set_xlabel(x_label)
    ax.set_ylabel('Relative Frequency')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.title('Occupancy Relative Frequency Distribution')
    plt.tight_layout()
    return fig, ax


def calculate_prob_delay(relative_frequencies, cumulative_frequencies):
    prob_delay = np.array(relative_frequencies) / np.array(cumulative_frequencies)
    return prob_delay


def prob_delay_plot(prob_delay, unique_values, x_label="No. acute beds available", fig_size=(12, 5)):
    fig, ax = plt.subplots(figsize=fig_size)
    ax.step(unique_values, prob_delay, where='post')
    
    # Dynamically set x-axis ticks based on the range of unique values
    max_value = max(unique_values)
    tick_step = max(1, max_value // 10)  # Ensure at least 10 ticks, but not more than the number of unique values
    ax.set_xticks(np.arange(0, max_value + 1, tick_step))
    
    ax.set_xlabel(x_label)
    ax.set_ylabel('Probability of Delay')
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.title('Probability of Delay Distribution')
    plt.tight_layout()
    return fig, ax

def single_run(experiment):
    """Run a single simulation with the provided experiment configuration.

    Parameters:
    - experiment (Experiment): The experiment configuration.

    Returns:
    - dict: A dictionary containing the occupancy frequencies and
    probability of delay for both the Acute Stroke Unit and the Rehabilitation Unit.
    """
    experiment.reset_kpi()

    env = simpy.Environment()

    # Create an instance of RehabilitationUnit and AcuteStrokeUnit
    # with the Experiment parameters
    rehab_unit = RehabilitationUnit(env, experiment)
    acu_experiment = AcuteStrokeUnit(env, experiment, rehab_unit)

    # Initialize patient generators as simpy processes in both units
    env.process(acu_experiment.stroke_patient_generator())
    env.process(acu_experiment.tia_patient_generator())
    env.process(acu_experiment.neuro_patient_generator())
    env.process(acu_experiment.other_patient_generator())

    env.process(rehab_unit.stroke_patient_generator())
    env.process(rehab_unit.neuro_patient_generator())
    env.process(rehab_unit.other_patient_generator())

    # Initialize audit functions for both units to record occupancy at intervals
    env.process(
        audit_rehab_occupancy(env, experiment.warm_up, 1, rehab_unit, experiment)
    )
    env.process(
        audit_acute_occupancy(env, experiment.warm_up, 1, acu_experiment, experiment)
    )

    # Run the simulation for the specified period (results_collection_period + warm_up)
    env.run(until=experiment.results_collection_period + experiment.warm_up)

    # Calculate occupancy frequencies and probability of
    # delay for both units and return the results in a dictionary
    (
        relative_freq_asu,
        cumulative_freq_asu,
        unique_vals_asu,
    ) = calculate_occupancy_frequencies(experiment.asu_occupancy)
    (
        relative_freq_rehab,
        cumulative_freq_rehab,
        unique_vals_rehab,
    ) = calculate_occupancy_frequencies(experiment.rehab_occupancy)

    prob_delay_asu = calculate_prob_delay(relative_freq_asu, cumulative_freq_asu)
    prob_delay_rehab = calculate_prob_delay(relative_freq_rehab, cumulative_freq_rehab)

    return {
        "relative_freq_asu": relative_freq_asu,
        "prob_delay_asu": prob_delay_asu,
        "unique_vals_asu": unique_vals_asu,
        "relative_freq_rehab": relative_freq_rehab,
        "prob_delay_rehab": prob_delay_rehab,
        "unique_vals_rehab": unique_vals_rehab,
    }


def multiple_replications(experiment_instance, num_replications=5):
    """Run multiple simulations with the provided experiment configuration
    and number of replications.

    Parameters:
    - experiment (Experiment): The experiment configuration.
    - num_replications (int): The number of simulations to run.

    Returns:
    - list: A list of dictionaries, each containing the occupancy
    frequencies and probability of delay for both the Acute Stroke Unit
    and the Rehabilitation Unit from a single simulation run.
    """
    rep_results = []
    for replication_number in range(num_replications):
        experiment_instance.setup_streams(replication_number)

        rep_results.append(single_run(experiment_instance))
    return rep_results


def combine_pdelay_results(rep_results):
    """Combine the probability of delay results from multiple simulation runs.

    Parameters:
    - results (list): A list of dictionaries, each containing the occupancy
    frequencies and probability of delay for both the Acute Stroke Unit and
    the Rehabilitation Unit from a single simulation run.
    """
    result_list_asu = []
    result_list_rehab = []
    
    max_occupancy_asu = max(max(rep['unique_vals_asu']) for rep in rep_results)
    max_occupancy_rehab = max(max(rep['unique_vals_rehab']) for rep in rep_results)
    
    for rep_result in rep_results:
        prob_delay_asu = rep_result['prob_delay_asu']
        unique_vals_asu = rep_result['unique_vals_asu']
        
        min_occupancy_asu = min(unique_vals_asu)
        
        new_array_asu = np.zeros(max_occupancy_asu + 1)
        for i, val in zip(unique_vals_asu, prob_delay_asu):
            new_array_asu[i] = val
        
        new_array_asu[:min_occupancy_asu] = 1.0
        
        result_list_asu.append(new_array_asu)
        
        prob_delay_rehab = rep_result['prob_delay_rehab']
        unique_vals_rehab = rep_result['unique_vals_rehab']
        
        min_occupancy_rehab = min(unique_vals_rehab)
        
        new_array_rehab = np.zeros(max_occupancy_rehab + 1)
        for i, val in zip(unique_vals_rehab, prob_delay_rehab):
            new_array_rehab[i] = val
        
        new_array_rehab[:min_occupancy_rehab] = 1.0
        
        result_list_rehab.append(new_array_rehab)
    
    return np.array(result_list_asu), np.array(result_list_rehab)

def combine_occup_results(rep_results):
    """Combine the occupancy frequency results from multiple simulation runs.

    Parameters:
    - results (list): A list of dictionaries, each containing the occupancy
    frequencies and probability of delay for both the Acute Stroke Unit
    and the Rehabilitation Unit from a single simulation run.
    """
    result_list_asu = []
    result_list_rehab = []
    
    max_occupancy_asu = max(max(rep['unique_vals_asu']) for rep in rep_results)
    max_occupancy_rehab = max(max(rep['unique_vals_rehab']) for rep in rep_results)
    
    for rep_result in rep_results:
        relative_freq_asu = rep_result['relative_freq_asu']
        unique_vals_asu = rep_result['unique_vals_asu']
        
        new_array_asu = np.zeros(max_occupancy_asu + 1)
        for i, val in zip(unique_vals_asu, relative_freq_asu):
            new_array_asu[i] = val
        
        result_list_asu.append(new_array_asu)
        
        relative_freq_rehab = rep_result['relative_freq_rehab']
        unique_vals_rehab = rep_result['unique_vals_rehab']
        
        new_array_rehab = np.zeros(max_occupancy_rehab + 1)
        for i, val in zip(unique_vals_rehab, relative_freq_rehab):
            new_array_rehab[i] = val
        
        result_list_rehab.append(new_array_rehab)
    
    return np.array(result_list_asu), np.array(result_list_rehab)


def mean_results(rep_results):
    return np.mean(rep_results, axis=0)


def summary_table(mean_pdelay, min_beds, max_beds, bed_type):
    """Generate a summary table of the occupancy frequencies
    and probability of delay results.

    Parameters:
    - results (dict): The combined occupancy frequency and
    probability of delay results for both the Acute Stroke Unit
    and the Rehabilitation Unit.

    """
    sliced_mean_pdelay = mean_pdelay[min_beds : max_beds + 1]
    inv_mean_pdelay = 1 / sliced_mean_pdelay
    inv_mean_pdelay_rounded = np.floor(inv_mean_pdelay).astype(int)

    df_summary_table = pd.DataFrame(
        {
            "p(delay)": sliced_mean_pdelay.round(2),
            "1 in every n patients delayed": inv_mean_pdelay_rounded,
        },
        index=pd.Index(range(min_beds, max_beds + 1), name="No. " + bed_type + " beds"),
    )

    return df_summary_table
