After downloading or cloning the repo, you can run the following script on bash to install the code and the local models server (Ollama):

```shell
$ bin/install.sh
```

---

**Alternatively, install the above manually:**

#### Create and activate a virtual environment (optional)

```shell
$ python3 -m venv .myvenv
$ source .myvenv/bin/activate
```

#### Install dependencies

```shell
$ pip3 install -r requirements.txt
```

##### Ollama

Install it to run large language models locally

```shell
$ curl -fsSL https://ollama.ai/install.sh | sh
```

Or follow the installation instructions for your operating system: [Install Ollama](https://ollama.com/download)

---
#### Model Set-Up

**With the repository and Ollama installed you need to Pull/Download the basic models and create the customized versions:**

On bash, you can run the following installation script:

```shell
$ bin/set-up-models.sh
```

**Or, manually:**

Pull the basic models:

```shell
$ ollama pull llama3.1
$ ollama pull llama3.2
```

Create the customized versions:

```shell
$ ollama create llama3.2-leichte-sprache:basic -f config/custom_model/Modelfile_llama32_LS_basic
$ ollama create llama3.2-leichte-sprache:fs -f config/custom_model/Modelfile_llama32_LS_fs
$ ollama create llama3.1-leichte-sprache:basic -f config/custom_model/Modelfile_llama31_LS_basic
$ ollama create llama3.1-leichte-sprache:fs -f config/custom_model/Modelfile_llama31_LS_fs
```

Pull the fined-tuned models:

```shell
$ ollama pull kisz/llama3.2-leichte-sprache-ft:latest
$ ollama pull kisz/llama3.1-leichte-sprache-ft:latest
```
---

#### Install with Docker

Prerequisites:
- Docker and Docker Compose installed on your system
- Ollama running locally (required as the container needs to access Ollama on the host machine)
- Model Set-Up step from above

Steps:
1. Download or clone the repository
2. Navigate to the project directory
3. Build and start the container:
   ```shell
   $ docker compose up -d
   ```
4. Access the application at http://localhost:7860

Notes:
- The exports directory is mounted as a volume, so all exports will be available in the local ./exports directory
- The container needs host network access to communicate with Ollama running on your machine
