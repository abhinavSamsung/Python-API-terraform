from fastapi import FastAPI
import platform
import os
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import uvicorn
import datetime as dt
import json
import time


class Item(BaseModel):
    json_obj: dict


app = FastAPI()

date_time_format = '%Y%m%dT%H%M%SZ'
log_list, last_write = list(), 0
CFP = os.getcwd()
OS_NAME = platform.system()

if OS_NAME == 'Windows':
    filepath = f'{CFP}\logs\TerraformAPILogs.txt'
    log_directory_path = f'{CFP}\logs'
else:
    filepath = f'{CFP}/logs/TerraformAPILogs.txt'
    log_directory_path = f'{CFP}/logs'

if not os.path.exists(log_directory_path):
    os.mkdir(log_directory_path)
if not os.path.exists(filepath):
    f1 = open(filepath, 'w+')
    f1.close()


@app.post('/logAggregator/')
def process_log(item: Item):
    try:
        global log_list, last_write
        json_data = jsonable_encoder(item)
        json_data['json_obj']['logTimestamp'] = dt.datetime.utcfromtimestamp(
            json_data['json_obj']['logTimestamp']).strftime(date_time_format)
        write_dict = dict({"rootMessage": json_data["json_obj"]})

        writable_log = f"{json_data['json_obj']['uid']}~~{json.dumps(write_dict)}\n"
        log_list.append(writable_log)

        if len(log_list) > 150 or time.time() - last_write > 10:
            write_data_log = open(filepath, 'a+')
            write_data_log.writelines(log_list)
            log_list, last_write = [], time.time()
            write_data_log.close()
            return ''
        else:
            log_list.append(writable_log)
    except KeyError as error:
        return ''


if __name__ == '__main__':
    uvicorn.run("LogAggregator:app", host="0.0.0.0", port=23412)
