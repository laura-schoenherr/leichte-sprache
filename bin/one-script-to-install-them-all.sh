#!/bin/bash
echo 'Installing/Updating ollama...' && \
curl -fsSL https://ollama.ai/install.sh | sh && \
read -p "Install the Leichte Sprache tool in a virtual environment? (Type 'y' to agree, or leave blank to skip. Press Enter):" VENV_CHOICE
if [[ $VENV_CHOICE == [yY] ]]; then
	echo 'Creating virtual environment...' && \
	python3 -m venv .myvenv && \
	echo 'Activating virtual environment...' && \
	source .myvenv/bin/activate
fi
echo 'Installing requirements...' && \
pip3 install -r requirements.txt
read -p "Install the additional tools? ('y' to agree, or press Enter to skip):" TOOLS_CHOICE
if [[ $TOOLS_CHOICE == [yY] ]]; then
	echo 'Installing additional tools...' && \
	pip3 install -r requirements_extended.txt
fi
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
echo -e 'Custom Models succesfully set' && \
echo -e '\nPulling Fine-tuned models...' && \
ollama pull kisz/llama3.2-leichte-sprache-ft:latest || echo 'Something went wrong while pulling llama3.2-leichte-sprache-ft' && \
ollama pull kisz/llama3.1-leichte-sprache-ft:latest || echo 'Something went wrong while pulling llama3.1-leichte-sprache-ft' && \
echo -e '\nRenaming...' && \
ollama cp kisz/llama3.2-leichte-sprache-ft:latest llama3.2-leichte-sprache-ft:latest && \
ollama rm kisz/llama3.2-leichte-sprache-ft:latest
ollama cp kisz/llama3.1-leichte-sprache-ft:latest llama3.1-leichte-sprache-ft:latest && \
ollama rm kisz/llama3.1-leichte-sprache-ft:latest
echo -e 'Fine-tuned Models succesfully set'