from typing import Optional, List
from pydantic import BaseModel
import time

class AwsKeys(BaseModel):
    aws_access_key_id: Optional[str]
    aws_secret_aceess_key: Optional[str]
    user_name: Optional[str]

class CreateKeys(BaseModel):
    show_error: Optional[bool]
    input_dict: Optional[dict]

class ModifyKeys(BaseModel):
    ec2_region: Optional[str]
    ec2_image: Optional[str]
    ec2_instance_type: Optional[str]
    ec2_count: Optional[int]
    show_error: Optional[bool]

class OutputType(BaseModel):
    ip_type: Optional[str]

class OutputTypeDict(BaseModel):
    ip_type: Optional[str]
    mac_address: Optional[str]
    dns_name: Optional[str]
    
def ResponseModel(result, message, code, operational):
    return {
        "Success": result,
        "message": message,
        "code": code,
        "operational": operational
    }   
