from importlib.resources import path
from xmlrpc.client import Server
from src.StateMachine.StateMachine import State
from src.CloudSightServer import CloudSightServer
import os
import src.config
from getpass import getpass


class OpenMenu(State):
    def __init__(self):
        super().__init__()

    def go_to_menu(self):
        self.program.setProgramState(SelectServers())

    def go_to_add_server(self):
        self.program.setProgramState(ChooseCryptoMethod())

    def go_to_remove_server(self):
        self.program.setProgramState(RemoveServer())

    def go_to_update_servers(self):
        self.program.setProgramState(UpdateServers())

    def go_to_exit(self):
        self.program.processor.exit_program()

    def execute(self):
        self.remove_key_files()
        self.program.processor.update_cs_pool()
        self.program.processor.update_general_info()
        self.show_banner()
        self.show_all_servers()
        self.show_options()
        action = input("Your input (Please fill in the number, ex.: 1): ")
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

    def remove_key_files(self):
        tmp_path = path = os.getcwd() + "/tmp/"
        for file_name in os.listdir(tmp_path):
            # construct full file path
            file = path + file_name
            if os.path.isfile(file):
                print('Deleting file:', file)
                os.remove(file)
        with open(os.getcwd() + "/ansible/hosts.yaml", "r+") as f:
            f.truncate(0)

    def show_all_servers(self):
        self.program.GUIhelper.list_servers(
            self.program.processor.get_all_cloudsight_server())

    def show_options(self):
        # self.program.show
        self.program.GUIhelper.show_options_open_menu()

    def show_banner(self):
        self.program.GUIhelper.show_banner()


class SelectServers(State):
    def __init__(self):
        super().__init__()

    def go_to_open_menu(self):
        self.program.setProgramState(OpenMenu())

    def go_to_server_state(self, action):
        success = self.program.processor.update_server_status(action)
        if success:
            self.program.setProgramState(ServerMenu(action))
        else:
            self.program.setProgramState(ServerMenuFail(action))

    def execute(self):
        self.show_banner()
        self.show_server_list()
        action = input(
            "Server's name (Please write the name of the server you want to select, ex: demo): ")
        if self.program.processor.check_in_cs_server_list(action):
            self.go_to_server_state(action)
        else:
            self.program.GUIhelper.select_server_fault_notice()
            self.go_to_open_menu()

    def show_server_list(self):
        self.program.GUIhelper.list_servers(
            self.program.processor.get_all_cloudsight_server())

    def show_banner(self):
        self.program.GUIhelper.show_banner()


class AddServerKey():

    def __init__(self):
        super().__init__()

    def go_to_open_menu(self):
        self.program.setProgramState(OpenMenu())

    def execute(self):
        self.show_banner()
        server_name = input("Server name: ")
        server_url = input("Server URL: ")
        server_access_port = input("Server access port: ")
        server_key_file = input("Path to key file: ")
        server_remote_user = input("Remote user: ")
        self.check_input_requirements()
        cs_server = CloudSightServer(
            name=server_name,
            url=server_url,
            key_file_path=server_key_file,
            remote_user=server_remote_user,
            access_port=server_access_port,
            crypto_method=src.config.crypto_method['key_file'])
        cs_server.extract_key()
        # TODO: Check if the file exist, check if the input correct!
        if self.program.processor.check_in_cs_server_list(server_name):
            self.program.GUIhelper.add_server_fault_notice()
        else:
            self.program.processor.add_server(cs_server)
        self.go_to_open_menu()

    def check_input_requirements(self):
        pass

    def show_banner(self):
        self.program.GUIhelper.show_banner()


class AddServerPassword():

    def __init__(self):
        super().__init__()

    def go_to_open_menu(self):
        self.program.setProgramState(OpenMenu())

    def execute(self):
        self.show_banner()
        server_name = input("Server name: ")
        server_url = input("Server URL: ")
        server_access_port = input("Server access port: ")
        ssh_password = input("SSH Password: ")
        server_remote_user = input("Remote user: ")
        self.check_input_requirements()
        cs_server = CloudSightServer(
            name=server_name,
            url=server_url,
            ssh_password=ssh_password,
            remote_user=server_remote_user,
            access_port=server_access_port,
            crypto_method=src.config.crypto_method['password'])
        if self.program.processor.check_in_cs_server_list(server_name):
            self.program.GUIhelper.add_server_fault_notice()
        else:
            self.program.processor.add_server(cs_server)
        self.go_to_open_menu()

    def check_input_requirements(self):
        pass

    def show_banner(self):
        self.program.GUIhelper.show_banner()


class ChooseCryptoMethod():

    def __init__(self):
        super().__init__()

    def go_to_add_server_ssh_key(self):
        self.program.setProgramState(AddServerKey())

    def go_to_add_server_ssh_password(self):
        self.program.setProgramState(AddServerPassword())

    def execute(self):
        self.show_banner()
        self.show_options()
        action = input("Your input (Please fill in the number, ex.: 1): ")
        if (action == "1"):
            self.go_to_add_server_ssh_key()
        elif (action == "2"):
            self.go_to_add_server_ssh_password()
        else:
            pass

    def show_server(self):
        self.program.GUIhelper.show_server(
            self.program.processor.get_cloudsight_server(
                self.cs_server))

    def show_options(self):
        self.program.GUIhelper.show_options_choose_crypto_method()

    def show_banner(self):
        self.program.GUIhelper.show_banner()

    def remove_key_files(self):
        tmp_path = path = os.getcwd() + "/tmp/"
        for file_name in os.listdir(tmp_path):
            # construct full file path
            file = path + file_name
            if os.path.isfile(file):
                print('Deleting file:', file)
                os.remove(file)
        with open(os.getcwd() + "/ansible/hosts.yaml", "r+") as f:
            f.truncate(0)


