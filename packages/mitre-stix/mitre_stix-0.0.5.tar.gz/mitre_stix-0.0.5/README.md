# MITRE STIX

A Python package to get mitre signatures from json logs format of stix2 objects

# Current Status: Beta
The project is currently in a beta stage, which means that the code and the functionality is changing, but the current main functions are stabilising. I would love to get your feedback to make it a better project.

# Usage
-----

a Python API that returns object STIX2.0 formatted ready to be added in STIX2.0 content.

``` python
import mitre_stix.scanrules as ms
import json
output = ms.logs(json.loads(json_object))
```

## Requirements

Python 3+

## Installation

You can install it via PIP:

```
pip install mitre_stix
```

Or you can also do the following:

```
git clone https://github.trendmicro.com/henryal/mitre-stix
cd mitre-stix
pip install .
```

# Author
* Henry Alarcon Jr.