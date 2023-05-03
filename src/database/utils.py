# This code was based on the following example by Google:
# https://developers.google.com/sheets/api/quickstart/python

from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID of se-database spreadsheet. View sheet here:
# https://docs.google.com/spreadsheets/d/18_1BmTraUsLMjflzU0s_KM_ePtelgOcl3MM1CwmqQzs/edit?usp=sharing
SPREADSHEET_ID = '18_1BmTraUsLMjflzU0s_KM_ePtelgOcl3MM1CwmqQzs'


def read(sheet='current', cell_range='A1:B100'):
    """
    Read contents of se-database sheet into a dict.

    Parameters:
    -----------
    sheet : str, optional
        The sheet to read (default current).
    cell_range : str, optional
        Range of cells to read (default A1:B100).
    Returns:
    --------
    values_dict : dict
        The values of the specified cells in the format:
        {'key': value}, where value is float.
        Empty rows are omitted.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        range_name = sheet + '!' + cell_range
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=range_name).execute()
        values = result.get('values', [])

        if not values:
            raise IOError('No data found.')

        values_dict = {values[row][0]: float(values[row][1]) for row in range(len(values))}

        return values_dict

    except HttpError as err:
        raise err
