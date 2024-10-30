#!/bin/bash
echo 'Pulling ollama models...' && \
echo -e '\nPulling llama 3.1 ...' && \
ollama pull llama3.1 || echo 'choose and download a model with $ ollama pull <your_model_of_choice>' && \
echo -e '\nPulling llama 3.2 ...' && \
ollama pull llama3.2 || echo 'choose and download a model with $ ollama pull <your_model_of_choice>'
