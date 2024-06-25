import streamlit as st
import numpy as np
from stroke_rehab_model_fix import (
    Experiment, multiple_replications, combine_pdelay_results, 
    combine_occup_results, mean_results, prob_delay_plot, 
    occupancy_plot, summary_table
)

def main():
    st.title("A modelling tool for capacity planning in acute and community stroke services")

    st.write("This model is a recreation of the model reported in a published academic study.")

    st.write("Original study citation:")
    st.write("Monks T, Worthington D, Allen M, Pitt M, Stein K, James MA. A modelling tool for capacity planning in acute and community stroke services. BMC Health Serv Res. 2016 Sep 29;16(1):530. doi: 10.1186/s12913-016-1789-4. PMID: 27688152; PMCID: PMC5043535.")

    st.write("Link to the original study: [https://doi.org/10.1186/s12913-016-1789-4](https://doi.org/10.1186/s12913-016-1789-4)")

    # Sidebar for Experiment parameters
    st.sidebar.header("Simulation Parameters")

    # Inter-arrival rates
    st.sidebar.subheader("Inter-arrival Rates")
    stroke_mean = st.sidebar.number_input("Stroke patients", value=1.2, step=0.1)
    tia_mean = st.sidebar.number_input("TIA patients", value=9.3, step=0.1)
    neuro_mean = st.sidebar.number_input("Complex Neurological patients", value=3.6, step=0.1)
    other_mean = st.sidebar.number_input("Other patients", value=3.2, step=0.1)

    # Model control
    st.sidebar.subheader("Model Control")
    trace = st.sidebar.checkbox("Trace patients in simulation", value=False)
    warm_up = st.sidebar.number_input("Warm-up period", value=1095, step=1)

    # Number of replications
    num_replications = st.number_input("Number of replications", value=100, min_value=1, step=1)

    if st.button("Simulate"):
        with st.spinner("Please wait for results..."):
            # Create an instance of Experiment with user-defined parameters
            experiment = Experiment(
                stroke_mean=stroke_mean,
                tia_mean=tia_mean,
                neuro_mean=neuro_mean,
                other_mean=other_mean,
                trace=trace,
                warm_up=warm_up
            )

            # Run multiple replications
            rep_results = multiple_replications(experiment, num_replications)

            # Combine results and take the mean 
            pd_asu, pd_rehab = combine_pdelay_results(rep_results)
            rel_asu, rel_rehab = combine_occup_results(rep_results)
            mean_pd_asu, mean_pd_rehab = mean_results(pd_asu), mean_results(pd_rehab)
            mean_rel_asu, mean_rel_rehab = mean_results(rel_asu), mean_results(rel_rehab)

        # Display tables
        st.subheader("Acute Care Results")
        df_acute = summary_table(mean_pd_asu, 9, 14, "acute")
        st.table(df_acute)

        st.subheader("Rehabilitation Results")
        df_rehab = summary_table(mean_pd_rehab, 10, 16, "rehab")
        st.table(df_rehab)

        # Display plots
        st.subheader("Probability Delay Plots")
        fig_pd_asu, ax_pd_asu = prob_delay_plot(mean_pd_asu, np.arange(len(mean_pd_asu)))
        st.pyplot(fig_pd_asu)

        fig_pd_rehab, ax_pd_rehab = prob_delay_plot(mean_pd_rehab, np.arange(len(mean_pd_rehab)), "No. rehab beds available")
        st.pyplot(fig_pd_rehab)

        st.subheader("Occupancy Plots")
        fig_occ_asu, ax_occ_asu = occupancy_plot(mean_rel_asu, np.arange(len(mean_rel_asu)))
        st.pyplot(fig_occ_asu)

        fig_occ_rehab, ax_occ_rehab = occupancy_plot(mean_rel_rehab, np.arange(len(mean_rel_rehab)), "No. people in rehab")
        st.pyplot(fig_occ_rehab)

if __name__ == "__main__":
    main()
