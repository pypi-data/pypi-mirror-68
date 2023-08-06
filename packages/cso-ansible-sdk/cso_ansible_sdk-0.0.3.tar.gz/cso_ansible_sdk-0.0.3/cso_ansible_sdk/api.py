import requests
import cso_ansible_sdk.constants
from cso_ansible_sdk.error_report import error_report


class ApiWrapper(object):
    def __init__(self, api_url=None, api_token=None):
        if not api_url or not api_token:
            raise ValueError("Mising the token or  URL")
        else:
            self.api_url = api_url
            self.api_token = api_token
    
    @error_report
    def get(self, endpoint):
        headers = {
            'x-auth-token': self.api_token,
            'Content-Type': 'application/json'
        }

        response = requests.get('{}{}'.format(self.api_url, endpoint), headers=headers)

        response.raise_for_status()

        return response

    @error_report
    def post(self, endpoint, payload):
        headers = {
            'x-auth-token': self.api_token,
            'Content-Type': 'application/json'
        }

        response = requests.post('{}{}'.format(self.api_url, endpoint), headers=headers, data=payload)

        response.raise_for_status()

        return response


class CSO(object):
    _CSO_API_URL = 'https://contrail-juniper.net'

    def __init__(self, api_token=None):
        if not api_token:
            raise ValueError("Please provide API token")
        else:
            self.api_wrapper = ApiWrapper(self._CSO_API_URL,api_token)

    def get_site_list(self):
        endpoint = cso_ansible_sdk.constants.GET_SITE_LIST
        response = self.api_wrapper.get(endpoint)
        response = response.json()

        return response

    def get_sites_by_name(self):
        endpoint = cso_ansible_sdk.constants.GET_SITE_LIST
        response = self.api_wrapper.get(endpoint)
        response = response.json()

        return response

    def create_site(self, payload):
        endpoint = cso_ansible_sdk.constants.CREATE_SITE
        response = self.api_wrapper.post(endpoint=endpoint, payload=payload)
        response = response.json()

        return response

    def delete_site(self, payload):
        endpoint = cso_ansible_sdk.constants.DELETE_SITE
        response = self.api_wrapper.post(endpoint=endpoint, payload=payload)
        response = response.json()

        return response

    def get_auth_token(self, payload):
        endpoint = cso_ansible_sdk.constants.GET_AUTH_TOKEN
        response = self.api_wrapper.post(endpoint=endpoint, payload=payload)
        response = response.json()

        return response
