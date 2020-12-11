import logging
import requests
import os
import requests
import json
import datetime

import azure.functions as func

def get_MSI_Token():
    identity_endpoint = os.environ["IDENTITY_ENDPOINT"]
    identity_header = os.environ["IDENTITY_HEADER"]
    resource_uri = "https://management.azure.com"
    # resource_uri = "https://storage.azure.com/"
    token_auth_uri = f"{identity_endpoint}?resource={resource_uri}&api-version=2019-08-01"
    head_msi = {'X-IDENTITY-HEADER':identity_header}

    resp = requests.get(token_auth_uri, headers=head_msi)
    access_token = resp.json()['access_token']
    # print(access_token)

    return access_token

def get_transactions(access_token, target_uri, t1, t2):
    today = t1
    yesterday = t2

    print(today)
    print(yesterday)

    headers = {
        "Authorization": 'Bearer ' + access_token
    }

    # # URLs for retrieving data
    uri_base = 'https://management.azure.com/'

    # Build search parameters from query details
    search_params = {
        'metricnames': 'Transactions',
        'metricnamespace': 'Microsoft.Storage/storageAccounts/blobServices',
        'interval': 'PT24H',
        'aggregation': 'total',
        'api-version': '2018-01-01',
        'timespan': "{}/{}".format(yesterday, today)
    }
    # print(search_params)
    # print(headers)

    # Build URL and send post request
    uri = uri_base + target_uri + '/blobServices/default/providers/microsoft.insights/metrics'

    try:
        response = requests.get(uri, params=search_params, headers=headers)
        logging.info('RESPONSE IS %s', response)
        # data = response.text
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    # except HTTPError as http_err:
    #     print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        data_json = response.json()
        T_value = data_json['value'][0]['timeseries'][0]['data'][0]['total']
        logging.info('T_VALUES IS %s', T_value )
        return int(T_value)


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    
    token = get_MSI_Token()
    logging.info('Access token is %s', token)

    t1 = datetime.datetime.now()
    t2 = t1 - datetime.timedelta(days=1)
    target_uri = "/subscriptions/d676200c-7ca5-43dd-9a48-210ec160c0ea/resourceGroups/mustang/providers/Microsoft.Storage/storageAccounts/mustangadls"
    v1 = get_transactions(token, target_uri, t1, t2)
    logging.info('TRANSACTIONS %s', v1)

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
