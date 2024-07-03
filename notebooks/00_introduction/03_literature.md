# Related literature

Before reviewing relevant generative AI research for simulation, we briefly define generative AI and describe popular LLMs and human interaction with them via Chatbot AI tools.  {numref}`key_concepts` summarises the key concepts.

## Generative AI, LLMs, and Chatbot AI

Traditional machine learning paradigms, such as classification, train a model to learn patterns within historical labelled data in order to classify new unseen instances. For example, classifying if an brain scan indicates Parkinson's Disease or is healthy. Generative AI models are trained on unlabelled data, and rather than predict or classify their aim is to *create novel digital content* such as text, images, music, or code. In our case this would include the generation of simulation model in Python code. LLMs are a subset of generative AI that specialize in natural language communication between humans and computers. The Generative Pre-trained Transformer (GPT) architecture, which underpin Chatbot AI tools like ChatGPT, is perhaps the most well known example of an LLM. GPT models are built on transformer-based neural network architectures, which use self-attention mechanisms to process and generate text {cite:p}`brown2020languagemodelsfewshotlearners`. In simple terms, GPT models are sequence predictors, trained predict the next token (e.g. a word) in a sequence based on the context of previous tokens. They are a recent innovation: GPT-1 was introduced in 2018 and consisted of 117 million parameters {cite:p}`Radford2018ImprovingLU`. The models have grown significantly in size and capability over time, with each iteration increasing in parameter count (and subsequent cost to train). For example, GPT-3, has 175 billion parameters i.e. weights within the neural network architecture {cite:p}`brown2020languagemodelsfewshotlearners`.

Since 2022, and at the time of writing, wide scale public access to LLMs has been made possible by general purpose Chatbot AI tools such as ChatGPT, Perplexity.AI, and Google's Gemini. The underlying LLMs are trained on large amounts of curated web data (including code from sources such as StackOverFlow and GitHub) and fine tuned for chat based human interaction. In general, the tools have been show to understand and generate human-like text (and code) across a wide range of tasks. The overall architecture and training of these models is complex and is not fully known given the commercial nature of the companies that create and operate them (at huge cost). As a general rule, however, LLMs such as GPT-3.5 or 4 are not used as is, instead the models are combined with reinforcement learning from human feedback (RLHF) where a workforce reviews and rates responses output by the model. RLHF aims to help Chatbot AI's tools align responses with the human values and the intentions of their prompts (the so called alignment problem). This process attempts to filter out inappropriate or offensive content while enhancing the models' ability to provide a relevant response. 

Human interaction with these models is via a user-friendly chat interface. The underpinning LLM is dependent on if the user has access to a free or paid tier (e.g. at the time of writing ChatGPT offers a free GPT-3.5 or paid GPT-4 tier). While the LLM architectures have no memory of prior prompts a chatbot AI tool has a context window  allowing a user to interact *iteratively* with an LLM within a larger history/context of prompts and responses. There are size restrictions on these context windows that varies with each chatbot AI tool and underlying model.

To mimic creativity, LLMs include an element of randomness in the generation of responses.  This randomness is typically controlled by a "temperature" parameter, where higher values increase variability in outputs, while lower values produce more deterministic results. The use of randomness allows LLMs to generate diverse and creative solutions, but it also means that given the same prompt, an LLM may produce different code outputs across multiple runs. This variability poses challenges for reproducibility in contexts such as code generation for simulation models, where consistent and replicable results are important. By default Chatbot AI tools may not offer direct user control over temperature.

Given the creativity and randomness used in generative AI, the final important concept to define is the formation of prompts.  This has given rise to the discipline of *prompt engineering*: the process of writing a prompt  that results in the most effective LLM performance {cite:p}`liu2021pretrainpromptpredictsystematic`. This is is very recent area of research and there is not yet a consensus on the most effective approaches although various patterns are available {cite:p}`white2023promptpatterncatalogenhance`. For example, *1-shot* or *few-shot* learning where the prompt includes 1 or more simple examples of the task to clarify the context for the LLM.

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
* - **Chatbot AI**
  - AI-powered conversational interfaces that use LLMs to understand and generate human-like responses in real-time interactions.
* - **Context Window**
  - The amount of previous conversation an LLM can consider when generating responses.
* - **Alignment Problem**
  - The challenge of ensuring AI outputs align with human values and intentions.
* - **Temperature**
  - A parameter controlling the randomness and creativity in LLM outputs.
* - **Prompt Engineering**
  - The process of crafting effective inputs to elicit desired outputs from LLMs.

