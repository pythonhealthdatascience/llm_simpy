import streamlit as st
import simpy
import numpy as np
import pandas as pd


class Experiment:
    def __init__(
        self,
        interarrival_means=[22.72, 26.0, 37.0, 47.2, 575.0, 17.91],
        stay_distributions=[
            (128.79, 267.51),
            (177.89, 276.54),
            (140.15, 218.02),
            (212.86, 457.67),
            (87.53, 108.67),
            57.34,
        ],
        elective_treatment_mean=57.34,
        num_critical_care_beds=24,
        intensive_cleaning_duration=5,
        warm_up_period=30 * 24,
        results_collection_period=12 * 30 * 24,
        trace=False,
        random_number_set=0,
    ):
        self.interarrival_means = interarrival_means
        self.stay_distributions = stay_distributions
        self.elective_treatment_mean = elective_treatment_mean
        self.num_critical_care_beds = num_critical_care_beds
        self.intensive_cleaning_duration = intensive_cleaning_duration
        self.warm_up_period = warm_up_period
        self.results_collection_period = results_collection_period
        self.total_treatment_time = 0
        self.cancelled_elective_count = 0
        self.mean_waiting_time_unplanned = 0
        self.total_unplanned_admissions = 0
        self.bed_occupancy = 0
        self.trace = trace
        self.patient_count = 0
        self.random_number_set = random_number_set
        self.streams = []

        self.setup_streams(random_number_set)

    def reset_kpi(self):
        self.total_treatment_time = 0
        self.cancelled_elective_count = 0
        self.mean_waiting_time_unplanned = 0
        self.total_unplanned_admissions = 0
        self.bed_occupancy = 0
        self.patient_count = 0

    def setup_streams(self, random_number_set):
        self.streams = []
        rng = np.random.default_rng(random_number_set)
        seeds = rng.integers(0, np.iinfo(np.int64).max, size=12)
        for seed in seeds:
            self.streams.append(np.random.default_rng(seed))


class CCUModel:
    def __init__(self, env, experiment):
        self.env = env
        self.experiment = experiment
        self.patient_count = 0
        self.critical_care_beds = simpy.Resource(
            env, capacity=experiment.num_critical_care_beds
        )

    def patient_arrival_AE(self):
        while True:
            yield self.env.timeout(
                self.experiment.streams[0].exponential(
                    self.experiment.interarrival_means[0]
                )
            )
            self.patient_count += 1
            if self.experiment.trace:
                print(
                    f"Patient {self.patient_count} arrived from Accident and Emergency at time {self.env.now}"
                )
            self.env.process(
                self.unplanned_admission(self.experiment.stay_distributions[0])
            )

    def patient_arrival_wards(self):
        while True:
            yield self.env.timeout(
                self.experiment.streams[1].exponential(
                    self.experiment.interarrival_means[1]
                )
            )
            self.patient_count += 1
            if self.experiment.trace:
                print(
                    f"Patient {self.patient_count} arrived from the Wards at time {self.env.now}"
                )
            self.env.process(
                self.unplanned_admission(self.experiment.stay_distributions[1])
            )

    def patient_arrival_surgery(self):
        while True:
            yield self.env.timeout(
                self.experiment.streams[2].exponential(
                    self.experiment.interarrival_means[2]
                )
            )
            self.patient_count += 1
            if self.experiment.trace:
                print(
                    f"Patient {self.patient_count} arrived from Emergency surgery at time {self.env.now}"
                )
            self.env.process(
                self.unplanned_admission(self.experiment.stay_distributions[2])
            )

    def patient_arrival_other_hospitals(self):
        while True:
            yield self.env.timeout(
                self.experiment.streams[3].exponential(
                    self.experiment.interarrival_means[3]
                )
            )
            self.patient_count += 1
            if self.experiment.trace:
                print(
                    f"Patient {self.patient_count} arrived from other hospitals at time {self.env.now}"
                )
            self.env.process(
                self.unplanned_admission(self.experiment.stay_distributions[3])
            )

    def patient_arrival_X_ray(self):
        while True:
            yield self.env.timeout(
                self.experiment.streams[4].exponential(
                    self.experiment.interarrival_means[4]
                )
            )
            self.patient_count += 1
            if self.experiment.trace:
                print(
                    f"Patient {self.patient_count} arrived from the X-Ray department at time {self.env.now}"
                )
            self.env.process(
                self.unplanned_admission(self.experiment.stay_distributions[4])
            )

    def patient_arrival_elective_surgery(self):
        while True:
            yield self.env.timeout(
                self.experiment.streams[5].normal(
                    self.experiment.interarrival_means[5], 3.16
                )
            )
            self.patient_count += 1
            if self.experiment.trace:
                print(
                    f"Elective surgery patient {self.patient_count} arrived at time {self.env.now}"
                )
            if len(self.critical_care_beds.users) == self.critical_care_beds.capacity:
                if self.experiment.trace:
                    print(
                        f"Elective surgery for patient {self.patient_count} cancelled due to no available critical care beds at time {self.env.now}"
                    )
                if self.env.now > self.experiment.warm_up_period:
                    self.experiment.cancelled_elective_count += 1
            else:
                self.env.process(
                    self.elective_surgery_process(
                        self.experiment.elective_treatment_mean
                    )
                )

    def unplanned_admission(self, stay_distribution):
        arrival_time = self.env.now
        with self.critical_care_beds.request() as req:
            yield req
            wait_time = self.env.now - arrival_time
            if self.experiment.trace:
                print(
                    f"Patient {self.patient_count} admitted to critical care bed at time {self.env.now}"
                )
            treatment_time = self.experiment.streams[6].lognormal(
                np.log(stay_distribution[0])
                - 0.5 * np.log(1 + (stay_distribution[1] / stay_distribution[0]) ** 2),
                np.sqrt(np.log(1 + (stay_distribution[1] / stay_distribution[0]) ** 2)),
            )
            yield self.env.timeout(treatment_time)
            if self.experiment.trace:
                print(
                    f"Patient {self.patient_count} discharged from critical care bed at time {self.env.now}"
                )
            if self.env.now > self.experiment.warm_up_period:
                self.experiment.total_treatment_time += treatment_time
                self.experiment.mean_waiting_time_unplanned += wait_time
                self.experiment.total_unplanned_admissions += 1
            yield self.env.timeout(self.experiment.intensive_cleaning_duration)
            if self.experiment.trace:
                print(
                    f"Critical care bed is available for next patient at time {self.env.now}"
                )

    def elective_surgery_process(self, treatment_mean):
        with self.critical_care_beds.request() as req:
            yield req
            if self.experiment.trace:
                print(
                    f"Elective surgery patient {self.patient_count} admitted to critical care bed at time {self.env.now}"
                )
            treatment_time = self.experiment.streams[7].exponential(treatment_mean)
            yield self.env.timeout(treatment_time)
            if self.experiment.trace:
                print(
                    f"Elective surgery patient {self.patient_count} discharged from critical care bed at time {self.env.now}"
                )
            if self.env.now > self.experiment.warm_up_period:
                self.experiment.total_treatment_time += treatment_time
            yield self.env.timeout(self.experiment.intensive_cleaning_duration)
            if self.experiment.trace:
                print(
                    f"Critical care bed is available for next patient at time {self.env.now}"
                )

    def warmup_complete(self):
        yield self.env.timeout(self.experiment.warm_up_period)
        self.patient_count = 0
        if self.experiment.trace:
            print("Warm-up complete")

    def run(self):
        self.env.process(self.patient_arrival_AE())
        self.env.process(self.patient_arrival_wards())
        self.env.process(self.patient_arrival_surgery())
        self.env.process(self.patient_arrival_other_hospitals())
        self.env.process(self.patient_arrival_X_ray())
        self.env.process(self.patient_arrival_elective_surgery())
        self.env.process(self.warmup_complete())
        self.env.run(
            until=self.experiment.results_collection_period
            + self.experiment.warm_up_period
        )
        if self.env.now > self.experiment.warm_up_period:
            mean_waiting_time_unplanned = (
                self.experiment.mean_waiting_time_unplanned
                / self.experiment.total_unplanned_admissions
            )
            bed_utilization = self.experiment.total_treatment_time / (
                self.experiment.num_critical_care_beds
                * self.experiment.results_collection_period
            )
            bed_occupancy = bed_utilization * self.experiment.num_critical_care_beds
            performance_measures = pd.DataFrame(
                {
                    "Cancelled Elective Operations": [
                        self.experiment.cancelled_elective_count
                    ],
                    "Bed Utilization": [bed_utilization],
                    "Mean Waiting Time Unplanned": [mean_waiting_time_unplanned],
                    "Bed Occupancy": [bed_occupancy],
                    "Patient Count": [self.patient_count],
                }
            )
            return performance_measures


