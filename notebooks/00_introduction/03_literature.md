# Related literature

## Generative AI, LLMs, and Chatbot AI

Before reviewing relevant generative AI research for simulation, we briefly define generative AI and describe popular LLMs and human interaction with them via Chatbot AI tools.  {numref}`key_concepts` summarises the key concepts.

```{list-table} Key Concepts in Generative AI
:header-rows: 1
:widths: 30 70
:name: key_concepts

* - **Topic**
  - Summary
* - **Generative AI**
  - AI models designed to create novel digital content such as text, images, music, or code.
* - **Large Language Models (LLMs)**
  - A subset of generative AI specializing in processing and generating human-like text.
* - **Transformer Architecture**
  - Neural network design using self-attention mechanisms to process and generate text.
* - **Zero-Shot Learning**
  - The ability of a model to perform tasks or make predictions on categories it hasn't explicitly seen during training.
* - **Model Scaling**
  - The process of increasing model size (number of parameters) to improve performance and capabilities.
* - **Hallucination**
  - The tendency of LLMs to generate plausible-sounding but factually incorrect or logically flawed content.
* - **Data Contamination**
  - The overlap of training data with test data, potentially leading to overestimated model performance.
* - **Temperature**
  - A parameter controlling the randomness and creativity in LLM outputs.
* - **Prompt Engineering**
  - The process of crafting effective inputs to elicit desired outputs from LLMs.
* - **Chatbot AI**
  - AI-powered conversational interfaces that use LLMs to understand and generate human-like responses in real-time interactions.
* - **Context Window**
  - The amount of previous conversation an LLM can consider when generating responses.
* - **RLHF (Reinforcement Learning from Human Feedback)**
  - A technique used to fine-tune LLMs based on human ratings of model outputs.
* - **Alignment Problem**
  - The challenge of ensuring AI outputs align with human values and intentions.


```
### Generating novel content using LLMs

Traditional Machine Learning (ML) paradigms, such as classification, train a model to learn patterns within historical labelled data in order to classify new unseen instances. For example, classifying if a brain scan indicates Parkinson's Disease or is healthy. Generative AI models are trained on unlabelled data, and rather than predict or classify their aim is to *create novel digital content* such as text, images, music, or code. For example the generation of simulation model in Python code {cite:p}`jackson_2024`. LLMs are a subset of generative AI that specialize in natural language communication between humans and computers. The Generative Pre-trained Transformer (GPT) architecture, which underpins Chatbot AI tools like ChatGPT, is perhaps the most well known example of an LLM. GPT models are built on transformer-based neural network architectures, which use self-attention mechanisms to process and generate text {cite:p}`brown2020languagemodelsfewshotlearners, vaswani2023attentionneed`. In simple terms, GPT models are sequence predictors, trained to predict the next token (e.g. a word) in a sequence based on the context of previous tokens. 

### Zero-shot learning and model scaling

A key advancement that distinguishes LLMs from traditional ML approaches is their capacity for zero-shot learning - the ability to perform tasks on previously unseen categories without explicit training {cite:p}`brown2020languagemodelsfewshotlearners`. This capability enables LLMs to adapt to novel contexts and tasks, such as generating code based on user specifications, without additional training. The evolution of zero-shot learning has been closely tied to the increasing scale of language models. When GPT-1 was introduced in 2018, it contained 117 million parameters {cite:p}`Radford2018ImprovingLU`. Subsequent iterations have seen substantial growth in model size, with GPT-3 including 175 billion parameters {cite:p}`brown2020languagemodelsfewshotlearners`. The exact specifications of GPT-4 have not been officially confirmed by OpenAI, but it is speculated to contain up to a trillion parameters {cite:p}`Giabbanelli_GPT_Sim`. 

### Challenges: Hallucination and data contamination

Evaluating the zero-shot capabilities of LLMs is challenging due to the potential contamination of test data {cite:p}`xu2024benchmarkdatacontaminationlarge`. The concept of contamination is analogous to leakage in traditional supervised machine learning {cite:p}`leakage_reference`, i.e., the training data overlaps with test data, accuracy measures are overstated, and the model is simply outputting data it has memorised in training. In the case of LLMs, it is difficult to determine if the training data overlaps with test data and careful evaluations must be designed.

