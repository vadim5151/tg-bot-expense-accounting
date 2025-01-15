import gspread
from oauth2client.service_account import ServiceAccountCredentials
import httplib2 
import apiclient.discovery # type: ignore
from oauth2client.service_account import ServiceAccountCredentials	
from datetime import datetime



async def update_table(title, data):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    client =  gspread.authorize(creds)

    sheet = client.open(title).sheet1
    
    sheet.append_row(data)


async def create_worksheet(title):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

    client = gspread.authorize(creds)

    sheet =  client.open(title)
    # Получение текущего месяца
    current_month_year = datetime.now().strftime("%B-%Y")  # Получает название месяца (например, "October")
    # Создание нового листа с именем текущего месяца
    try:
        sheet.add_worksheet(title=current_month_year, rows="100", cols="15")
        print(f"Лист '{current_month_year}' успешно создан.")
    except Exception as e:
        print(f"Ошибка при создании листа: {e}")


async def create_table(title):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    httpAuth = creds.authorize(httplib2.Http()) # Авторизуемся в системе
    
    service =  apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 

    current_month_year = datetime.now().strftime("%B-%Y")

    spreadsheet =  service.spreadsheets().create(body = {
        'properties': {'title': title, 'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': current_month_year,
                               'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
    }).execute()
    
    spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла

    driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API

    access = driveService.permissions().create(
        fileId = spreadsheetId,
        body = {'type': 'user', 'role': 'writer', 'emailAddress': 'ocirovvadim51@gmail.com'},  # Открываем доступ на редактирование
        fields = 'id',
        sendNotificationEmail=False
    ).execute()

    # create_worksheet(title)
    spreadsheet_id = spreadsheetId
    return spreadsheet_id


async def find_last_row(title):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open(title).sheet1

    data = sheet.get_all_values()

    last_filled_row_index = None

    for row_index in range(len(data)-1, -1, -1):  # Идем с конца к началу
        if any(data[row_index]):  # Проверяем, есть ли заполненные ячейки в строке
            last_filled_row_index = row_index +1 # +1, чтобы учесть нумерацию с 1
            break

    # Проверяем, найдена ли последняя заполненная строка
    if last_filled_row_index is not None:
        last_row_data = data[last_filled_row_index -1]
        return last_filled_row_index, last_row_data
    


async def delete_data_sheet(title, last_filled_row_index):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open(title).sheet1

    sheet.batch_clear([f'A{last_filled_row_index}:C{last_filled_row_index}'])


# def create_diagram(title, last_filled_row_index):
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

#     client = gspread.authorize(creds)

#     sheet = client.open(title).sheet1

#     worksheet = sheet.get_worksheet(0)

#     chart = sheet.add_chart({
#     'type': 'LINE',
#     'title': title,
#     'range': f'A2::C{last_filled_row_index}'
# })
#     return chart


async def get_values(title, last_filled_row_index):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open(title).sheet1

    values_list = []
    all_values = ''

    for i in range(2, last_filled_row_index+1):
        values_list.append(sheet.row_values(i))
    
    for i in values_list:
        all_values += f"{' '.join(map(str, i))}\n"
    return all_values



async def get_title_worksheet(title):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)

    client = gspread.authorize(creds)

    sheet = client.open(title)
    worksheets = sheet.worksheets()

    all_title_worksheets = []

    for worksheet in worksheets:
        all_title_worksheets.append(worksheet.title)
    
    return all_title_worksheets