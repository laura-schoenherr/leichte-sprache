import os
from urllib.parse import urljoin

# Set language for textstat
LANGUAGE = "de"

LLMBASEURL = urljoin(os.getenv("OLLAMA_HOST", "http://localhost:11434"), "api/")

# First on the list is used as default
LLM_CHOICES = [
    "llama3.1-leichte-sprache:fs",
    "llama3.1-leichte-sprache-ft:latest",
    "kisz/llama3.1-leichte-sprache-ft:latest",
    "llama3.1-leichte-sprache:basic",
    "llama3.2-leichte-sprache:fs",
    "llama3.2-leichte-sprache-ft:latest",
    "kisz/llama3.2-leichte-sprache-ft:latest",
    "llama3.2-leichte-sprache:basic",
]
MODEL = os.getenv("OLLAMA_MODEL", LLM_CHOICES[0])

# Set for processing tools as well as for GUI default value
USE_RULES = False

# LLM default parameters
TOP_K = 2
TOP_P = 0.9
TEMP = 0.2

# Other Features
EXPORT_PATH = "exports"

EXAMPLE = "Kindertagesstätten\nIn unserer Gemeinde gibt es drei Kinderkrippen und vier Kindergärten. Die Trägerschaft liegt bei der Gemeinde sowie bei der evangelischen Kirche. Es kann zwischen verschiedenen Öffnungszeiten gewählt werden, von den Regelöffnungszeiten bis hin zur Ganztagesbetreuung."
