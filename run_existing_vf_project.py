# import argparse
#
# parser = argparse.ArgumentParser(
#     description='Invoke Visual Forecasting REST API to run an existing project with new data.')
# parser.add_argument('--protocol', default='http')
# parser.add_argument('--host', required=True)
# parser.add_argument('--port', default='80')
# parser.add_argument('--username', required=True)
# parser.add_argument('--password', required=True)
# parser.add_argument('--projectId', default='2e907a90-e798-4eaa-b7de-6ee084870312')
# env = parser.parse_args()
#
# print(env)
#
# # !/usr/bin/python

import sys
import argparse
import requests
import json
import time


def vf_new_iteration(argv):
    # parse arguments
    parser = argparse.ArgumentParser(
        description='Invoke Visual Forecasting REST API to run an existing project with new data.')
    parser.add_argument('--protocol', default='http')
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', default='80')
    parser.add_argument('--username', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument(
        '--projectId', default='a26c680f-62a4-43cc-96f3-d44312b3c25e')
    env = parser.parse_args()

    get_auth_token(env)
    # get_data_spec(env)
    # import_new_data(env)
    # run_pipelines(env)
    # wait_for_pipelines(env)
    # # prepare_for_overrides(env)
    # resubmit_overrides(env)


def get_auth_token(env):
    print('Get authorization token...')
    uri = '{env.protocol}://{env.host}:{env.port}/SASLogon/oauth/token'.format(
        **locals())
    headers = {
        'Authorization': 'Basic c2FzLmVjOg==',
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = 'grant_type=password&username={env.username}&password={env.password}'.format(
        **locals())
    response = requests.post(uri, headers=headers, data=body)
    print('Response Status: {response.status_code}'.format(**locals()))
    print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
    env.status = response.status_code
    env.authtoken = response.json()['access_token']


def get_data_spec(env):
    print('Fetch data specification, checking for updated input data...')
    # uri=env.protocol+"://"+env.host+":"+env.port+"/forecastingGateway/projects/a26c680f-62a4-43cc-96f3-d44312b3c25e/dataSpecification?checkForDataUpdates=true"

    uri = '{env.protocol}://{env.host}:{env.port}/forecastingGateway/projects/{env.projectId}/dataSpecification?checkForDataUpdates=true'.format(
        **locals())
    headers = {
        'Authorization': 'bearer {env.authtoken}'.format(**locals()),
        'Accept': 'application/vnd.sas.analytics.forecasting.data.definition+json'
    }
    response = requests.get(uri, headers=headers)
    print('Response Status: {response.status_code}'.format(**locals()))
    print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
    env.status = response.status_code


def import_new_data(env):
    print('If necessary, import new input data...')
    uri = '{env.protocol}://{env.host}:{env.port}/forecastingGateway/projects/{env.projectId}/dataSpecification/inputData'.format(
        **locals())
    headers = {
        'Authorization': 'bearer {env.authtoken}'.format(**locals())
    }
    response = requests.put(uri, headers=headers)
    print('Response Status: {response.status_code}'.format(**locals()))
    print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
    env.status = response.status_code


def run_pipelines(env):
    print('Run all pipelines...')
    uri = '{env.protocol}://{env.host}:{env.port}/forecastingGateway/projects/{env.projectId}/pipelineJobs'.format(
        **locals())
    headers = {
        'Authorization': 'bearer {env.authtoken}'.format(**locals()),
        'Accept': 'application/vnd.sas.job.execution.job+json'
    }
    response = requests.post(uri, headers=headers)
    print('Response Status: {response.status_code}'.format(**locals()))
    print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
    env.status = response.status_code


def wait_for_pipelines(env):
    print('Wait for pipelines to finish running...')
    uri = '{env.protocol}://{env.host}:{env.port}/forecastingGateway/projects/{env.projectId}/pipelineJobs/@currentJob'.format(
        **locals())
    headers = {
        'Authorization': 'bearer {env.authtoken}'.format(**locals()),
        'Accept': 'application/vnd.sas.job.execution.job+json'
    }

    i = 0
    while True:
        response = requests.get(uri, headers=headers)
        print('Response Status: {response.status_code}'.format(**locals()))
        print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
        env.status = response.status_code
        env.jobState = response.json()['state']

        time.sleep(10)

        if env.jobState != 'running' or i == 30:
            break

        i += 1


def prepare_for_overrides(env):
    print('Prepare for overrides...')
    uri = '{env.protocol}://{env.host}:{env.port}/forecastingGateway/projects/{env.projectId}/dataSpecification/overridesDataPrep'.format(
        **locals())
    headers = {
        'Authorization': 'bearer {env.authtoken}'.format(**locals()),
        'Content-Type': 'application/vnd.sas.analytics.forecasting.data.specification+json'
    }
    response = requests.put(uri, headers=headers)
    print('Response Status: {response.status_code}'.format(**locals()))
    print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
    env.status = response.status_code


def resubmit_overrides(env):
    print('Resubmit overrides...')
    uri = '{env.protocol}://{env.host}:{env.port}/forecastingGateway/projects/{env.projectId}/transactions/jobs'.format(
        **locals())
    headers = {
        'Authorization': 'bearer {env.authtoken}'.format(**locals()),
        'Accept': 'application/vnd.sas.forecasting.overrides.engine.transaction.collection.job+json',
        'Content-Type': 'application/vnd.sas.forecasting.overrides.engine.transaction.collection.job.request+json'
    }
    body = '{\"firstTransaction\":\"@first\",\"lastTransaction\":\"@last\"}'

    i = 0
    while True:
        response = requests.post(uri, headers=headers, data=body)
        print('Response Status: {response.status_code}'.format(**locals()))
        print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
        env.status = response.status_code

        time.sleep(10)

        if env.status == 201 or i == 6:
            break

        i += 1


if __name__ == "__main__":
    vf_new_iteration(sys.argv[1:])

# Testing other endpoints
"""
project_settings_uri=env.protocol+"://"+env.host+":"+env.port+"/forecastingGateway/projects/a26c680f-62a4-43cc-96f3-d44312b3c25e/settings"
headers = {
    'Authorization': 'bearer {env.authtoken}'.format(**locals()),
    'Accept': 'application/vnd.sas.forecasting.project.settings+json'
}
"""
