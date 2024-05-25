import sys
from llama_cpp import Llama

def run_llama2(input_text: str) -> str:
    llm = Llama(model_path="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf", verbose=False)
    output = llm(f"<user>\n{input_text}\n<assistant>\n", max_tokens=120)
    return output['choices'][0]["text"] + "..."