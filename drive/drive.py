from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

import os
import tempfile

# Dummy Folder ids 
folders = {'abc':'1GmAY9OJg-w4agwvpUqAT-mJUhZnuO569',
'yxz':'1U3OoBO5vrPqEtXihn6yBi-Hk94Js8Dfg',
'xyz':'1UlU9dLGtsW0DoVYXzEvb1WPf9yC-88ty',
'cba':'1_mBodhS0QxyvyNuuGQE1jaJZt9obnm7'}
'''
(Get your folder ids by running the query "mimeType = 'application/vnd.google-apps.folder'")
then print out the id key of the result items
'''

# Authentication using local file
def auth():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("credentials.json")
    return GoogleDrive(gauth)

# Create GoogleDrive instance with authenticated GoogleAuth instance.
drive = auth()

def PostFile(contents,title,desc,par):
    cwd = os.getcwd()
    ext = '.' + title.split(".")[1] # Getting extension from uploaded file
    tmpf = tempfile.NamedTemporaryFile(mode='wb', delete=False, dir=cwd, suffix=ext) # Creating temporary file to supply to SetContentFile
    with open(tmpf.name, 'wb') as f:
        f.write(contents) 
    tmpf.close()
    file1 = drive.CreateFile({"title": title, 'description':desc, "parents": [{"id": folders[par]}]})
    # Read file and set it as a content of this instance.
    file1.SetContentFile(tmpf.name) 
    file1.Upload() # Upload the file.

def GetFileList(parent):
    files_dict = {}
    try:
        folder_id_query = drive.ListFile({'q': f"title = '{parent}' and mimeType = 'application/vnd.google-apps.folder'"}).GetList()
        folder_id = folder_id_query[0]['id'] 
        file_list = drive.ListFile({'q': "'" + folder_id + "' in parents" + " and trashed=false"}).GetList()
        for file1 in file_list:
            files_dict[file1['title']] = file1['id']
        return files_dict
    except IndexError as e:
        return None

def GetFile(parent,title):
    try:
        folder_id_query = drive.ListFile({'q': f"title = '{parent}' and mimeType = 'application/vnd.google-apps.folder'"}).GetList()
        folder_id = folder_id_query[0]['id']
        file_query = drive.ListFile({'q': f"title contains '{title}' and " + "'" + folder_id + "' in parents" + " and trashed=false"}).GetList()
        file_id = file_query[0]['id']
        file_name = file_query[0]['title']
        tmp_file_name = 'tmp' + file_name
        downloaded = drive.CreateFile({'id': file_id})
        downloaded.GetContentFile(tmp_file_name)
        return tmp_file_name
    except IndexError as e:
        return None        