import sys
from llama_cpp import Llama
llm = Llama(model_path="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf", verbose=False)
output = llm("<user>\n" + sys.argv[1] + "\n<assistant>\n", max_tokens=120)
print(output['choices'][0]["text"] + "...")