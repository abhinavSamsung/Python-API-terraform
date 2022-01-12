from python_terraform import *

class AWSTerraform(object):
    
    def __init__(self, aws_credential_file):
        # terraform file path.
        self.filepath = aws_credential_file
        self.tf = Terraform(working_dir= self.filepath)

    def create(self, show_error:bool=False):
        create_output = {}
        try:
            # terraform init
            self.tf.init(capture_output=False)

            # terraform destroy
            self.tf.destroy(auto_approve=True, force=IsNotFlagged, capture_output=False)
        
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
                create_output["code"] = 204

            return create_output
        except Exception as e:
            create_output["success"] = 'Some Error Occured.'
            create_output["message"] = e
            create_output["code"] = 400
            return create_output
           

    def modify(self, tf_variables:dict, show_error:bool=False):
        try:
            create_output = {}
            tf_var = {}
            ec2_region = tf_variables['ec2_region'] if 'ec2_region' in tf_variables else 'us-east-1'
            ec2_image = tf_variables['ec2_image'] if 'ec2_image' in tf_variables else 'ami-0ff8a91507f77f867'
            ec2_instance_type = tf_variables['ec2_instance_type'] if 'ec2_instance_type' in tf_variables else 't3.micro'
            ec2_count = tf_variables['ec2_count'] if 'ec2_count'  in tf_variables else 1
            if ec2_count > 1:
                ec2_count = 1

            tf_var = {"ec2_region": ec2_region, "ec2_image": ec2_image, "ec2_instance_type": ec2_instance_type,
                    "ec2_count":ec2_count}
            
            # terraform init
            self.tf.init(capture_output=False)
            
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
                create_output["code"] = 204

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
                create_output["message"] = 'Intialize the EC2 instance.'
                create_output["code"] = 200
            if len(stderror) > 50:   
                create_output["success"] = False
                create_output["message"] = 'Error'
                create_output["code"] = 204

            return create_output
        except Exception as e:
            create_output["success"] = 'Some Error Occured.'
            create_output["message"] = e
            create_output["code"] = 400
            return create_output

    def get_output(self, ip_type='public'):
        # terraform init 
        self.tf.init()
        create_output = {}
        # terraform output
        try:
            output_json = self.tf.output()
            if ip_type == 'private':
                create_output["success"] = True
                create_output["message"] = output_json['instance_ip_addr']['value']
                create_output["code"] = 200
                
            elif ip_type == 'public':
                create_output["success"] = True
                create_output["message"] = output_json['instance_ips']['value']
                create_output["code"] = 200
            
            return create_output

        except Exception as e:
            create_output["success"] = True
            create_output["message"] = output_json['instance_ips']['value']
            create_output["code"] = 200
            
            return create_output

    def get_output_watch(self, keys:dict):
        # terraform init 
        self.tf.init()
        create_output = {}
        ip_type = keys["ip_type"]
        #mac_address = keys["mac_address"]
        dns_name = keys["dns_name"]
        # terraform output
        try:
            output_json = self.tf.output()
            print(output_json)
            if ip_type == 'private':
                create_output["success"] = True
                create_output["message"] = output_json['instance_ip_addr']['value']
                create_output["code"] = 200
                
            elif ip_type == 'public':
                create_output["success"] = True
                create_output["message"] = output_json['instance_ips']['value']
                create_output["code"] = 200

            if "dns_name" in keys:
                create_output["dns_name"] = output_json["addresses"]["value"]

            # elif mac_address == keys["mac_address"]:
            #     create_output["mac"] = output_json["addresses"]["value"]

            print(create_output)
            return create_output

        except Exception as e:
            create_output["success"] = True
            create_output["message"] = output_json['instance_ips']['value']
            create_output["code"] = 200
            
            return create_output        