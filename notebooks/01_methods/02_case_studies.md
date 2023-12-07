# Case study selection

A threat to the external validity of our study is selecting a DES study where the exact or very similar model is available within the training data.  The risk being that the LLM simply outputs the training data when prompted. As we are using Python one way to reduce this risk is to select a DES study where the model has been reported to be developed in a commercial simulation package interface such as Simul8, Arena, or Excel.  These models are contained within a bespoke format and even if available are unlikely to be translatable directly to Python. 

## Case 1: Griffith's Critical Care Unit Model

The first case study is a [2010 publication in the Journal of Simulation](https://doi.org/10.1057/jos.2009.22):

> J D Griffiths, M Jones, M S Read & J E Williams (2010) A simulation model of bed-occupancy in a critical care unit, Journal of Simulation, 4:1, 52-59, DOI: 10.1057/jos.2009.22

The model was coded in VBA and has never been published online to our knowledge.  The description of the model was published prior to any reporting guidelines for DES, but the paper contains a detailed description of the model and its parameters, although in some areas they are not reported in a manner that allows full replication of quantitative results reported in the paper (for example, empirical distribution were used, but not detailed).

The model represents a Critical (Intensive) Care Unit (CCU). It consists of six classes of entity that arrive following varying static distributions.  These arrivals are either unplanned (emergency) or planned (elective surgery) who share a total of 24 beds.  Unplanned emergency patients are prioritised for critical care beds.  Elective patient balk (a cancelled elective operations) if no beds are available. Patient classes have their own treatment time distributions (length of stay in the CCU).  After discharge a deterministic bed turnaround time is included to allow for intensive cleaning. The aim of the study was to explore capacity requirements and related scenarios and their impact on the number of cancelled operations.   