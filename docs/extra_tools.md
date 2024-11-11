### Extra Tools

In addition to the main graphical user interface, you can use several CLI tools to directly process data in .csv format.

Make sure to install the additional necessary dependencies:

```shell
$ pip3 install -r requirements_extended.txt
```

Check the scripts available in the respective tools folder. For example, you can analyze a data set by calculating the complexity metrics and generating the corresponding graphs, or you can process an entire data set with a selected model.

Get usage information by running the script with the "-h" ("--help") flag.

```shell
$ python3 -m leichtesprache.tools.process_dataset -h

Output:

usage: process_dataset.py [-h] [-m MODEL] [-r] [-c COLUMN] file_path

Process a dataset with Leichte Sprache model.

positional arguments:
  file_path             Path to the input CSV file.

options:
  -h, --help            show this help message and exit
  -m MODEL, --model MODEL
                        Model to use for processing.
  -r, --use_rules       Use rules for processing.
  -c COLUMN, --column COLUMN
                        Name of the column containing the text to process.
```

Examples:

```shell
$ python3 -m leichtesprache.tools.analysedata data/test_set.csv

$ python3 -m leichtesprache.tools.process_dataset data/test_set_analysed.csv
```
