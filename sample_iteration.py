#!/usr/bin/python

import sys, argparse, requests, json, time


###############################################################################
# Invoke Visual Forecasting REST API to run an existing project with new data.
###############################################################################
def vf_new_iteration(argv):
    # parse arguments
    parser = argparse.ArgumentParser(
        description='Invoke Visual Forecasting REST API to run an existing project with new data.')
    parser.add_argument('--protocol', default='http')
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', default='80')
    parser.add_argument('--username', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--projectId', default='2e907a90-e798-4eaa-b7de-6ee084870312')
    env = parser.parse_args()

    get_auth_token(env)
    get_data_spec(env)
    import_new_data(env)
    run_pipelines(env)
    wait_for_pipelines(env)
    prepare_for_overrides(env)
    resubmit_overrides(env)


###############################################################################
# Get authorization token...
###############################################################################
def get_auth_token(env):
    print('Get authorization token...')
    uri = '{env.protocol}://{env.host}:{env.port}/SASLogon/oauth/token'.format(**locals())
    headers = {
        'Authorization': 'Basic c2FzLmVjOg==',
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = 'grant_type=password&username={env.username}&password={env.password}'.format(**locals())
    response = requests.post(uri, headers=headers, data=body)
    print('Response Status: {response.status_code}'.format(**locals()))
    print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
    env.status = response.status_code
    env.authtoken = response.json()['access_token']

    if not env.status == 200:
        sys.exit(1)


###############################################################################
# Fetch data specification, checking for updated input data...
###############################################################################
def get_data_spec(env):
    print('Fetch data specification, checking for updated input data...')
    uri = '{env.protocol}://{env.host}:{env.port}/forecastingGateway/projects/{env.projectId}/dataDefinitions/@current?checkForUpdates=true'.format(
        **locals())
    headers = {
        'Authorization': 'bearer {env.authtoken}'.format(**locals()),
        'Accept': 'application/vnd.sas.analytics.forecasting.data.definition+json'
    }
    response = requests.get(uri, headers=headers)
    print('Response Status: {response.status_code}'.format(**locals()))
    print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
    env.status = response.status_code

    if not env.status == 200:
        sys.exit(1)


###############################################################################
# If necessary, import new input data...
###############################################################################
def import_new_data(env):
    print('If necessary, import new input data...')
    uri = '{env.protocol}://{env.host}:{env.port}/forecastingGateway/projects/{env.projectId}/dataDefinitions/@current/dataUpdateJobs?category=INPUT'.format(
        **locals())
    headers = {
        'Authorization': 'bearer {env.authtoken}'.format(**locals())
    }
    response = requests.post(uri, headers=headers)
    print('Response Status: {response.status_code}'.format(**locals()))
    print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
    env.status = response.status_code

    if not env.status == 202:
        sys.exit(1)


###############################################################################
# Run all pipelines...
###############################################################################
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

    if not env.status == 202:
        sys.exit(1)


###############################################################################
# Wait for pipelines to finish running...
###############################################################################
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

        if env.jobState == 'completed' or i == 30:
            break

        i += 1

    if not env.jobState == 'completed':
        sys.exit(1)


###############################################################################
# Prepare for overrides...
###############################################################################
def prepare_for_overrides(env):
    print('Prepare for overrides...')
    uri = '{env.protocol}://{env.host}:{env.port}/forecastingGateway/projects/{env.projectId}/dataDefinitions/@current/dataUpdateJobs?category=FORECAST'.format(
        **locals())
    headers = {
        'Authorization': 'bearer {env.authtoken}'.format(**locals()),
        'Content-Type': 'application/vnd.sas.analytics.forecasting.data.specification+json'
    }
    response = requests.post(uri, headers=headers)
    print('Response Status: {response.status_code}'.format(**locals()))
    print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
    env.status = response.status_code

    if not env.status == 202:
        sys.exit(1)


###############################################################################
# Resubmit overrides...
###############################################################################
def resubmit_overrides(env):
    print('Resubmit overrides...')
    uri = '{env.protocol}://{env.host}:{env.port}/forecastingGateway/projects/{env.projectId}/transactionJobs'.format(
        **locals())
    headers = {
        'Authorization': 'bearer {env.authtoken}'.format(**locals()),
        'Accept': 'application/vnd.sas.forecasting.overrides.transaction.collection.job+json',
        'Content-Type': 'application/vnd.sas.forecasting.overrides.transaction.collection.job.request+json'
    }
    body = '{\"firstTransaction\":\"@first\",\"lastTransaction\":\"@last\",\"autoResolve\":true}'

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

    if not env.status == 201:
        sys.exit(1)


if __name__ == "__main__":
    vf_new_iteration(sys.argv[1:])
