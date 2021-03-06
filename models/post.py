from typing import Optional
from pydantic import BaseModel
import datetime
import requests
import os, platform

class AwsKeys(BaseModel):
    aws_access_key_id: Optional[str]
    aws_secret_aceess_key: Optional[str]
    user_name: Optional[str]


class CreateKeys(BaseModel):
    show_error: Optional[bool]
    create: Optional[dict]
    userId: str
    clusterId: str


class ModifyKeys(BaseModel):
    show_error: Optional[bool]
    modify: dict
    userId: str
    clusterId: str

class DestroyUsers(BaseModel):
    userId : str
    clusterId: str

class OutputType(BaseModel):
    publicIP: Optional[str]
    privateIP: Optional[str]


class OutputTypeDict(BaseModel):
    ip_type: Optional[str]
    mac_address: Optional[str]
    dns_name: Optional[str]


def ResponseModel(result, message, code, operational, logFile):
    """
    :param result: result by terraform API.
    :param message: message of API
    :param code: API Response code
    :param operational: Type of API
    :param logFile: output log file
    :return: JSON Response
    """
    return {
        "Success": result,
        "message": message,
        "code": code,
        "operational": operational,
        "logFile": logFile
    }

def clusterFilePath(userId:str, clusterId):
    try:
        headers = {'Content-Type': 'application/json'}
        payload = {}
        result = requests.request("GET", url=f"http://127.0.0.1:8000/user/{userId}/cluster?clusterId={clusterId}",
                                  headers=headers, data=payload).json()
        filepath = result["message"][0]['filePath']
        if len(result['message']) == 0:
            return 'cluster not exist.', 400
        if os.path.exists(filepath):
            return result["message"][0]['filePath'], 200
        else:
            return f"Filepath of given user {userId} does not exist.", 400

    except Exception as err:
        return 'cluster not exist.', 400


def DateTimeLogfileName(current_time):
    date_time_format = '%Y%m%dT%H%M%SZ'
    date_time_log_file = f"output-{datetime.datetime.utcfromtimestamp(current_time).strftime(date_time_format)}.log"
    return date_time_log_file