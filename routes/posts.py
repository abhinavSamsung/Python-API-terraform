from fastapi import APIRouter, Body, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from controller.actions import create_credentials_file, create, modify_terrform, destroy_ec2, output_ip, output_watch
from models.post import AwsKeys, ModifyKeys, CreateKeys, ResponseModel
from config import requestvars
from typing import Optional, List
import datetime
import time

# g is the global
g = requestvars.g()
router = APIRouter()
date_time_format = '%Y%m%dT%H%M%SZ'
date_time_log_file = f"output-{datetime.datetime.utcfromtimestamp(time.time()).strftime(date_time_format)}.log"


@router.post("/user_creation/", response_description="User Access key and secret Initializing.")
async def user_initialize(post: AwsKeys = Body(...)):
    post = jsonable_encoder(post)
    create_credentials = create_credentials_file
    pass


@router.post("/create", response_description="Initialize Terraform and create 0 ec2 instances.")
async def intialize_terraform(post: CreateKeys = Body(...)):
    """
    :param post: show_error:bool, create:dict
    :return: JSON Response with message
    """
    request_dict = jsonable_encoder(post)
    create_dict = dict()
    if request_dict['create'] is None:
        request_dict.pop('create', None)
    if 'create' in request_dict.keys() and len(request_dict["create"]) == 0:
        result = {"message": "Key 'Create' is empty.", "code":200, "success": False}
    else:
        for keys, item in request_dict.items():
            g.req_log[keys] = item
        result = create(default_create=create_dict, show_error=post.show_error)
    g.req_log["API"] = 'Create'
    g.req_log['logFile'] = date_time_log_file
    g.req_log["success"], g.req_log["message"], g.req_log["code"] = result["success"], str(result["message"]), result["code"]
    return JSONResponse(status_code=result["code"],
                        content=ResponseModel(str(result["success"]), str(result["message"]), result["code"], 
                                              'Initialize', g.req_log['logFile']))


@router.post("/apply", response_description="Terraform apply and create 1 ec2 instances.")
async def modify(ec2_keys: ModifyKeys = Body(...)):
    """
    :param ec2_keys: dict by user that contains the variables to modify in the terraform file.
    :return: JSON response
    """
    ec2_keys = jsonable_encoder(ec2_keys)
    for keys, item in ec2_keys.items():
        g.req_log[keys] = item
    result = modify_terrform(ec2_keys)
    g.req_log["API"] = 'Apply'
    g.req_log['logFile'] = date_time_log_file
    g.req_log["success"], g.req_log["message"], g.req_log["code"] = result["success"], result["message"], result["code"]
    return JSONResponse(status_code=result["code"],
                        content=ResponseModel(str(result["success"]), str(result["message"]), result["code"],
                                              'Apply', g.req_log['logFile']))


@router.post("/destroy", response_description="destroy all ec2 instances.")
async def destroy_terraform():
    result = destroy_ec2()
    g.req_log["API"] = 'Destroy'
    g.req_log['logFile'] = date_time_log_file
    g.req_log["success"], g.req_log["message"], g.req_log["code"] = result["success"], result["message"], result["code"]
    return JSONResponse(status_code=result["code"],
                        content=ResponseModel(result["success"], result["message"], result["code"],
                                              'Destroy', g.req_log['logFile']))


@router.get("/output/{ip_type}", response_description="Give the IP Address of ec2 instances")
async def output_ip_address(ip_type: Optional[str]):
    """
    :param ip_type: by user[optional] private or public[default]
    :return: JSON Response
    """
    if ip_type == 'public' or ip_type == 'private':
        ip_type = ip_type
        g.req_log['ip_type'] = ip_type
    else:
        ip_type = 'public'
    g.req_log["API"] = 'Output'
    result = output_ip(ip_type=ip_type)
    g.req_log['logFile'] = date_time_log_file
    g.req_log["success"], g.req_log["message"], g.req_log["code"] = result["success"], result["message"], result["code"]
    return JSONResponse(status_code=result["code"],
                        content=ResponseModel(result["success"], result["message"], result["code"],
                                              'Output', g.req_log['logFile']))

@router.get("/watcher", response_description="Give Output according to the user input dictionary.")
async def watcher(q: Optional[List[str]] = Query(None)):
    """
    :param q: By User according to the output user wants to get from terraform file.
    :return: JSON Response
    """
    if len(q) == 0:
        return JSONResponse(status_code=400, content="No Parameter.")
    g.req_log['watch_list'] = q
    g.req_log["API"] = 'Watcher'
    result = output_watch(input_list=q)
    g.req_log['logFile'] = date_time_log_file
    g.req_log["success"], g.req_log["message"], g.req_log["code"] = result["success"], result["message"], result["code"]
    return JSONResponse(status_code=result["code"],
                        content=ResponseModel(result["success"], result["message"], result["code"],
                                              'Output', g.req_log['logFile']))

