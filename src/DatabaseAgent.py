from CloudSightServer import CloudSightServer
import mysql.connector
import mysql
from mysql.connector.locales.eng import client_error
from mysql.connector.plugins import *

class DatabaseAgent:
    def __init__(self):
        #FIXME: we have not deal with the case that we dont habe database in the first place, let's assume we already have the database named: CloudSightServers
        self.mydb = None
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

    def check_connection(self, host, user, password, database, table_name):
        try:
            self.mydb = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database, 
                # auth_plugin='mysql_native_password',
            )
            self.table_name = table_name
            self.create_table(self.table_name)
            return True
        except:
            print("An exception occurred")
            return False

    def get_all_CS_servers(self):
        mycursor = self.mydb.cursor()
        sql = f"SELECT * FROM {self.table_name}"
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        cs_server_list = list()
        for x in myresult:
            cs_server = CloudSightServer(name=x[0], url=x[1], key=x[2],  remote_user=x[3], status=x[4], version=x[5], last_time_update_info=x[6], certi_expiry_date= x[7], access_port= x[8])
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

    def update_CS_servers(self, cs_server_list):
        mycursor = self.mydb.cursor()

        sql = f"INSERT INTO {self.table_name} (name, url , server_ssh_key , remote_use , status, version , date, expiry_date, port) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        data = list()
        print(cs_server_list)
        for cs_server in cs_server_list:
            # TODO: check if the server is there, if it is, then we remove the old one
            if self.check_if_server_exist(cs_server):
                self.remove_server(cs_server)
            data.append(cs_server.get_tuple_data())

        mycursor.executemany(sql, data)

        self.mydb.commit()

        print(mycursor.rowcount, "was inserted.")

    def update_CS_server(self, cs_server):
        mycursor = self.mydb.cursor()

        sql = f"INSERT INTO {self.table_name} (name, url , server_ssh_key , remote_use , status, version , date, expiry_date, port) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        data = list()
        if self.check_if_server_exist(cs_server):
            self.remove_server(cs_server)
        data.append(cs_server.get_tuple_data())
        
        
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
        mycursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (name VARCHAR(50), url VARCHAR(255), server_ssh_key VARCHAR(1024), remote_use VARCHAR(50), status VARCHAR(50), version VARCHAR(10), date VARCHAR(50), PRIMARY KEY(name))")


    
