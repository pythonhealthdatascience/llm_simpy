# Primary aims

Our study is focussed on the feasibility of prompting LLMs to support the coding and recreation of simulation models in health. By recreation we mean that the design of a discrete-event simulation model is based on model documentation reported in an academic journal article. Recreations will be in the Python simulation package `simpy`. To test the feasibility of LLMs for this task, we aim to generate all code representing model logic (arrival processes, queuing, activities, sampling, balking etc). We will engineer plain English prompts for an LLM and use the generated code. We will not perform any manual coding ourselves, but will debug and test the LLM generated code. As the recreated model is code based, and potentially not user friendly for individuals not trained in Python, we will also investigate prompting an LLM to generate a simple browser based user interface.  Our primary research objectives are:

1. Given a set of engineered prompts describing a DES model, establish if it is feasible to use an LLM to generate a Python and `simpy` model that is functional and passes verification tests designed by a human user.
2. Given a set of engineered prompts of a user interface, establish if it feasible to use an LLM to generate a `streamlit` dashboard interface to a `simpy` model that can pass verification tests designed by a human user.
3. Pilot using a LLM to support the recreation of two healthcare DES models identified in the literature.
4. Pilot generating a contemporary user interface to increase accessibility.
5. Test to what degree the study can be reproduced by another modeller. 

There is much interest in LLMs and the potential for modelling support. Our long-term aim is to provide guidance (e.g. the form and language used in prompts), opportunities, challenges, risks to validity, and limitations in the use of LLMs to support recreating models to enable reproduction of results, models reuse and enhance education.