# Azure-Functions-with-MSI

We can use Manage service Identity to fetch access token to interact with various Azure services. Code sample at https://docs.microsoft.com/en-us/azure/app-service/overview-managed-identity?tabs=python#code-examples

## For App Service Plan 
There are two inbuit Environment variables which we can accall in our app to get the access token.
identity_endpoint = os.environ["IDENTITY_ENDPOINT"]
identity_header = os.environ["IDENTITY_HEADER"]
head_msi = {'X-IDENTITY-HEADER':identity_header}
API_VERSION =2019-08-01

## For Conumtion tier plan 
There are two inbuit Environment variables which we can accall in our app to get the access token. An older version of this protocol, using the "2017-09-01" API version, used the secret header instead of X-IDENTITY-HEADER and only accepted the clientid property for user-assigned. It also returned the expires_on in a timestamp format. MSI_ENDPOINT can be used as an alias for IDENTITY_ENDPOINT, and MSI_SECRET can be used as an alias for IDENTITY_HEADER. This version of the protocol is currently required for Linux Consumption hosting plans
https://docs.microsoft.com/en-us/azure/app-service/overview-managed-identity?tabs=python#using-the-rest-protocol

identity_endpoint = os.environ["MSI_ENDPOINT"]
identity_header = os.environ["MSI_SECRET"]
head_msi = {'secret':identity_header}
API_VERSION = 2017-09-0
