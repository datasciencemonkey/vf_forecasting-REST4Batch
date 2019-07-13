# Get the final forecasts published
""""The project uses some python 36 code efficiencies.
The general flow of the script is as follows
1. Use the bearer and the basic connection parameters to extract the data spec for the project we want the forecasts for
2. One the data definition ID is obtained from the spec, we can then use it to export forecasts to a caslib of our choice
3. Before #2 happens, we also need to ensure that we delete any old tables with the same name from the caslib of interest
for table export"""

import requests, json
from config import login
import swat

creds = login()

#  Target Caslib for export
caslib_short = "Public"
# Target CasTable
castable_dest = "outfor"
# Initiate a new CAS Session
conn = swat.CAS(creds["hostname"], 8777, creds["username"], creds["password"], protocol="http")
# change the current caslib to cas us
conn.setsessopt(caslib=caslib_short)


def get_auth_token(host, user, pswd):
    """Get bearer for requests"""
    print('Get authorization token...')
    uri = f'http://{host}:80/SASLogon/oauth/token'
    headers = {
        'Authorization': 'Basic c2FzLmVjOg==',
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = f'grant_type=password&username={user}&password={pswd}'
    response = requests.post(uri, headers=headers, data=body)
    print(f'Response Status: {response.status_code}')
    print(json.dumps(response.json(), indent=2, separators=(',', ': ')) + '\n')
    return response.json()['access_token']


def make_caslib_export_ready(sess, caslib_short, castable_dest):
    """Check if the castable already exists in caslib or the source"""
    if castable_dest.upper() in list(sess.tableinfo()['TableInfo']['Name']):
        print(f"INFO: Table {castable_dest.upper()} already exists")
        print(f"INFO: Deleting existing table from {caslib_short}.{castable_dest}")
        sess.droptable(name=castable_dest, caslib=caslib_short)
        print(f"INFO: In-Memory Table Deleted. Now Checking Source Files")
    else:
        print(f"INFO: The table is not available In-Memory. Now Checking Source Files")
    source_files = [i for i in map(str.lower, list(sess.fileinfo()['FileInfo']['Name']))]
    if castable_dest.lower() + '.sashdat' in source_files:
        print(f"INFO: Now Deleting Table from source")
        sess.deletesource(source=f"{castable_dest}.sashdat", caslib="Public")
        print(f"INFO: Previous versions of {castable_dest} - fully deleted")
    else:
        print(f"INFO: Table {castable_dest}.sashdat wasn't saved in the source directory of caslib {caslib_short}")
    print("INFO: Ready for to export new forecasts output table!")


# Run pre-check to see if the table exists
make_caslib_export_ready(conn, caslib_short, castable_dest)

# get auth token and then start to make requests per plan
authtoken = get_auth_token(creds['hostname'], creds['username'], creds['password'])

project_id = "a26c680f-62a4-43cc-96f3-d44312b3c25e"

dataspec_uri = f"http://{creds['hostname']}:80/forecastingGateway/projects/{project_id}/dataSpecification"

headers = {
    'Authorization': f'bearer {authtoken}',
    'Accept': 'application/vnd.sas.analytics.forecasting.data.definition+json'
}

dataspec_response = requests.get(dataspec_uri, headers=headers)
data_definition_id = dataspec_response.json()["id"]  # 4a91c448-0e06-435d-af76-c3a393d7aba0

# Now finally we can check for the export URI to get data out
export_forecast_uri = "http://dl-viya-cluster-1.dlviyacluster.sashq-r.openstack.sas.com:80/forecastingGateway/dataDefinitions/4a91c448-0e06-435d-af76-c3a393d7aba0/spec/finalForecasts"

headers = {
    'Authorization': f'bearer {authtoken}',
    'Content-Type': 'application/vnd.sas.forecasting.table.reference+json'
}

# Pay load contains destination caslib and the tablename
# To Publish Forecasts in the Public caslib
# caslib_dest = "/dataSources/providers/cas/sources/cas-shared-default~fs~Public"

body = """{"dataSourceUri": "/dataSources/providers/cas/sources/cas-shared-default~fs~Public","tableName": "outfor"}"""

# Make the post request and then treat response accordingly

move_forecasts = requests.post(export_forecast_uri, headers=headers, data=body)
if str(move_forecasts.status_code)[0] == '4':
    print(f"ERROR : Process Terminated with Status code {move_forecasts.status_code}")
    print(f"REASON:{move_forecasts.json()['message']}")
    print("FULL RESPONSE:")
    print(move_forecasts.json())
elif str(move_forecasts.status_code)[0] == '2':
    print(f"SUCCESS : Process Ended with Status code {move_forecasts.status_code}")
