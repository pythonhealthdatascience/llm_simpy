"""A SimPy-based simulation model for analyzing patient flow in stroke care units.
INTERNAL REPRODUCTION RUN - STAGE 2

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
generated between Jun-Jul 2024 by the LLM implemented by Perplexity.AI 
https://www.perplexity.ai/

Auto-formatting:
----------------
After generation was complete We used `black` to autoformat the code
to PEP8 standards

Prompts used:
-----------
The prompts were taken from stage 1 model creation. Additional prompts
were used when needed i.e. if the original prompt did not provide the 
desired output in stage 2.
"""

import math
import statistics
import simpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# lognormal function


def lognormal_to_normal(mean, std):
    """
    Convert lognormal moments to normal moments.

    Parameters:
    mean (float): Mean of the lognormal distribution.
    std (float): Standard deviation of the lognormal distribution.

    Returns:
    tuple: (mean, std) of the corresponding normal distribution.
    """
    normal_mean = np.log(mean**2 / np.sqrt(std**2 + mean**2))
    normal_std = np.sqrt(np.log(std**2 / mean**2 + 1))
    return normal_mean, normal_std


# Experiment class


class Experiment:
    def __init__(self, params=None, random_number_set=0):
        default_params = {
            "results_collection_period": 5 * 365,
            "warm_up": 1095,
            "trace": False,
            "acute_audit_interval": 1,
            "rehab_audit_interval": 1,
            "rehab_stroke_iat": 21.8,
            "rehab_neuro_iat": 31.7,
            "rehab_other_iat": 28.6,
            "rehab_stroke_esd_los_mean": 30.3,
            "rehab_stroke_esd_los_std": 23.1,
            "rehab_stroke_other_los_mean": 28.4,
            "rehab_stroke_other_los_std": 27.2,
            "rehab_complex_neuro_los_mean": 27.6,
            "rehab_complex_neuro_los_std": 28.4,
            "rehab_other_los_mean": 16.1,
            "rehab_other_los_std": 14.1,
            "rehab_stroke_post_destination_probs": [0.4, 0.6],
            "rehab_complex_neuro_post_destination_probs": [0.09, 0.91],
            "rehab_other_post_destination_probs": [0.12, 0.88],
            "patient_types": {
                "Stroke": {
                    "interarrival_time": 1.2,
                    "post_asu_probabilities": [0.24, 0.13, 0.63],
                    "los_params": {
                        "Rehab": (7.4, 8.6),
                        "ESD": (4.6, 4.8),
                        "Other": (7.0, 8.7),
                    },
                },
                "TIA": {
                    "interarrival_time": 9.3,
                    "post_asu_probabilities": [0.01, 0.01, 0.98],
                    "los_params": (1.8, 5.0),
                },
                "Complex Neurological": {
                    "interarrival_time": 3.6,
                    "post_asu_probabilities": [0.11, 0.05, 0.84],
                    "los_params": (4.0, 5.0),
                },
                "Other": {
                    "interarrival_time": 3.2,
                    "post_asu_probabilities": [0.05, 0.10, 0.85],
                    "los_params": (3.8, 5.2),
                },
            },
        }

        if params is None:
            self.params = default_params
        else:
            self.params = self.merge_params(default_params, params)

        self.asu_occupancy = []
        self.rehab_occupancy = []
        self.warm_up = self.params["warm_up"]

        self.setup_streams(random_number_set)

    def merge_params(self, default, new):
        merged = default.copy()
        for key, value in new.items():
            if isinstance(value, dict) and key in merged:
                merged[key] = self.merge_params(merged[key], value)
            else:
                merged[key] = value
        return merged

    def audit_acute_occupancy(
        self, env, first_interval, audit_interval, asu, experiment
    ):
        yield env.timeout(first_interval)
        while True:
            experiment.asu_occupancy.append(asu.occupancy)
            yield env.timeout(audit_interval)

    def audit_rehab_occupancy(
        self, env, first_interval, audit_interval, rehab_unit, experiment
    ):
        yield env.timeout(first_interval)
        while True:
            experiment.rehab_occupancy.append(rehab_unit.occupancy)
            yield env.timeout(audit_interval)

    def reset_kpi(self):
        self.asu_occupancy = []
        self.rehab_occupancy = []

    def setup_streams(self, random_number_set):
        self.streams = []
        generator = np.random.default_rng(random_number_set)
        seeds = generator.integers(0, np.iinfo(np.int64).max, size=25)
        for seed in seeds:
            self.streams.append(np.random.default_rng(seed))


