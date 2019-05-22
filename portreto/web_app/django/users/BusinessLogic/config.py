
#        Sensitive variables for Security
# --------------------------------------------
# TODO : Key from Zookeeper
AES_KEY = 'uxuR8hD4sLS92ebmaWy0bdGOKGuTnGiy'
SALT = 'Zl6UsIWcV4NGWRhn'
BS = 16
# --------------------------------------------



#        Sensitive variables for Tokens
# --------------------------------------------
# TODO : Key from Zookeeper
SECRET_KEY= 'vt8X9rEvwfnbQ1Fn'

LOGIN_TOKEN_EXPIRE_AFTER=30
CREATE_USER_TOKEN_EXPIRE_AFTER=1
USER_ID_TOKEN_EXPIRE_AFTER=30
STORAGE_TOKEN_EXPIRE_AFTER=10

ACTIONS = {
    "CU": "Create User If not exists"
}
# --------------------------------------------



#        For Tokens' Decoding
# --------------------------------------------
APPLICATION_SERVICE='app'
STORAGE_SERVICE='storage'
AUTHENTICATION_SERVICE='auth'
WEB_SERVICE='web'
# --------------------------------------------





#        For Error Codes
# --------------------------------------------
POST_REQUEST= '01'
USER_EXISTS= '60'
WRONG_CREDENTIALS= '50'
TOKENS=''
JSON_NEED=''
UNEXPECTED_ERROR='69'
NOT_ACCEPTED=''
OP_FAILED=''
# --------------------------------------------