import mimetypes

from googleapiclient.http import MediaFileUpload
from Modules import google_apis
import os

def ExportDataGoogle(dfRent):
    # Set up credentials
    creds = service_account.Credentials.from_service_account_file(
        # 'sources/adept-presence-382819-26dcb4f3e4ea.json',
        'sources/client_secret_862476552574-h0aig0ke3sn3dh3hjmlh462qrhso9d1v.apps.googleusercontent.com.json',
        scopes=['https://www.googleapis.com/auth/drive']
    )

    # Create a Google Drive service
    drive_service = build('drive', 'v3', credentials=creds)

    # Set the file details
    currentPath = os.getcwd()
    file_name = 'data_cso_ie_rent_out.csv'  # Change this to your desired file name
    file_path = currentPath + '/output/data_cso_ie_rent_out.csv'  # Specify the path to your dataset file
    # Set the ID of the new parent folder where you want to upload the file
    new_parent_folder_id = '1i_3t_r_wh31VNQ46t6uiM-wbP0nl4CH8'

    # Upload the file
    media = MediaFileUpload(file_path, mimetype='application/octet-stream')
    request = drive_service.files().create(
        media_body=media,
        body={
            'name': file_name,
            'parents': [new_parent_folder_id]
        }
    )

    response = request.execute()
    print(f'File uploaded successfully! File ID: {response["id"]}')

    # Get the file's information
    file_id = response['id']
    file_info = drive_service.files().get(fileId=file_id, fields='parents').execute()

    # Check if the 'parents' field is present in the response
    if 'parents' in file_info:
        parent_folder_id = file_info['parents'][0]

        # Now you have the ID of the parent folder
        # You can use it to get more information about the folder if needed
        folder_info = drive_service.files().get(fileId=parent_folder_id).execute()
        folder_name = folder_info['name']

        print(f"The file '{file_name}' was uploaded to the folder '{folder_name}'.")
    else:
        print(f"The file '{file_name}' was uploaded, but its parent folder information is not available.")

    return (1)


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


def ExportDataGoogle3():
    currentPath = os.getcwd()
    # Set up a credentials object I think
    creds = ServiceAccountCredentials.from_json_keyfile_name('sources/portfolio-project-401115-28061c5f8795.json',
                                                             ['https://www.googleapis.com/auth/drive'])

    # Now build our api object, thing
    drive_api = build('drive', 'v3', credentials=creds)

    file_name = currentPath + '/output/data_cso_ie_rent_out.csv'
    print("Uploading file " + file_name + "...")

    # We have to make a request hash to tell the google API what we're giving it
    body = {'name': file_name, 'mimeType': 'application/vnd.google-apps.document'}

    # Now create the media file upload object and tell it what file to upload,
    # in this case 'test.html'
    media = MediaFileUpload(file_name, mimetype='text/csv')

    # Now we're doing the actual post, creating a new file of the uploaded type
    fiahl = drive_api.files().create(body=body, media_body=media).execute()

    # Because verbosity is nice
    print("Created file '%s' id '%s'." % (fiahl.get('name'), fiahl.get('id')))
    return (1)
