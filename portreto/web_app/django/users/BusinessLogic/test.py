from . import Tokens
from . import config

def AuthUser_demo():
        try:
                o = Tokens.AuthUser()
                print("AuthUser - Demo")
                print("======================================== START ===========================================")
                print()
                token = o.create_token(
                                "User1", 
                                'password',
                                "user@mail.com",
                                None
                        )
                print("Token created:")
                print("------------------- Start --------------------------")
                print(token)
                print("--------------------- End --------------------------")
                print()
                print()
                payload = o.decode_token(token, config.AUTHENTICATION_SERVICE)
                print("User Decoded Payload:")
                print("------------------- Start --------------------------")
                import pprint
                print(pprint.pprint(payload))
                print("--------------------- End --------------------------")
                print("======================================== END ===========================================")
                print()
                print()
        except Exception as e:
                print(str(e))

def UserIdentity_demo():
        try:
                o = Tokens.UserIdentity()
                print("UserIdentity - Demo")
                print("======================================== START ===========================================")
                print()
                token = o.create_token(
                                "User1", 
                                "user@mail.com", 
                                "1", 
                                False, 
                                False,
                                "None",
                                None
                        )
                print("Token created:")
                print("------------------- Start --------------------------")
                print(token)
                print("--------------------- End --------------------------")
                print()
                print()
                payload = o.decode_token(token, config.APPLICATION_SERVICE)
                print("User Decoded Payload:")
                print("------------------- Start --------------------------")
                import pprint
                print(pprint.pprint(payload))
                print("--------------------- End --------------------------")
                print("======================================== END ===========================================")
                print()
                print()
        except Exception as e:
                print(str(e))

def CreateUser_demo():
        try:
                o = Tokens.CreateUser()
                print("CreateUser - Demo")
                print("======================================== START ===========================================")
                print()
                token = o.create_token(
                                "User1", 
                                "password", 
                                "user@mail.com", 
                                True, 
                                None
                        )
                print("Token created:")
                print("------------------- Start --------------------------")
                print(token)
                print("--------------------- End --------------------------")
                print()
                print()
                payload = o.decode_token(token, config.AUTHENTICATION_SERVICE)
                print("User Decoded Payload:")
                print("------------------- Start --------------------------")
                import pprint
                print(pprint.pprint(payload))
                print("--------------------- End --------------------------")
                print("======================================== END ===========================================")
                print()
                print()
        except Exception as e:
                print(str(e))



def StoragePermission_demo():
        try:
                o = Tokens.StoragePermission()
                print("StoragePermission - Demo")
                print("======================================== START ===========================================")
                print()
                token = o.create_token(
                                "User1", 
                                "user@mail.com", 
                                "user-1",
                                "http://portreto.com/eikona1", 
                                "eikona-id-1", 
                                "onomaeikonas", 
                                None
                        )
                print("Token created:")
                print("------------------- Start --------------------------")
                print(token)
                print("--------------------- End --------------------------")
                print()
                print()
                payload = o.decode_token(token, config.STORAGE_SERVICE)
                print("User Decoded Payload:")
                print("------------------- Start --------------------------")
                import pprint
                print(pprint.pprint(payload))
                print("--------------------- End --------------------------")
                print("======================================== END ===========================================")
                print()
                print()
        except Exception as e:
                print(str(e))

#CreateUser_demo()
#UserIdentity_demo()
#StoragePermission_demo()
AuthUser_demo()