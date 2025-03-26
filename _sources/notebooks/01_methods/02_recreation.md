# Model recreation

The study followed an iterative approach to model recreation. In each iteration new details from the design are added to the model or the model is modified in order to remove prior simplifications included to get a working model.

When designing the study our hypothesis was that the current generation of LLMs cannot replace the training and expertise of a simulation modeller, but given the right prompts that LLMs can aid the efficiency in which a model described in an article is reconstructed. {numref}`methods_fig` illustrates the process for a traditional *manual* approach to recreating a simulation model from the literature without the aid of an LLM versus incorporating an LLM.  Central to {numref}`methods_fig` is the training that a simulation modeller holds in simulation theory, coding, sofware and best practices. This training is used regardless of the approach to model reconstruction - manual or via a LLM. In both approaches to model reconstruction note the role of model testing also known as model verification.  Model testing is defined as ensuring that the computer program of the computerized model and its implementation are correct {cite:p}`Sargent_verification`.  Testing a model is implemented correctly is a critical step in a simulation study regardless of whether the code was written by a human or a LLM.  The primary difference between the two approaches in {numref}`methods_fig` is *prompt engineering*: the process of converting a description of a simulation model into a natural language input for a LLM that produces the desired simulation model code.  

```{figure} ../../images/iterative_model_recreation.png
---
name: methods_fig
---
The iterative process for recreating a model from a textual description: with and without a LLM.
```
## References

```{bibliography}
:filter: docname in docnames


