from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash.SHA256 import hashlib
import base64

## Custom
from . import config
    
class encryption:
    def __init__(self):
        self.key = hashlib.sha256(config.AES_KEY.encode('utf-8')).digest()

    def pad(self, s):
        return s + '^' * (config.BS - len(s) % config.BS) 

    def unpad(self, s):
        return s.rstrip('^')

    def encrypt(self, plaintext):
        iv = Random.new().read(config.BS)
        aes = AES.new(self.key, AES.MODE_CBC, iv)
        try:
            cipherText = aes.encrypt(self.pad(str(plaintext)))
            cipherInBytes = base64.b64encode(iv + cipherText)
            return str(cipherInBytes, 'utf-8')
        except:
            raise Exception("Failed to Encrypt message")

    def decrypt(self, encodedCipherTextInStr):
        encodedCipherText = bytes(encodedCipherTextInStr, 'utf-8')
        cipherText = base64.b64decode(encodedCipherText)
        iv = cipherText[:config.BS] 
        cipherText = cipherText[config.BS:]
        aes = AES.new(self.key, AES.MODE_CBC, iv)
        try:
            paddedPlainText = aes.decrypt(cipherText)
            return self.unpad(paddedPlainText.decode("utf-8"))
        except:
            raise Exception("Failed to Decrypt message")
