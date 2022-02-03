from terraCOP.python_tf.terraform import Terraform, IsNotFlagged
import time

class AWSTerraform(object):

    def __init__(self, aws_credential_file):
        # terraform file path.
        self.filepath = aws_credential_file
        self.tf = Terraform(working_dir=self.filepath)
        self.watcher_dict = {"dns_name":"addresses", "public_ip": "instance_ips",
                             "private_ip": "instance_ip_addr", "mac_address": ""}

    def create(self, default_create: dict, show_error: bool = False):
        create_output = {}
        method = ''
        if 'ec2_image' and 'ec2_count' in default_create:
            method = 'Apply'
        try:
            # terraform init
            stdcode, stdout, stderror = self.tf.init(capture_output=True)
            if method == 'Apply':
                tf_variables = default_create
                ec2_region = tf_variables['ec2_region'] if 'ec2_region' in tf_variables else 'us-east-1'
                ec2_image = tf_variables['ec2_image'] if 'ec2_image' in tf_variables else 'ami-0ff8a91507f77f867'
                ec2_instance_type = tf_variables[
                    'ec2_instance_type'] if 'ec2_instance_type' in tf_variables else 't3.micro'
                ec2_count = tf_variables['ec2_count'] if 'ec2_count' in tf_variables else 1
                if ec2_count > 1:
                    ec2_count = 1
            
                tf_var = {"ec2_region": ec2_region, "ec2_image": ec2_image, "ec2_instance_type": ec2_instance_type,
                          "ec2_count": ec2_count}
                stdcode, stdout, stderror = self.tf.apply(lock=False, skip_plan=True, var=tf_var, capture_output=True)
            else:
                # terraform apply
                stdcode, stdout, stderror = self.tf.apply(lock=False, skip_plan=True, capture_output=True)
            message = stderror if show_error is True else 'Error'
            if len(stdout) > 100:
                create_output["success"] = True
                create_output["message"] = 'Intialize the EC2 instance.'
                create_output["code"] = 200
            if len(stderror) > 50:
                create_output["success"] = False
                create_output["message"] = message
                create_output["code"] = 400
            else:
                create_output["success"] = True
                create_output["message"] = 'Intialize already done'
                create_output["code"] = 200

            return create_output
        except Exception as e:
            create_output["success"] = 'Some Error Occured.'
            create_output["message"] = e
            create_output["code"] = 400
            return create_output

    def modify(self, tf_variables: dict, show_error: bool = False):
        create_output = {}
        try:
            ec2_region = tf_variables['ec2_region'] if 'ec2_region' in tf_variables else 'us-east-1'
            ec2_image = tf_variables['ec2_image'] if 'ec2_image' in tf_variables else 'ami-0ff8a91507f77f867'
            ec2_instance_type = tf_variables['ec2_instance_type'] if 'ec2_instance_type' in tf_variables else 't3.micro'
            ec2_count = tf_variables['ec2_count'] if 'ec2_count' in tf_variables else 1
            if ec2_count > 1:
                ec2_count = 1

            tf_var = {"ec2_region": ec2_region, "ec2_image": ec2_image, "ec2_instance_type": ec2_instance_type,
                      "ec2_count": ec2_count}

            # terraform init
            stdcode, stdout, stderror = self.tf.init(capture_output=True)

            # terraform apply
            stdcode, stdout, stderror = self.tf.apply(lock=False, skip_plan=True, var=tf_var, capture_output=True)
            message = stderror if show_error is True else 'Error'
            if len(stdout) > 100:
                create_output["success"] = True
                create_output["message"] = 'Applied the requirements.'
                create_output["code"] = 200
            if len(stderror) > 50:
                create_output["success"] = False
                create_output["message"] = message
                create_output["code"] = 400
            else:
                create_output["success"] = True
                create_output["message"] = 'Intialize already done'
                create_output["code"] = 200
            return create_output
        except Exception as e:
            create_output["success"] = 'Some Error Occured.'
            create_output["message"] = e
            create_output["code"] = 400
            return create_output

    def destroy(self):
        create_output = {}
        # terraform init
        self.tf.init()
        # terraform destroy
        try:
            stdcode, stdout, stderror = self.tf.destroy(auto_approve=True, force=IsNotFlagged)
            if len(stdout) > 100:
                create_output["success"] = True
                create_output["message"] = "Destroyed the EC2 instance."
                create_output["code"] = 200
            if len(stderror) > 50:
                create_output["success"] = False
                create_output["message"] = 'Error'
                create_output["code"] = 400
            else:
                create_output["success"] = True
                create_output["message"] = 'There are no instances.'
                create_output["code"] = 200


            return create_output
        except Exception as e:
            create_output["success"] = 'Some Error Occured.'
            create_output["message"] = str(e)
            create_output["code"] = 400
            return create_output

    def get_output(self, ip_type='public'):
        # terraform init 
        self.tf.init()
        create_output = {"message":{}}
        # terraform output
        try:
            output_json = self.tf.output()
            if ip_type == 'private':
                create_output["success"] = True
                create_output["message"]["private"] = output_json['instance_ip_addr']['value']
                create_output["code"] = 200

            elif ip_type == 'public':
                create_output["success"] = True
                create_output["message"]["public"] = output_json['instance_ips']['value']
                create_output["code"] = 200
            return create_output

        except Exception as e:
            create_output["success"] = False
            create_output["message"] = 'Error'
            create_output["code"] = 400

            return create_output

    def get_output_watch(self, output_list: list):
        # terraform init 
        self.tf.init()
        create_output = {"message": {}}
        keys = {}
        for each_item in output_list:
            keys[each_item] = self.watcher_dict[each_item]
        # terraform output
        try:
            output_json = self.tf.output()
            time.sleep(1)
            if 'public_ip' in keys:
                create_output["success"] = True
                create_output["message"]["public"] = output_json[keys['public_ip']]['value']

            if 'private_ip' in keys:
                create_output["success"] = True
                create_output["message"]["private"] = output_json[keys['private_ip']]['value']

            if "dns_name" in keys:
                create_output["message"]["dns_name"] = output_json[keys["dns_name"]]["value"]

            # if keys["mac_address"]:
            #     create_output["mac"] = output_json["addresses"]["value"]
            create_output["code"] = 200
            return create_output

        except Exception as e:
            create_output["success"] = False
            create_output["message"] = 'Error'
            create_output["code"] = 400

            return create_output
