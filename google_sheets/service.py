from __future__ import print_function
import httplib2
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from googleapiclient.errors import HttpError
from itertools import zip_longest
import time
import json
from utils.log import cool_print_decoration
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
from config import CLIENT_SECRET_FILE, SCOPES, APPLICATION_NAME
from params import GET_NOTES_API, SPREADSHEET_ID, EVALUATION_NAME, SHEET_ID

class GoogleSheets:
    def __init__(self, _type='', *args, **kw):
        self._credentials = self.get_credentials()
        self._type = _type
        self._http = None
        self._service = None
    
    def get_credentials(self):
        """
        Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Same example code from Google.
        :return: Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(
            credential_dir, 'sheets.googleapis.com-python-quickstart.json')
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            cool_print_decoration('Storing credentials to ' +
                                credential_path, style='info')
        return credentials

    def authorize_credentials(self):
        http = httplib2.Http()
        self._http = self._credentials.authorize(http)
    def create_service(self):
        """
        Creates callable Google service.
        :param http: authorization
        :param _type: SHEETS o SCRIPT.
        :return: function that calls google's correponding api.
        """
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
        if self._type == 'SHEETS':
            self._service = discovery.build(
                'sheets', 'v4', http=self._http, discoveryServiceUrl=discoveryUrl).spreadsheets().values()

            def __service_sheets(_range, extract=True):
                """
                Calls Google's service and returns array result from an api call
                :param _range: Cell range to look for
                :param extract: Boolean that indicates top level extraction
                :return: array of elements resulting from api call
                """
                try:
                    result = self._service.get(spreadsheetId=SPREADSHEET_ID, range=_range).execute()[
                        'values']
                except HttpError as e:
                    cool_print_decoration(
                        "Request limit reached. Try again later (>100s)\n{}".format(e), style='alert')
                    sys.exit(0)
                else:
                    return result[0] if extract else result

            return __service_sheets
        else:
            self._service = discovery.build('script', 'v1', http=self._http).scripts()

            def __service_scripts(_range):
                """
                Calls Google's service and returns array result from an api call
                :param _range: Cell range to look for
                :return: array of elements resulting from api call
                """
                script_name = 'getNotes'  # spreadsheet script function name
                return self._service.run(body={'function': script_name, 'parameters': [SPREADSHEET_ID, _range]}, scriptId=GET_NOTES_API).execute()['response']['result'][0]

            return __service_scripts


if __name__ == '__main__':
    google_sheets = GoogleSheets(_type='SHEETS')
    google_sheets.authorize_credentials()
    google_sheets.create_service()
    cool_print_decoration('Connection with API successful.', style='result')
