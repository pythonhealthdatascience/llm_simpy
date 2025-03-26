import streamlit as st
import numpy as np
from stroke_rehab_model import (
    Experiment, multiple_replications, combine_pdelay_results, 
    combine_occup_results, mean_results, prob_delay_plot, 
    occupancy_plot, summary_table
)

def main():
    st.title("Stroke Rehabilitation Model Simulation")

    if st.button("Simulate"):
        with st.spinner("Please wait for results..."):
            # Create an instance of Experiment (default params, default warm-up and rcp)
            experiment = Experiment()

            # Run multiple replications
            rep_results = multiple_replications(experiment, 100)

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
        fig_pd_asu, ax_pd_asu = prob_delay_plot(mean_pd_asu, np.arange(0, 30))
        st.pyplot(fig_pd_asu)

        fig_pd_rehab, ax_pd_rehab = prob_delay_plot(mean_pd_rehab, np.arange(0, 30), "No. rehab beds available")
        st.pyplot(fig_pd_rehab)

        st.subheader("Occupancy Plots")
        fig_occ_asu, ax_occ_asu = occupancy_plot(mean_rel_asu, np.arange(0, 30))
        st.pyplot(fig_occ_asu)

        fig_occ_rehab, ax_occ_rehab = occupancy_plot(mean_rel_rehab, np.arange(0, 30), "No. people in rehab")
        st.pyplot(fig_occ_rehab)

if __name__ == "__main__":
    main()
