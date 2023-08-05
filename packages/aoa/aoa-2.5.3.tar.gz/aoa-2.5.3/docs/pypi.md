# Teradata AnalyticOps Client

Python client for Teradata AnalyticOps Accelerator. It is composed of both an client API implementation to access the AOA Core APIs and a command line interface (cli) tool which can be used for many common tasks. 

## Installation

You can install via pip. The minimum python version required is 3.5+

```
pip install aoa
```

## CLI

The cli can be used to perform a number of interactions and guides the user to perform those actions. 

```
> aoa -h
usage: aoa [-h] [--debug] {add,run,init,clone,configure} ...

AOA CLI

optional arguments:
  -h, --help            show this help message and exit
  --debug               Enable debug logging

actions:
  valid actions

  {add,run,init,clone,configure}
    add                 Add model
    run                 Train and Evaluate model
    init                Initialize model directory with basic structure
    clone               Clone Project Repository
    configure           Configure AOA client
```

To see the details or help for a specific action, just select the action and add -h

```
> aoa run -h
usage: aoa run [-h] [-id MODEL_ID] [-m MODE] [-d DATA]

optional arguments:
  -h, --help            show this help message and exit
  -id MODEL_ID, --model_id MODEL_ID
                        Which model_id to use (prompted to select if not provided)
  -m MODE, --mode MODE  The model (train or evaluate) (prompted to select if not provided)
  -d DATA, --data DATA  Json file containing data configuration (prompted to select if not provided)
```

## Client API

We have a client implementation for all of the entities exposed in the AOA API. We provide the RESTful and RPC client usage for this. We'll show an example of the Dataset API here but the same applies for all.

To configure the client you simply run the cli which will guide you through the process and create the configuration file `.aoa/config.yaml` in your home directly. Note you can override this configuration at runtime via environment variables or constructor arguments. 

```
aoa configure
```

Create the client. Note there are a number of options to specify the client information and credentials. The example here is where you specify everything in the constructor. 

```
from aoa import AoaClient
from aoa import DatasetApi


client = AoaClient()
client.set_project_id("23e1df4b-b630-47a1-ab80-7ad5385fcd8d")

dataset_api = DatasetApi(aoa_client=client)

```

Now, find all datasets or a specific dataset
```
import pprint

datasets = dataset_api.find_all()
pprint.pprint(datasets)

dataset = dataset_api.find_by_id("11e1df4b-b630-47a1-ab80-7ad5385fcd8c")
pprint.pprint(dataset)
```

Add a dataset
```
dataset_definition = {
    "name": "my dataset",
    "description": "adding sample dataset",
    "metadata": {
        "url": "http://nrvis.com/data/mldata/pima-indians-diabetes.csv",
        "test_split": "0.2"
    }
}

dataset = dataset_api.save(dataset=dataset_definition)
pprint.pprint(dataset)
```
