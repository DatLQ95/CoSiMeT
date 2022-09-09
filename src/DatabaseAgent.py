from src.CloudSightServer import CloudSightServer
import mysql.connector
import mysql
from mysql.connector.locales.eng import client_error
from mysql.connector.plugins import *
import src.config
from os import urandom
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import sys
import binascii
import base64

class DatabaseAgent:
    def __init__(self):
        #FIXME: we have not deal with the case that we dont habe database in the first place, let's assume we already have the database named: CloudSightServers
        self.mydb = None
        self.fernet = None
        
        # try:
        #     self.mydb = mysql.connector.connect(
        #         host=host,
        #         user=user,
        #         password=password,
        #         database=database, 
        #         # auth_plugin='mysql_native_password',
        #     )
        #     self.table_name = table_name
        #     self.create_table(self.table_name)
        # except:
        #     print("An exception occurred")
        pass

    def update_fernet(self):
        self.get_salt()
        self.fernet = Fernet(self.get_key())

    def get_salt(self):
        mycursor = self.mydb.cursor()
        sql = f"SELECT * FROM {self.constant_table} WHERE item=\"salt\""
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        src.config.general_info['salt']=myresult[0][1]

    def check_connection(self, user, password):
        try:
            self.mydb = mysql.connector.connect(
                host=src.config.database['host'],
                user=user,
                password=password,
                database=src.config.database['database'], 
                auth_plugin='mysql_native_password',
            )
            self.table_name =src.config.database['table']
            self.general_info_table = src.config.database['general_info_table']
            self.constant_table = src.config.database['constant_table']
            self.create_table(self.table_name)
            return True
        except:
            print("An exception occurred")

    def check_crypto_key(self):
        mycursor = self.mydb.cursor()
        sql = f"SELECT * FROM {self.general_info_table} WHERE item=\"crypto_key_hash\""
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        current_hash = hashlib.sha224(src.config.general_info['crypto_key'].encode()).hexdigest()
        if myresult[0][1] == current_hash:
            return True
        else :
            return False

    def get_all_CS_servers(self):
        mycursor = self.mydb.cursor()
        sql = f"SELECT * FROM {self.table_name}"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        cs_server_list = list()
        for x in myresult:
            cs_server = CloudSightServer(name=x[0], url=x[1], key=self.fernet.decrypt(x[2]),  remote_user=x[3], status=x[4], version=x[5], last_time_update_info=x[6], certi_expiry_date= x[7], access_port= x[8], certi_issuer=x[9])
            cs_server_list.append(cs_server)
        return cs_server_list

    
    def check_if_server_exist(self, cs_server):
        exist = False
        mycursor = self.mydb.cursor()
        print(type(cs_server))
        mycursor.execute(f"SELECT * FROM {self.table_name} WHERE name ='{cs_server.get_name()}'")
        for x in mycursor:
            if x:
                exist = True
        return exist
    
    def remove_server(self, cs_server):
        mycursor = self.mydb.cursor()

        sql = f"DELETE FROM {self.table_name} WHERE name = '{cs_server.get_name()}'"

        mycursor.execute(sql)

        self.mydb.commit()

    def encrypt_ssh_key(self, data):
        """
        Get a list of data
        Return a encrypted SSH key tuple
        """
        for cs_server_list in data:
            cs_server_list[2] = self.fernet.encrypt(cs_server_list[2])
        return tuple(cs_server_list)

    def update_CS_servers(self, cs_server_list):
        mycursor = self.mydb.cursor()
        
        sql = f"INSERT INTO {self.table_name} (name, url , server_ssh_key , remote_use , status, version , date, expiry_date, port, certi_issuer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        data = list()
        print(cs_server_list)
        for cs_server in cs_server_list:
            if self.check_if_server_exist(cs_server):
                self.remove_server(cs_server)
            data.append(cs_server.get_list_data())
        self.encrypt_ssh_key(data)
            
        mycursor.executemany(sql, data)

        self.mydb.commit()

        print(mycursor.rowcount, "was inserted.")

    def update_CS_server(self, cs_server):
        mycursor = self.mydb.cursor()

        sql = f"INSERT INTO {self.table_name} (name, url , server_ssh_key , remote_use , status, version , date, expiry_date, port, certi_issuer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        data = list()
        if self.check_if_server_exist(cs_server):
            self.remove_server(cs_server)
        data.append(cs_server.get_list_data())
        self.encrypt_ssh_key(data)
        
        mycursor.executemany(sql, data)

        self.mydb.commit()

        print(mycursor.rowcount, "was inserted.")

    def create_database(self, db_name):
        mycursor = self.mydb.cursor()
        mycursor.execute("SHOW DATABASES;")
        # print(type(mycursor))
        exist = False
        for x in mycursor:
            # print(type(x))
            if db_name in x:
                exist = True
        if not exist:
            mycursor.execute(f"CREATE DATABASE {db_name}")
        
    def create_table(self, table_name):
        mycursor = self.mydb.cursor()
        mycursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (name VARCHAR(50), url VARCHAR(255), server_ssh_key VARCHAR(1024), remote_use VARCHAR(50), status VARCHAR(50), version VARCHAR(10), date VARCHAR(50), expiry_date VARCHAR(50), port VARCHAR(50), certi_issuer VARCHAR(50), PRIMARY KEY(name))")

    def erase_general_info_table(self):
        mycursor = self.mydb.cursor()

        mycursor.execute(f"TRUNCATE TABLE {self.general_info_table}")

        self.mydb.commit()

    def update_general_info(self):
        """
        Update the general info with new encrypt key 
        """
        print("updateing the general info")
        mycursor = self.mydb.cursor()
        
        sql = f"INSERT INTO {self.general_info_table} (item, info) VALUES (%s, %s)"
        
        data = list()
        self.erase_general_info_table()
        for key, value in src.config.general_info.items():
            if key == "crypto_key":
                continue
            data.append((key, self.fernet.encrypt(value.encode())))
        # Add the hash:
        data.append(("crypto_key_hash", hashlib.sha224(src.config.general_info['crypto_key'].encode()).hexdigest()))
        print(data)
        mycursor.executemany(sql, data)

        self.mydb.commit()

        print(mycursor.rowcount, "was inserted.")
        pass

    def get_general_info(self):
        mycursor = self.mydb.cursor()
        sql = f"SELECT * FROM {self.general_info_table}"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        for item in myresult:
            if item[0] in src.config.general_info.keys():
                src.config.general_info[item[0]] = self.fernet.decrypt(item[1].encode())

    def get_key(self):
        # salt = os.urandom(16)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt = src.config.general_info['salt'].encode(),iterations=100,backend=default_backend())
        key=base64.urlsafe_b64encode(kdf.derive(src.config.general_info['crypto_key'].encode()))
        return key

    