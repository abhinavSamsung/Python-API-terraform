from fastapi import FastAPI
import platform
import os
from typing import Optional
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

CFP = os.getcwd()
OS_NAME = platform.system()

if OS_NAME == 'Windows':
    log_directory_path = f'{CFP}\logs'
else:
    log_directory_path = f'{CFP}/logs'

if not os.path.exists(log_directory_path):
    os.mkdir(log_directory_path)


def read_logfile(logFile:str):
    fileName = logFile
    if OS_NAME == 'Windows':
        filepath = f"{log_directory_path}\\{fileName}"
    else:
        filepath = f"{log_directory_path}/{fileName}"

    if not os.path.exists(filepath):
        return {"Output":'File does not exist'}, 400
    outputFile = open(filepath, 'r')
    logList = []
    for line in outputFile:
        line = line.replace('\\n','').rstrip()
        if len(line) != 2:
            logList.append(line.replace("'",'').rstrip())
    outputFile.close()
    return_dict = {"Output":logList}
    return return_dict, 200

@app.get("/output/log/{logFile}",response_description="Read output.log file and show in response body")
async def output_log(logFile: Optional[str]):
    if '.log' in logFile:
        logFile = logFile
    else:
        logFile = 'output.log'
    result, code = read_logfile(logFile= logFile)
    return JSONResponse(content=result, status_code=code)

if __name__ == '__main__':
    uvicorn.run("output:app", host="0.0.0.0", port=23678)
