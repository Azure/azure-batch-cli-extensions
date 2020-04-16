## Python

These settings apply only when `--python` is specified on the command line.
Please also specify `--python-sdks-folder=<path to the root directory of your azure-sdk-for-python clone>`.
Use `--python-mode=update` if you already have a setup.py and just want to update the code itself.

``` yaml $(python)
python:
  azure-arm: true
  license-header: MICROSOFT_MIT_NO_VERSION
  payload-flattening-threshold: 2
  package-name: azure-batch
  clear-output-folder: true
```

### Python multi-api

Generate all API versions currently shipped for this package

```yaml $(python) && $(multiapi)
batch:
  - tag: package-2018-03-01-only
  - tag: package-2018-08-01-only
  - tag: package-2018-12-01-only
  - tag: package-2019-06-01-only
  - tag: package-2019-08-01-only
```

### Tag: package-2018-03-01-only and python

These settings apply only when `--tag=package-2018-03-01-only --python` is specified on the command line.
Please also specify `--python-sdks-folder=<path to the root directory of your azure-sdk-for-python clone>`.

``` yaml $(tag) == 'package-2018-03-01-only' && $(python)
python:
  namespace: azure.batch.v2018_03_01
  output-folder: $(python-sdks-folder)/sdk/batch/azure-batch/v2018_03_01
  input-file: $(rest-api-folder)/2018-03-01.6.1/BatchService.json
```

### Tag: package-2018-08-01-only and python

These settings apply only when `--tag=package-2018-08-01-only --python` is specified on the command line.
Please also specify `--python-sdks-folder=<path to the root directory of your azure-sdk-for-python clone>`.

``` yaml $(tag) == 'package-2018-08-01-only' && $(python)
python:
  namespace: azure.batch.v2018_08_01
  output-folder: $(python-sdks-folder)/sdk/batch/azure-batch/v2018_08_01
  input-file: $(rest-api-folder)/2018-08-01.7.0/BatchService.json
```

### Tag: package-2018-12-01-only and python

These settings apply only when `--tag=package-2018-12-01-only --python` is specified on the command line.
Please also specify `--python-sdks-folder=<path to the root directory of your azure-sdk-for-python clone>`.

``` yaml $(tag) == 'package-2018-12-01-only' && $(python)
python:
  namespace: azure.batch.v2018_12_01
  output-folder: $(python-sdks-folder)/sdk/batch/azure-batch/v2018_12_01
  input-file: $(rest-api-folder)/2018-12-01.8.0/BatchService.json
```

### Tag: package-2019-06-01-only and python

These settings apply only when `--tag=package-2019-06-01-only --python` is specified on the command line.
Please also specify `--python-sdks-folder=<path to the root directory of your azure-sdk-for-python clone>`.

``` yaml $(tag) == 'package-2019-06-01-only' && $(python)
python:
  namespace: azure.batch.v2019_06_01
  output-folder: $(python-sdks-folder)/sdk/batch/azure-batch/v2019_06_01
  input-file: $(rest-api-folder)/2019-06-01.9.0/BatchService.json
```

### Tag: package-2019-08-01-only and python

These settings apply only when `--tag=package-2019-08-01-only --python` is specified on the command line.
Please also specify `--python-sdks-folder=<path to the root directory of your azure-sdk-for-python clone>`.

``` yaml $(tag) == 'package-2019-08-01-only' && $(python)
python:
  namespace: azure.batch.v2019_08_01
  output-folder: $(python-sdks-folder)/sdk/batch/azure-batch/v2019_08_01
  input-file: $(rest-api-folder)/2019-08-01.10.0/BatchService.json
```
