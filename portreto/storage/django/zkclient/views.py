from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from kazoo.client import KazooClient
from kazoo.client import KazooState
import logging
import socket
import yaml

#For sending and reading zookeeper values
def dict_to_bytes(the_dict):
    b = bytes(yaml.dump(the_dict), 'utf-8')
    return b

def bytes_to_dict(the_binary):
    d = yaml.load(the_binary)
    return d

logging.basicConfig(level=logging.DEBUG)

# Connecto to zookeeper
zk = KazooClient(hosts="zoo1:2181,zoo2:2181,zoo3:2181")
zk.start()



# def zklistener(state):
#     if state == KazooState.LOST:
#         zkstate = "LOST"
#         # Register somewhere that the session was lost
#     elif state == KazooState.SUSPENDED:
#         zkstate = "SUSPENDED"
#         # Handle being disconnected from Zookeeper
#     else:
#         zkstate = "CONNECTED"
#         # Handle being connected/reconnected to Zookeeper


# zk.add_listener(zklistener)

print("zk client started")
print("Storage_ID: "+str(settings.FS_ID))

zkdata = {
    "ID" : settings.FS_ID,
    "hostname" : socket.gethostname()
}

# Make sure path exists
zk.ensure_path("/storage")

# Make (or update) an entity in zookeeper about yourself
if zk.exists("/storage/storage_"+str(settings.FS_ID)) != None:
    zk.set("/storage/storage_"+str(settings.FS_ID),dict_to_bytes(zkdata))
else:
    zk.create("/storage/storage_"+str(settings.FS_ID),dict_to_bytes(zkdata))

nodes = zk.get_children("/storage/")
for n in nodes:
    print(n)
    print(bytes_to_dict(zk.get("/storage/"+n)[0]))

# Create your views here.
def index(request):
    ID = settings.FS_ID
    responce = "Storage server ID: " + str(ID) + " SK State: " + str(zk.state)
    return HttpResponse(responce)