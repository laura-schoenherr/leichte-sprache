# Customized Model

Based on an existing model and using a model file with the desired settings, you can customize a model for your purposes.

## Create a customized model

Command:
```
$ ollama create choose-a-model-name -f <pathTo/Modelfile>'
$ ollama run choose-a-model-name
```

Basic Modelfile Example:
```
FROM llama3.1
PARAMETER temperature 0.2
SYSTEM """
Du bist ein hilfreicher Assistent, der Texte in Leichte Sprache, Sprachniveau A2, umschreibt. Sei immer wahrheitsgemäß und objektiv. Schreibe nur das, was du sicher aus dem Text des Benutzers weisst. Arbeite die Texte immer vollständig durch und kürze nicht. Mache keine Annahmen. Schreibe einfach und klar und immer in deutscher Sprache.
"""
```

It is also possible to customize the model by using the MESSAGE instruction/parameter to add a few-shot approach, as follows:

Example:
```
MESSAGE user Is Toronto in Canada?
MESSAGE assistant yes
MESSAGE user Is Sacramento in Canada?
MESSAGE assistant no
MESSAGE user Is Ontario in Canada?
MESSAGE assistant yes
```


Fewshot approach format for the current use case:

```
MESSAGE user """Bitte schreibe den folgenden schwer verständlichen Text vollständig in Leichte Sprache auf dem Niveau A2 um.
Füge keine Erklärungen oder Kommentare hinzu, sondern nur die vereinfachte Version des folgendes Textes.
Text:

"""
MESSAGE assistant """

"""
```

Check further parameters: [Modelfile Parameters](https://github.com/ollama/ollama/blob/main/docs/modelfile.md#parameter)

### Local Examples

```
ollama create llama3.1-ls:8b-sysm -f custom_model/Modelfile_LS_base

ollama create llama3.1-ls:8b-fs -f custom_model/Modelfile_LS_Fewshot
```


