# import os
import gradio as gr
from process_dataset import llm_generate
from prompts import PROMPT_TEMPLATE
import parameters as p


pinfo = {
    "Top k": "LLM Parameter. A higher value will produce more varied text",
    "Top p": "LLM Parameter. A higher value will produce more varied text",
    "Temp": "LLM Parameter. Higher values increase the randomness of the answer",
}


def simplify_text(text: str, llm: str, top_k: int, top_p: float, temp: float) -> str:
    if llm is None:
        llm = "llama3.1"
    prompt = PROMPT_TEMPLATE.format(text=text)
    simplified_text = llm_generate(prompt, llm, top_k, top_p, temp)
    return simplified_text


ls_ui = gr.Interface(
    simplify_text,
    gr.Textbox(label="Original Text", lines=17),
    gr.Textbox(label="Leichte Sprache", lines=17),
    description="Simplify your text with a LLM!",
    examples=[[p.EXAMPLE, p.LLM_CHOICES[0], 5, 0.9, 0.3]],
    allow_flagging="manual",
    flagging_dir=p.EXPORT_PATH,
    flagging_options=[("Export", "export")],
    additional_inputs=[
        gr.Dropdown(choices=p.LLM_CHOICES, value=p.LLM_CHOICES[0], label="Model"),
        gr.Slider(1, 10, value=5, step=1, label="Top k", info=pinfo.get("Top k")),
        gr.Slider(
            0.1, 1, value=0.9, step=0.1, label="Top p", info=pinfo.get("Top p"), visible=False
        ),
        gr.Slider(0.1, 1, value=0.3, step=0.1, label="Temp", info=pinfo.get("Temp")),
    ],
    additional_inputs_accordion=gr.Accordion(label="Settings", open=False),
    submit_btn="Simplify!",
    clear_btn=None,
)


if __name__ == "__main__":

    ls_ui.launch()
