# load the large language model file
from llama_cpp import Llama
LLM = Llama(model_path="./llama-2-7b.ggmlv3.q4_1.bin", n_ctx=2048)

# create a text prompt
prompt = "how does linear algebra realte to graph neural networks"
# generate a response (takes several seconds)
output = LLM(prompt, max_tokens=0)

# display the response
print(output)