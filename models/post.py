from typing import Optional, List
from pydantic import BaseModel
import datetime

class AwsKeys(BaseModel):
    aws_access_key_id: Optional[str]
    aws_secret_aceess_key: Optional[str]
    user_name: Optional[str]


class CreateKeys(BaseModel):
    show_error: Optional[bool]
    create: Optional[dict]


class ModifyKeys(BaseModel):
    show_error: Optional[bool]
    modify: dict

class OutputType(BaseModel):
    publicIP: Optional[str]
    privateIP: Optional[str]


class OutputTypeDict(BaseModel):
    ip_type: Optional[str]
    mac_address: Optional[str]
    dns_name: Optional[str]


def ResponseModel(result, message, code, operational, logFile):
    return {
        "Success": result,
        "message": message,
        "code": code,
        "operational": operational,
        "logFile": logFile
    }


def DateTimeLogfileName(current_time):
    date_time_format = '%Y%m%dT%H%M%SZ'
    date_time_log_file = f"output-{datetime.datetime.utcfromtimestamp(current_time).strftime(date_time_format)}.log"
    return date_time_log_file