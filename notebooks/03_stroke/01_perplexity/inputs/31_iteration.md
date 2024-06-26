The functions `combine_pdelay_results` and `combine_occup_results` contain a bug when the number of unique values is greater than 30.  Fix the bug so that the functions can handle more or less than 30 unique values, but still ensure that all arrays are of the same length.

display all code in the modified functions.

```python
def combine_pdelay_results(rep_results):
    result_list_asu = []
    result_list_rehab = []
    
    for rep_result in rep_results:
        prob_delay_asu = rep_result['prob_delay_asu']
        unique_vals_asu = rep_result['unique_vals_asu']
        
        min_occupancy_asu = min(unique_vals_asu)
        
        new_array_asu = np.zeros(30)
        for i, val in zip(unique_vals_asu, prob_delay_asu):
            new_array_asu[i] = val
        
        new_array_asu[:min_occupancy_asu] = 1.0
        
        result_list_asu.append(new_array_asu)
        
        prob_delay_rehab = rep_result['prob_delay_rehab']
        unique_vals_rehab = rep_result['unique_vals_rehab']
        
        min_occupancy_rehab = min(unique_vals_rehab)
        
        new_array_rehab = np.zeros(30)
        for i, val in zip(unique_vals_rehab, prob_delay_rehab):
            new_array_rehab[i] = val
        
        new_array_rehab[:min_occupancy_rehab] = 1.0
        
        result_list_rehab.append(new_array_rehab)
    
    return np.array(result_list_asu), np.array(result_list_rehab)



def combine_occup_results(rep_results):
    result_list_asu = []
    result_list_rehab = []
    
    for rep_result in rep_results:
        relative_freq_asu = rep_result['relative_freq_asu']
        unique_vals_asu = rep_result['unique_vals_asu']
        
        new_array_asu = np.zeros(30)
        for i, val in zip(unique_vals_asu, relative_freq_asu):
            new_array_asu[i] = val
        
        result_list_asu.append(new_array_asu)
        
        relative_freq_rehab = rep_result['relative_freq_rehab']
        unique_vals_rehab = rep_result['unique_vals_rehab']
        
        new_array_rehab = np.zeros(30)
        for i, val in zip(unique_vals_rehab, relative_freq_rehab):
            new_array_rehab[i] = val
        
        result_list_rehab.append(new_array_rehab)
    
    return np.array(result_list_asu), np.array(result_list_rehab)

```