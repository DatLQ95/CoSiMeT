from CloudSightPool import CloudSightPool
from DatabaseAgent import DatabaseAgent
import config
import sys
import socket
import ssl

class CSProcessor():
    def __init__(self):
        self.cspool = CloudSightPool()
        self.dbAgent = None
        # self.dbAgent = DatabaseAgent(host=config.database['host'], \
        #     user=config.database['user'], password=config.database['password'], \
        #     database=config.database['database'], table_name=config.database['table'])
        

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
        self.dbAgent.update_CS_servers(self.cspool.get_cloudsight_servers(cs_server_list))
    
    def add_server(self, cs_server):
        self.cspool.add_server(cs_server)
        print(self.cspool.get_CS_list())
        print(cs_server)
        print(self.cspool.get_cloudsight_servers(cs_server))
        self.dbAgent.update_CS_server(cs_server)
    
    def remove_server(self, cs_server_name):
        self.dbAgent.remove_server(self.cspool.get_cloudsight_server(cs_server_name))
        self.cspool.remove_server(cs_server_name)
    
    def update_all_server_status(self):
        self.cspool.check_connect_all_server()
        self.dbAgent.update_CS_servers(self.cspool.get_CS_list())
        
    def upgrade_server_version(self, cs_server_name):
        
        pass

    def update_certificate(self, cs_server_list):
        self.cspool.update_certificate(cs_server_list)
        pass

    def connect_ssh(self, cs_server_name):
        # Print out the cmd to run to access the server in a new terminal
        pass

    def exit_program(self):
        sys.exit()

    def update_server_status(self, cs_server_name):
        self.cspool.check_status(self.get_cloudsight_server(cs_server_name=cs_server_name))
        self.dbAgent.update_CS_server(self.get_cloudsight_server(cs_server_name=cs_server_name))
        
    def check_version(self, version, cs_server_name):
        '''
        If the verion is bigger than CS server current version.
        Check th upgrade condition also :)
        
        4.x -> 5.x -> 6.0.x -> 6.1.x -> 6.2.x
        '''
        # Check format if it is in "x.x.x" or "xxx":
        #TODO: 
        pass

    def upgrade_server_version(self, version, cs_server_name):
        '''
        Upgrade the server to a target version.
        '''
        self.cspool.upgrade_version(version, self.get_cloudsight_server(cs_server_name=cs_server_name))
        self.dbAgent.update_CS_server(self.get_cloudsight_server(cs_server_name=cs_server_name))
        pass

    def check_user(self, user_name, user_password):
        '''
        Connect to MySQL to check if this user is in database user list
        '''
        self.dbAgent = DatabaseAgent()
        return self.dbAgent.check_connection(host=config.database['host'], \
            user=user_name, password=user_password, \
            database=config.database['database'], table_name=config.database['table'])
        
        