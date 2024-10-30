#!/bin/bash
echo 'Pulling ollama models...' && \
echo -e '\nPulling llama 3.1 ...' && \
ollama pull llama3.1 || echo 'choose and download a model with $ ollama pull <your_model_of_choice>' && \
echo -e '\nPulling llama 3.2 ...' && \
ollama pull llama3.2 || echo 'choose and download a model with $ ollama pull <your_model_of_choice>' && \
echo -e '\nSetting up local models ...' && \
echo -e 'llama3.2-leichte-sprache:basic...' && \
ollama create llama3.2-leichte-sprache:basic -f config/custom_model/Modelfile_llama32_LS_basic && \
echo -e 'llama3.2-leichte-sprache:fs...' && \
ollama create llama3.2-leichte-sprache:fs -f config/custom_model/Modelfile_llama32_LS_fs && \
echo -e 'llama3.1-leichte-sprache:basic...' && \
ollama create llama3.1-leichte-sprache:basic -f config/custom_model/Modelfile_llama31_LS_basic && \
echo -e 'llama3.1-leichte-sprache:fs...' && \
ollama create llama3.1-leichte-sprache:fs -f config/custom_model/Modelfile_llama31_LS_fs && \
echo -e 'Models succesfully set'
