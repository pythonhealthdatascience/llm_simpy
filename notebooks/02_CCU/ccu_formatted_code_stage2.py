import numpy as np
import pandas as pd
import math

import simpy


class Experiment:
    def __init__(
        self,
        accident_emergency_arrival_rate=22.72,
        wards_arrival_rate=26.0,
        emergency_surgery_arrival_rate=37.0,
        other_hospitals_arrival_rate=47.2,
        xray_department_arrival_rate=575.0,
        elective_surgery_arrival_rate=17.91,
        elective_surgery_arrival_std_dev=3.16,
        accident_emergency_lognormal_mu=128.79,
        accident_emergency_lognormal_sigma=267.51,
        wards_lognormal_mu=177.89,
        wards_lognormal_sigma=276.54,
        emergency_surgery_lognormal_mu=140.15,
        emergency_surgery_lognormal_sigma=218.02,
        other_hospitals_lognormal_mu=212.86,
        other_hospitals_lognormal_sigma=457.67,
        xray_department_lognormal_mu=87.53,
        xray_department_lognormal_sigma=108.67,
        elective_surgery_treatment_rate=57.34,
        num_critical_care_beds=24,
        intensive_cleaning_duration=5,
        results_collection_period=12 * 30 * 24,
        warm_up_period=30 * 24,
        trace=False,
        random_number_set=0,
    ):
        self.accident_emergency_arrival_rate = accident_emergency_arrival_rate
        self.wards_arrival_rate = wards_arrival_rate
        self.emergency_surgery_arrival_rate = emergency_surgery_arrival_rate
        self.other_hospitals_arrival_rate = other_hospitals_arrival_rate
        self.xray_department_arrival_rate = xray_department_arrival_rate
        self.elective_surgery_arrival_rate = elective_surgery_arrival_rate
        self.elective_surgery_arrival_std_dev = elective_surgery_arrival_std_dev
        self.accident_emergency_lognormal_mu = accident_emergency_lognormal_mu
        self.accident_emergency_lognormal_sigma = accident_emergency_lognormal_sigma
        self.wards_lognormal_mu = wards_lognormal_mu
        self.wards_lognormal_sigma = wards_lognormal_sigma
        self.emergency_surgery_lognormal_mu = emergency_surgery_lognormal_mu
        self.emergency_surgery_lognormal_sigma = emergency_surgery_lognormal_sigma
        self.other_hospitals_lognormal_mu = other_hospitals_lognormal_mu
        self.other_hospitals_lognormal_sigma = other_hospitals_lognormal_sigma
        self.xray_department_lognormal_mu = xray_department_lognormal_mu
        self.xray_department_lognormal_sigma = xray_department_lognormal_sigma
        self.elective_surgery_treatment_rate = elective_surgery_treatment_rate
        self.num_critical_care_beds = num_critical_care_beds
        self.intensive_cleaning_duration = intensive_cleaning_duration
        self.results_collection_period = results_collection_period
        self.warm_up_period = warm_up_period
        self.total_run_length = self.warm_up_period + self.results_collection_period
        self.trace = trace
        self.random_number_set = random_number_set
        self.rng_accident_emergency = np.random.default_rng()
        self.rng_wards = np.random.default_rng()
        self.rng_emergency_surgery = np.random.default_rng()
        self.rng_other_hospitals = np.random.default_rng()
        self.rng_xray_department = np.random.default_rng()
        self.rng_elective_surgery = np.random.default_rng()
        self.rng_elective_treatment = np.random.default_rng()
        self.rng_unplanned_treatment = np.random.default_rng()
        self.setup_streams(random_number_set)

    def setup_streams(self, random_number_set):
        master_stream = np.random.default_rng(random_number_set)
        seeds = master_stream.integers(0, np.iinfo(np.int64).max, 12, dtype=np.int64)
        self.rng_accident_emergency = np.random.default_rng(seeds[0])
        self.rng_wards = np.random.default_rng(seeds[1])
        self.rng_emergency_surgery = np.random.default_rng(seeds[2])
        self.rng_other_hospitals = np.random.default_rng(seeds[3])
        self.rng_xray_department = np.random.default_rng(seeds[4])
        self.rng_elective_surgery = np.random.default_rng(seeds[5])
        self.rng_unplanned_treatment = np.random.default_rng(seeds[6])
        self.rng_elective_treatment = np.random.default_rng(seeds[7])


