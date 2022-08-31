from curses import erasechar
import os
from xml.etree.ElementPath import get_parent_map
from tabulate import tabulate
from CloudSightServer import CloudSightServer
from CSProcessor import CSProcessor

from colorama import Fore, init
from colorama import Style
import sys
import config

class GUIHelper:
    def __init__(self):
        init(autoreset=True)
        
    def remove_server_fault_notice(self):
        print(f"{Fore.CYAN}This server is not in the list")
        input("Press anykey to return: ")
        
    def add_server_fault_notice(self):
        print(f"{Fore.CYAN}This server already exist, can not add new one")
        input("Press anykey to return: ")
    
    def upgrade_server_version_fault_notice(self):
        print(f"{Fore.CYAN}Wrong value or not suitable version, please check again!")
        input("Press anykey to return: ")

    def select_server_fault_notice(self):
        print(f"{Fore.CYAN}Server's name is not exist in database, please check again!")
        input("Press anykey to return: ")

    def check_input_requirements(self):
        pass

    def list_servers(self, cs_list):
        data = list()
        for cs_server in cs_list:
            data.append(self.coloring_status(cs_server))
        print (tabulate(data, headers=["Name", "URL", "Status", "Version", "Date updated last time", "Certificate expiry date"]))
    
    def show_server(self, cs_server_name):
        data = list()
        data.append(self.coloring_status(cs_server_name))
        print (tabulate(data, headers=["Name", "URL", "Status", "Version", "Date updated last time", "Certificate expiry date"]))
    

    def show_banner(self):
        os.system('clear')
        print(f"{Fore.CYAN}----------------------------------------------------")
        print(f"{Fore.CYAN}---------CLOUDSIGHT MANAGEMENT TOOL-----------------")
        print(f"{Fore.CYAN}----------------------------------------------------")

    def coloring_status(self, cs_server):
        if cs_server.get_status() == config.status_state['available']:
            color = Fore.GREEN
        elif cs_server.get_status() == config.status_state['failed']:
            color = Fore.YELLOW
        elif cs_server.get_status() == config.status_state['unreachable']:
            color = Fore.RED
        else:
            color = Fore.WHITE
        color_data = list()
        for data in cs_server.get_data():
            color_data.append(f"{color}{data}")
        return color_data
        
    def show_options_open_menu(self):
        print("----------------------------------------------------")
        print("Please chose the following options")
        print("1. Select servers")
        print("2. Add a server")
        print("3. Remove a server")
        print("4. Update all servers")
        print("5. Exit")
    
    def show_options_menu(self):
        print("----------------------------------------------------")
        print("Please enter a server's name of list of server (separated by a comma): ")


    def show_options_server_menu(self):
        print("----------------------------------------------------")
        print("Please chose the following options:")
        print("1. Go back")
        print("2. Update status")
        print("3. Do sanity check and get the report")
        print("4. Connect to the server")
        print("5. Update HTTP certificate")
        print("6. Upgrade to new version")        

    def show_options_server_menu_fail(self):
        print("----------------------------------------------------")
        print("Please chose the following options:")
        print("1. Go back")
        print("2. Update status")