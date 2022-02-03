from fastapi import APIRouter, Body, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from controller.actions import create_credentials_file, create, modify_terrform, destroy_ec2, output_ip, output_watch
from models.post import AwsKeys, ModifyKeys, CreateKeys, ResponseModel
from config import requestvars
from typing import Optional, List
import datetime
import time

g = requestvars.g()
router = APIRouter()
date_time_format = '%Y%m%dT%H%M%SZ'

@router.post("/user_creation/", response_description="User Access key and secret Initializing.")
async def user_initialize(post: AwsKeys = Body(...)):
    post = jsonable_encoder(post)
    create_credentials = create_credentials_file


@router.post("/create", response_description="Initialize Terraform and create 0 ec2 instances.")
async def intialize_terraform(post: CreateKeys = Body(...)):
    request_dict = jsonable_encoder(post)
    create_dict = dict()
    if 'create' in request_dict:
        create_dict = request_dict["create"]
    for keys, item in request_dict.items():
        g.req_log[keys] = item
    g.req_log["API"] = 'Create'
    result = create(default_create=create_dict, show_error=post.show_error)
    g.req_log['logFile'] = f"output-{datetime.datetime.utcfromtimestamp(time.time()).strftime(date_time_format)}.log"
    g.req_log["success"], g.req_log["message"], g.req_log["code"] = result["success"], str(result["message"]), result["code"]
    return JSONResponse(status_code=result["code"],
                        content=ResponseModel(str(result["success"]), str(result["message"]), result["code"], 
                                              'Initializing', g.req_log['logFile']))


@router.post("/apply", response_description="Terraform apply and create 1 ec2 instances.")
async def modify(ec2_keys: ModifyKeys = Body(...)):
    ec2_keys = jsonable_encoder(ec2_keys)
    for keys, item in ec2_keys.items():
        g.req_log[keys] = item
    g.req_log["API"] = 'Apply'
    result = modify_terrform(ec2_keys)
    g.req_log['logFile'] = f"output-{datetime.datetime.utcfromtimestamp(time.time()).strftime(date_time_format)}.log"
    g.req_log["success"], g.req_log["message"], g.req_log["code"] = result["success"], result["message"], result["code"]
    return JSONResponse(status_code=result["code"],
                        content=ResponseModel(result["success"], result["message"], result["code"],
                                              'Apply', g.req_log['logFile']))


@router.post("/destroy", response_description="destroy all ec2 instances.")
async def destroy_terraform():
    g.req_log["API"] = 'Destroy'
    result = destroy_ec2()
    g.req_log['logFile'] = f"output-{datetime.datetime.utcfromtimestamp(time.time()).strftime(date_time_format)}.log"
    g.req_log["success"], g.req_log["message"], g.req_log["code"] = result["success"], result["message"], result["code"]
    return JSONResponse(status_code=result["code"],
                        content=ResponseModel(result["success"], result["message"], result["code"],
                                              'Destroy', g.req_log['logFile']))


@router.get("/output/{ip_type}", response_description="Give the IP Address of ec2 instances")
async def output_ip_address(ip_type: Optional[str]):
    if ip_type == 'public' or ip_type == 'private':
        ip_type = ip_type
        g.req_log['ip_type'] = ip_type
    else:
        ip_type = 'public'
    g.req_log["API"] = 'Output'
    result = output_ip(ip_type=ip_type)
    g.req_log['logFile'] = f"output-{datetime.datetime.utcfromtimestamp(time.time()).strftime(date_time_format)}.log"
    g.req_log["success"], g.req_log["message"], g.req_log["code"] = result["success"], result["message"], result["code"]
    return JSONResponse(status_code=result["code"],
                        content=ResponseModel(result["success"], result["message"], result["code"],
                                              'Output', g.req_log['logFile']))

@router.get("/watcher", response_description="Give Output according to the user input dictionary.")
async def watcher(q: Optional[List[str]] = Query(None)):
    if len(q) == 0:
        return JSONResponse(status_code=400, content="No Parameter.")
    g.req_log['watch_list'] = q
    g.req_log["API"] = 'Watcher'
    result = output_watch(input_list=q)
    g.req_log['logFile'] = f"output-{datetime.datetime.utcfromtimestamp(time.time()).strftime(date_time_format)}.log"
    g.req_log["success"], g.req_log["message"], g.req_log["code"] = result["success"], result["message"], result["code"]
    return JSONResponse(status_code=result["code"],
                        content=ResponseModel(result["success"], result["message"], result["code"],
                                              'Output', g.req_log['logFile']))

