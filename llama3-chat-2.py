import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import List, Tuple

class LlamaInterface:
    #def __init__(self, model_name="meta-llama/Llama-2-7b-chat-hf"):
    def __init__(self, model_name="meta-llama/Llama-3.1-8B-Instruct"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)
        if torch.cuda.is_available():
            self.model = self.model.cuda()
        self.context = ""
        self.system_prompt = ""
        
    def generate(self, prompt: str) -> str:
        try:
            full_prompt = f"{self.system_prompt}\n{self.context}\n{prompt}".strip()
            inputs = self.tokenizer(full_prompt, return_tensors="pt")
            
            if torch.cuda.is_available():
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            outputs = self.model.generate(
                **inputs,
                max_length=2048,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            return f"Error: {str(e)}"

    def set_context(self, context: str):
        self.context = context

    def set_system_prompt(self, prompt: str):
        self.system_prompt = prompt

def create_interface():
    llm = LlamaInterface()
    
    with gr.Blocks() as demo:
        with gr.Tabs():
            with gr.Tab("Chat"):
                chatbot = gr.Chatbot(height=600)
                with gr.Row():
                    msg = gr.Textbox(
                        label="Message",
                        placeholder="Enter your message here... (Press Enter to send)",
                        lines=2
                    )
                    submit = gr.Button("Send")

            with gr.Tab("Context Management"):
                system_prompt = gr.TextArea(
                    label="System Prompt",
                    placeholder="Enter system prompt...",
                    lines=3
                )
                context_input = gr.TextArea(
                    label="Context",
                    placeholder="Paste reference text here...",
                    lines=5
                )
                with gr.Row():
                    load_context = gr.Button("Load Context & System Prompt")
                    clear_context = gr.Button("Clear All")
                status = gr.Textbox(label="Status", interactive=False)

        def handle_context(sys_prompt: str, context: str) -> str:
            llm.set_system_prompt(sys_prompt)
            llm.set_context(context)
            return "Context and system prompt loaded"
            
        def clear_context_fn() -> str:
            llm.set_system_prompt("")
            llm.set_context("")
            return "Cleared"

        def respond(message: str, history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str, str]]]:
            response = llm.generate(message)
            history.append((message, response))
            return "", history

        load_context.click(
            fn=handle_context,
            inputs=[system_prompt, context_input],
            outputs=[status]
        )
        clear_context.click(
            fn=clear_context_fn,
            outputs=[status]
        )
        submit.click(
            fn=respond,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot]
        )
        msg.submit(
            fn=respond,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot]
        )

    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch(server_name="0.0.0.0", server_port=7861)
