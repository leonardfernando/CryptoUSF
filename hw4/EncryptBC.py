import base64
import hashlib
import sys
from Crypto import Random
from Crypto.Cipher import AES

chunksize = 1024

class EncryptBC(object):
    #initializing the block size and protecting the key
    def __init__(self, key):
        self.bs = 16
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, plain):
        plain = self._pad(plain) #adding padding to the plain text
        iv = Random.new().read(self.bs) #creating iv
        cipher = AES.new(self.key, AES.MODE_CBC, iv) #new AES with CBC mode
        return base64.b64encode(iv + cipher.encrypt(plain)) #encrypting

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

if __name__ == '__main__':
    plain = 'yo'
    key = 'password'
    ebc = EncryptBC(key)
    if len(sys.argv) == 1:
        print "No -i flag for input"
    else:
        if str(sys.argv[1]) == '-i':
            if len(sys.argv) == 2:
                print "No input file"
            else:
                if str(sys.argv[2]).endswith(".txt"):
                    with open(sys.argv[2], 'rb') as infile:
                        with open('encrypted.txt', 'wb') as outfile:
                            while True:
                                chunk = infile.read(chunksize)
                                if len(chunk) == 0:
                                    break
                                outfile.write(ebc.encrypt(chunk))
                else:
                    print('Not a text file')

    print('File successfully encrypted')