class CCU:
    def __init__(self, env, experiment):
        self.env = env
        self.experiment = experiment
        self.patient_id_counter = 0
        self.cancelled_operations = 0
        self.warmup_end_time = self.experiment.warm_up_period
        self.total_unplanned_waiting_time = 0
        self.total_unplanned_admissions = 0
        self.total_treatment_time = 0
        self.critical_care_beds = simpy.Resource(
            env, capacity=self.experiment.num_critical_care_beds
        )

    def lognormal_to_normal(self, mu, sigma):
        zeta = np.log(mu ** 2 / np.sqrt(sigma ** 2 + mu ** 2))
        sigma_norm = np.sqrt(np.log(sigma ** 2 / mu ** 2 + 1))
        mu_norm = zeta
        return mu_norm, sigma_norm

    def warmup_complete(self):
        yield self.env.timeout(self.warmup_end_time)
        self.patient_id_counter = 0
        if self.experiment.trace:
            print("Warm-up complete")

    def reset_kpi(self):
        """Reset all performance measures to their original values"""
        self.cancelled_operations = 0
        self.total_unplanned_waiting_time = 0
        self.total_unplanned_admissions = 0
        self.total_treatment_time = 0
        self.patient_id_counter = 0  # Reset patient_id_counter

    def accident_emergency_arrivals(self):
        while True:
            yield self.env.timeout(
                self.experiment.rng_accident_emergency.exponential(
                    self.experiment.accident_emergency_arrival_rate
                )
            )
            self.patient_id_counter += 1
            if self.experiment.trace:
                print(
                    f"Patient {self.patient_id_counter} arrived from Accident and Emergency at {self.env.now:.2f} hours"
                )
            self.env.process(
                self.unplanned_admissions_process("Accident and Emergency")
            )

    def wards_arrivals(self):
        while True:
            yield self.env.timeout(
                self.experiment.rng_wards.exponential(
                    self.experiment.wards_arrival_rate
                )
            )
            self.patient_id_counter += 1
            if self.experiment.trace:
                print(
                    f"Patient {self.patient_id_counter} arrived from the Wards at {self.env.now:.2f} hours"
                )
            self.env.process(self.unplanned_admissions_process("Wards"))

    def emergency_surgery_arrivals(self):
        while True:
            yield self.env.timeout(
                self.experiment.rng_emergency_surgery.exponential(
                    self.experiment.emergency_surgery_arrival_rate
                )
            )
            self.patient_id_counter += 1
            if self.experiment.trace:
                print(
                    f"Patient {self.patient_id_counter} arrived from Emergency Surgery at {self.env.now:.2f} hours"
                )
            self.env.process(self.unplanned_admissions_process("Emergency Surgery"))

    def other_hospitals_arrivals(self):
        while True:
            yield self.env.timeout(
                self.experiment.rng_other_hospitals.exponential(
                    self.experiment.other_hospitals_arrival_rate
                )
            )
            self.patient_id_counter += 1
            if self.experiment.trace:
                print(
                    f"Patient {self.patient_id_counter} arrived from Other Hospitals at {self.env.now:.2f} hours"
                )
            self.env.process(self.unplanned_admissions_process("Other Hospitals"))

    def xray_department_arrivals(self):
        while True:
            yield self.env.timeout(
                self.experiment.rng_xray_department.exponential(
                    self.experiment.xray_department_arrival_rate
                )
            )
            self.patient_id_counter += 1
            if self.experiment.trace:
                print(
                    f"Patient {self.patient_id_counter} arrived from the X-Ray Department at {self.env.now:.2f} hours"
                )
            self.env.process(self.unplanned_admissions_process("X-Ray Department"))

    def elective_surgery_arrivals(self):
        while True:
            yield self.env.timeout(
                self.experiment.rng_elective_surgery.normal(
                    self.experiment.elective_surgery_arrival_rate,
                    self.experiment.elective_surgery_arrival_std_dev,
                )
            )
            self.patient_id_counter += 1
            if self.experiment.trace:
                print(
                    f"Elective Patient {self.patient_id_counter} arrived at {self.env.now:.2f} hours"
                )
            self.env.process(self.elective_admissions_process())

    def unplanned_admissions_process(self, source):
        patient_id = self.patient_id_counter
        if self.experiment.trace:
            print(
                f"Patient {patient_id} from {source} requests a critical care bed at {self.env.now:.2f} hours"
            )
        waiting_time = self.env.now
        with self.critical_care_beds.request() as req:
            yield req
            waiting_time = self.env.now - waiting_time
            if self.experiment.trace:
                print(
                    f"Patient {patient_id} from {source} waited {waiting_time:.2f} hours"
                )
                print(
                    f"Patient {patient_id} from {source} admitted to a critical care bed at {self.env.now:.2f} hours"
                )
            if source == "Accident and Emergency":
                mu, sigma = self.lognormal_to_normal(
                    self.experiment.accident_emergency_lognormal_mu,
                    self.experiment.accident_emergency_lognormal_sigma,
                )
                length_of_stay = self.experiment.rng_unplanned_treatment.lognormal(
                    mu, sigma
                )
            elif source == "Wards":
                mu, sigma = self.lognormal_to_normal(
                    self.experiment.wards_lognormal_mu,
                    self.experiment.wards_lognormal_sigma,
                )
                length_of_stay = self.experiment.rng_unplanned_treatment.lognormal(
                    mu, sigma
                )
            elif source == "Emergency Surgery":
                mu, sigma = self.lognormal_to_normal(
                    self.experiment.emergency_surgery_lognormal_mu,
                    self.experiment.emergency_surgery_lognormal_sigma,
                )
                length_of_stay = self.experiment.rng_unplanned_treatment.lognormal(
                    mu, sigma
                )
            elif source == "Other Hospitals":
                mu, sigma = self.lognormal_to_normal(
                    self.experiment.other_hospitals_lognormal_mu,
                    self.experiment.other_hospitals_lognormal_sigma,
                )
                length_of_stay = self.experiment.rng_unplanned_treatment.lognormal(
                    mu, sigma
                )
            else:
                mu, sigma = self.lognormal_to_normal(
                    self.experiment.xray_department_lognormal_mu,
                    self.experiment.xray_department_lognormal_sigma,
                )
                length_of_stay = self.experiment.rng_unplanned_treatment.lognormal(
                    mu, sigma
                )
            yield self.env.timeout(length_of_stay)
            if self.env.now >= self.warmup_end_time:
                self.total_treatment_time += length_of_stay
                self.total_unplanned_waiting_time += waiting_time
                self.total_unplanned_admissions += 1
            if self.experiment.trace:
                print(
                    f"Patient {patient_id} from {source} discharged from a critical care bed at {self.env.now:.2f} hours"
                )
            yield self.env.timeout(self.experiment.intensive_cleaning_duration)
            if self.experiment.trace:
                print(
                    f"Intensive cleaning completed for Patient {patient_id} from {source} at {self.env.now:.2f} hours"
                )

    def elective_admissions_process(self):
        patient_id = self.patient_id_counter
        if self.critical_care_beds.count == self.critical_care_beds.capacity:
            if self.env.now >= self.warmup_end_time:
                if self.experiment.trace:
                    print(
                        f"Elective Patient {patient_id} operation cancelled at {self.env.now:.2f} hours due to lack of available beds"
                    )
                self.cancelled_operations += 1
            else:
                if self.experiment.trace:
                    print(
                        f"Elective Patient {patient_id} operation cancelled at {self.env.now:.2f} hours due to lack of available beds (warm-up period)"
                    )
        else:
            if self.experiment.trace:
                print(
                    f"Elective Patient {patient_id} requests a critical care bed at {self.env.now:.2f} hours"
                )
            with self.critical_care_beds.request() as req:
                yield req
                if self.experiment.trace:
                    print(
                        f"Elective Patient {patient_id} admitted to a critical care bed at {self.env.now:.2f} hours"
                    )
                length_of_stay = self.experiment.rng_elective_treatment.exponential(
                    self.experiment.elective_surgery_treatment_rate
                )
                yield self.env.timeout(length_of_stay)
                if self.env.now >= self.warmup_end_time:
                    self.total_treatment_time += length_of_stay
                if self.experiment.trace:
                    print(
                        f"Elective Patient {patient_id} discharged from a critical care bed at {self.env.now:.2f} hours"
                    )
                yield self.env.timeout(self.experiment.intensive_cleaning_duration)
                if self.experiment.trace:
                    print(
                        f"Intensive cleaning completed for Elective Patient {patient_id} at {self.env.now:.2f} hours"
                    )

    def run(self):
        accident_emergency_process = self.env.process(
            self.accident_emergency_arrivals()
        )
        wards_process = self.env.process(self.wards_arrivals())
        emergency_surgery_process = self.env.process(self.emergency_surgery_arrivals())
        other_hospitals_process = self.env.process(self.other_hospitals_arrivals())
        xray_department_process = self.env.process(self.xray_department_arrivals())
        elective_surgery_process = self.env.process(self.elective_surgery_arrivals())
        warmup_complete_process = self.env.process(self.warmup_complete())
        self.env.run(until=self.experiment.total_run_length)

        # Calculate bed utilization as a proportion
        bed_utilization = self.total_treatment_time / (
            self.experiment.num_critical_care_beds
            * self.experiment.results_collection_period
        )

        # Calculate bed occupancy
        bed_occupancy = bed_utilization * self.experiment.num_critical_care_beds

        performance_measures = {
            "Total Cancelled Elective Operations": self.cancelled_operations,
            "Mean Unplanned Admission Waiting Time (hours)": self.total_unplanned_waiting_time
            / self.total_unplanned_admissions
            if self.total_unplanned_admissions > 0
            else 0,
            "Bed Utilization": bed_utilization,
            "Bed Occupancy": bed_occupancy,
            "Patient Count": self.patient_id_counter,
        }

        results_df = pd.DataFrame.from_dict(performance_measures, orient="index").T
        return results_df


