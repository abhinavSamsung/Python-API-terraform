from terraCOP.python_tf.terraform import Terraform, IsNotFlagged
import time

class AWSTerraform(object):

    def __init__(self, aws_credential_file):
        """
        :param aws_credential_file:path of ".tf" file
        """
        # terraform file path.
        self.filepath = aws_credential_file
        self.tf = Terraform(working_dir=self.filepath)
        self.watcher_dict = {"dns_name":"addresses", "public_ip": "instance_ips",
                             "private_ip": "instance_ip_addr", "mac_address": ""}

    def create(self, default_create: dict, show_error: bool = False):
        """
        :param default_create: dict by user (Optional)
        :param show_error: bool
        :return: dict with keys:- code, message, success.
        """
        create_output = {}
        method = ''
        if 'create' in default_create.keys() and len(default_create["create"]) > 0:
            method = 'Apply'
        try:
            # terraform init
            stdcode, stdout, stderror = self.tf.init(capture_output=True)
            if method == 'Apply':
                stdcode, stdout, stderror = self.tf.apply(lock=False, skip_plan=True, var=default_create, capture_output=True)
            else:
                # terraform apply
                stdcode, stdout, stderror = self.tf.apply(lock=False, skip_plan=True, capture_output=True)
            message = stderror if show_error is True else 'Error'
            if len(stdout) > 100:
                create_output["success"] = "True"
                create_output["message"] = 'Intialize the EC2 instance.'
                create_output["code"] = 200
            else:
                create_output["success"] = "True"
                create_output["message"] = 'Intialize already done'
                create_output["code"] = 200

            if len(stderror) > 50:
                create_output["success"] = "False"
                create_output["message"] = message
                create_output["code"] = 400

            return create_output
        except Exception as e:
            create_output["success"] = 'False'
            create_output["message"] = e
            create_output["code"] = 400
            return create_output

    def modify(self, tf_variables: dict, show_error: bool = False):
        """
        :param tf_variables: dict by user that contains the variables to apply in the terraform file.
        :param show_error: bool
        :return: dict with keys:- code, message, success.
        """
        create_output = {}
        try:
            # terraform init
            stdcode, stdout, stderror = self.tf.init(capture_output=True)
            # terraform apply
            stdcode, stdout, stderror = self.tf.apply(lock=False, skip_plan=True, var=tf_variables, capture_output=True)
            message = stderror if show_error is True else 'Error'
            if len(stdout) > 100:
                create_output["success"] = "True"
                create_output["message"] = 'Applied the requirements.'
                create_output["code"] = 200
            else:
                create_output["success"] = "True"
                create_output["message"] = 'Intialize already done'
                create_output["code"] = 200

            if len(stderror) > 50:
                create_output["success"] = "False"
                create_output["message"] = message
                create_output["code"] = 400

            return create_output
        except Exception as e:
            create_output["success"] = 'Some Error Occured.'
            create_output["message"] = e
            create_output["code"] = 400
            return create_output

    def destroy(self):
        """
        :return: dict with keys:- code, message, success.
        """
        create_output = {}
        # terraform init
        self.tf.init()
        # terraform destroy
        try:
            stdcode, stdout, stderror = self.tf.destroy(auto_approve=True, force=IsNotFlagged)
            if len(stdout) > 100:
                create_output["success"] = "True"
                create_output["message"] = "Destroyed the EC2 instance."
                create_output["code"] = 200
            else:
                create_output["success"] = "True"
                create_output["message"] = 'There are no instances.'
                create_output["code"] = 200

            if len(stderror) > 50:
                create_output["success"] = "False"
                create_output["message"] = 'Error'
                create_output["code"] = 400


            return create_output
        except Exception as e:
            create_output["success"] = 'Some Error Occured.'
            create_output["message"] = str(e)
            create_output["code"] = 400
            return create_output

    def get_output(self, ip_type='public'):
        """
        :param ip_type: by user[optional] private or public[default]
        :return: dict with keys:- code, message:{}, success.
        """
        # terraform init 
        self.tf.init()
        create_output = {"message":{}}
        # terraform output
        try:
            output_json = self.tf.output()
            if ip_type == 'private':
                create_output["success"] = True
                create_output["message"]["private"] = output_json['instance_ip_addr']['value']

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
        """
        :param output_list: By User according to the output user wants to get from terraform file.
        :return: dict with keys:- code, message:{}, success.
        """
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