# ### ASU Patient type class


class PatientType:
    def __init__(self, name, interarrival_time, post_asu_probabilities, los_params):
        self.name = name
        self.interarrival_time = interarrival_time
        self.count = 0
        self.rng = None  # This will be set in the patient_generator method
        self.post_asu_probabilities = post_asu_probabilities
        self.los_params = los_params

    def generate_interarrival_time(self):
        return self.exponential(self.interarrival_time)

    def sample_post_asu_destination(self):
        if self.rng is None:
            raise ValueError("RNG not set for PatientType")
        return self.rng.choice(["Rehab", "ESD", "Other"], p=self.post_asu_probabilities)

    def normal_moments(self, destination=None):
        if self.name == "Stroke":
            mean, std = self.los_params[destination]
        else:
            mean, std = self.los_params

        normal_mean = math.log(mean**2 / math.sqrt(std**2 + mean**2))
        normal_std = math.sqrt(math.log(1 + (std**2 / mean**2)))

        return normal_mean, normal_std


# Acute stroke unit class


class AcuteStrokeUnit:
    def __init__(self, env, experiment, rehab_unit):
        self.env = env
        self.experiment = experiment
        self.rehab_unit = rehab_unit
        self.total_arrivals = 0
        self.occupancy = 0
        self.trace = experiment.params["trace"]

        self.patient_types = {}
        for name, params in experiment.params["patient_types"].items():
            self.patient_types[name] = PatientType(
                name,
                params["interarrival_time"],
                params["post_asu_probabilities"],
                params["los_params"],
            )

    def run(self):
        for patient_type in self.patient_types.values():
            self.env.process(self.patient_generator(patient_type))

    def patient_generator(self, patient_type):
        # Assign specific streams for each patient type
        if patient_type.name == "Stroke":
            arrival_stream = self.experiment.streams[6]
            post_asu_stream = self.experiment.streams[7]
        elif patient_type.name == "TIA":
            arrival_stream = self.experiment.streams[8]
            post_asu_stream = self.experiment.streams[9]
        elif patient_type.name == "Complex Neurological":
            arrival_stream = self.experiment.streams[10]
            post_asu_stream = self.experiment.streams[11]
        else:  # Other
            arrival_stream = self.experiment.streams[12]
            post_asu_stream = self.experiment.streams[13]

        # Replace the RNG in the PatientType instance
        patient_type.rng = post_asu_stream

        while True:
            interarrival_time = arrival_stream.exponential(
                patient_type.interarrival_time
            )
            yield self.env.timeout(interarrival_time)
            self.total_arrivals += 1
            patient_type.count += 1
            patient_id = self.total_arrivals - 1
            post_asu_destination = patient_type.sample_post_asu_destination()

            # Assign different seeds based on post-ASU destination for stroke patients
            if patient_type.name == "Stroke":
                if post_asu_destination == "Rehab":
                    los_stream = self.experiment.streams[0]
                elif post_asu_destination == "ESD":
                    los_stream = self.experiment.streams[1]
                else:  # Other
                    los_stream = self.experiment.streams[2]
            else:
                los_stream = None  # Placeholder for non-stroke patients

            if self.trace:
                print(
                    f"Time {self.env.now:.2f}: Patient {patient_id} ({patient_type.name}) arrived"
                )
                print(f" Total arrivals: {self.total_arrivals}")
                print(f" {patient_type.name} arrivals: {patient_type.count}")
                print(f" Post-ASU destination: {post_asu_destination}")
                print(
                    f" Next {patient_type.name} arrival in {interarrival_time:.2f} days"
                )
            self.occupancy += 1
            if self.trace:
                print(f" Current occupancy: {self.occupancy}")
            self.env.process(
                self.acute_treatment(
                    patient_type, patient_id, post_asu_destination, los_stream
                )
            )

    def acute_treatment(
        self, patient_type, patient_id, post_asu_destination, los_stream
    ):
        if patient_type.name == "Stroke":
            yield from self.stroke_acute_treatment(
                patient_type, patient_id, post_asu_destination, los_stream
            )
        elif patient_type.name == "TIA":
            yield from self.tia_acute_treatment(
                patient_type, patient_id, post_asu_destination, los_stream
            )
        elif patient_type.name == "Complex Neurological":
            yield from self.complex_neurological_acute_treatment(
                patient_type, patient_id, post_asu_destination, los_stream
            )
        else:  # Other
            yield from self.other_acute_treatment(
                patient_type, patient_id, post_asu_destination, los_stream
            )
        self.occupancy -= 1
        if self.trace:
            print(
                f"Time {self.env.now:.2f}: Patient {patient_id} ({patient_type.name}) left ASU"
            )
            print(f" Current occupancy: {self.occupancy}")

    def stroke_acute_treatment(
        self, patient_type, patient_id, post_asu_destination, los_stream
    ):
        normal_mean, normal_std = self.patient_types["Stroke"].normal_moments(
            post_asu_destination
        )
        los = los_stream.lognormal(mean=normal_mean, sigma=normal_std)
        if self.trace:
            print(
                f"Time {self.env.now:.2f}: Patient {patient_id} (Stroke) starting acute treatment"
            )
            print(f" Length of stay: {los:.2f} days")
        yield self.env.timeout(los)
        if self.trace:
            print(
                f"Time {self.env.now:.2f}: Patient {patient_id} (Stroke) finished acute treatment"
            )
        if post_asu_destination == "Rehab":
            self.rehab_unit.occupancy += 1
            self.rehab_unit.arrivals_from_asu += 1
            self.env.process(
                self.rehab_unit.rehab_treatment(patient_type.name, patient_id)
            )
            if self.trace:
                print(
                    f" Post-ASU destination (stroke to stroke rehab): {post_asu_destination, patient_id}"
                )

    def tia_acute_treatment(
        self, patient_type, patient_id, post_asu_destination, los_stream
    ):
        normal_mean, normal_std = patient_type.normal_moments()
        los = self.experiment.streams[3].lognormal(mean=normal_mean, sigma=normal_std)
        if self.trace:
            print(
                f"Time {self.env.now:.2f}: Patient {patient_id} (TIA) starting acute treatment"
            )
            print(f" Length of stay: {los:.2f} days")
        yield self.env.timeout(los)
        if self.trace:
            print(
                f"Time {self.env.now:.2f}: Patient {patient_id} (TIA) finished acute treatment"
            )
        if post_asu_destination == "Rehab":
            self.rehab_unit.occupancy += 1
            self.rehab_unit.arrivals_from_asu += 1
            self.env.process(
                self.rehab_unit.rehab_treatment(patient_type.name, patient_id)
            )
            if self.trace:
                print(
                    f" Post-ASU destination (tia to tia rehab): {post_asu_destination, patient_id}"
                )

    def complex_neurological_acute_treatment(
        self, patient_type, patient_id, post_asu_destination, los_stream
    ):
        normal_mean, normal_std = patient_type.normal_moments()
        los = self.experiment.streams[4].lognormal(mean=normal_mean, sigma=normal_std)
        if self.trace:
            print(
                f"Time {self.env.now:.2f}: Patient {patient_id} (Complex Neurological) starting acute treatment"
            )
            print(f" Length of stay: {los:.2f} days")
        yield self.env.timeout(los)
        if self.trace:
            print(
                f"Time {self.env.now:.2f}: Patient {patient_id} (Complex Neurological) finished acute treatment"
            )
        if post_asu_destination == "Rehab":
            self.rehab_unit.occupancy += 1
            self.rehab_unit.arrivals_from_asu += 1
            self.env.process(
                self.rehab_unit.rehab_treatment(patient_type.name, patient_id)
            )
            if self.trace:
                print(
                    f" Post-ASU destination (complex to complex rehab): {post_asu_destination, patient_id}"
                )

    def other_acute_treatment(
        self, patient_type, patient_id, post_asu_destination, los_stream
    ):
        normal_mean, normal_std = patient_type.normal_moments()
        los = self.experiment.streams[5].lognormal(mean=normal_mean, sigma=normal_std)
        if self.trace:
            print(
                f"Time {self.env.now:.2f}: Patient {patient_id} (Other) starting acute treatment"
            )
            print(f" Length of stay: {los:.2f} days")
        yield self.env.timeout(los)
        if self.trace:
            print(
                f"Time {self.env.now:.2f}: Patient {patient_id} (Other) finished acute treatment"
            )
        if post_asu_destination == "Rehab":
            self.rehab_unit.occupancy += 1
            self.rehab_unit.arrivals_from_asu += 1
            self.env.process(
                self.rehab_unit.rehab_treatment(patient_type.name, patient_id)
            )
            if self.trace:
                print(
                    f" Post-ASU destination (other to other rehab): {post_asu_destination, patient_id}"
                )


