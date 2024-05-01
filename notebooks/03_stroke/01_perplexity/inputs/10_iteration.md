code a function `calculate_prob_delay` that accepts to array-like parameters: relative and cumulative frequencies. The function should convert the parameters to numpy arrays and calculate and return relative / cumulative frequency (prob_delay)

The prob_delay, unique values, a string called "x_label" (default value = "No. acute beds available"), and figure size (default = (12, 5)) should be passed to a function called `prob_delay_plot` that creates a matplotlib step chart of the prob_delay.  the x axis values are taken from the unique values parameter. The x axis ticks should run from 0 to 30 and all values should be displayed.  the x axis is label is set to the value of "x_label" Return the matplotlib figure and axis objects. 

Display the new functions and the script to

1. create an experiment,
2. run the model
3. calculate the relative and cumulative frequencies
4. creates the step chart.

