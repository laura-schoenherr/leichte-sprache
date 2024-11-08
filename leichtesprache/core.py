import os, logging
from leichtesprache.prompts import PROMPT_TEMPLATE, RULES_LS
from leichtesprache.parameters import MODEL
from leichtesprache.llm import llm_generate

logging.basicConfig(format=os.getenv("LOG_FORMAT", "%(asctime)s [%(levelname)s] %(message)s"))
logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", logging.INFO))


def simplify_text(
    text: str, llm: str, use_rules: bool, top_k: int, top_p: float, temp: float
) -> str:
    if llm is None:
        logging.warning(f"No LLM specified. Setting {MODEL} as default")
        llm = MODEL
    prompt = create_prompt(text, use_rules)
    simplified_text = llm_generate(prompt, llm, top_k, top_p, temp)
    return simplified_text


def create_prompt(text: str, use_rules: bool = False):
    if use_rules:
        return PROMPT_TEMPLATE.format(rules=RULES_LS, text=text)
    else:
        return PROMPT_TEMPLATE.format(rules="", text=text)