def get_experiments():
    experiments = {}
    for num_beds in range(23, 29):
        experiment_name = f"Experiment with {num_beds} beds"
        experiment = Experiment(num_critical_care_beds=num_beds)
        experiments[experiment_name] = experiment
    return experiments


def run_all_experiments(experiments, num_replications):
    experiment_summaries = {}
    for experiment_name, experiment in experiments.items():
        print(f"Running {experiment_name}")
        env = simpy.Environment()
        ccu = CCU(env, experiment)
        results = multiple_replications(experiment, num_replications)
        summary = results_summary(results)
        experiment_summaries[experiment_name] = summary
    return experiment_summaries


def summary_of_experiments(experiment_summaries):
    summary_df = pd.DataFrame()
    for experiment_name, summary in experiment_summaries.items():
        if summary_df.empty:
            summary_df = summary
            summary_df = summary_df.add_prefix(f"{experiment_name}_")
        else:
            summary = summary.add_prefix(f"{experiment_name}_")
            summary_df = pd.concat([summary_df, summary], axis=1)
    return summary_df


def multiple_replications(experiment, num_replications=5):
    all_results = []
    for i in range(num_replications):
        experiment.setup_streams(i)  # Call setup_streams method
        env = simpy.Environment()
        ccu = CCU(env, experiment)
        ccu.reset_kpi()
        results = ccu.run()
        results["Replication"] = i + 1
        all_results.append(results)
    combined_results = pd.concat(all_results, ignore_index=True)
    return combined_results


