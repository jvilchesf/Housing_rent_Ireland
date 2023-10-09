import mimetypes

from googleapiclient.http import MediaFileUpload
from Modules import google_apis
import os

def ExportDataGoogle2():

    currentPath = os.getcwd()
    client_file = 'sources/portfolio-project-401115-307078c5ca86.json'
    API_NAME = 'drive'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service = google_apis.create_service(client_file, API_NAME, API_VERSION, SCOPES)

    file_name = 'data_cso_ie_rent_out.csv'
    parent_folder_id = '1i_3t_r_wh31VNQ46t6uiM-wbP0nl4CH8'
    starred = 'TRUE'
    file_path = currentPath + '/output/data_cso_ie_rent_out.csv'

    mime_type, _ = mimetypes.guess_type(file_path)
    media_content = MediaFileUpload(file_path)

    request_body = {
        'name': file_name,
        'starred': starred
    }
    if parent_folder_id:
        request_body['parents'] = [parent_folder_id]
    print('Uploading File')

    service.files().create(
        body=request_body,
        media_body=media_content
    ).execute()

    return (1)

