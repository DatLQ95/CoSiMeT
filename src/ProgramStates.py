from xmlrpc.client import Server
from StateMachine.StateMachine import State
from CloudSightServer import CloudSightServer
import os

class OpenMenu(State):
    def __init__(self):
        super().__init__()

    def go_to_menu(self):
        self.program.setProgramState(SelectServers())
    
    def go_to_add_server(self):
        self.program.setProgramState(AddServer())
    
    def go_to_remove_server(self):
        self.program.setProgramState(RemoveServer())
    
    def go_to_update_servers(self):
        self.program.setProgramState(UpdateServers())
    
    def go_to_exit(self):
        self.program.processor.exit_program()
    
    def execute(self):
        self.show_banner()
        self.show_all_servers()
        self.show_options()
        action = input("Your input: ")
        if (action == "1"):
            self.go_to_menu()
        elif (action == "2"):
            self.go_to_add_server()
        elif (action == "3"):
            self.go_to_remove_server()
        elif (action == "4"):
            self.go_to_update_servers()
        elif (action == "5"):
            self.go_to_exit()
        else:
            pass

    def show_all_servers(self):
        self.program.GUIhelper.list_servers(self.program.processor.get_all_cloudsight_server())
    
    def show_options(self):
        # self.program.show
        self.program.GUIhelper.show_options_open_menu()

    def show_banner(self):
        self.program.GUIhelper.show_banner()


class SelectServers(State):    
    def __init__(self):
        super().__init__()

    # if down button is pushed it should move one floor down and open the door
    def go_to_open_menu(self):
        self.program.setProgramState(OpenMenu())

    def go_to_server_state(self, action):
        self.program.processor.update_server_status(action)
        self.program.setProgramState(ServerMenu(action))

    def execute(self):
        self.show_banner()
        self.show_server_list()
        action = input("Server's name: ")
        if self.program.processor.check_in_cs_server_list(action):
            self.go_to_server_state(action)
        else: 
            self.go_to_open_menu()

    def show_server_list(self):
        self.program.GUIhelper.list_servers(self.program.processor.get_all_cloudsight_server())
    
    def show_banner(self):
        self.program.GUIhelper.show_banner()

class AddServer(State):
    
    def __init__(self):
        super().__init__()

    # if down button is pushed it should move one floor down and open the door
    def go_to_open_menu(self):
        self.program.setProgramState(OpenMenu())

    def execute(self):
        self.show_banner()
        server_name= input("Server name: ")
        server_url = input("Server URL: ")
        server_access_port = input("Server access port: ")
        server_key_file = input("Path to key file: ")
        server_remote_user = input("Remote user: ")
        self.check_input_requirements()
        cs_server = CloudSightServer(name=server_name, url=server_url, key_file_path=server_key_file,remote_user=server_remote_user, access_port=server_access_port)
        cs_server.extract_key()
        if self.program.processor.check_in_cs_server_list(server_name):
            self.program.GUIhelper.add_server_fault_notice()
        else:
            self.program.processor.add_server(cs_server)
        self.go_to_open_menu()

    def check_input_requirements(self):
        pass

    def show_banner(self):
        self.program.GUIhelper.show_banner()

class RemoveServer(State):
    #TODO: maybe asking if the user really sure to delete this ?
    def __init__(self):
        super().__init__()

    # if down button is pushed it should move one floor down and open the door
    def go_to_open_menu(self):
        self.program.setProgramState(OpenMenu())

    def execute(self):
        self.show_banner()
        server_name= input("Server name: ")
        if self.program.processor.check_in_cs_server_list(server_name):
            self.program.processor.remove_server(server_name)
        else:
            self.program.GUIhelper.remove_server_fault_notice()
        self.go_to_open_menu()

    def check_input_requirements(self):
        pass

    def show_banner(self):
        self.program.GUIhelper.show_banner()

class UpdateServers(State):
    def __init__(self):
        super().__init__()

    # if down button is pushed it should move one floor down and open the door
    def go_to_open_menu(self):
        self.program.setProgramState(OpenMenu())

    def execute(self):
        self.show_banner()
        self.program.processor.update_all_server_status()
        self.go_to_open_menu()

    def check_input_requirements(self):
        pass

    def show_banner(self):
        self.program.GUIhelper.show_banner()

