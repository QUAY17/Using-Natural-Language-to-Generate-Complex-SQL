# Llama 2

[The Paper](https://arxiv.org/abs/2307.09288)

Llama 2 is a collection of pretrained and fine-tuned large language models (LLMs) ranging in scale from 7 billion to 70 billion parameters.

## 4.1 Using Llama 2 for Development

- To run the Llama 2 models locally, a NVDA GPU / CUDA environment is required, helpful links to get started:
  - [Llama 2 download](https://github.com/facebookresearch/llama#readme)

- To interact with Llama 2 chat locally using Python, without the above requirement, use the [llama-cpp-python package](https://pypi.org/project/llama-cpp-python/).

pip install llama-cpp-python

Then download the model in GGML format from Hugging Face, [llama-2-7b](https://huggingface.co/TheBloke/Llama-2-7B-GGML/blob/main/llama-2-7b.ggmlv3.q4_1.bin) \*\*

Update: GGML is unsupported as of Aug 2023 , new format is GGUF. Link to [Llama-2-7B-GGUF](https://huggingface.co/TheBloke/Llama-2-7B-GGUF)

\*\*I followed [this article](https://swharden.com/blog/2023-07-29-ai-chat-locally-with-python/) for easy install, but it loads the older GGML models.

### 4.11 Models

- Llama 2, an updated version of Llama 1, trained on a new mix of publicly available data.
  - An increased pretraining corpus size by 40%, double the context length of the model, and adopted grouped-query attention (Ainslie et al, 2023).
  - Released variants of Llama 2 are 7B, 13B, and 70B.

- Llama 2-Chat, a fine tuned version of Llama 2 that is optimized for dialogue use cases and out performed close sourced models on several metrics.
  - Released variants of Llama 2-Chat are 7B, 13B, and 70B.
  - Achieved alignment with human preferences using techniques such as Reinforcement Learning with Human Feedback (RLHF).
  - RLHF is the foundation of closed product LLMs and greatly improves their usability and safety.
  - The fine-tuning step can be resource-intensive.
    - Requires significant compute and human annotation costs.
    - The process is often not transparent or easily reproducible/ hinders progress within the AI community.

![Shape1](RackMultipart20231004-1-hgjn9c_html_1715f7da2cb69919.gif)

- By downloading a model, you are agreeing to the [license](https://l.facebook.com/l.php?u=https%3A%2F%2Fai.meta.com%2Fllama%2Flicense&h=AT2M25Lzvy9uNdInezcflTlDSAKGcUzF6528cRyPZbHJWtXQ-3HUMOH2qDuyOUGDyH9XfL3WHf3hXKaOLJ5HIUPB5rCVk3BQv-E0wKQK3wC8EDaXRvvYzof35njttXJLA1si9-iVK0bWEyh3b2rVN-2IJu4Bz57F), [acceptable use policy](https://l.facebook.com/l.php?u=https%3A%2F%2Fai.meta.com%2Fllama%2Fuse-policy&h=AT0L8VicJ7Nkbn1xybAKT168Eog9aNOZcaUcZFsCM9q9I9er_FiK-ZQ7MeRtlnqaa8hMKMU_ACCBkX08HdQS0xkJVaUFKiQ6oFRIq_OFN4e7fIOOjEYjbNYyjTokPHqzwfw5FLrVidj5JN4PMTuXxtsIL5MBnEMl) and Meta's [privacy policy](https://www.facebook.com/privacy/policy/).
- All liability is assumed by the user and a license only needs to be obtained if using commercially with over 700M users.

### 3.12 Fine Tuning

An important paradigm of natural language processing consists of large-scale pre-training on general domain data and adaptation to particular tasks or domains. As we pre-train larger models, full fine-tuning, which retrains all model parameters, becomes less feasible.

Documentation from Meta "receipes" on fine tuning:

- [Llama 2](https://github.com/facebookresearch/llama-recipes/blob/main/docs/LLM_finetuning.md) finetuning recipe using Low Rank Adaption of LLMs [LoRA](https://arxiv.org/pdf/2106.09685.pdf)

#### Fine tuning the base model:

1. Locally, needs a NVDA GPU- Using [Autotrain Advanced](https://github.com/huggingface/autotrain-advanced) from Hugging face
2. Google Collab notebook- also using [Autotrain Advanced](https://github.com/huggingface/autotrain-advanced) from Hugging face
  1. Hugging face profile and token for access
  2. Data set: csv
  3. format:
    1. alpaca 4 gpt: instruction (string), input(string) , output(string), text(string)- puts everything together
    2. human token ### then response from the assistant
    3. trainer: sft super wise training format
  4. dataset will need to be sized manageably in order to not time out

#### Data Format:

![Shape2](RackMultipart20231004-1-hgjn9c_html_a651aa0ed4197e23.gif)

| **.csv** | **Input** | **Output** | **Text** |
| --- | --- | --- | --- |
| 0 | prompt | response | ###Human:\ngenerate this\n\n###Assistant:\nThis is what I generated... |
| 1 | prompt | response | ###Human:\ngenerate this\n\n###Assistant:\nThis is what I generated... |

#### The Code

**Fine Tuning in Google Collab**

! autotrain llm --train --project\_name 'llama2-assistant'

--model /Llama-2-7B-sharded

--data\_path /folder

--text\_column text

--use\_pft (Parameter Eficifient Fine Tuning Method)

--use\_int4

--learning\_rate 2e-4

--train\_batch\_size 2

--num\_train\_epochs 3

--trainer sft (Superwise Fine Tuning)

--model\_max\_length 2048

#### Inference

Download the model and start using it with the Transformers package.
