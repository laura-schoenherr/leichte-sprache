import os
from urllib.parse import urljoin

# Set language for textstat
LANGUAGE = "de"

LLMBASEURL = urljoin(os.getenv("OLLAMA_HOST", "http://localhost:11434"), "api/")

# First on the list is used as default
LLM_CHOICES = ["llama3.1-ls:8b-sysm", "llama3.1-ls:8b-fs-v02", "llama3.1:latest"]
MODEL = os.getenv("OLLAMA_MODEL", LLM_CHOICES[0])

USE_RULES = False

# Other Features
EXPORT_PATH = "exports"

EXAMPLE = "Kindertagesstätten\nIn unserer Gemeinde gibt es drei Kinderkrippen und vier Kindergärten. Die Trägerschaft liegt bei der Gemeinde sowie bei der evangelischen Kirche. Es kann zwischen verschiedenen Öffnungszeiten gewählt werden, von den Regelöffnungszeiten bis hin zur Ganztagesbetreuung."
