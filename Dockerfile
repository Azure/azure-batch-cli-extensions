FROM azuresdk/azure-cli-python:2.0.10
RUN pip install azure-cli-batch-extensions==1.0.0
CMD bash