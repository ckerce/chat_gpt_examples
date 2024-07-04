import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def bot(message, chat_history, max_new_tokens, temp, top_p, file_content):
    """
    Generate a response using the Mixtral model.

    Args:
    message (str): The current user message
    chat_history (list): List of previous messages and responses
    max_new_tokens (int): Maximum number of tokens to generate
    temp (float): Temperature for sampling
    top_p (float): Top-p sampling parameter
    file_content (str): Content of the uploaded file

    Returns:
    str: Generated response
    """
    messages = []

    for prompt, response in chat_history:
        messages.append({"role": "user", "content": prompt.strip()})
        if response is not None:
            messages.append({"role": "assistant", "content": response.strip()})

    if file_content is not None:
        messages.append({"role": "user", "content": file_content.strip()})

    messages.append({"role": "user", "content": message.strip()})

    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    if len(prompt) > 4 * args.truncate:
        prompt = prompt[-4 * args.truncate:]

    do_sample = not (temp == 0 or top_p == 0)
    temp = None if not do_sample else temp
    top_p = None if not do_sample else top_p

    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    attention_mask = torch.ones_like(input_ids)

    model = model.to("cuda" if torch.cuda.is_available() else "cpu")
    input_ids = input_ids.to(model.device)
    attention_mask = attention_mask.to(model.device)

    new_response = ""
    with torch.no_grad():
        outputs = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens,
            temperature=temp,
            top_p=top_p,
            repetition_penalty=1,
            do_sample=do_sample
        )
        for output in outputs:
            new_response += tokenizer.decode(output, skip_special_tokens=True)
            new_response = new_response.replace("", "")
            yield new_response

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--ui_port", type=int, default=6199, help="Port to serve UI on.")
    parser.add_argument("--truncate", type=int, default=6000, help="Rough number of tokens to truncate the input context to.")
    args = parser.parse_args()

    model_id = "mistralai/Mixtral-8x22B-Instruct-v0.1"
    model = AutoModelForCausalLM.from_pretrained(model_id)
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    file_upload = gr.components.File(type="text", label="Upload a text file")

    def load_file(file):
        if file is None:
            return ""
        else:
            return file.read().decode("utf-8")

    gr.ChatInterface(
        bot,
        chatbot=gr.Chatbot(
            height=800,
            label="Mixtral-8x22B-Instruct",
            layout="panel",
            show_copy_button=True,
            line_breaks=False,
            latex_delimiters=[
                {"left": "$$", "right": "$$", "display": True},
                {"left": "$", "right": "$", "display": False},
            ],
        ),
        title="Mixtral-8x22B-Instruct",
        analytics_enabled=False,
        additional_inputs=[
            gr.Slider(value=1024, label="max_new_tokens", minimum=1, maximum=2048, step=8, interactive=True),
            gr.Slider(value=0.6, label="temperature", minimum=0.0, maximum=1.5, step=0.01, interactive=True),
            gr.Slider(value=0.9, label="top_p", minimum=0.0, maximum=0.99, step=0.01, interactive=True),
            file_upload
        ],
        preprocessors=[load_file],
        concurrency_limit=16
    ).queue().launch(server_name="0.0.0.0", server_port=args.ui_port)