# Rehabilitation Unit class


class RehabilitationUnit:
    def __init__(self, env, experiment):
        self.env = env
        self.experiment = experiment
        self.trace = experiment.params["trace"]
        self.total_arrivals = 0
        self.arrivals_from_asu = 0
        self.patient_counts = {
            "Stroke": 0,
            "Complex Neurological": 0,
            "Other": 0,
            "TIA": 0,
        }
        self.occupancy = 0
        self.stroke_iat_external = experiment.params["rehab_stroke_iat"]
        self.complex_neuro_iat_external = experiment.params["rehab_neuro_iat"]
        self.other_iat_external = experiment.params["rehab_other_iat"]

        # Convert lognormal moments to normal moments
        self.stroke_esd_mean, self.stroke_esd_std = lognormal_to_normal(
            experiment.params["rehab_stroke_esd_los_mean"],
            experiment.params["rehab_stroke_esd_los_std"],
        )
        self.stroke_other_mean, self.stroke_other_std = lognormal_to_normal(
            experiment.params["rehab_stroke_other_los_mean"],
            experiment.params["rehab_stroke_other_los_std"],
        )
        self.complex_neuro_mean, self.complex_neuro_std = lognormal_to_normal(
            experiment.params["rehab_complex_neuro_los_mean"],
            experiment.params["rehab_complex_neuro_los_std"],
        )
        self.other_mean, self.other_std = lognormal_to_normal(
            experiment.params["rehab_other_los_mean"],
            experiment.params["rehab_other_los_std"],
        )
        self.tia_mean, self.tia_std = lognormal_to_normal(18.7, 23.5)  # TIA parameters

    def run(self):
        self.env.process(self.stroke_generator())
        self.env.process(self.complex_neuro_generator())
        self.env.process(self.other_generator())

    def stroke_generator(self):
        stream = self.experiment.streams[14]
        while True:
            yield self.env.timeout(stream.exponential(self.stroke_iat_external))
            self.patient_arrival("Stroke")

    def complex_neuro_generator(self):
        stream = self.experiment.streams[15]
        while True:
            yield self.env.timeout(stream.exponential(self.complex_neuro_iat_external))
            self.patient_arrival("Complex Neurological")

    def other_generator(self):
        stream = self.experiment.streams[16]
        while True:
            yield self.env.timeout(stream.exponential(self.other_iat_external))
            self.patient_arrival("Other")

    def patient_arrival(self, patient_type):
        patient_id = self.total_arrivals
        self.total_arrivals += 1
        self.patient_counts[patient_type] += 1
        self.occupancy += 1

        if self.experiment.params["trace"]:
            print(
                f"Time {self.env.now:.2f}: Patient {patient_id} ({patient_type}) arrived at RU"
            )
            print(f" Total arrivals: {self.total_arrivals}")
            print(f" {patient_type} arrivals: {self.patient_counts[patient_type]}")
            print(f" Current patient counts: {self.patient_counts}")
            print(f" Current occupancy: {self.occupancy}")

        self.env.process(self.rehab_treatment(patient_type, patient_id))

    def rehab_treatment(self, patient_type, patient_id):
        if patient_type == "Stroke":
            yield from self.stroke_rehab_treatment(patient_id)
        elif patient_type == "Complex Neurological":
            yield from self.complex_neurological_rehab_treatment(patient_id)
        elif patient_type == "TIA":
            yield from self.tia_rehab_treatment(patient_id)
        else:
            yield from self.other_rehab_treatment(patient_id)

        self.occupancy -= 1
        if self.experiment.params["trace"]:
            print(
                f"Time {self.env.now:.2f}: Patient {patient_id} ({patient_type}) left RU"
            )
            print(f" Current occupancy: {self.occupancy}")

    def stroke_rehab_treatment(self, patient_id):
        stream = self.experiment.streams[20]
        post_rehab_destination = self.experiment.streams[19].choice(
            ["ESD", "Other"],
            p=self.experiment.params["rehab_stroke_post_destination_probs"],
        )

        if post_rehab_destination == "ESD":
            length_of_stay = stream.lognormal(self.stroke_esd_mean, self.stroke_esd_std)
        else:
            length_of_stay = stream.lognormal(
                self.stroke_other_mean, self.stroke_other_std
            )

        yield self.env.timeout(length_of_stay)

        if self.experiment.params["trace"]:
            print(
                f"Time {self.env.now:.2f}: Patient {patient_id} (Stroke) completed rehab treatment"
            )
            print(f" Post-rehab destination: {post_rehab_destination}")
            print(f" Length of stay: {length_of_stay:.2f} days")

    def complex_neurological_rehab_treatment(self, patient_id):
        stream = self.experiment.streams[22]
        post_rehab_destination = self.experiment.streams[21].choice(
            ["ESD", "Other"],
            p=self.experiment.params["rehab_complex_neuro_post_destination_probs"],
        )

        length_of_stay = stream.lognormal(
            self.complex_neuro_mean, self.complex_neuro_std
        )

        yield self.env.timeout(length_of_stay)

        if self.experiment.params["trace"]:
            print(
                f"Time {self.env.now:.2f}: Patient {patient_id} (Complex Neurological) completed rehab treatment"
            )
            print(f" Post-rehab destination: {post_rehab_destination}")
            print(f" Length of stay: {length_of_stay:.2f} days")

    def other_rehab_treatment(self, patient_id):
        stream = self.experiment.streams[24]
        post_rehab_destination = self.experiment.streams[23].choice(
            ["ESD", "Other"],
            p=self.experiment.params["rehab_other_post_destination_probs"],
        )

        length_of_stay = stream.lognormal(self.other_mean, self.other_std)

        yield self.env.timeout(length_of_stay)

        if self.experiment.params["trace"]:
            print(
                f"Time {self.env.now:.2f}: Patient {patient_id} (Other) completed rehab treatment"
            )
            print(f" Post-rehab destination: {post_rehab_destination}")
            print(f" Length of stay: {length_of_stay:.2f} days")

    def tia_rehab_treatment(self, patient_id):
        stream = self.experiment.streams[18]
        post_rehab_destination = self.experiment.streams[17].choice(
            ["ESD", "Other"], p=[0, 1]
        )  # Always 'Other' for TIA patients

        length_of_stay = stream.lognormal(self.tia_mean, self.tia_std)

        yield self.env.timeout(length_of_stay)

        if self.experiment.params["trace"]:
            print(
                f"Time {self.env.now:.2f}: Patient {patient_id} (TIA) completed rehab treatment"
            )
            print(f" Post-rehab destination: {post_rehab_destination}")
            print(f" Length of stay: {length_of_stay:.2f} days")


