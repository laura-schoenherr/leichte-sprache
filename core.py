from prompts import PROMPT_TEMPLATE, RULES_LS
from llm import llm_generate


def simplify_text(text: str, llm: str, top_k: int, top_p: float, temp: float) -> str:
    if llm is None:
        llm = "llama3.1"
    prompt = create_prompt(text)
    simplified_text = llm_generate(prompt, llm, top_k, top_p, temp)
    return simplified_text


def create_prompt(text: str, use_rules: bool = False):
    if use_rules:
        return PROMPT_TEMPLATE.format(rules=RULES_LS, text=text)
    else:
        return PROMPT_TEMPLATE.format(rules="", text=text)
