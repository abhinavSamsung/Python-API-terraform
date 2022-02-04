import os
from terraCOP.terraCOP import AWSTerraform
import platform
import json

default_dict = {
    "ec2_count": 1,
    "ec2_image": "ami-0ff8a91507f77f867",
    "show_error": False,
    "ec2_instance_type": "t3.micro"
}

OS_NAME = platform.system()
terraform_dir = 'terraform'
pwd = os.getcwd()
if OS_NAME == 'Windows':
    tf = AWSTerraform(f"{pwd}/{terraform_dir}")
else:
    tf = AWSTerraform(f"{pwd}/{terraform_dir}")

def create_credentials_file(post):
    aws_access_key_id = post['aws_access_key_id']
    aws_secret_access_key = post['aws_secret_aceess_key']
    user_name = post['user_name']
    pass


def create(default_create:dict, show_error:bool=False):
    """
    :param default_create: Optional dict
    :param show_error: bool True or False
   :return: dict terrCop output
    """
    if default_create is None:
        default_create = {}
    output = tf.create(default_create=default_create, show_error=show_error)
    return output


def modify_terrform(ec2_keys: dict = default_dict, show_error: bool = False):
    if 'show_error' in ec2_keys:
        show_error = ec2_keys["show_error"]
        del ec2_keys["show_error"]
    else:
        show_error = False
    output = tf.modify(tf_variables=ec2_keys, show_error=show_error)
    return output


def destroy_ec2():
    output = tf.destroy()
    return output


def output_ip(ip_type: str = 'public'):
    output = tf.get_output(ip_type=ip_type)
    return output


def output_watch(input_list: list):
    output = tf.get_output_watch(input_list)
    return output