import argparse
import csv
import json
import boto3
import logging
from typing import List


def load_json(filename: str) -> dict:
    """
    Load json data from file
    :param filename: json file name
    :return: json data
    """
    with open(filename, newline='') as f:
        return json.load(f)


def list_lambdas(client: boto3.client) -> List[str]:
    """
    List all Lambdas in the account
    :param client: boto3 client
    :return: List of Lambda names
    """
    lambda_list = []
    paginator = client.get_paginator('list_functions')
    page_iterator = paginator.paginate()
    for page in page_iterator:
        functions = [function['FunctionName']
                     for function in page['Functions']]
        lambda_list += functions
    return lambda_list


def get_depracated_by_region(session, region, DEPRECATED_RUNTIMES):
    logging.info(f'Running on {region}')
    client = session.client('lambda', region_name=region)
    lambda_list = list_lambdas(client)

    lambdas = []

    for lambda_name in lambda_list:
        response = client.get_function_configuration(
            FunctionName=lambda_name
        )
        if (response['Runtime'] in DEPRECATED_RUNTIMES):
            logging.warning(
                f'Registrando lambda com runtime depreciado: {response["FunctionName"]}')
            lambdas.append({
                'arn': response['FunctionArn'], 'runtime': response['Runtime'], 'region': region
            })
        else:
            logging.info(
                f'Lambda ok: {response["FunctionName"]}')

    return lambdas


def run_to_all_lambdas(DEPRECATED_RUNTIMES, session, region_list):
    all_lambdas = []
    for region in region_list:
        all_lambdas = all_lambdas + \
            get_depracated_by_region(session, region, DEPRECATED_RUNTIMES)

    return all_lambdas


def save_report(profile, all_lambdas, keys):
    with open(f'deprecated_lambdas.{profile}.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys, delimiter=';')
        dict_writer.writeheader()
        dict_writer.writerows(all_lambdas)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log_level', required=False)
    parser.add_argument('-d', '--deprecated_runtime_list', required=True,
                        help='path to the deprecated_runtime_list file')
    parser.add_argument('-p', '--profiles', required=True,
                        help='env profile', nargs='+')
    args = parser.parse_args()
    log_level = 'WARNING'
    if (args.log_level):
        log_level = args.log_level
    deprecated_runtime_list = args.deprecated_runtime_list
    profiles = args.profiles
    logging.basicConfig(level=logging._nameToLevel[log_level],
                        filename='scan_lambdas.log', filemode='w')

    logging.info(f'load {deprecated_runtime_list}')
    DEPRECATED_RUNTIMES = load_json(deprecated_runtime_list)

    for profile in profiles:
        logging.info(f'Running in {profile}')
        session = boto3.Session(profile_name=profile)
        region_list = ['sa-east-1', 'us-east-1']

        all_lambdas = run_to_all_lambdas(
            DEPRECATED_RUNTIMES, session, region_list)

        logging.info(f'Generating report')

        keys = ["runtime", "region", "arn"]
        save_report(profile, all_lambdas, keys)


if __name__ == '__main__':
    main()
