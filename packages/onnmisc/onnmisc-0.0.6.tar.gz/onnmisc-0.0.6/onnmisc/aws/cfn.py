import boto3
from botocore.handlers import json_decode_template_body
import json


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


def get_template(stack_name) -> dict:
    """Description:
        Extracts CloudFormation templates from existing stack

    Args:
        stack_name: Name of the CloudFormation stack

    Example:
        Example usage:

            from pprint import pprint
            template = get_template('demo_template')
            pprint(template)
            {'Resources': {'Instance': {'Properties': {'ImageId': 'ami-0d1deba769f118333',
                                           'InstanceType': 't2.medium',
                                           'NetworkInterfaces': [{'AssociatePublicIpAddress': True,
                                           ...

    Returns:
        CloudFormation template as a dict
    """
    cf_client = boto3.client('cloudformation')

    # workaround for https://github.com/boto/botocore/issues/1889
    cf_client.meta.events.unregister('after-call.cloudformation.GetTemplate', json_decode_template_body)
    original_cfn_template = cf_client.get_template(StackName=stack_name)['TemplateBody']
    cfn_template_removed_newline = original_cfn_template.replace('\n', '')
    dict_template = json.loads(cfn_template_removed_newline)

    return dict_template


def cfn_outputs_to_dict(cfn_outputs) -> dict:
    """Description:
        Converts CloudFormation outputs to a dict

    Args:
        cfn_outputs: CloudFormation outputs

    Example:
        Example usage:

            import boto3
            client = boto3.client('cloudformation')
            stack = client.describe_stacks(StackName='Trend-DevOps-base-infrastructure-shared')
            outputs = stack['Stacks'][0]['Outputs']
            output_dict = outputs_to_dict(outputs)
            print(output_dict)
            {'VpcId': 'vpc-hf73ls9374vdy3921', 'PublicSubnetId': 'subnet-k34mns3l120dy2i'}

    Returns:
        CloudFormation outputs as a dict
    """
    output = {}
    for entry in cfn_outputs:
        key = entry['OutputKey']
        value = entry['OutputValue']
        output[key] = value

    return output
