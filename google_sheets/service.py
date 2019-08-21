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
from time import sleep
from utils.log import cool_print_decoration
from .config import CLIENT_SECRET_FILE, SCOPES, APPLICATION_NAME
from .params import get_params

flags = None

class GoogleSheets:
    SPREADSHEET_ID = ('', '', '')
    def __init__(self, _type='', sheets_data='', spreadsheet_id='', *args, **kw):
        self._credentials = self.get_credentials()
        self._type = _type
        self._http = None
        self._service = None
        self._students_data = []
        if (spreadsheet_id): GoogleSheets.SPREADSHEET_ID = spreadsheet_id
        if (not spreadsheet_id and sheets_data): self.set_initial_global_params(sheets_data)
    def set_initial_global_params(self, sheets_data):
        params = get_params(file_data=sheets_data)
        GoogleSheets.SPREADSHEET_ID = params['evaluation_sheet_id']
    
    @property
    def students_data(self):
        return self._students_data
    
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

    def create_service(self) -> None:
        """
        Creates callable Google service.
        :param http: authorization
        :param _type: SHEETS o SCRIPT.
        :return: function that calls google's correponding api.
        """
        discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
        if self._type == 'SHEETS':
            service = discovery.build(
                'sheets', 'v4', http=self._http, discoveryServiceUrl=discoveryUrl).spreadsheets().values()

            def __service_sheets(_range, extract=True):
                """
                Calls Google's service and returns array result from an api call
                :param _range: Cell range to look for
                :param extract: Boolean that indicates top level extraction
                :return: array of elements resulting from api call
                """
                try:
                    result = service.get(spreadsheetId=GoogleSheets.SPREADSHEET_ID, range=_range).execute()[
                        'values']
                except HttpError as e:
                    cool_print_decoration(
                        "Request limit reached. Try again later (>100s)\n{}".format(e), style='alert')
                    sys.exit(0)
                else:
                    return result[0] if extract else result

            self._service = __service_sheets
        else:
            service = discovery.build('script', 'v1', http=self._http).scripts()

            def __service_scripts(_range):
                """
                Calls Google's service and returns array result from an api call
                :param _range: Cell range to look for
                :return: array of elements resulting from api call
                """
                script_name = 'getNotes'  # spreadsheet script function name
                return service.run(body={'function': script_name, 'parameters': [GoogleSheets.SPREADSHEET_ID, _range]}).execute()['response']['result'][0]

            self._service = __service_scripts
    
    def get_header_range(self, information_cell='A1') -> str:
        header_range = self._service(information_cell)
        return header_range[0] if header_range else None
    
    def get_next_range(self, header_range: str) -> int:
        """
        Yields next range to look for
        :param header_range: String that represents start and end range from spreadsheet. Ex: A1:B20
        :return: Yields next range
        """
        start, end = header_range.split(':')
        next_num = int(start[-1]) + 1
        start = start[:1]
        end = end[:1]
        while True:
            yield ':'.join(['{0}{1}'.format(start, next_num), '{0}{1}'.format(end, next_num)])
            next_num += 1
    
    def get_row_number(self, column_row_range):
        index = 0
        column_row_range = column_row_range.split(':')[0]
        while column_row_range[index:][0].isalpha():
            index += 1
        return column_row_range[index:]
    
    def fetch_data(self):
        header_range = self.get_header_range()
        range_generator = self.get_next_range(header_range)
        students_data = {}
        key_error = False
        data: list
        while not key_error:
            nxt = next(range_generator)
            row = self.get_row_number(nxt)
            if (int(row) % 90 == 0):
                # API limit requests: 100 requests per 100s per user
                cool_print_decoration(
                    'Too many requests. Going to sleep...', style='info')
                sleep(100)
                cool_print_decoration('Ready to work again!', style='result')
            try:
                data = self._service(nxt)
                print(data)
                if len(data) > 1:
                    student_id = data[0]
                    student_array = data[1:]
                    students_data[student_id] = student_array
            except KeyError:
                cool_print_decoration('Done with API.', style='result')
                key_error = True
        self._students_data = students_data

if __name__ == '__main__':
    google_sheets = GoogleSheets(_type='SHEETS')
    google_sheets.authorize_credentials()
    google_sheets.create_service()
    cool_print_decoration('Connection with API successful.', style='result')
