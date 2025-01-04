import gspread
from oauth2client.service_account import ServiceAccountCredentials
import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	



def update_table(title, data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open(title).sheet1
    
    sheet.update([data])

    return "Данные добавлены успешно!"


def create_table(title):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    httpAuth = creds.authorize(httplib2.Http()) # Авторизуемся в системе
    
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 

    spreadsheet = service.spreadsheets().create(body = {
        'properties': {'title': title, 'locale': 'ru_RU'}
    }).execute()
    spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла

    driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
    access = driveService.permissions().create(
        fileId = spreadsheetId,
        body = {'type': 'user', 'role': 'writer', 'emailAddress': 'ocirovvadim51@gmail.com'},  # Открываем доступ на редактирование
        fields = 'id',
        sendNotificationEmail=False
    ).execute()

    spreadsheet_id = f'https://docs.google.com/spreadsheets/d/{spreadsheetId}'
    return spreadsheet_id



scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)