def dict_to_cfn_params(dict_params) -> list:
    """Description:
        Converts a `dict` to CloudFormation parameters

    Args:
        dict_params: Dictionary that needs to be converted to CloudFormation parameters

    Example:
        Example usage:

            params = {
                'AccountId': '123456789012',
                'ExternalId': '098765432109',
                }

            cfn_params = dict_to_cfn_params(params)
            pprint(cfn_params)
            [{'ParameterKey': 'AccountId', 'ParameterValue': '123456789012'},
            {'ParameterKey': 'ExternalId', 'ParameterValue': '098765432109'}]

    Returns:
        List of CloudFormation parameters
    """
    cfn_params = []

    for key, value in dict_params.items():
        entry = {
            'ParameterKey': key,
            'ParameterValue': value,
        }

        cfn_params.append(entry)

    return cfn_params


# def outputs_to_dict(cfn_id, cfn_resource=None):
#     """
#
#     Args:
#         cfn_id: CloudFormation ID from which to extract the outputs
#         cfn_resource: (Optional) `cloudformation` resource - used for assumed roles
#
#     Example:
#         Example usage:
#
#             cfn_outputs = cfn.outputs_to_dict(cfn_id)
#             pprint(cfn_outputs)
#             {'Hostname': 'TestHost',
#             'Version': '1.18'}
#
#     Returns:
#         CloudFormation outputs as a dictionary
#     """
#     self.logger.entry('debug', 'Converting CloudFormation outputs to dict...')
#     cfn_resource = cfn_resource if cfn_resource else self.default_cfn_resource
#
#     cfn_details = cfn_resource.describe_stacks(StackName=cfn_id)
#     cfn_outputs = cfn_details['Stacks'][0]['Outputs']
#     self.logger.entry('debug', f'CloudFormation outputs:\n{pformat(cfn_outputs)}')
#
#     output = {}
#     for entry in cfn_outputs:
#         key = entry['OutputKey']
#         value = entry['OutputValue']
#         output[key] = value
#
#     self.logger.entry('debug', f'Dict outputs:\n{pformat(output)}')
#     return output


