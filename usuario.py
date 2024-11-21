import os
from dotenv import load_dotenv

class Usuario():
    def __init__(self,tipo):
        load_dotenv()
        # os.add_dll_directory(os.getenv('CLIDRIVER_PATH'))
        if tipo == 'mysql':
            self.username = os.getenv('DB_USERNAME')
            self.password = os.getenv('DB_PASSWORD')
            self.hostname = os.getenv('DB_HOSTNAME')
            self.port = os.getenv('DB_PORT')
        elif tipo == 'db2':
            self.username = os.getenv('DB2_USERNAME')
            self.password = os.getenv('DB2_PASSWORD')
            self.hostname = os.getenv('DB2_HOST')
            self.port = os.getenv('DB2_PORT')
        elif tipo == 'dev':
            self.username = os.getenv('DB2_DEV_USERNAME')
            self.password = os.getenv('DB2_DEV_PASSWORD')
            self.hostname = os.getenv('DB2_DEV_HOST')
            self.port = os.getenv('DB2_DEV_PORT')