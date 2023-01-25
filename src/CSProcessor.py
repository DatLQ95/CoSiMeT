from src.CloudSightPool import CloudSightPool
from src.DatabaseAgent import DatabaseAgent
import src.config
import sys
import socket
import ssl
import os


class CSProcessor():
    def __init__(self):
        self.cspool = CloudSightPool()
        self.dbAgent = None
        self.encryption = None
        # self.dbAgent = DatabaseAgent(host=src.config.database['host'], \
        #     user=src.config.database['user'], password=src.config.database['password'], \
        # database=src.config.database['database'],
        # table_name=src.config.database['table'])

    def update_cs_pool(self):
        self.cspool.update_CS_list(self.dbAgent.get_all_CS_servers())

    def get_all_cloudsight_server(self):
        return self.cspool.get_CS_list()

    def check_in_cs_server_list(self, server_name):
        return self.cspool.check_in_cs_list(server_name)

    def get_cloudsight_server_list(self, cs_server_list):
        return self.cspool.get_cloudsight_servers(cs_server_list)

    def get_cloudsight_server(self, cs_server_name):
        return self.cspool.get_cloudsight_server(cs_server_name=cs_server_name)

    def do_sanity_check(self, cs_server_list):
        self.cspool.sanity_check(cs_server_list)
        self.dbAgent.update_CS_servers(
            self.cspool.get_cloudsight_servers(cs_server_list))

    def add_server(self, cs_server):
        self.cspool.add_server(cs_server)
        self.dbAgent.update_CS_server(cs_server)

    def remove_server(self, cs_server_name):
        self.dbAgent.remove_server(
            self.cspool.get_cloudsight_server(cs_server_name))
        self.cspool.remove_server(cs_server_name)

    def update_all_server_status(self):
        self.cspool.check_connect_all_server()
        self.dbAgent.update_CS_servers(self.cspool.get_CS_list())

    def upgrade_server_version(self, cs_server_name):

        pass

    def update_certificate_expiry_date(self, cs_server_list):
        self.cspool.update_certificate_expiry_date(cs_server_list)
        pass

    def connect_ssh(self, cs_server_name):
        # Print out the cmd to run to access the server in a new terminal
        pass

    def exit_program(self):
        sys.exit()

    def update_server_status(self, cs_server_name):
        self.cspool.check_status(
            self.get_cloudsight_server(
                cs_server_name=cs_server_name))
        self.dbAgent.update_CS_server(
            self.get_cloudsight_server(
                cs_server_name=cs_server_name))
        if self.get_cloudsight_server(cs_server_name=cs_server_name).get_status(
        ) == src.config.status_state['available']:
            return True
        else:
            return False

    def check_version(self, version, cs_server_name):
        return self.cspool.check_version(
            version=version, cs_server=self.get_cloudsight_server(cs_server_name=cs_server_name))

    def upgrade_server_version(self, version, cs_server_name):
        '''
        Upgrade the server to a target version.
        '''
        self.cspool.upgrade_version(
            version, self.get_cloudsight_server(
                cs_server_name=cs_server_name))
        self.dbAgent.update_CS_server(
            self.get_cloudsight_server(
                cs_server_name=cs_server_name))
        pass

    def check_user(self, user_name, user_password):
        '''
        Connect to MySQL to check if this user is in database user list
        '''
        self.dbAgent = DatabaseAgent()
        return self.dbAgent.check_connection(
            user=user_name, password=user_password)

    def check_crypto_key(self):
        '''
        Connect to MySQL to check if this user is in database user list
        '''
        return self.dbAgent.check_crypto_key()

    def update_http_certificate(self, cs_server_name, path):
        '''
        Update the HTTP certificate for cs_server
        '''
        print("Update Certificate in CS PRogram")
        self.cspool.update_http_certificate(
            self.get_cloudsight_server(
                cs_server_name=cs_server_name), path)
        self.dbAgent.update_CS_server(
            self.get_cloudsight_server(
                cs_server_name=cs_server_name))
        pass

    def update_general_info(self):
        self.dbAgent.get_general_info()

    def update_fernet(self):
        self.dbAgent.update_fernet()

    def prepare_folder(self, cs_server_name):
        #TODO: if the folder certificates is there, then we dont create, if it is not there, create a new one
        # If the cs_server folder is not there, create it, if it is there, do nothing.
        path = f'certificates/{cs_server_name}'

        # Check whether the specified path exists or not
        isExist = os.path.exists(path)

        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(path)
