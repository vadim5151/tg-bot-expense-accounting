import gspread
from oauth2client.service_account import ServiceAccountCredentials
import httplib2 
import apiclient.discovery # type: ignore
from oauth2client.service_account import ServiceAccountCredentials	



def update_table(title, data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open(title).sheet1
    
    sheet.append_row(data)


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

    spreadsheet_id = spreadsheetId
    return spreadsheet_id


def find_last_row(title):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open(title).sheet1

    data = sheet.get_all_values()

    last_filled_row_index = None

    for row_index in range(len(data)-1, -1, -1):  # Идем с конца к началу
        if any(data[row_index]):  # Проверяем, есть ли заполненные ячейки в строке
            last_filled_row_index = row_index + 1  # +1, чтобы учесть нумерацию с 1
            break

    # Проверяем, найдена ли последняя заполненная строка
    if last_filled_row_index is not None:
        last_row_data = data[last_filled_row_index - 1]
        return last_filled_row_index, last_row_data
    else:
        print("Заполненных строк не найдено.")


def delete_data_sheet(title, last_filled_row_index):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open(title).sheet1

    sheet.batch_clear([f'A{last_filled_row_index}:C{last_filled_row_index}'])