A key challenge in the use of LLMs is *hallucination*. LLMs are sequence prediction models: given an input an LLM will always return an output regardless of it is right of wrong. The result is that an LLM will confidently present content that is factually incorrect or logically wrong {cite:p}`huang2023surveyhallucinationlargelanguage`. For example, an LLM might generate plausible-sounding fabricated references in an academic essay, or produce code that appears functional but contains logical errors. Both of these errors may go unnoticed by a user. The causes of hallucination are complex. In the case of coding this may include pre-training of the LLM on code that contains both obvious and subtle bugs.  Active areas of hallucination research include iterative retrieval of information {cite:p}`khot2023_iterative, yao2023_iterative`. Overall it is clear that some level of fact checking or testing must be incorporated into any process that uses content generated by an LLM.

### Randomness and prompt engineering

LLMs include an element of randomness in the generation of responses.  This randomness is typically controlled by a "temperature" parameter, where higher values increase variability in outputs, while lower values produce more deterministic results. The use of randomness allows LLMs to generate diverse and creative solutions, but it also means that given the same prompt, an LLM may produce different code outputs across multiple runs. This variability poses challenges for reproducibility in contexts such as code generation for simulation models, where consistent and replicable results are important. By default Chatbot AI tools may not offer direct user control over temperature.

Given the randomness used in generative AI, and a LLMs tendency to hallucinate, another important concept to define is the formation of prompts. This has given rise to the discipline of *prompt engineering*: the process of writing a prompt  that results in the most effective LLM performance {cite:p}`liu2021pretrainpromptpredictsystematic`. This is is very recent area of research and there is not yet a consensus on the most effective approaches although various patterns are available {cite:p}`white2023promptpatterncatalogenhance`. For example, *1-shot* or *few-shot* learning where the prompt includes 1 or more simple examples of the task to clarify the context for the LLM.

### Fine tuning LLMs and Chatbot AI

Since 2022, and at the time of writing, wide scale public access to LLMs has been made possible by general purpose Chatbot AI tools such as ChatGPT, Perplexity.AI, and Google's Gemini. The underlying LLMs are trained on large amounts of curated web data (including code from sources such as StackOverFlow and GitHub) and fine tuned for chat based human interaction. In general, the tools have been show to understand and generate human-like text (and code) across a wide range of tasks. The overall architecture and training of these models is complex and is not fully known given the commercial nature of the companies that create and operate them (at huge cost). As a general rule, however, LLMs such as GPT-3.5 or 4 are not used as is, instead the models are combined with reinforcement learning from human feedback (RLHF) where a workforce reviews and rates responses output by the model {cite:p}`casper2023RLHFlimitations`. RLHF aims to help Chatbot AI's tools align responses with the human values and the intentions of their prompts (the so called alignment problem). This process attempts to filter out inappropriate or offensive content while enhancing the models' ability to provide a relevant response. 

Human interaction with these models is via a user-friendly chat interface. The underpinning LLM in use varies by free and paid tiers (e.g. at the time of writing ChatGPT offers a free GPT-3.5 or paid GPT-4 tier). While the LLM architectures have no memory of prior prompts a chatbot AI tool has a context window allowing a user to interact *iteratively* with an LLM within a larger history/context of prompts and responses. There are size restrictions on these context windows that varies with each chatbot AI tool and underlying model.

## Generative AI and computer simulation

Recent research has begun to investigate hybrid modelling where generative AI is combined with computer simulation. Several pioneering studies have examined small scale applications and conceptual frameworks {cite:p}`jackson_2024, Akhavan_2024, Shrestha_gpt_explain_model, Giabbanelli_GPT_Sim, plooy_ai_2023`. These studies have spanned discrete-event simulation, system dynamics, conceptual modelling, and model documentation and demonstrate the broad potential of generative AI to computer simulation.

