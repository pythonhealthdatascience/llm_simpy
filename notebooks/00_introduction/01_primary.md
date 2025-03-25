# Primary aims

Our study investigates the feasibility of using generative AI to recreate DES models in healthcare based on textual descriptions from the academic literature. We focus on generating models in the Python simulation package SimPy {cite}`simpy`, selected for its (i) compatibility with language models' code-generating capabilities, (ii) growing adoption in health service Operational Research {cite:p}`monks_harper_des_review`, and (iii) our expertise in developing SimPy models for healthcare applications {cite:p}`harper2023development,allen2020simulation`.

To assess feasibility, we engineer prompts for Perplexity.AI to generate complete Python and SimPy code that captures model logic (e.g. arrival processes, queuing, activities, sampling, and balking). Additionally, we explore generating browser-based user interfaces using Streamlit {cite}`streamlit` to enhance accessibility for non-programmers. Our research objectives are to:

- Determine if generative AI can produce functional, verifiable SimPy models from engineered prompts describing DES models
- Assess the feasibility of generating usable Streamlit web interfaces for these models
- Pilot this approach by recreating two published healthcare DES models
- Evaluate the reproducibility of our methodology when conducted by different modelers

This work contributes to the growing interest in generative AI applications for modeling {cite:p}`tolk2024hybrid,frydenlund2024modeler,giabbanelli2024broadening,Giabbanelli_GPT_Sim`. Our long-term goal is to develop guidance on prompt engineering and to document the opportunities, challenges, and limitations of using AI to recreate DES models—ultimately supporting result reproduction, model reuse, and educational applications.

## References

```{bibliography}
:style: plain
:filter: docname in docnames
```