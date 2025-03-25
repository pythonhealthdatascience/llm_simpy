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

Traditional Machine Learning (ML) paradigms, such as classification, train a model to learn patterns within historical labelled data in order to classify new unseen instances. For example, classifying if a brain scan indicates Parkinson's Disease or is healthy. Generative AI models are trained on unlabelled data, and rather than predict or classify their aim is to *create novel digital content* such as text, images, music, or code. For example the generation of a simple simulation model in Python code {cite:p}`jackson_2024`. LLMs are a subset of generative AI that specialize in natural language communication between humans and computers. The Generative Pre-trained Transformer (GPT) architecture, that underpins AI Chatbot tools like ChatGPT, is perhaps the most well known example of an LLM. GPT models are built on transformer-based neural network architectures, which use self-attention mechanisms to process and generate text {cite:p}`brown2020languagemodelsfewshotlearners, vaswani2023attentionneed`. In simple terms, GPT models are sequence predictors, trained to predict the next token (e.g. a word) in a sequence based on the context of previous tokens. 

### Zero-shot learning and model scaling

A key advancement that distinguishes LLMs from traditional ML approaches is their capacity for zero-shot learning - the ability to perform tasks on previously unseen categories without explicit training {cite:p}`brown2020languagemodelsfewshotlearners`. This capability enables LLMs to adapt to novel contexts and tasks, such as generating code based on user specifications, without additional training. The evolution of zero-shot learning has been closely tied to the increasing scale of language models. When GPT-1 was introduced in 2018, it contained 117 million parameters {cite:p}`Radford2018ImprovingLU`. Subsequent iterations have seen substantial growth in model size, with GPT-3 including 175 billion parameters {cite:p}`brown2020languagemodelsfewshotlearners`. The exact specifications of GPT-4 have not been officially confirmed by OpenAI, but it is speculated to contain up to a trillion parameters {cite:p}`Giabbanelli_GPT_Sim`. 

### Challenges and limitations: data contamination and hallucination

Evaluating the zero-shot capabilities of LLMs is challenging due to the potential contamination of test data {cite:p}`xu2024benchmarkdatacontaminationlarge`. The concept of contamination is analogous to leakage in traditional supervised machine learning {cite:p}`leakage_reference`, i.e., the training data overlaps with test data, accuracy measures are overstated, and the model is simply outputting data it has memorised in training. In the case of LLMs, it is difficult to determine if the training data overlaps with test data and careful evaluations must be designed.

A key challenge in the use of LLMs is mitigating the risk of *hallucination*. LLMs are sequence prediction models that prioritize generating the most probable next word in a sequence, even if it is inaccurate. Simply put, given an input, a model will always produce an output, whether it is correct or not. As a result, an LLM may "hallucinate": confidently present content that is factually incorrect, logically flawed, or at odds with the provided training data {cite:p}`huang2023surveyhallucinationlargelanguage, Ziwei_hallucinations_ref2`.

For example, an LLM might generate plausible-sounding but fabricated references in an academic essay or produce code that appears functional but contains logical errors. These errors may go unnoticed by users, and have consequences that vary from minor (e.g. wasted time from debugging nonsensical code) to severe (e.g. incorrect decisions based on the results of a flawed simulation model). The causes of hallucination are complex and varied. In coding, for instance, it might stem from pre-training the LLM on code that contains both obvious and subtle bugs.

Hallucination is a major limitation of generative AI and hence is an active area of research {cite:p}`Ziwei_hallucinations_ref2`. Promising approaches include variations on the theme of iterative retrieval of information {cite:p}`khot2023_iterative, yao2023_iterative`, that can involve refining outputs through multiple iterations each providing more context or fact checking. Another approach is to estimate model uncertainty statistics that can highlight LLM knowledge deficiencies {cite:p}`Farquhar2024`. For the immediate future it seems likely that hallucination will continue to be a major challenge for safe and productive use of generative AI with some arguing it cannot be fully eliminated {cite:p}`xu2024_hallucination_inevitable`. As such it is crucial to incorporate some form of fact-checking or testing mechanisms in any work that relies on content generated by an LLM.

### Randomness and prompt engineering

LLMs include an element of randomness in the generation of responses.  This randomness is typically controlled by a "temperature" parameter, where higher values increase variability in outputs (and increase hallucinations), while lower values produce more deterministic results. The use of randomness allows LLMs to generate diverse and creative solutions, but it also means that given the same prompt, an LLM may produce different code outputs across multiple runs. This variability poses challenges for reproducibility in contexts such as code generation for simulation models, where consistent and replicable results are important. By default Chatbot AI tools may not offer direct user control over temperature.

Given the randomness used in generative AI, and a LLMs tendency to hallucinate, another important concept to define is the formation of prompts. This has given rise to the discipline of *prompt engineering*: the process of writing a prompt that results in the most effective LLM performance {cite:p}`liu2021pretrainpromptpredictsystematic`. This is is very recent area of research and there is not yet a consensus on the most effective approaches although various patterns are available {cite:p}`white2023promptpatterncatalogenhance`. For example, *1-shot* or *few-shot* learning where the prompt includes 1 or more simple examples of the task to clarify the context for the LLM.

