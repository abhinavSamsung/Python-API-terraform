from terraCOP.terraCOP import AWSTerraform


class TerraCluster(object):
    def __init__(self, filepath) -> None:
        self.tf = AWSTerraform(f"{filepath}")

    def create_credentials_file(self,post):
        aws_access_key_id = post['aws_access_key_id']
        aws_secret_access_key = post['aws_secret_aceess_key']
        user_name = post['user_name']
        pass


    def create(self,default_create:dict, show_error:bool=False):
        """
        :param default_create: Optional dict
        :param show_error: bool True or False
       :return: dict from terrCop
        """
        if default_create is None:
            default_create = {}
        output = self.tf.create(default_create=default_create, show_error=show_error)
        return output


    def modify_terrform(self,ec2_keys: dict):
        """
        :param ec2_keys: dict by user that contains the variables to modify in the terraform file.
        :param show_error: bool
        :return: dict from terraCOP
        """
        if 'show_error' in ec2_keys:
            show_error = ec2_keys["show_error"]
            del ec2_keys["show_error"]
        else:
            show_error = False
        output = self.tf.modify(tf_variables=ec2_keys, show_error=show_error)
        return output


    def destroy_ec2(self):
        """
        :return: dict from terraCOP
        """
        output = self.tf.destroy()
        return output


    def output_ip(self, ip_type: str = 'public'):
        """
        :param ip_type: by user[optional] private or public[default]
        :return: dict from terraCOP
        """
        output = self.tf.get_output(ip_type=ip_type)
        return output


    def output_watch(self, input_list: list):
        """
        :param input_list: By User according to the output user wants to get from terraform file.
        :return: dict from terraCOP
        """
        output = self.tf.get_output_watch(input_list)
        return output