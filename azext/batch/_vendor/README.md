# Batch CLI Vendoring

For each breaking change, to support back comparability we will need to vendor
our last SDK and SDK Extension.  This allows us to serialize/deserialize to that
versions models as well as maintain any templating policies which were in place.

To vendor the previous SDK:
* pip download -r azure-batch-extensions==x.x.x
* Delete all dependencies/files other than:
    * azext/batch/models
    * azext/batch/init.py
    * azext/batch/_file_utils.py
    * azext/batch/_pool_utils.py
    * azext/batch/_template_utils.py
    * azext/batch/errors.py
    * azure/batch/models
    * azext/batch/init.py
* Update azext\batch\models\constants.py SupportedRestApi variables to include 
details on API version