class ServerMenu(State):
    
    def __init__(self, cs_server):
        super().__init__()
        self.cs_server = cs_server
    
    def go_to_open_menu(self):
        self.program.setProgramState(OpenMenu())
    
    def go_to_sanity_check(self):
        self.program.setProgramState(SanityCheck(self.cs_server))
    
    def go_to_connect_server(self):
        self.program.setProgramState(ServerConnectSSH(self.cs_server))
    
    def go_to_update_certificate(self):
        self.program.setProgramState(UpdateCertificate(self.cs_server))
    
    def go_to_upgrade_server(self):
        self.program.setProgramState(UpgradeServerVersion(self.cs_server))

    def go_to_update_server(self):
        self.program.setProgramState(UpdateServerStatus(self.cs_server))

    def execute(self):
        
        self.show_banner()
        self.show_server()
        self.show_options()
        action = input("Your input: ")
        if (action == "1"):
            self.go_to_open_menu()
        elif (action == "2"):
            self.go_to_update_server()
        elif (action == "3"):
            self.go_to_sanity_check()
        elif (action == "4"):
            self.go_to_connect_server()
        elif (action == "5"):
            self.go_to_update_certificate()
        elif (action == "6"): 
            self.go_to_upgrade_server()
        else:
            pass

    def show_server(self):
        self.program.GUIhelper.show_server(self.program.processor.get_cloudsight_server(self.cs_server))

    def show_options(self):
        self.program.GUIhelper.show_options_server_menu()
    
    def show_banner(self):
        self.program.GUIhelper.show_banner()

class SanityCheck(State):
    
    def __init__(self, cs_server):
        super().__init__()
        self.cs_server = cs_server

    def go_to_server_menu(self):
        self.program.setProgramState(ServerMenu(self.cs_server))

    def execute(self):
        self.do_sanity_check()
        self.go_to_server_menu()

    def do_sanity_check(self):
        self.program.processor.do_sanity_check(self.cs_server)


class ServerConnectSSH(State):

    def __init__(self, cs_server):
        super().__init__()
        self.cs_server = cs_server

    def go_to_server_menu(self):
        self.program.setProgramState(ServerMenu(self.cs_server))

    def execute(self):
        self.connect_ssh()
        self.go_to_server_menu()

    def connect_ssh(self):
        # TODO: Implement a way to connect to the SSH of the server
        print("Not implement this feature yet, sorry, please come back later!")
        action = input("Press anykey to come back: ")
        #  self.program.processor.connect_ssh(self.cs_server)


class UpdateCertificate(State):

    def __init__(self, cs_server):
        super().__init__()
        self.cs_server = cs_server

    def go_to_server_menu(self):
        self.program.setProgramState(ServerMenu(self.cs_server))

    def execute(self):
        self.update_certificate()
        self.go_to_server_menu()

    def update_certificate(self):
        print("Not implement this feature yet, sorry, please come back later!")
        action = input("Press anykey to come back: ")
        # self.program.processor.update_certificate(self.cs_server)


class UpgradeServerVersion(State):

    def __init__(self, cs_server):
        super().__init__()
        self.cs_server = cs_server

    def go_to_server_menu(self):
        self.program.setProgramState(ServerMenu(self.cs_server))

    def execute(self):
        version = input("Version: ")
        #TODO: Check the correct target verion here!!! 
        # if self.program.processor.check_version(version, self.cs_server):
            
        self.upgrade_server_version(version)
        self.go_to_server_menu()

    def upgrade_server_version(self, version):
        # print("Not implement this feature yet, sorry, please come back later!")
        # action = input("Press anykey to come back: ")
        self.program.processor.upgrade_server_version(version, self.cs_server)

class UpdateServerStatus(State):
    def __init__(self, cs_server):
        super().__init__()
        self.cs_server = cs_server

    def go_to_server_menu(self):
        self.program.setProgramState(ServerMenu(self.cs_server))

    def execute(self):
        self.update_server_status()
        self.go_to_server_menu()

    def update_server_status(self):
        self.program.processor.update_server_status(self.cs_server)