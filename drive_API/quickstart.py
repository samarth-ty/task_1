from importlib.metadata import files

from importlib.resources import path

import os.path
import io
import google.auth
from googleapiclient.http import MediaIoBaseDownload

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', 'https://www.googleapis.com/auth/spreadsheets']

SAMPLE_SPREADSHEET_ID = '1C2jhU7V2FZTHxpxqhjt9uAsZE7GHAH80kj74KmnWP_c'
SAMPLE_RANGE_NAME = 'A1:E2'


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
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
        # HTTP   = creds.authorize(Http())
        # DRIVE  = discovery.build('drive',  'v3', http=HTTP)
        # SHEETS = discovery.build('sheets', 'v4', http=HTTP)
        service1 = build('drive', 'v3', credentials=creds)
        service2 = build('sheets', 'v4', credentials=creds)

        # Call the Drive v3 API
        results = service1.files().list(
            q="mimeType='application/vnd.google-apps.folder'", pageSize=10, fields="nextPageToken, files(id, name, webViewLink)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        # print('Files:')
        for item in items:
            res = service1.files().list(fields="nextPageToken, files(id, name)").execute()
            itms = res.get('files',[])
            if not itms:
                print('No files found.')
                return
            print(f"Files inside folder {item['name']}:")
            for itm in itms:
                print(u'{0} ({1})'.format(itm['name'], itm['id']))
            print('files should end here--------------------------------------------')
            print(u'{0} ({1}) ({2})'.format(item['name'], item['id'], item['webViewLink'],))

        sheet = service2.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        # print('Folder Link, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))


    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


# def update_values(spreadsheet_id, range_name, value_input_option,
#                   _values):

#     creds = None
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)

#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     try:

#         service = build('sheets', 'v4', credentials=creds)
#         values = [
#             _values
#         ]
#         body = {
#             'values': values
#         }
#         result = service.spreadsheets().values().update(
#             spreadsheetId=spreadsheet_id, range=range_name,
#             valueInputOption=value_input_option, body=body).execute()
#         # print(f"{result.get('updatedCells')} cells updated.")
#         print(result)

#     except HttpError as error:
#         print(f"An error occurred: {error}")
#         return error


def download_file(real_file_id):

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
        # create gmail api client
        service = build('drive', 'v3', credentials=creds)

        file_id = real_file_id

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(F'Download {int(status.progress() * 100)}.')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.getvalue()

if __name__ == '__main__':
    main()
    # update_values("1C2jhU7V2FZTHxpxqhjt9uAsZE7GHAH80kj74KmnWP_c",
    #               "A3:E3", "USER_ENTERED",
    #               [
    #                   ['link.nfdnfwfunwufnwuuduvn.com', 'testfile.pdf', '84848484884', 'email@gmail.com', 'https://www.linkedin.com/in/sam-tyagi-6b6487245/']
    #               ])
    # download_file(real_file_id='1q5Zf2yWDQOKwGRpxhvosKHfNU9QXIq6A')