{cite:t}`jackson_2024` explored the potential of using GPT-based models to produce simulation models for inventory and process control in logistics systems. Their research focused on the concept of an "NLP shortcut," which aims to bypass traditional conceptual modelling and coding steps for discrete-event simulation. The study used the OpenAI Davinci Codex (a code based API to the GPT-3 model) to successfully generate simple Python based simulations of logistics systems (e.g. a single-product inventory-control system). The LLM outputs consists of 20-30 lines of Python code implementing simple DES model logic and code to plot model output.  Use of the Codex is incorporated into a framework that included dynamic execution of the generated code and review by a human expert.

{cite:t}`Akhavan_2024` and {cite:t}`plooy_ai_2023` investigated the application of ChatGPT in System Dynamics modelling. Both studies take the position that generative AI should not replace a modeller but rather serve as a tool to facilitate the research process, review content, and enhance idea implementation in simulation modelling. {cite:t}`Akhavan_2024` develop a simple System Dynamics model of Covid-19's impact on economic growth. Their approach first prompts ChatGPT (GPT-4) in an iterative manner to support conceptual modelling and decisions about methods. The authors **manually code** a small Python model (40 lines of code) and provide this along with prompts to ChatGPT to generation suggestions for code optimisations, additional plotting code, and improvements to model documentation.

