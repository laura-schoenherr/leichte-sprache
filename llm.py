import logging, os
import requests, json
from urllib.parse import urljoin
from parameters import LLMBASEURL, MODEL

logging.basicConfig(format=os.getenv("LOG_FORMAT", "%(asctime)s [%(levelname)s] %(message)s"))
logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", logging.INFO))

# ============== LLM (Ollama) =================================================


def llm_generate(prompt: str, model: str = MODEL, top_k: int = 5, top_p: float = 0.9, temp: float = 0.2) -> str:
    url = urljoin(LLMBASEURL, "generate")
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temp, "top_p": top_p, "top_k": top_k},
    }

    try:
        # logger.debug(f"Sending request to LLM {model}")
        r = requests.post(url, json=data)
        response_dic = json.loads(r.text)
        return response_dic.get("response", "")

    except Exception as e:
        logger.error(f"Exception: {e}")
        logger.debug(f"url:{url}")
        logger.debug(f"Request data:{data}")
        logger.debug(f"Response:{r}")


if __name__ == "__main__":
    print("Quick test of LLM")
    print("Model:", MODEL)
    prompt = "Hi, who are you and what can you do?"
    print("Prompt:", prompt)
    response = llm_generate(prompt)
    print("Response:")
    print(response)
