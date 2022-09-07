from ensurepip import version
import re
import subprocess
from unicodedata import name
import src.config
import yaml
from src.CloudSightServer import CloudSightServer
import os
from datetime import datetime
import sys

class ConnectionAgent:
    def __init__(self):
        pass

    def do_upgrade_version_server(self, version, cs_server_list):
        '''
        Upgrade to a desired version
        Input: list of servers need to check
        Output: list of servers with updated properties
        '''
        print("Do upgrade version")
        self.do_connection_check(cs_server_list=cs_server_list)
        avail_hosts = self.filter_unreachable_hosts(cs_server_list)
        print(avail_hosts)
        
        # if avail_hosts is empty: 
        if avail_hosts:
            print("the avail host is not empty")
            self.prepare_cs_server_list_file_for_upgrade(version, avail_hosts)
            self.sanity_output_processing(avail_hosts, self.run_ansible(role="upgrade"))
        return cs_server_list

    def do_sanity_check(self, cs_server_list):
        '''
        Do sanity on the available hosts
        Input: list of servers need to check
        Output: list of servers with updated properties
        '''
        print(" OD sanity check")
        self.do_connection_check(cs_server_list=cs_server_list)
        avail_hosts = self.filter_unreachable_hosts(cs_server_list)
        print(avail_hosts)
        
        # if avail_hosts is empty: 
        if avail_hosts:
            print("the avail host is not empty")
            self.prepare_cs_server_list_file_for_sanity_check(avail_hosts)
            self.sanity_output_processing(avail_hosts, self.run_ansible(role="sanity_check"))
        return cs_server_list

    def do_update_http_certificate(self, cs_server_list, path):
        '''
        '''
        print("Do update HTTP certificate")
        self.do_connection_check(cs_server_list=cs_server_list)
        avail_hosts = self.filter_unreachable_hosts(cs_server_list)
        print(avail_hosts)
        
        # if avail_hosts is empty: 
        if avail_hosts:
            print("the avail host is not empty")
            self.prepare_cs_server_list_file_for_certificate_renewal(path, cs_server_list)
            self.sanity_output_processing(cs_server_list, self.run_ansible(role="renewal_certificate"))
        return cs_server_list

    def filter_unreachable_hosts(self, hostlist):
        avail_list = list()
        for cs_server in hostlist:
            print(cs_server.get_status())
            print(src.config.status_state['available'])
            if cs_server.get_status() == src.config.status_state['available']:
                avail_list.append(cs_server)
            else:
                pass
        return avail_list

    def do_connection_check(self, cs_server_list):
        '''
        This function connect each server and retrieve the CS version
        Input: list of servers need to check
        Output: update the properties: CS version, updated_time, certificate_expery, status
        '''
        cs_list = list()
        for cs_server in cs_server_list:
            cs_server.create_key_file_path()
            self.prepare_host_file(cs_server)
            cs_server = self.output_analyse(cs_server, self.run_ansible(role="connection_check"))
            cs_list.append(cs_server)
        return cs_list

    def prepare_host_file(self, cs_server):
        dict_file = dict()
        dict_file['all'] = dict()
        dict_file['all']['hosts'] = dict()
        dict_file['all']['hosts'][cs_server.get_name()] = dict()
        dict_file['all']['hosts'][cs_server.get_name()]['ansible_host'] = cs_server.get_url()
        dict_file['all']['hosts'][cs_server.get_name()]['ansible_user'] = cs_server.get_remote_user()
        if cs_server.get_access_port():
            dict_file['all']['hosts'][cs_server.get_name()]['ansible_port'] = cs_server.get_access_port()
        dict_file['all']['hosts'][cs_server.get_name()]['ansible_ssh_private_key_file'] = cs_server.get_key_file_path()
        print(dict_file)
        
        with open(src.config.ansible_data['inventory_file_path'], 'w') as file:
            yaml.dump(dict_file, file)

    def prepare_cs_server_list_file_for_sanity_check(self, cs_server_list):
        dict_file = dict()
        dict_file['all'] = dict()
        dict_file['all']['hosts'] = dict()
        for cs_server in cs_server_list:
            dict_file['all']['hosts'][cs_server.get_name()] = dict()
            dict_file['all']['hosts'][cs_server.get_name()]['ansible_host'] = cs_server.get_url()
            dict_file['all']['hosts'][cs_server.get_name()]['ansible_user'] = cs_server.get_remote_user()
            if cs_server.get_access_port():
                dict_file['all']['hosts'][cs_server.get_name()]['ansible_port'] = cs_server.get_access_port()
            dict_file['all']['hosts'][cs_server.get_name()]['ansible_ssh_private_key_file'] = cs_server.get_key_file_path()

            dict_file['all']['hosts'][cs_server.get_name()]['license_server_address'] = src.config.general_info['license_server_address']
            dict_file['all']['hosts'][cs_server.get_name()]['license_server_IP_addr'] = src.config.general_info['license_server_IP_addr']
            dict_file['all']['hosts'][cs_server.get_name()]['license_server_port'] = src.config.general_info['license_server_port']
            dict_file['all']['hosts'][cs_server.get_name()]['domain'] = cs_server.get_url()

        print(dict_file)
        
        with open(src.config.ansible_data['inventory_file_path'], 'w') as file:
            yaml.dump(dict_file, file)
    
    def prepare_cs_server_list_file_for_upgrade(self, version, cs_server_list):
        dict_file = dict()
        dict_file['all'] = dict()
        dict_file['all']['hosts'] = dict()
        for cs_server in cs_server_list:
            dict_file['all']['hosts'][cs_server.get_name()] = dict()
            dict_file['all']['hosts'][cs_server.get_name()]['ansible_host'] = cs_server.get_url()
            dict_file['all']['hosts'][cs_server.get_name()]['ansible_user'] = cs_server.get_remote_user()
            if cs_server.get_access_port():
                dict_file['all']['hosts'][cs_server.get_name()]['ansible_port'] = cs_server.get_access_port()
            dict_file['all']['hosts'][cs_server.get_name()]['ansible_ssh_private_key_file'] = cs_server.get_key_file_path()

            dict_file['all']['hosts'][cs_server.get_name()]['cloudsight_server_install_url'] = src.config.general_info['cloudsight_server_install_url']
            dict_file['all']['hosts'][cs_server.get_name()]['inteno_user'] = src.config.general_info['inteno_user']
            dict_file['all']['hosts'][cs_server.get_name()]['inteno_password'] = src.config.general_info['inteno_password']
            dict_file['all']['hosts'][cs_server.get_name()]['cloudsight_version'] = version


        print(dict_file)
        
        with open(src.config.ansible_data['inventory_file_path'], 'w') as file:
            yaml.dump(dict_file, file)

    def prepare_cs_server_list_file_for_certificate_renewal(self, path, cs_server_list):
        dict_file = dict()
        dict_file['all'] = dict()
        dict_file['all']['hosts'] = dict()
        for cs_server in cs_server_list:
            dict_file['all']['hosts'][cs_server.get_name()] = dict()
            dict_file['all']['hosts'][cs_server.get_name()]['ansible_host'] = cs_server.get_url()
            dict_file['all']['hosts'][cs_server.get_name()]['ansible_user'] = cs_server.get_remote_user()
            if cs_server.get_access_port():
                dict_file['all']['hosts'][cs_server.get_name()]['ansible_port'] = cs_server.get_access_port()
            dict_file['all']['hosts'][cs_server.get_name()]['ansible_ssh_private_key_file'] = cs_server.get_key_file_path()
            dict_file['all']['hosts'][cs_server.get_name()]['cloudsight_version'] = cs_server.get_version()
            dict_file['all']['hosts'][cs_server.get_name()]['key_file_path'] = path
            dict_file['all']['hosts'][cs_server.get_name()]['time_str'] = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
            

        print(dict_file)
        
        with open(src.config.ansible_data['inventory_file_path'], 'w') as file:
            yaml.dump(dict_file, file)

    def read_host_file(self):
        with open(src.config.ansible_data['inventory_file_path']) as file:
            # The FullLoader parameter handles the conversion from YAML
            # scalar values to Python the dictionary format
            cs_server_lists = yaml.load(file, Loader=yaml.FullLoader)

            print(cs_server_lists)

    

    def run_ansible(self, role):
        output_text = str()
        with subprocess.Popen(['ansible-playbook', '-i', src.config.ansible_data['inventory_file_path'], src.config.ansible_data['main_file_path'], '--tags', role], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
            for line in p.stdout:
                print(line, end='') # process line here
                output_text += line
            # raise ProcessException(command, exitCode, output)
        print("output is ", output_text)
        return output_text
        
    def result_file_analyse(self, cs_server):
        '''
        Analyse the output and  update the properties
        '''
        cs_server.set_status()
        cs_server.set_update_time()
        if cs_server.get_status() == src.config.status_state['available']:
            cs_server.set_version()
            cs_server.set_expiry_date_certificate()
        return cs_server
    
    def output_analyse(self, cs_server, output):
        '''
        Analyse the output of checking connection:
        Return the already checked server!
        '''
        # print(output.stdout)
        out = output
        # Check if the server is reachable:
        result = out.find('UNREACHABLE!')
        print(result)
        if result != -1: 
            cs_server.set_status(src.config.status_state['unreachable'])

        result = out.find('ok:')
        if result != -1: 
            cs_server.set_status(src.config.status_state['available'])
            
        result = out.find('FAILED!')
        if result != -1: 
            cs_server.set_status(src.config.status_state['failed'])
        
        if cs_server.get_status() == "Available":
            result = out.find('iopsys.server.version')
            print(result)
            if result == -1:
                print("This string is not exist! Seems like the server not isntall correctly!")
            else:
                start_index = result + 22
                end_index = start_index + 5
                cs_server.set_version(out[start_index:end_index])
        cs_server.set_last_update_time()
        return cs_server

    def sanity_output_processing(self, avail_cs_servers, output):
        '''
        processing the output of sanity check
        '''
        print("in sanity process outpyt")
        out = output
        path = '../result/'

        # Check whether the specified path exists or not
        isExist = os.path.exists(path)

        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(path)
        host_name = str()
        if len(avail_cs_servers) == 1 : 
            host_name = avail_cs_servers[0].get_name()
        else :
            for cs_server in avail_cs_servers:
                host_name += cs_server.get_name()
        
        file_path = path + host_name + "_" + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".txt"
        with open(file_path, "w+") as f:
            f.write(out)
