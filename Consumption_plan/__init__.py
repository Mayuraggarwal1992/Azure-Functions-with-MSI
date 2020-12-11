import logging
import requests
import os
import requests
import json
import datetime

import azure.functions as func

def get_MSI_Token():
    identity_endpoint = os.environ["MSI_ENDPOINT"]
    identity_header = os.environ["MSI_SECRET"]
    logging.info('IDENTITY_ENDPOINT %s', identity_endpoint)
    # resource_uri = "https://management.azure.com"
    resource_uri = "https://thingworxrepo.blob.core.windows.net"
    token_auth_uri = f"{identity_endpoint}?resource={resource_uri}&api-version=2017-09-01"
    # head_msi = {'X-IDENTITY-HEADER':identity_header}
    head_msi = {'secret':identity_header}

    resp = requests.get(token_auth_uri, headers=head_msi)
    logging.info('MSI REPSONSE %s', resp)
    access_token = resp.json()['access_token']
    # print(access_token)

    return access_token


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    
    token = get_MSI_Token()
    logging.info('Access token is %s', token)
    logging.info('Python timer trigger function ran at %s', utc_timestamp)
