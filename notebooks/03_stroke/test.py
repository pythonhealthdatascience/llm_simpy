from stroke_rehab_model import *
import pytest
import numpy as np

@pytest.mark.parametrize('values, rel_expected, cum_expected', [
                            ([1, 1, 1, 1, 2, 2, 2, 3, 3, 4], 
                             [0.4, 0.3, 0.2, 0.1], [0.4, 0.7, 0.9, 1.0])
])
def test_result_processing_1(values, rel_expected, cum_expected):
    '''
    Test the `calculate_occupancy_frequencies` function works
    as expected.

    Expected result: relative frequencies and cumulative freqs
    are the same as expected values.

    Params:
    ------
    values: list
        list of values to test

    rel_expected: list
        list of floats - expected relative freqs

    cum_expected: list
        list of floats - expected cumulative freqs

    Returns:
    -------
    bool: does the model pass the test.
    '''
    rel, cum, unique = calculate_occupancy_frequencies(values)
    # use all close to allow for minor floating point differences.
    assert (set(rel) == set(rel_expected)) and np.allclose(np.array(cum_expected), cum)