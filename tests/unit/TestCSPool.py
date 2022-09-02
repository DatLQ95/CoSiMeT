import unittest

from src.CSProcessor import CSProcessor
from src.CloudSightServer import CloudSightServer
from src.CloudSightPool import CloudSightPool

cspool = CloudSightPool()
cs_server = CloudSightServer(name='cs624', url='localhost', remote_user='vagrant', access_port='8888', key_file_path='credentials/cs624_key', version='6.2.5')
cspool.add_server(cs_server)

class TestCSPool(unittest.TestCase):
    def test_check_version1(self):
        """
        Test if a version is valid
        """
        data = "6.2.6"
        result = cspool.check_version(data, cs_server)
        self.assertTrue(result)
    
    def test_check_version2(self):
        """
        Test if a version is valid
        """
        data = "7.0.9"
        result = cspool.check_version(data, cs_server)
        self.assertTrue(result)
    
    def test_check_version3(self):
        """
        Test if a version is valid
        """
        data = "6.2.1"
        result = cspool.check_version(data, cs_server)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()