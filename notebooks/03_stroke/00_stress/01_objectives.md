# 1. Objectives

## 1.1 Purpose of the model

```{admonition} Primary purpose
The simulation model provides capacity planning tools for acute stroke and rehabilitation units across a shared service that cares for Stroke, TIA, Complex Neurology and other types of neurological dependency patients. It guides users on the likelihood that a given capacity will cause admission delays.
```

## 1.2 Model Outputs

At the end of a model run the following is calculated:

* The probability of delay - p(delay) - in admission to an Acute Stroke Unit by bed numbers.
* The probability of delay - p(delay) - in admission to a Rehabilitation Unit by bed numbers.
* The reciprocal of p(delay) for both ASU and Rehab. Interpretted as 1 in every n patients is delayed.
* The occupancy distribution of the Acute Stroke Unit
* The occupancy distribution of the Rehabilitation Unit

The probability of delay is calculated as follows:

$$P(N = n)/P(N \leq n)$$

## 1.3 Experimentation aims

This is an infinite server model.  A single scenario is run, given set of arrival and length of stay parameters, to produce a distribution of outputs.


