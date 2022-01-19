from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from controller.actions import create_credentials_file, create, modify_terrform, destroy_ec2, output_ip, output_watch
from models.post import AwsKeys, ModifyKeys, CreateKeys, ResponseModel, OutputType, OutputTypeDict
from config import requestvars

g = requestvars.g()

router = APIRouter()


@router.post("/user_creation/", response_description="User Access key and secret Initializing.")
async def user_initialize(post: AwsKeys = Body(...)):
    post = jsonable_encoder(post)
    create_credentials = create_credentials_file


@router.post("/create", response_description="Initialize Terraform and create 0 ec2 instances.")
async def intialize_terraform(post: CreateKeys = Body(...)):
    request_dict = jsonable_encoder(post)
    for keys, item in request_dict.items():
        g.req_log[keys] = item
    g.req_log["API"] = 'Create'
    result = create(show_error=post.show_error)
    g.req_log["success"], g.req_log["message"], g.req_log["code"] = result["success"], result["message"], result["code"]
    return JSONResponse(status_code=result["code"],
                        content=ResponseModel(result["success"], result["message"], result["code"], 'Initializing'))


@router.post("/apply", response_description="Terraform apply and create 1 ec2 instances.")
async def modify(ec2_keys: ModifyKeys = Body(...)):
    ec2_keys = jsonable_encoder(ec2_keys)
    for keys, item in ec2_keys.items():
        g.req_log[keys] = item
    g.req_log["API"] = 'Apply'
    result = modify_terrform(ec2_keys)
    g.req_log["success"], g.req_log["message"], g.req_log["code"] = result["success"], result["message"], result["code"]
    return JSONResponse(status_code=result["code"],
                        content=ResponseModel(result["success"], result["message"], result["code"], 'Apply'))


@router.post("/destroy", response_description="destroy all ec2 instances.")
async def destroy_terraform():
    g.req_log["API"] = 'Destroy'
    result = destroy_ec2()
    g.req_log["success"], g.req_log["message"], g.req_log["code"] = result["success"], result["message"], result["code"]
    return JSONResponse(status_code=result["code"],
                        content=ResponseModel(result["success"], result["message"], result["code"], 'Destroy'))


@router.post("/output", response_description="Give the IP Address of ec2 instances")
async def output_ip_address(address: OutputType = Body(...)):
    g.req_log['ip_type'] = address.ip_type
    g.req_log["API"] = 'Output'
    result = output_ip(ip_type=address.ip_type)
    g.req_log["success"], g.req_log["message"], g.req_log["code"] = result["success"], result["message"], result["code"]
    return JSONResponse(status_code=result["code"],
                        content=ResponseModel(result["success"], result["message"], result["code"], 'Output'))


@router.post("/watcher", response_description="Give Output according to the user input dictionary.")
async def watcher(keys: OutputTypeDict = Body(...)):
    watch_keys = jsonable_encoder(keys)
    for keys, item in watch_keys.items():
        g.req_log[keys] = item
    g.req_log["API"] = 'Watcher'
    result = output_watch(input_dict=keys)
    g.req_log["success"], g.req_log["message"], g.req_log["code"] = result["success"], result["message"], result["code"]
    return JSONResponse(status_code=result["code"],
                        content=ResponseModel(result["success"], result["message"], result["code"], 'Output'))