{cite:t}`plooy_ai_2023` focussed on using ChatGPT (GPT-4) to generate Python code implementing a simple System Dynamics model of a resource bound population in equilibrium. They outline a six step approach to iterative generate a model with ChatGPTs help. Early steps focus on textual information describing equations for stocks and flows that are first manually implemented in the commercial simulation package [iSee Stella Architect](https://iseesystems.com/). The final step converts the generated equations into 32 lines of Python code with outputs verified by comparing the manually created and generated models.

{cite:t}`Giabbanelli_GPT_Sim` is a conceptual study that hypothesised about the potential of LLM application across common simulation tasks. The study focused on four key areas: structuring conceptual models, summarizing simulation outputs, improving accessibility to simulation platforms, and explaining simulation errors with guidance for resolution. For example, 

{cite:t}`Shrestha_gpt_explain_model` proposed a process to automatically explain simulation models by generative AI to create version a simplified conceptual model text from more complex causal maps. Their approach involved decomposing large conceptual models into smaller parts and then performing Natural Language Generation (NLG) using a fine-tuned GPT-3 model. 

While these studies demonstrate the potential of generative AI in simulation modelling, they also highlight the need for a balanced approach that leverages AI capabilities while maintaining the critical role of human expertise. As the field continues to evolve, further research is needed to explore the full potential of human-AI collaboration in simulation modeling and to address the challenges associated with integrating generative AI into existing simulation practices.



{cite:p}`Akhavan_2024`




## Notes


title brainstorming:
>"Using LLMs for recreating published DES models in simpy: feasibility and pilot"
>"Investigating Generative AI to recreate published healthcare discrete-event simulation in python: a feasibility and pilot study"




**From natural language to simulations: applying AI to automate simulation modelling of logistics systems**
By Jackson et al. 2024
* https://doi.org/10.1080/00207543.2023.2276811
* Focuses on GPT rather than ChatGPT
* "the language model could produce simulation models for inventory and process control"
* "enable a significant simplification of simulation model development"
* Generative AI, a specialised branch of Machine Learning (ML) that focuses on the generation of new content, including images, music, or video, by discerning patterns from existing data (Brynjolfsson, Li, and Raymond Citation2023)
* Codex (Zaremba and Brockman Citation2021), an advanced model designed to generate code in multiple programming languages based on descriptive prompts, streamlining the coding process and enhancing software development efficiency.
* we have yet to be aware of research that studies human-AI collaboration in the context of simulation modelling (MacCarthy and Ivanov Citation2022; Saenz, Revilla, and Simon Citation2020a)
* RQ1: ‘How could simulation models of logistics systems be produced automatically from verbal descriptions in natural language?’.
* RQ2: ‘How do human experts and AI-based expert systems successfully collaborate in the domain of simulation modelling of logistic systems?’.
* The idea of the *NLP shortcut*: by-pass conceptual modelling and coding [**WE ARGUE THIS ISN'T TRUE**]
* **Contributions**:
* makes two substantial contributions. First, we offer guidelines and a design of the NLP-based framework on how to build simulation models of logistics systems automatically, given the verbal description. Second, and more generally, our work offers a technological underpinning of human-AI collaboration for the development of simulation models
* Most code generation tasks are focussed on classic software engineering problems not simulation.
*  Python is selected as the programming language for this endeavor, given that GPT-3 Codex demonstrates the highest level of proficiency in Python 3 (Chen et al. Citation2021)
*  Experiments:
*  Model has 20-30 lines of python code.  Note that the language model makes decisions about plotting.
*  CLAIM: "As highlighted in our study, one of the pivotal advantages of automating the development of simulation models is the potential reduction in time, resources, and human error. Traditional simulation approaches, such as agent-based simulations, often require intricate design, extensive calibration, and rigorous validation. These processes, while essential, are time-consuming and prone to human errors, especially when modelling complex supply chain systems."

**Generative AI and simulation modeling: how should you (not) use large language models like ChatGPT**
By Akhavan et al. 2024
* Akhavan_2024
* https://doi.org/10.1002/sdr.1773
* System Dynamics model
* Throughout this article, we show and emphasize that generative AI should not replace thinking; instead, it is a useful tool to facilitate the research process, a practical way to review the content generated by researchers, and an enhancement of idea implementation in simulation modeling.
* Thus, one contribution of this article is providing well-crafted examples of prompts that illustrate effective communication with generative AI. These examples serve as practical guides for users to understand how to formulate prompts that elicit meaningful responses from tools like ChatGPT.
* Used it more as an assistant to get feedback, refine ideas, and present options.  Some code was provided to assist with python plots and interfaces to models.

**AI USEFULNESS IN SYSTEMS MODELLING AND SIMULATION: GPT-4 APPLICATION**
plooy_ai_2023
*  However, the application of GPT-4 in system dynamics modelling is not without its difficulties. As a language model,  GPT-4  is  inherently  limited  by  the  quality  and  breadth  of  the  data  it  has  been  trained  on.  Consequently, its performance in specialised domains, such as system dynamics, may be contingent on the availability of relevant training data
*  Despite  the  promise  of  AI-driven  system  dynamics  modelling,  the  role  of  human  expertise  remains  indispensable
*  To harness AI's potential in system dynamics fully, it is essential to strike a balance between leveraging AI’s capabilities and maintaining the critical role of human expertise
*  GPT-4.0 was able to design a simple SD model; although it could not identify an error in the simulation.
*  results demonstrated the importance for a human in the process.

**CHANCES AND CHALLENGES OF CHATGPT AND SIMILAR MODELS
FOR EDUCATION IN M&S**
* consider how generative AI will affect simulation education and how teaching in hr
the field should adapt to accomodate and exploit it.  One such option is student and AI teams where the teams works over a number of iterations to build a computer simulation model. A hypothetical example in NetLogo is presented.

**GPT-BASED MODELS MEET SIMULATION: HOW TO EFFICIENTLY USE LARGE-SCALE PRE-TRAINED LANGUAGE MODELS ACROSS SIMULATION TASKS** by Giabbanelli 2023
Giabbanelli_GPT_Sim

* https://dl.acm.org/doi/10.5555/3643142.3643385
* We focus on four modeling and simulation tasks,
* structure of a conceptual model to promote the engagement of participants in the modeling process
* summarizing simulation outputs
* broaden accessibility to simulation platforms by conveying the insights of simulation visualizations via tex
* explaining simulation errors and providing guidance to resolve them.


**Automatically Explaining a Model: Using Deep Neural Networks to Generate Text From Causal Maps** 
by Shrestha et al 2022
Shrestha_gpt_explain_model

* We proposed a process to transform a large conceptual model (in the form of a causal map) into sentences, by decomposing it into smaller parts and then performing Natural Language Generation (NLG) via a fine-tuned GPT-3 (Figure 2). Automatic metrics that tolerate variations in language show encouraging performances on two case studies (Table 1)



## References

```{bibliography}
:style: plain
:filter: docname in docnames
```
