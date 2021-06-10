# Akatsuki Archive API
The goal of this project was to create a simple api layer between a shared google drive account and multiple applications needing a way to read/write resources to that drive account.

## Libraries used
1. [Fastapi](https://github.com/tiangolo/fastapi)
2. [Pydrive2](https://github.com/iterative/PyDrive2)
 
## Building on your own
- Follow pydrive2's quicstart [instructions](https://iterative.github.io/PyDrive2/docs/build/html/quickstart.html)
- Get your credentials.json, put it in the root directory
- Authenticate using browser when using for the first time
- Create Folders titled after your friends (or whatever categories you want)
- Try out on local server using uvicorn
- If all goes well deploy to heroku by using the procfile provided