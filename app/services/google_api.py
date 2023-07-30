from datetime import datetime
from typing import List

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject

FORMAT = '%Y/%m/%d %H:%M:%S'
SPREADSHEET_BODY = {
    'properties': {'title': '',
                   'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист1',
                               'gridProperties': {'rowCount': 100,
                                                  'columnCount': 11}}}]
}


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """Функция создания гугл-таблицы с отчётом."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = SPREADSHEET_BODY.copy()
    spreadsheet_body['properties']['title'] = f'Отчёт по закрытым пожертвованиям на {now_date_time}'
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    """Выдача прав доступа на созданную гугл-таблицу."""
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects_closed: List[CharityProject],
        wrapper_services: Aiogoogle
) -> None:
    """Функция обновления данных в гугл-таблице."""
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    table_values = [
        ['Отчёт от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects_closed:
        new_row = [
            str(project['name']),
            str(project['collection_time']),
            str(project['description'])
        ]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    format_body = {
        'requests': [
            {
                'autoResizeDimensions': {
                    'dimensions': {
                        'dimension': 'COLUMNS',
                        'startIndex': 0,
                        'endIndex': 3
                    }
                }
            }
        ]
    }

    rows_value = len(table_values)
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'A1:C{rows_value}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )

    await wrapper_services.as_service_account(
        service.spreadsheets.batchUpdate(
            spreadsheetId=spreadsheet_id,
            json=format_body
        )
    )
