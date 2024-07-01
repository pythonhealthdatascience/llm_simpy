# Related literature



## Generative AI, Large Language Models and Chatbot AI

Generative AI, unlike traditional supervised machine learning, is designed to create new content such as text, art, music, or code. LLMs are a subset of generative AI that specialize in natural language communication between humans and computers. The Generative Pre-trained Transformer (GPT) architecture, which underpins models like ChatGPT, is a prominent example of an LLM. GPT models have grown significantly in size over time, with each iteration increasing in parameter count (and subsequent storage requirements). For example, GPT-3, has 175 billion parameters (i.e. weights within the neural network architecture) [CITATION NEEDED]. 

Since 2022, and at the time of writing, public access to LLMs has been made possible via general purpose Chatbot AI tools such as ChatGPT, Perplexity.AI, and Google's Gemini. These LLMs are trained on large amounts of curated text data (including code) from the internet, allowing them to understand and generate human-like text (and code) across a wide range of tasks. ChatGPT, developed by OpenAI, uses the GPT architecture and has been through multiple iterations (GPT-3, GPT-3.5, GPT-4). Perplexity AI uses a similar transformer-based model, potentially incorporating multiple language models including GPT variants. Google's Gemini is a multimodal model designed to work across text, images, audio, and video.  The chatbot's discussed so far are proprietary models. An open source alternative is Meta's Llama. The Llama series has evolved rapidly, with Llama 3 released in April 2024. Llama's architecture is similar to other transformer-based models but aims for efficiency, allowing smaller models to achieve competitive performance. 

The overall architecture and training of these models is complex and is not fully transparent given the commercial nature of the companies that create and operate them (at huge cost). In general terms of the models discussed employ techniques like unsupervised pre-training on large datasets, followed by fine-tuning and reinforcement learning from human feedback (RLHF). This latter reinforcement learning is achieved by humans rating responses from the model. It aims to help Chatbot AI's align their output with the human values and intentions of their prompts (the so called alignment problem). This process attempts to filter out inappropriate or offensive content while enhancing the models' ability to provide a relevant response. 

Chatbot AI tools offer user-friendly "chat" interfaces, allowing humans to interact with them using natural language. They are available in both free and paid tiers, with advanced versions (e.g. at the time of writing GPT-4 for ChatGPT and Perplexity AI, or advanced tiers for Gemini) offering enhanced capabilities.  While LLMs themselves have no memory a chatbot AI has a context window or thread allowing user to interact iteratively with an LLM within a larger context. These contexts have limits and  







Unlike Supervised Machine Learning that aims to classify or predict data, Generative  AI is a creative tool that aims to create new content e.g art, music, video, writing or code. LLMs are part of subset of Generative AI that specialises in communication between human's and computers using natural language {cite:p}`jackson_2024`. A well known type of LLM, is the Generative Pre-Trained Transformer (GPT). These are very large models (for example, GPT3.0 has 175 billion weights in its neural network) trained on text data from the internet.

At the time of writing, LLMs, such as the GPT model, are built into commercial products at both free and paid tiers. For example, Open.AI's ChatGPT, and Perplexity.AI offer a free tier for GPT 3.5 and a paid tier providing GPT 4.0 (at the time of writing). Similarly Google's Gemini has free and advanced tiers. Regardless of LLM these AI tools provide a chat interface where humans can interact using natural language.

The output from a LLM is then refined by Reinforcement Learning from Human Feedback. This approach attempts to solve the AI alignment problem - to ensure that AI tools are aligned with human values and needs.  As LLM are also trained on text from the internet it also serves a way to filter offensive and inapproraite feedback out of responses to prompts.

* How they work - within context windows.  Give example show screenshot. Discuss limits.





## Generative AI and computer simulation



{cite:p}`jackson_2024`
{cite:p}`Akhavan_2024`

## References

```{bibliography}
:filter: docname in docnames
```


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
