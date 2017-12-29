# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


def arg_name(name):
    """Convert snake case argument name to a command line name.
    :param str name: The argument parameter name.
    :returns: str
    """
    return "--" + name.replace('_', '-')


def validate_client_parameters(cmd, namespace):
    """Retrieves Batch connection parameters from environment variables"""
    # simply try to retrieve the remaining variables from environment variables
    if not namespace.account_name:
        namespace.account_name = cmd.cli_ctx.config.get('batch', 'account', None)
    if not namespace.account_endpoint:
        namespace.account_endpoint = cmd.cli_ctx.config.get('batch', 'endpoint', None)

    if not namespace.account_name:
        raise ValueError("Please specify the batch account name using --account-name "
                         "or the AZURE_BATCH_ACCOUNT enviroment variable.")
    if not namespace.account_endpoint:
        raise ValueError("Please specify the batch account endpoint using --account-endpoint "
                         "or the AZURE_BATCH_ENDPOINT enviroment variable.")


def validate_mutually_exclusive(namespace, required, param1, param2):
    """Validate whether two or more mutually exclusive arguments or
    argument groups have been set correctly.
    :param bool required: Whether one of the parameters must be set.
    :param str param1: Mutually exclusive parameter name 1.
    :param str param2: Mutually exclusive parameter name 2.
    """
    value1 = getattr(namespace, param1, None)
    value2 = getattr(namespace, param2, None)

    message = None
    if not value1 and not value2 and required:
        message = "One of the following arguments are required: \n"
    elif value1 and value2:
        message = ("The follow arguments are mutually "
                   "exclusive and cannot be combined: \n")
    if message:
        missing = ','.join([arg_name(param1), arg_name(param2)])
        message += missing
        raise ValueError(message)


def validate_pool_settings(ns):
    """Custom parsing to enfore that either PaaS or IaaS instances are configured
    in the add pool request body.
    """
    if not ns.json_file and not ns.template:
        if ns.node_agent_sku_id and not ns.image:
            raise ValueError("Missing required argument: --image")
        if not ns.id:
            raise ValueError("id is required")
        if not ns.vm_size:
            raise ValueError("The --vm-size is required")

        validate_mutually_exclusive(ns, False, 'target_dedicated_nodes', 'auto_scale_formula')
        validate_mutually_exclusive(ns, True, 'os_family', 'image')
