import argparse
import csv
import boto3
import logging


NODE_RUNTIME = 'nodejs16.x'
PYTHON_RUNTIME = 'python3.9'


def load_csv(filename):
    with open(filename, newline='') as f:
        reader = csv.DictReader(f, delimiter=';')
        data = list(reader)
    return data


def parse_data(dataitem):
    runtime = NODE_RUNTIME
    region = dataitem['region']
    arn = dataitem['arn']
    if 'python' in dataitem['runtime']:
        runtime = PYTHON_RUNTIME
    return {
        'arn': arn.replace(':$LATEST', ''),
        'region': region,
        'runtime': runtime
    }


def update_lambda(item, profile='DEV'):
    region = item['region']
    function_arn = item['arn']
    runtime = item['runtime']

    session = boto3.Session(profile_name=profile, region_name=region)
    client = session.client('lambda')

    return client.update_function_configuration(FunctionName=function_arn, Runtime=runtime)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log_level', required=False)
    parser.add_argument('-s', '--source_csv', required=True,
                        help='path to the csv file')
    parser.add_argument('-p', '--profile', required=True,
                        help='env profile')
    args = parser.parse_args()
    log_level = 'WARNING'
    if (args.log_level):
        log_level = args.log_level
    SOURCE_CSV = args.source_csv
    PROFILE = args.profile

    logging.basicConfig(
        level=logging._nameToLevel[log_level], filename='update_runtimes.log', filemode='w')
    logging.info(f'load csv {SOURCE_CSV}')
    data = load_csv(SOURCE_CSV)

    logging.info('parse csv')
    collection = [parse_data(dataitem) for dataitem in data]

    for lambda_config in collection:
        logging.info(f'update_lambda: {PROFILE} - { lambda_config["arn"] }')
        try:
            update_lambda(lambda_config, PROFILE)
        except:
            logging.error(f'Erro { lambda_config["arn"] }')


if __name__ == '__main__':
    main()
