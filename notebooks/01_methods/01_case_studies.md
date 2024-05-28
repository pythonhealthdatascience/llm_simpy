# Case study selection

A threat to the external validity of our study is selecting a DES study where the exact or very similar model is available within the training data of the LLM.  The risk being that the LLM simply outputs the training data when prompted. The exact training data of commercial LLMs is unknown, but we assumed it would include popular code repositories such as Github and coding question and answer sites such as StackOverFlow. As we are using Python one way to reduce this risk is to select a DES study where the model has been reported to be developed in a commercial simulation package interface such as Simul8, Arena, or Excel.  The majority of such models are contained within a bespoke proprietary format and not the natural (or coding) language that a LLM is typically trained on. Our hypothesis was that even if these commercial models are available online in a location we did not know about they were unlikely to be translatable directly to Python. 

## Case 1: Critical Care Unit Model

The first case study is a [2010 publication in the Journal of Simulation](https://doi.org/10.1057/jos.2009.22):

> J D Griffiths, M Jones, M S Read & J E Williams (2010) A simulation model of bed-occupancy in a critical care unit, Journal of Simulation, 4:1, 52-59, DOI: 10.1057/jos.2009.22

The model was coded in VBA and has never been published online to our knowledge.  The description of the model was published prior to any reporting guidelines for DES, but the paper contains a detailed description of the model and its parameters, although in some areas they are not reported in a manner that allows full replication of quantitative results reported in the paper (for example, empirical distribution were used, but not detailed); although some obvious simplification were available based on descriptions in the paper (e.g. use of a statistical distribution for elective inter-arrival time instead of an unreported empirical distribution).

The model represents a Critical (Intensive) Care Unit (CCU). It consists of six classes of entity that arrive following varying static distributions.  These arrivals are either unplanned (emergency) or planned (elective surgery) who share a total of 24 beds.  Unplanned emergency patients are prioritised for critical care beds.  Elective patient balk (a cancelled elective operations) if no beds are available. Patient classes have their own treatment time distributions (length of stay in the CCU).  After discharge a deterministic bed turnaround time is included to allow for intensive cleaning. The aim of the study was to explore capacity requirements and related scenarios and their impact on the number of cancelled operations. A warm-up period and multiple replications are employed.

## Case 2: Stroke Pathway Capacity Planning Model

The second case study is a [2016 publication in BMC Health Services Research](https://bmchealthservres.biomedcentral.com/articles/10.1186/s12913-016-1789-4):

> Monks T, Worthington D, Allen M, Pitt M, Stein K, James MA. A modelling tool for capacity planning in acute and community stroke services. BMC Health Serv Res. 2016 Sep 29;16(1):530. doi: 10.1186/s12913-016-1789-4. PMID: 27688152; PMCID: PMC5043535.

The model was coded in the commercial simulation package Simul8 and has never been published online. The authors present a simple generic model to support health services plan to acute stroke ward, rehabilitation ward, and (optionally), early support discharge capacity (ESD). The model was published prior to reporting guidelines for DES, but contains a details appendix allowing for recreation of the model (and uses simple parameters and equations). 

The model allows users to specify a population of stroke, transient ischaemic attack (TIA; or mini-stroke), complex neurological, and other patient types that use acute and rehabilitation services. The patient classes have their own external inter-arrival distributions to acute and rehabilitation services, transfer probabilities between services and length of stay distributions (where first sub division occurs to model ESD versus non-ESD patients).  The model takes an infinite capacity approach to capacity planning and estimates the probability of delay. A warm-up period and multiple replications are employed.  It has a clear logic diagram and good documentation of parameters in the main article and an appendix.