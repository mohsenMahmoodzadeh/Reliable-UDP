'''
Name: Mohsen Mahmoodzadeh
Student ID: 9622762362
'''
import hashlib

class Packet():
    checksum = 0
    length = 0
    seqNo = 0
    data = 0
    
    def __init__(self, data):
        self.data = data
        self.length = str(len(data))
        # self.checksum = hashlib.sha1(str(data).encode('utf-8')).hexdigest()

    # def make(self, data):
    #     self.data = data
    #     self.length = str(len(data))
    #     self.checksum=hashlib.sha1(data).hexdigest()