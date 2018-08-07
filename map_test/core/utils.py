from django.conf import settings

from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
from google.oauth2 import service_account

from .models import Address, FusionTable


def init_credentials(scope):
    """
    :param scope: scope of the current auth (readonly, full access)
    :return: an authenticated session

    Gets authorization from google's API
    """
    credentials = service_account.Credentials.from_service_account_file(
        settings.BASE_DIR + '/google.json',
        scopes=[scope])
    return credentials


def build_service(service, version, scope='https://www.googleapis.com/auth/fusiontables'):
    """
    :param service: Google servide to use i.e 'drive', 'analytics'
    :param version: Google Api's version to use
    :param scope: scope of the current auth (readonly, full access)

    :return: Google Api's instance

    creates a new Google Api instance to consume the API REST
    """
    credentials = init_credentials(scope=scope)
    service = build(service, version, credentials=credentials)
    return service


def create_fusion_table():
    """
    :return: core.models.FusionTable instace

    Creates a new table on googlefusion and stores its id
    """
    fusion_columns = {
        "name": "Points",
        "columns": [
            {
                "name": "location",
                "type": "LOCATION"
            }
        ],
        "description": "Test points",
        "isExportable": "true"
    }

    service = build_service('fusiontables', 'v2')
    newtable = service.table().insert(body=fusion_columns)
    response = newtable.execute()
    print(response)
    table = FusionTable.objects.create(table_id=response['tableId'])

    drive_service = build_service('drive', 'v3', 'https://www.googleapis.com/auth/drive')
    batch = drive_service.new_batch_http_request()
    user_permission = {
        'value': 'default',
        'type': 'anyone',
        'role': 'reader'
    }
    batch.add(drive_service.permissions().create(
        fileId=response['tableId'],
        body=user_permission,
        fields='id'))
    res = batch.execute()
    return table


def query_fusion_table(query):
    """
    :param query: a SQL query to run against googlefusion table

    :return: dict with the G Api's response structure

    run a query agains googlefusion table
    """
    service = build_service('fusiontables', 'v2')
    response = service.query().sql(sql=query)
    response = response.execute()
    return response


def add_point(data):
    """
    :param data: dict containing lat, lon and address in order to store
                 the data into de database
    :return: core.models.Address instance

    creates a new record in the database storing a new address and its
    coordinates
    """
    lat = data.get('lat')
    lon = data.get('lon')
    address, _ = Address.objects.get_or_create(
        lat=lat, lon=lon, address=data.get('address'))
    fusion_table = FusionTable.objects.first()
    if not fusion_table:
        fusion_table = create_fusion_table()

    verify_data = query_fusion_table(
        f'''
        select * from {fusion_table.table_id} where location='{lat},{lon}'
        '''
    )
    if 'rows' not in verify_data:
        insert = query_fusion_table(
            f'''
            insert into {fusion_table.table_id} (location) VALUES ('{lat},{lon}')
            ''')

    return address


def get_fusion_key():
    """
    :return: str object containing a googlefussion's table id

    retrieves the id of the googlefusion table if exists or creates a new one
    """
    fusion_table = FusionTable.objects.first()
    if not fusion_table:
        fusion_table = create_fusion_table()
    return fusion_table.table_id
