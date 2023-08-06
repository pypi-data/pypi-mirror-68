# Isogeo Scan - Metadata Processor

[![Build Status](https://dev.azure.com/isogeo/Scan/_apis/build/status/isogeo.scan-metadata-processor?branchName=master)](https://dev.azure.com/isogeo/Scan/_build/latest?definitionId=54&branchName=master)

![PyPI](https://img.shields.io/pypi/v/isogeo-scan-metadata-processor)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/isogeo-scan-metadata-processor?style=flat-square)

[![Documentation: sphinx](https://img.shields.io/badge/doc-sphinx--auto--generated-blue)](http://help.isogeo.com/scan/isogeo-scan-metadata-processor/index.html)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Middleware used to process metadata issued by Isogeo Scan.

Available as:

- Python package
- Windows executable

## Requirements

- Python 3.7

## Development

### Quickstart

```powershell
# create virtual env
py -3.7 -m venv .venv
# activate it
.\.venv\Scripts\activate
# update basic tooling
python -m pip install -U pip setuptools wheel
# install requirements
python -m pip install -U -r ./requirements.txt
# install package for development
python -m pip install --editable .
```

### Try it

1. Rename the `.env.example` into `.env` and fill the settings
2. Launch the [CLI](https://fr.wikipedia.org/wiki/Interface_en_ligne_de_commande)

For example, get the help:

```powershell
scan-metadata-processor --help
```

Check:

```powershell
# for all default formats
scan-metadata-processor --label "CheckProcessConfig" --settings .\.env check
```

Process metadata:

```powershell
scan-metadata-processor --label "ProcessInputMetadata" --settings .\.env process
```

There is also a clean task to automatically remove outdated logs and output files:

```powershell
scan-metadata-processor --label "CleanLogs" --settings .\.env clean
```

----

## Usage of the executable

Just replace `scan-metadata-processor` by the executable filename:

```powershell
.\Isogeo_ScanMetadataProcessor.exe --label "ProcessInputMetadata" --settings .\.env process
```

----

## Deployment

Every tagged commit pushed to `master` triggers a deployment to:

- Azure Storage : Isogeo/isogeoscan/app/isogeo-scan-metadata-processor/
- Python Package Index
- [Github Releases](/releases)