```


## unused text

ChatGPT, developed by OpenAI, uses the GPT architecture and has been through multiple iterations (GPT-3, GPT-3.5, GPT-4). Perplexity.AI uses a similar transformer-based model, potentially incorporating multiple language models including GPT variants. Google's Gemini is a multimodal model designed to work across text, images, audio, and video.  The chatbot's discussed so far are proprietary models. An open source alternative is Meta's Llama. The Llama series has evolved rapidly, with Llama 3 released in April 2024. Llama's architecture is similar to other transformer-based models but aims for efficiency, allowing smaller models to achieve competitive performance. 




Unlike Supervised Machine Learning that aims to classify or predict data, Generative  AI is a creative tool that aims to create new content e.g art, music, video, writing or code. LLMs are part of subset of Generative AI that specialises in communication between human's and computers using natural language {cite:p}`jackson_2024`. A well known type of LLM, is the Generative Pre-Trained Transformer (GPT). These are very large models (for example, GPT3.0 has 175 billion weights in its neural network) trained on text data from the internet.

At the time of writing, LLMs, such as the GPT model, are built into commercial products at both free and paid tiers. For example, Open.AI's ChatGPT, and Perplexity.AI offer a free tier for GPT 3.5 and a paid tier providing GPT 4.0 (at the time of writing). Similarly Google's Gemini has free and advanced tiers. Regardless of LLM these AI tools provide a chat interface where humans can interact using natural language.

The output from a LLM is then refined by Reinforcement Learning from Human Feedback. This approach attempts to solve the AI alignment problem - to ensure that AI tools are aligned with human values and needs.  As LLM are also trained on text from the internet it also serves a way to filter offensive and inapproraite feedback out of responses to prompts.

* How they work - within context windows.  Give example show screenshot. Discuss limits.







## Generative AI and computer simulation



{cite:p}`jackson_2024`
{cite:p}`Akhavan_2024`




## Notes


title brainstorming:
>"Using LLMs for recreating published DES models in simpy: feasibility and pilot"
>"Investigating Generative AI to recreate published healthcare discrete-event simulation in python: a feasibility and pilot study"

* Need to distinguish between GPT and ChatGPT/Perplexity etc.
* List of ChatGPT (3.5 versus 4.0); perplexity-AI Google Gemini (formerly Bard)
* Need in introduce prompt engineering (why, how code generation is tough etc.)
* Describe how a ChatGPT like interface works?
* Our prompts also included code ... e.g. for 1-shot prompt engineering.


**From natural language to simulations: applying AI to automate simulation modelling of logistics systems**
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
* https://doi.org/10.1002/sdr.1773
* System Dynamics model
* Throughout this article, we show and emphasize that generative AI should not replace thinking; instead, it is a useful tool to facilitate the research process, a practical way to review the content generated by researchers, and an enhancement of idea implementation in simulation modeling.
* Thus, one contribution of this article is providing well-crafted examples of prompts that illustrate effective communication with generative AI. These examples serve as practical guides for users to understand how to formulate prompts that elicit meaningful responses from tools like ChatGPT.
* Used it more as an assistant to get feedback, refine ideas, and present options.  Some code was provided to assist with python plots and interfaces to models.

**AI USEFULNESS IN SYSTEMS MODELLING AND SIMULATION: GPT-4 APPLICATION**
*  However, the application of GPT-4 in system dynamics modelling is not without its difficulties. As a language model,  GPT-4  is  inherently  limited  by  the  quality  and  breadth  of  the  data  it  has  been  trained  on.  Consequently, its performance in specialised domains, such as system dynamics, may be contingent on the availability of relevant training data
*  Despite  the  promise  of  AI-driven  system  dynamics  modelling,  the  role  of  human  expertise  remains  indispensable
*  To harness AI's potential in system dynamics fully, it is essential to strike a balance between leveraging AI’s capabilities and maintaining the critical role of human expertise
*  GPT-4.0 was able to design a simple SD model; although it could not identify an error in the simulation.
*  results demonstrated the importance for a human in the process.

**CHANCES AND CHALLENGES OF CHATGPT AND SIMILAR MODELS
FOR EDUCATION IN M&S**
* consider how generative AI will affect simulation education and how teaching in hr
the field should adapt to accomodate and exploit it.  One such option is student and AI teams where the teams works over a number of iterations to build a computer simulation model. A hypothetical example in NetLogo is presented.

## References

```{bibliography}
:filter: docname in docnames
```
