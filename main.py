from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse, HTMLResponse
from typing import Optional

from drive.drive import PostFile, GetFileList, GetFile
import glob
import os

app = FastAPI()

# Cleans up tmp files from the filesystem
def cleanup():
    try:
        temps = glob.glob('*tmp*')
        for i in range(len(temps)):
            os.remove(temps[i])
    except:
        pass    

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
    <!doctype html>

    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>Api index</title>
        <meta name="description" content="Akatsuki Api">
        <meta name="author" content="Suraj">
        <style>
            *, *:before, *:after {
                -moz-box-sizing: border-box;
                -webkit-box-sizing: border-box;
                box-sizing: border-box;
            }

            body {
                font-family: Arial, sans-serif;
                color: #384047;
            }

            table {
                max-width: 960px;
                margin: 10px auto;
            }

            caption {
                font-size: 1.6em;
                font-weight: 400;
                padding: 10px 0;
            }

            thead th {
                font-weight: 400;
                background: #8a97a0;
                color: #FFF;
            }

            tr {
                background: #f4f7f8;
                border-bottom: 1px solid #FFF;
                margin-bottom: 5px;
            }

            tr:nth-child(even) {
                background: #e8eeef;
            }
            ul {
                list-style-type: none;
                margin: 0;
                padding: 0;
                overflow: hidden;
            }

            li {
                float: left;
            }

            li a {
                display: block;
                text-align: center;
                padding: 14px 16px;
                text-decoration: none;
            }
            li p {
                text-align: center;
                padding-left: 14px;
                text-decoration: none;
            }

            li a:hover:not(.active) {
                background-color: #ADD8E6;
            }

            .active {
                background-color: #04AA6D;
            }
        </style>
    </head>
    <body>
        <header style="text-align: center;">
            <h1>Akatsuki Api</h1>
        </header>    
        <table>
        <thead>    
            <tr>
                <th>Endpoint</th>
                <th>Description</th>
                <th>Example</th>
            </tr>    
        </thead>
        </tr>
        <tbody>
            <tr>
                <th scope="row">'/uploadfile/parent/?description=<some_desc>/'</th>    
                <td>POST: Send post request with queries equal to parent folder (in which to upload to) and <b>optional</b> description to add along</td>
                <td>http://localhost:8000/uploadfile/parent/suraj/?description=test</td>
            </tr>  
            <tr>
                <th scope="row">'/getfilelist/parent/'</th>    
                <td>GET: Get a list of files in a specified parent folder</td>
                <td>http://localhost:8000/getfilelist/piyush</td>
            </tr> 
            <tr>
                <th scope="row">'/getfile/parent/title'</th>    
                <td>GET: Get file of specified name and inside given parent folder</td>
                <td>http://localhost:8000/getfile/piyush/failure.png</td>
            </tr>   
        </tbody>  
        <ul>
            <li><p>API Docs ➡</p></li>
            <li style="float:right"><a href="https://mylightningstrikeshard.herokuapp.com/redoc">Openapi Docs</a></li> 
            <li style="float:right"><a href="https://mylightningstrikeshard.herokuapp.com/docs">Swagger Docs</a></li>
    </body>
    </html>
    """

@app.post("/uploadfile/{parent}")
async def create_upload_file(*, file: UploadFile = File(...), parent: str, description: Optional[str] = None, background_tasks: BackgroundTasks):
    contents = await file.read()
    PostFile(contents,file.filename,description,parent)
    background_tasks.add_task(cleanup)
    return {"status": "uploaded ok"}

@app.get("/getfilelist/{parent}")
async def get_file_list(parent: str):
    file_list = GetFileList(parent)
    if file_list is None:
        raise HTTPException(status_code=404, detail="Requested folder not found (bad query)")
    return {'parent': parent, 'files': [file_list]}

@app.get('/getfile/{parent}/{title}')
async def get_file(parent: str, title: str, background_tasks: BackgroundTasks):
    tmp_file_path = GetFile(parent,title)
    background_tasks.add_task(cleanup)
    if tmp_file_path is None:
        raise HTTPException(status_code=404, detail="Requested file/folder not found (bad query)")
    return FileResponse(tmp_file_path)