class RemoveServer(State):
    # TODO: maybe asking if the user really sure to delete this ?
    def __init__(self):
        super().__init__()

    def go_to_open_menu(self):
        self.program.setProgramState(OpenMenu())

    def execute(self):
        self.show_banner()
        self.show_all_servers()
        server_name = input(
            "Server name (Please write the name of server you want to remove, ex: demo): ")
        if self.program.processor.check_in_cs_server_list(server_name):
            self.program.processor.remove_server(server_name)
        else:
            self.program.GUIhelper.remove_server_fault_notice()
        self.go_to_open_menu()

    def check_input_requirements(self):
        pass

    def show_banner(self):
        self.program.GUIhelper.show_banner()

    def show_all_servers(self):
        self.program.GUIhelper.list_servers(
            self.program.processor.get_all_cloudsight_server())


class UpdateServers(State):
    def __init__(self):
        super().__init__()

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
        self.remove_key_files()
        self.show_banner()
        self.show_server()
        self.show_options()
        action = input("Your input (Please fill in the number, ex.: 1): ")
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
        self.program.GUIhelper.show_server(
            self.program.processor.get_cloudsight_server(
                self.cs_server))

    def show_options(self):
        self.program.GUIhelper.show_options_server_menu()

    def show_banner(self):
        self.program.GUIhelper.show_banner()

    def remove_key_files(self):
        tmp_path = path = os.getcwd() + "/tmp/"
        for file_name in os.listdir(tmp_path):
            # construct full file path
            file = path + file_name
            if os.path.isfile(file):
                print('Deleting file:', file)
                os.remove(file)
        with open(os.getcwd() + "/ansible/hosts.yaml", "r+") as f:
            f.truncate(0)


class ServerMenuFail(State):

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
        action = input("Your input (Please fill in the number, ex.: 1): ")
        if (action == "1"):
            self.go_to_open_menu()
        elif (action == "2"):
            self.go_to_update_server()
        else:
            pass

    def show_server(self):
        self.program.GUIhelper.show_server(
            self.program.processor.get_cloudsight_server(
                self.cs_server))

    def show_options(self):
        self.program.GUIhelper.show_options_server_menu_fail()

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
        # self.program.processor.connect_ssh(self.cs_server)
class UpdateCertificate(State):

    def __init__(self, cs_server):
        super().__init__()
        self.cs_server = cs_server

    def go_to_server_menu(self):
        self.program.setProgramState(ServerMenu(self.cs_server))

    def execute(self):
        #TODO: create a certificate folder and CS server folder name inside, then ask the customer to copy the file there.
        self.prepare_folder()
        action = input(
            "Put the https.keystore file to certificates/cs_server_name (ex.: certificates/demoportal) then hit any key to continue ")
        path = f'certificates/{self.cs_server}/http.keystore'
        print(path)
        if os.path.isfile(path):
            self.update_certificate(path)
        else:
            self.program.GUIhelper.update_certificate_fail_notice()
        self.go_to_server_menu()

    def update_certificate(self, path):
        # print("Not implement this feature yet, sorry, please come back later!")
        # action = input("Press anykey to come back: ")
        self.program.processor.update_http_certificate(self.cs_server, path)
    
    def prepare_folder(self):
        self.program.processor.prepare_folder(self.cs_server)


class UpgradeServerVersion(State):

    def __init__(self, cs_server):
        super().__init__()
        self.cs_server = cs_server

    def go_to_server_menu(self):
        self.program.setProgramState(ServerMenu(self.cs_server))

    def execute(self):
        version = input(
            "Version (Fill in the version you want to update in format x.x.x, ex: 6.2.5): ")
        if self.program.processor.check_version(version, self.cs_server):
            self.upgrade_server_version(version)
        else:
            self.program.GUIhelper.upgrade_server_version_fault_notice()
        self.go_to_server_menu()

    def upgrade_server_version(self, version):
        # print("Not implement this feature yet, sorry, please come back later!")
        # action = input("Press anykey to come back: ")
        self.program.processor.upgrade_server_version(version, self.cs_server)


class UpdateServerStatus(State):
    def __init__(self, cs_server):
        super().__init__()
        self.cs_server = cs_server

    def execute(self):
        self.update_server_status()

    def update_server_status(self):
        success = self.program.processor.update_server_status(self.cs_server)
        if success:
            self.program.setProgramState(ServerMenu(self.cs_server))
        else:
            self.program.setProgramState(ServerMenuFail(self.cs_server))


class LoginState(State):
    def __init__(self):
        super().__init__()

    def go_to_open_menu(self):
        self.program.setProgramState(OpenMenu())

    def execute(self):
        self.show_banner()
        # user_name= input("User name: ")
        # user_password = getpass()
        # src.config.general_info['crypto_key'] = getpass(prompt='Encryption key: ')

        user_name = "dat-mysql"
        user_password = "12345678"
        src.config.general_info['crypto_key'] = "cosimet"
        if self.program.processor.check_user(user_name, user_password):
            if self.program.processor.check_crypto_key():
                self.program.processor.update_fernet()
                self.go_to_open_menu()
            else:
                self.program.processor.exit_program()
        else:
            self.program.processor.exit_program()

    def show_banner(self):
        self.program.GUIhelper.show_banner()
