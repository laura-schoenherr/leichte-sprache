# import os
import gradio as gr
from core import simplify_text
from llm import list_local_models
import parameters as p


pinfo = {
    "Top k": "LLM Parameter. A higher value will produce more varied text",
    "Top p": "LLM Parameter. A higher value will produce more varied text",
    "Temp": "LLM Parameter. Higher values increase the randomness of the answer",
}

LLM_CHOICES = list(set(p.LLM_CHOICES) & set(list_local_models()))
DEAFULT_MODEL = LLM_CHOICES[0]

ls_ui = gr.Interface(
    simplify_text,
    gr.Textbox(label="Original Text", lines=17),
    gr.Textbox(label="Leichte Sprache", lines=17),
    description="Simplify your text with a LLM!",
    examples=[[p.EXAMPLE, DEAFULT_MODEL, False, 5, 0.9, 0.3]],
    allow_flagging="manual",
    flagging_dir=p.EXPORT_PATH,
    flagging_options=[("Export", "export")],
    additional_inputs=[
        gr.Dropdown(choices=LLM_CHOICES, value=DEAFULT_MODEL, label="Model"),
        gr.Checkbox(value=False, label="Use Rules", info="Use rules for simplification"),
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