def multiple_replications(experiment, num_replications=5):
    all_results = []

    for i in range(num_replications):
        experiment.setup_streams(
            i
        )  # Call the setup_streams method and pass in the current replication number
        model = CCUModel(simpy.Environment(), experiment)
        experiment.reset_kpi()
        results = model.run()
        results.insert(0, "Replication", i + 1)
        all_results.append(results)

    return pd.concat(all_results, ignore_index=True)


def results_summary(results):
    # Drop the 'Replication' column
    results = results.drop(columns="Replication")

    # Calculate the mean and standard deviation of each column
    mean = results.mean()
    std = results.std()

    # Create a summary dataframe
    summary = pd.DataFrame({"Mean": mean, "Standard Deviation": std})

    return summary


def get_experiments():
    experiments = {}
    for i in range(23, 29):
        exp = Experiment(num_critical_care_beds=i)
        experiments[f"Experiment_{i}"] = exp
    return experiments


def run_all_experiments(experiments, num_replications):
    summaries = {}
    for name, exp in experiments.items():
        print(f"Running experiment: {name}")
        model = CCUModel(simpy.Environment(), exp)
        results = multiple_replications(exp, num_replications)
        summary = results_summary(results)
        summaries[name] = summary
    return summaries


def summary_of_experiments(experiment_summaries):
    return pd.concat(experiment_summaries, axis=1)


def main():
    st.title("A simulation model of bed-occupancy in a critical care unit")
    st.write(
        "This model is a recreation of the model reported in a published academic study:"
    )
    st.write(
        "J D Griffiths, M Jones, M S Read & J E Williams (2010) A simulation model of bed-occupancy in a critical care unit, Journal of Simulation, 4:1, 52-59, DOI: 10.1057/jos.2009.22"
    )
    st.write(
        "Original Study: [Journal of Simulation](https://www.tandfonline.com/doi/full/10.1057/jos.2009.22)"
    )

    with st.sidebar:
        st.subheader("Experiment Parameters")
        num_beds = st.slider("Number of Critical Care Beds", 23, 28, 23)
        cleaning_duration = st.slider("Intensive Cleaning Duration", 1, 10, 5)
        trace = st.checkbox("Enable Trace", False)
        num_replications = st.number_input("Number of Replications", 1, 10, 5)

    experiment = Experiment(
        num_critical_care_beds=num_beds,
        intensive_cleaning_duration=cleaning_duration,
        trace=trace,
    )
    simulate_button = st.button("Simulate")

    if simulate_button:
        with st.spinner("Please wait for results..."):
            results = multiple_replications(experiment, num_replications)
            summary = results_summary(results)
            st.write(summary)


if __name__ == "__main__":
    main()
