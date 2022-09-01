from http import server
from unicodedata import name
from CloudSightServer import CloudSightServer
import socket
import ssl
from datetime import datetime
from urllib.request import Request, urlopen, ssl, socket
from urllib.error import URLError, HTTPError
import json
import config
from ConnectionAgent import ConnectionAgent

class CloudSightPool:
    def __init__(self):
        #TODO: 
        self.csPoolList = list()
        pass

    def get_name(self):
        name_list = list()
        for cs_server in self.csPoolList:
            name_list.append(cs_server.get_name())
        return name_list

    def update_CS_list(self, cs_server_list):
        for cs_server in cs_server_list:
            if self.check_in_cs_list(cs_server_name=cs_server.get_name()):
                self.csPoolList.remove(self.get_cloudsight_server(cs_server.get_name()))
            self.csPoolList.append(cs_server)
    
    def update_CS(self, cs_server):
        if self.check_in_cs_list(cs_server_name=cs_server.get_name()):
            self.csPoolList.remove(self.get_cloudsight_server(cs_server.get_name()))
        self.csPoolList.append(cs_server)

    def get_CS_list(self):
        return self.csPoolList

    def check_in_cs_list(self, cs_server_name):
        is_in_cs_list = False
        for cs_server in self.csPoolList:
            if cs_server_name == cs_server.get_name():
                is_in_cs_list =  True
                break
        return is_in_cs_list
    
    def get_cloudsight_server(self, cs_server_name):
        for cs_server in self.csPoolList:
            if cs_server.get_name() == cs_server_name:
                return cs_server
        return False
    
    def get_cloudsight_servers(self, cs_server_list_name):
        cs_list = list()
        for cs_server in self.csPoolList:
            if cs_server.get_name() == cs_server_list_name:
                cs_list.append(cs_server)
        return cs_list
    
    def sanity_check(self, server_list_name):
        # call agent Ansible and run the code or should we implement here?
        host_list = self.get_cloudsight_servers(server_list_name)
        ansibleHelper = ConnectionAgent()
        cs_server_list =  ansibleHelper.do_sanity_check(host_list)
        self.update_CS_list(cs_server_list)

    def add_server(self,cs_server):
        self.csPoolList.append(cs_server)
    
    def remove_server(self, cs_server_name):
        self.csPoolList.remove(self.get_cloudsight_server(cs_server_name))

    def check_connect_all_server(self):
        ansibleHelper = ConnectionAgent()
        cs_server_list =  ansibleHelper.do_connection_check(self.get_CS_list())
        cs_server_list = self.update_certificate_expiry_date(self.get_CS_list())
        self.update_CS_list(cs_server_list)

    def update_certificate_expiry_date(self, cs_server_list):
        
        for cs_server in cs_server_list:
            print(cs_server.get_url())
            try:
                exprity_date = self.ssl_expiry_datetime(cs_server.get_url())
                cs_server.set_certi_expiry_date(exprity_date)
            except: 
                print("Unreachable")
        return cs_server_list
    
    def update_server_certificate(self, cs_server):
        try:
            exprity_date = self.ssl_expiry_datetime(cs_server.get_url())
            print("expiry_date: ", exprity_date)
            cs_server.set_certi_expiry_date(exprity_date)
        except: 
            print("Unreachable")
        return cs_server

    def ssl_expiry_datetime(self, hostname):
        context = ssl.create_default_context()

        with socket.create_connection((hostname, config.cs_server_info['admin_port'])) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                # print(ssock.version())
                data = json.dumps(ssock.getpeercert()["notAfter"])
                # print(ssock.getpeercert())
        return data

    def check_status(self, cs_server):
        ansibleHelper = ConnectionAgent()
        cs_list = list()
        cs_list.append(cs_server)
        cs_server =  ansibleHelper.do_connection_check(cs_list)[0]
        cs_server = self.update_server_certificate(cs_server)
        self.update_CS(cs_server)
        return cs_server

    def upgrade_version(self, version, cs_server):
        ansibleHelper = ConnectionAgent()
        cs_list = list()
        cs_list.append(cs_server)
        cs_server =  ansibleHelper.do_upgrade_version_server(version, cs_list)[0]
        cs_server = self.update_server_certificate(cs_server)
        self.update_CS(cs_server)
        return cs_server
    
    def update_http_certificate(self, cs_server, path):
        print("in Cs pool")
        ansibleHelper = ConnectionAgent()
        cs_list = list()
        cs_list.append(cs_server)
        cs_server =  ansibleHelper.do_update_http_certificate(cs_list, path)[0]
        cs_server = self.update_server_certificate(cs_server)
        self.update_CS(cs_server)
        return cs_server