### AI Chatbots and alignment

Since 2022, and at the time of writing, wide scale public access to LLMs has been made possible by general purpose Chatbot AI tools such as ChatGPT, Perplexity.AI, and Google's Gemini. The underlying LLMs are trained on large amounts of curated web data (including code from sources such as StackOverFlow and GitHub) and fine tuned for chat based human interaction. In general, the tools have been show to understand and generate human-like text (and code) across a wide range of tasks. The overall architecture and training of these models is complex and is not fully known given the commercial nature of the companies that create and operate them (at huge cost). As a general rule, however, LLMs such as GPT-3.5 or 4 are not used as is, instead the models are combined with reinforcement learning from human feedback (RLHF) where a workforce reviews and rates responses output by the model {cite:p}`casper2023RLHFlimitations`. RLHF aims to help Chatbot AI's tools align responses with the human values and the intentions of their prompts (the so called alignment problem). This process attempts to filter out inappropriate or offensive content while enhancing the models' ability to provide a relevant response. 

Human interaction with these models is via a user-friendly chat interface. The underpinning LLM in use varies by free and paid tiers (e.g. at the time of writing ChatGPT offers a free GPT-3.5 or paid GPT-4 tier). While the LLM architectures have no memory of prior prompts a chatbot AI tool has a context window allowing a user to interact *iteratively* with an LLM within a larger history/context of prompts and responses. There are size restrictions on these context windows that varies with each chatbot AI tool and underlying model.

## Generative AI and computer simulation

## Automated code generation

Recent research has begun to investigate hybrid modelling where generative AI is combined with computer simulation. Several pioneering studies have examined small scale applications and conceptual frameworks {cite:p}`jackson_2024, Akhavan_2024, Shrestha_gpt_explain_model, Giabbanelli_GPT_Sim, plooy_ai_2023`. These studies have spanned discrete-event simulation, system dynamics, conceptual modelling, and model documentation and demonstrate the broad potential of generative AI to computer simulation.

{cite:t}`jackson_2024` explored the potential of using GPT-based models to produce simulation models for inventory and process control in logistics systems. Their research focused on the concept of an "NLP shortcut," which aims to bypass traditional conceptual modelling and coding steps for discrete-event simulation. The study used the OpenAI Davinci Codex (a code based API to the GPT-3 model) to successfully generate simple Python based simulations of logistics systems (e.g. a single-product inventory-control system). The LLM outputs consists of 20-30 lines of Python code implementing simple DES model logic and code to plot model output.  Use of the Codex is incorporated into a framework that included dynamic execution of the generated code and review by a human expert.

{cite:t}`Akhavan_2024` and {cite:t}`plooy_ai_2023` investigated the application of ChatGPT in System Dynamics modelling. Both studies take the position that generative AI should not replace a modeller but rather serve as a tool to facilitate the research process, review content, and enhance idea implementation in simulation modelling. {cite:t}`Akhavan_2024` develop a simple System Dynamics model of Covid-19's impact on economic growth. Their approach first prompts ChatGPT (GPT-4) in an iterative manner to support conceptual modelling and decisions about methods. The authors **manually code** a small Python model (40 lines of code) and provide this along with prompts to ChatGPT to generation suggestions for code optimisations, additional plotting code, and improvements to model documentation.

{cite:t}`plooy_ai_2023` focussed on using ChatGPT (GPT-4) to generate Python code implementing a simple System Dynamics model of a resource bound population in equilibrium. They outline a six step approach to iterative generate a model with ChatGPTs help. Early steps focus on textual information describing equations for stocks and flows that are first manually implemented in the commercial simulation package [iSee Stella Architect](https://iseesystems.com/). The final step converts the generated equations into 32 lines of Python code with outputs verified by comparing the manually created and generated models.

### Conceputal modelling

{cite:t}`Giabbanelli_GPT_Sim` is a conceptual study that hypothesised about the potential of LLM application across common simulation tasks. The study focused on four key areas: structuring conceptual models, summarizing simulation outputs, improving accessibility to simulation platforms, and explaining simulation errors with guidance for resolution. For example, the potential to use the emerging capability of LLMs to convert images to text to provide automated explanations of charts of simulation output could benefit both non-experts and people with visual impaired.

{cite:t}`Shrestha_gpt_explain_model` proposed a process to automatically explain simulation models by generative AI to create version a simplified conceptual model text from more complex causal maps. Their approach involved decomposing large conceptual models into smaller parts and then performing Natural Language Generation (NLG) using a fine-tuned GPT-3 model. 

### Conclusions

Despite the limited body of research, these initial investigations suggest a potential role for generative AI in the future of computer simulation. 

* Role of modeller still vital in planning and verification:
* Iterative role
* Not explored issues with hallucination
* Not explore more complex models.

Further research is needed to explore the integration of generative AI across a wider range of simulation paradigms and to develop robust frameworks for human-AI collaboration in the simulation development process.


## References

```{bibliography}
:style: plain
:filter: docname in docnames
```
