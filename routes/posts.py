from time import sleep
from fastapi import APIRouter, Body, Response
from fastapi.encoders import jsonable_encoder
from typing import KeysView, Optional
from controller.actions import create_credentials_file, create, modify_terrform, destroy_ec2, output_ip, output_watch
from models.post import AwsKeys, ModifyKeys, CreateKeys, ResponseModel, OutputType, OutputTypeDict
import time

router = APIRouter()

@router.post("/user_creation/", response_description ="User Access key and secret Initializing.")
async def user_initialize(post: AwsKeys = Body(...)):
    post = jsonable_encoder(post)
    create_credentials = create_credentials_file


@router.post("/create")
async def intialize_terraform(post: CreateKeys = Body(...)):
    result = create(show_error=post.show_error)
    return ResponseModel(result["success"], result["message"], result["code"], 'Initializing')

@router.post("/apply")
async def modify(ec2_keys: ModifyKeys = Body(...)): 
    ec2_keys = jsonable_encoder(ec2_keys) 
    result = modify_terrform(ec2_keys)
    return ResponseModel(result["success"], result["message"], result["code"], 'Apply')

@router.post("/destroy")
async def destroy_terraform():
    result = destroy_ec2()
    return ResponseModel(result["success"], result["message"], result["code"], 'Destroy')

@router.post("/output")
async def output_ip_address(address: OutputType= Body(...)):
    result = output_ip(ip_type=address.ip_type)
    return ResponseModel(result["success"], result["message"], result["code"], 'Output')


@router.post("/watcher")
async def watcher(keys: OutputTypeDict= Body(...) ):
    keys = jsonable_encoder(keys)
    result = output_watch(input_dict = keys)
    return result

    