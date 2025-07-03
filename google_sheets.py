from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_sheet_data(spreadsheet_id, range_name="Sheet1"):
    creds = service_account.Credentials.from_service_account_file("credentials.json")
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return result.get('values', [])
