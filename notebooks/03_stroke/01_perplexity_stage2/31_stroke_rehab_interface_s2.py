import streamlit as st
import numpy as np
from stroke_rehab_model_s2 import (
    Experiment, multiple_replications, combine_pdelay_results,
    combine_occup_results, mean_results, prob_delay_plot,
    occupancy_plot, summary_table
)

def main():
    st.title("A Modelling Tool for Capacity Planning in Acute and Community Stroke Services")
    
    st.write("""
    This model is a recreation of the model reported in a published academic study.
    """)
    
    st.write("""
    **Citation:**
    
    Monks T, Worthington D, Allen M, Pitt M, Stein K, James MA. A modelling tool for capacity planning in acute and community stroke services. BMC Health Serv Res. 2016 Sep 29;16(1):530. doi: 10.1186/s12913-016-1789-4. PMID: 27688152; PMCID: PMC5043535.
    """)
    
    st.write("[Link to the original study](https://doi.org/10.1186/s12913-016-1789-4)")
    
    # Sidebar for input parameters
    st.sidebar.header("Set Patient Inter-arrival Rates")
    stroke_mean = st.sidebar.slider("Stroke patients", min_value=0.0, max_value=10.0, value=1.2, step=0.1)
    tia_mean = st.sidebar.slider("TIA patients", min_value=0.0, max_value=10.0, value=9.3, step=0.1)
    neuro_mean = st.sidebar.slider("Complex Neurological patients", min_value=0.0, max_value=10.0, value=3.6, step=0.1)
    other_mean = st.sidebar.slider("Other patients", min_value=0.0, max_value=10.0, value=3.2, step=0.1)
    
    st.sidebar.header("Model Control")
    trace = st.sidebar.checkbox("Trace patients in simulation", value=False)
    warm_up = st.sidebar.number_input("Warm-up period (days)", value=1095, step=1)
    
    num_replications = st.number_input("Number of Replications", value=100, min_value=1)
    
    if st.button("Simulate"):
        with st.spinner("Please wait for results..."):
            # Create the experiment
            experiment_params = {
                'results_collection_period': 365*5,
                'trace': trace,
                'warm_up': warm_up,
                'patient_types': {
                    'Stroke': {
                        'interarrival_time': stroke_mean,
                        'los_params': {'Rehab': (7.4, 8.6), 'ESD': (4.6, 4.8), 'Other': (7.0, 8.7)}
                    },
                    'TIA': {
                        'interarrival_time': tia_mean,
                        'los_params': (1.8, 5.0)
                    },
                    'Complex Neurological': {
                        'interarrival_time': neuro_mean,
                        'los_params': (4.0, 5.0)
                    },
                    'Other': {
                        'interarrival_time': other_mean,
                        'los_params': (3.8, 5.2)
                    }
                }
            }
            experiment = Experiment(experiment_params)
            
            # Run multiple replications
            rep_results = multiple_replications(experiment, num_replications=num_replications)
            
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
            
            # Generate plots with dynamic ranges
            x_range_asu = np.arange(len(mean_pdelay_asu))
            x_range_rehab = np.arange(len(mean_pdelay_rehab))
            
            fig_pd_asu, ax_pd_asu = prob_delay_plot(mean_pdelay_asu, x_range_asu)
            fig_pd_rehab, ax_pd_rehab = prob_delay_plot(mean_pdelay_rehab, x_range_rehab, "No. rehab beds available")
            fig_occ_asu, ax_occ_asu = occupancy_plot(mean_occup_asu, x_range_asu)
            fig_occ_rehab, ax_occ_rehab = occupancy_plot(mean_occup_rehab, x_range_rehab, "No. people in rehab")
        
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
