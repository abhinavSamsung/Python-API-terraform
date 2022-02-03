from fastapi import FastAPI, Request
from config import requestvars
import types
from starlette.responses import Response
from fastapi.responses import JSONResponse
import random, string
import time
from routes.posts import router as PostRouter
import uvicorn
import requests
import subprocess
import json
import os
import platform

api_version = '1.0.0'  # API version
app = FastAPI()
g = requestvars.g()  # global Namespace
CWD = os.getcwd()
OS_NAME = platform.system()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    # start time
    start_time = time.time()
    initial_g = types.SimpleNamespace()
    requestvars.request_global.set(initial_g)
    # generate unique id
    g.uid = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    g.req_log = dict([('uid', g.uid)])
    g.req_log['logTimestamp'], g.req_log['host'], g.req_log["user-agent"], \
    g.req_log["accept"], g.req_log["accept-encoding"], g.req_log["connection"], g.req_log["content-length"] = \
        start_time, request.headers.get("host"), request.headers.get("user-agent"), \
        request.headers.get("accept"), request.headers.get("accept-encoding"), \
        request.headers.get("connection"), request.headers.get("content-length")
    try:
        response = await call_next(request)  # Get the Response
        process_time = time.time() - start_time
        g.req_log["process_time"] = process_time
        response.headers["X-Process-Time"] = str(process_time)
        g.req_log['apiVersion'] = api_version
        payload = json.dumps({"json_obj": g.req_log})
        headers = {'Content-Type': 'application/json'}
        try:
            # Logging Results from API
            requests.request("POST", url="http://127.0.0.1:23412/logAggregator", headers=headers, data=payload)
        except requests.exceptions.ConnectionError:
            # If Logging API not started.
            subprocess.Popen('python LogAggregator.py', shell=True)  # start logAggregator
            time.sleep(1)
            requests.request("POST", url="http://127.0.0.1:23412/logAggregator", headers=headers, data=payload)
        # Renaming the output.log
        if OS_NAME == 'Windows':
            filepath = f"{CWD}\logs\output.log"
            log_directory_path = f"{CWD}\logs\\"
        else:
            filepath = f"{CWD}/logs/output.log"
            log_directory_path = f"{CWD}/logs/"

        if os.path.exists(filepath):
            new_fileName = g.req_log['logFile']
            old_file = os.path.join(f"{log_directory_path}", f"output.log")
            new_file = os.path.join(f"{log_directory_path}", new_fileName)
            try:
                # open both files
                with open(old_file,'r') as firstfile, open(new_file,'a') as secondfile:
                    for line in firstfile:
                        secondfile.write(line)
                firstfile.close()
                #os.remove(old_file)
            except Exception as err:
                print('Error in copying from one file to another.', err)

        return response
    except (IndexError, Exception) as err:
        g.req_log['errorLog'] = f"{type(err)}"
        process_time = time.time() - start_time
        g.req_log["process_time"] = process_time
        g.req_log['apiVersion'] = api_version
        payload = json.dumps({"json_obj": g.req_log})
        headers = {'Content-Type': 'application/json'}
        try:
            # Logging Results from API
            requests.request("POST", url="http://127.0.0.1:23412/logAggregator", headers=headers, data=payload)
        except requests.exceptions.ConnectionError:
            # If Logging API not started.
            subprocess.Popen('python LogAggregator.py', shell=True)  # start logAggregator
            time.sleep(1)
            requests.request("POST", url="http://127.0.0.1:23412/logAggregator", headers=headers, data=payload)
        return JSONResponse(status_code=500, content='Unable to process')


@app.get('/', tags=["Root"])
async def read_root(request: Request, response: Response):
    return {"message": "Welcome to the"}


app.include_router(PostRouter, tags=["TerraformApp"], prefix="/terraform-app")

if __name__ == '__main__':
    uvicorn.run("app:app", reload=True, debug=True, workers=3)