def results_summary(results_df):
    # Drop the replication column
    results_df = results_df.drop("Replication", axis=1)

    # Calculate the mean and standard deviation of each column
    summary_df = results_df.describe().loc[["mean", "std"]].T

    return summary_df


import streamlit as st
import pandas as pd

# from your_module import Experiment, multiple_replications, results_summary


def main():
    st.title("A simulation model of bed-occupancy in a critical care unit")
    st.write("This is a recreation of a model reported in a published academic study:")
    st.write(
        """
    "J D Griffiths, M Jones, M S Read & J E Williams (2010) A simulation model of bed-occupancy in a critical care unit, Journal of Simulation, 4:1, 52-59, DOI: 10.1057/jos.2009.22"
    """
    )
    st.markdown(
        "[Link to the original study](https://www.tandfonline.com/doi/full/10.1057/jos.2009.22)"
    )

    # Add sidebar
    st.sidebar.title("Experiment Parameters")

    # Number of critical care beds
    num_critical_care_beds = st.sidebar.slider(
        "Number of Critical Care Beds", min_value=20, max_value=30, value=24, step=1
    )

    # Intensive cleaning duration
    intensive_cleaning_duration = st.sidebar.number_input(
        "Intensive Cleaning Duration (hours)",
        min_value=1.0,
        max_value=10.0,
        value=5.0,
        step=0.1,
    )

    # Trace
    trace = st.sidebar.checkbox("Trace", value=False)

    # Number of replications
    num_replications = st.sidebar.number_input(
        "Number of Replications", min_value=1, max_value=10, value=5, step=1
    )

    # Create a button to trigger the simulation
    if st.button("Simulate"):
        # Display a spinner while the simulation is running
        with st.spinner("Please wait for results..."):
            # Create an instance of Experiment with the specified parameters
            experiment = Experiment(
                num_critical_care_beds=num_critical_care_beds,
                intensive_cleaning_duration=intensive_cleaning_duration,
                trace=trace,
                random_number_set=0,
            )

            # Run the simulation
            results = multiple_replications(
                experiment, num_replications=num_replications
            )

            # Call the results_summary function
            summary = results_summary(results)

            # Display the results as a DataFrame
            st.subheader("Simulation Results")
            st.dataframe(summary)


if __name__ == "__main__":
    main()
