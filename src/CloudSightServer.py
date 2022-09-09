import os
from datetime import datetime
import stat
import src.config
from stat import *
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import sys
import binascii
import base64


class CloudSightServer:
    def __init__(self, name, url, remote_user, access_port, key_file_path=None, key = None, status= src.config.cs_server_info['default_status'], \
                version = src.config.cs_server_info['default_version'], \
                last_time_update_info = src.config.cs_server_info['default_date'], \
                certi_expiry_date = src.config.cs_server_info['default_expiry_date'], \
                certi_issuer = None):
        self._name = name
        self._url = url
        self._key = key
        self._access_port = access_port
        self.key_file_path = key_file_path
        self.status = status
        self.version = version
        self._remote_user= remote_user
        self.last_time_update_info = last_time_update_info
        self.certi_expiry_date =  certi_expiry_date
        self.certi_issuer = certi_issuer
        self.fernet = None

    def get_access_port(self):
        return self._access_port

    def get_status(self):
        return self.status
    
    def set_status(self, status):
        self.status = status

    def get_name(self):
        return self._name

    def get_remote_user(self):
        return self._remote_user

    def set_name(self, name):
        self._name = name

    def set_version(self, version):
        self.version = version

    def get_version(self):
        return self.version

    def get_key(self):
        return self._key

    def get_url(self):
        return self._url

    def print_info(self):
        print(self._name, self._url, self.status, self.version)
    
    def get_data(self):
        return [self._name, self._url, self.status, self.version, self.last_time_update_info, self.certi_expiry_date, self.certi_issuer]

    def get_tuple_data(self):
        return (self._name, self._url, self._key, self._remote_user, self.status, self.version, self.last_time_update_info, self.certi_expiry_date, self._access_port, self.certi_issuer)
    
    def get_key(self):
        return self._key
    
    def get_last_time_update_info(self):
        return self.last_time_update_info
    
    def get_certi_expiry_date(self):
        return self.certi_expiry_date
    
    def get_certi_issuer(self):
        return self.certi_issuer
    
    def get_access_port(self):
        return self._access_port
    

    def create_result_file(self, host):
        path = os.getcwd() + '/result/' + host

        # Check whether the specified path exists or not
        isExist = os.path.exists(path)

        if not isExist:
            # Create a new directory because it does not exist
            try:
                original_umask = os.umask(0)
                os.makedirs(path, 0x777)
            finally:
                os.umask(original_umask)
        
        file_path = path + "/" + host + "_" + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".json"
        return file_path

    def set_last_update_time(self):
        self.last_time_update_info = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    def set_certi_expiry_date(self, certi_expiry_date):
        self.certi_expiry_date = certi_expiry_date
    
    def set_certi_issuer(self, certi_issuer):
        self.certi_issuer = certi_issuer

    def get_key(self, password):
        # salt = os.urandom(16)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt = src.config.general_info['salt'].encode(),iterations=100,backend=default_backend())
        key=base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def extract_key(self):
        # Convert digital data to binary format
        self.fernet = Fernet(self.get_key(src.config.general_info['crypto_key'].encode()))
        if os.path.isfile(self.key_file_path):
            with open(self.key_file_path, 'rb') as file:
                self._key = self.fernet.encrypt(file.read())
                print(self._key)
    
    def create_key_file_path(self):
        path = os.getcwd() + "/tmp/"
        # Form: name_key
        isExist = os.path.exists(path)
        self.fernet = Fernet(self.get_key(src.config.general_info['crypto_key'].encode()))
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(path, 0x777)
            # try:
            #     original_umask = os.umask(0)
            #     os.makedirs(path, 0x777)
            # finally:
            #     os.umask(original_umask)

        if self._key:
            self.key_file_path = path + self.get_name() + "key"
            with open(self.key_file_path, 'wb') as file:
                # TODO: try catch for wrong crypto key here!
                file.write(self.fernet.decrypt(self._key))
            os.chmod(self.key_file_path, stat.S_IRUSR | stat.S_IWUSR)
            print(self.key_file_path)
    
    def get_key_file_path(self):
        return self.key_file_path
    
    def remove_key_file(self):
        if os.path.isfile(self.key_file_path):
            os.remove(self.key_file_path)
            print("File has been deleted")
        else:
            print("File does not exist")
    