import streamlit as st
import numpy as np
from stroke_rehab_model_s2 import (
    Experiment, multiple_replications, combine_pdelay_results,
    combine_occup_results, mean_results, prob_delay_plot,
    occupancy_plot, summary_table
)

def main():
    st.title("Stroke Rehabilitation Model Simulation")

    if st.button("Simulate"):
        with st.spinner("Please wait for results..."):
            # Create the experiment
            experiment = Experiment({
                'results_collection_period': 365*5,  # Run for 5 years
                'trace': False,  # Set to True if you want to see detailed logs
            })

            # Run multiple replications
            rep_results = multiple_replications(experiment, num_replications=100)

            # Combine results
            asu_pdelay, rehab_pdelay = combine_pdelay_results(rep_results)
            asu_occup, rehab_occup = combine_occup_results(rep_results)

            # Calculate mean results
            mean_pdelay_asu = mean_results(asu_pdelay)
            mean_pdelay_rehab = mean_results(rehab_pdelay)
            mean_occup_asu = mean_results(asu_occup)
            mean_occup_rehab = mean_results(rehab_occup)

            # Create summary tables
            asu_summary = summary_table(mean_pdelay_asu, min_beds=9, max_beds=14, bed_type="ASU")
            rehab_summary = summary_table(mean_pdelay_rehab, min_beds=10, max_beds=16, bed_type="Rehab")

            # Generate plots
            fig_pd_asu, ax_pd_asu = prob_delay_plot(mean_pdelay_asu, np.arange(0, 30))
            fig_pd_rehab, ax_pd_rehab = prob_delay_plot(mean_pdelay_rehab, np.arange(0, 30), "No. rehab beds available")
            fig_occ_asu, ax_occ_asu = occupancy_plot(mean_occup_asu, np.arange(0, 30))
            fig_occ_rehab, ax_occ_rehab = occupancy_plot(mean_occup_rehab, np.arange(0, 30), "No. people in rehab")

        # Display results
        st.subheader("Acute Stroke Unit Results")
        st.table(asu_summary)

        st.subheader("Rehabilitation Unit Results")
        st.table(rehab_summary)

        st.subheader("Probability Delay Plots")
        st.pyplot(fig_pd_asu)
        st.pyplot(fig_pd_rehab)

        st.subheader("Occupancy Plots")
        st.pyplot(fig_occ_asu)
        st.pyplot(fig_occ_rehab)

if __name__ == "__main__":
    main()