# Occupancy post-processing code


def calculate_occupancy_frequencies(occupancy_list):
    unique_values, counts = np.unique(occupancy_list, return_counts=True)
    relative_freq = counts / len(occupancy_list)
    cumulative_freq = np.cumsum(relative_freq)
    return relative_freq, cumulative_freq, unique_values


def occupancy_plot(
    relative_freq, unique_values, x_label="No. people in ward", figsize=(12, 5)
):
    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(unique_values, relative_freq)
    ax.set_xlabel(x_label)
    ax.set_ylabel("Relative Frequency")
    ax.set_title("Occupancy Distribution")

    # Set x-axis ticks and limits based on the data
    max_value = max(unique_values)
    ax.set_xticks(range(0, max_value + 1, max(1, max_value // 10)))
    ax.set_xlim(0, max_value)

    return fig, ax


# Probability of deplay post-processing code


def calculate_prob_delay(relative_freq, cumulative_freq):
    rel_freq = np.array(relative_freq)
    cum_freq = np.array(cumulative_freq)
    return rel_freq / cum_freq


def prob_delay_plot(
    prob_delay, unique_values, x_label="No. acute beds available", figsize=(12, 5)
):
    fig, ax = plt.subplots(figsize=figsize)
    ax.step(unique_values, prob_delay, where="post")
    ax.set_xlabel(x_label)
    ax.set_ylabel("Probability of Delay")
    ax.set_title("Probability of Delay vs. Number of Beds Available")

    # Set x-axis ticks and limits based on the data
    max_value = max(unique_values)
    ax.set_xticks(range(0, max_value + 1, max(1, max_value // 10)))
    ax.set_xlim(0, max_value)

    ax.set_ylim(0, 1)
    return fig, ax


# Function to perform a single run of ASU+REHAB


def single_run(experiment):
    experiment.reset_kpi()

    # Create the simulation environment
    env = simpy.Environment()

    # Create models
    rehab_unit = RehabilitationUnit(env, experiment)
    asu = AcuteStrokeUnit(env, experiment, rehab_unit)

    # Run models
    rehab_unit.run()
    asu.run()

    # Start the audit processes
    env.process(
        experiment.audit_acute_occupancy(
            env,
            experiment.warm_up,
            experiment.params["acute_audit_interval"],
            asu,
            experiment,
        )
    )
    env.process(
        experiment.audit_rehab_occupancy(
            env,
            experiment.warm_up,
            experiment.params["rehab_audit_interval"],
            rehab_unit,
            experiment,
        )
    )

    # Run the simulation
    env.run(until=experiment.warm_up + experiment.params["results_collection_period"])

    # Calculate occupancy frequencies and probabilities of delay
    rel_freq_a, cum_freq_a, unique_vals_a = calculate_occupancy_frequencies(
        experiment.asu_occupancy
    )
    prob_delay_a = calculate_prob_delay(rel_freq_a, cum_freq_a)

    rel_freq_r, cum_freq_r, unique_vals_r = calculate_occupancy_frequencies(
        experiment.rehab_occupancy
    )
    prob_delay_r = calculate_prob_delay(rel_freq_r, cum_freq_r)

    return {
        "relative_freq_asu": rel_freq_a,
        "prob_delay_asu": prob_delay_a,
        "unique_vals_asu": unique_vals_a,
        "relative_freq_rehab": rel_freq_r,
        "prob_delay_rehab": prob_delay_r,
        "unique_vals_rehab": unique_vals_r,
    }


# Multiple Replication function


def multiple_replications(experiment_instance, num_replications=5):
    rep_results = []
    for rep in range(num_replications):
        # Call setup_streams with the current replication number
        experiment_instance.setup_streams(rep)

        # Run the simulation for this replication
        rep_result = single_run(experiment_instance)

        # Append the results of this replication
        rep_results.append(rep_result)

    return rep_results


# Functions to combine replication results


def combine_pdelay_results(rep_results):
    asu_results = []
    rehab_results = []

    # Determine the maximum occupancy value across all results
    max_occupancy = max(
        max(max(result["unique_vals_asu"]), max(result["unique_vals_rehab"]))
        for result in rep_results
    )

    # Use max_occupancy + 1 to ensure we include the maximum value
    array_size = max_occupancy + 1

    for result in rep_results:
        prob_delay_asu = result["prob_delay_asu"]
        unique_vals_asu = result["unique_vals_asu"]
        min_occupancy_asu = min(unique_vals_asu)

        asu_array = np.zeros(array_size)
        asu_array[unique_vals_asu] = prob_delay_asu
        asu_array[:min_occupancy_asu] = 1.0
        asu_results.append(asu_array)

        prob_delay_rehab = result["prob_delay_rehab"]
        unique_vals_rehab = result["unique_vals_rehab"]
        min_occupancy_rehab = min(unique_vals_rehab)

        rehab_array = np.zeros(array_size)
        rehab_array[unique_vals_rehab] = prob_delay_rehab
        rehab_array[:min_occupancy_rehab] = 1.0
        rehab_results.append(rehab_array)

    return np.array(asu_results), np.array(rehab_results)


def combine_occup_results(rep_results):
    asu_results = []
    rehab_results = []

    # Determine the maximum occupancy value across all results
    max_occupancy = max(
        max(max(result["unique_vals_asu"]), max(result["unique_vals_rehab"]))
        for result in rep_results
    )

    # Use max_occupancy + 1 to ensure we include the maximum value
    array_size = max_occupancy + 1

    for result in rep_results:
        relative_freq_asu = result["relative_freq_asu"]
        unique_vals_asu = result["unique_vals_asu"]

        asu_array = np.zeros(array_size)
        asu_array[unique_vals_asu] = relative_freq_asu
        asu_results.append(asu_array)

        relative_freq_rehab = result["relative_freq_rehab"]
        unique_vals_rehab = result["unique_vals_rehab"]

        rehab_array = np.zeros(array_size)
        rehab_array[unique_vals_rehab] = relative_freq_rehab
        rehab_results.append(rehab_array)

    return np.array(asu_results), np.array(rehab_results)


def mean_results(rep_results):
    return np.mean(rep_results, axis=0)


# Tabular results for p(delay)


def summary_table(prob_delay, min_beds, max_beds, bed_type="ASU"):
    data = {
        f"No. {bed_type} beds": [],
        "Probability of delay": [],
        "% patients delayed": [],
        "1 in every n patients delayed": [],
    }

    for beds in range(min_beds, max_beds + 1):
        if beds < len(prob_delay):
            pdelay = prob_delay[beds]
            data[f"No. {bed_type} beds"].append(beds)
            data["Probability of delay"].append(f"{pdelay:.2f}")
            data["% patients delayed"].append(f"{pdelay * 100:.1f}%")
            if pdelay > 0:
                data["1 in every n patients delayed"].append(int(np.floor(1 / pdelay)))
            else:
                data["1 in every n patients delayed"].append("N/A")
        else:
            # If we've run out of data, fill with N/A
            data[f"No. {bed_type} beds"].append(beds)
            data["Probability of delay"].append("N/A")
            data["% patients delayed"].append("N/A")
            data["1 in every n patients delayed"].append("N/A")

    df = pd.DataFrame(data)
    df.set_index(f"No. {bed_type} beds", inplace=True)
    return df
