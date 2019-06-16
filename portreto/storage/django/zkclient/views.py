from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from kazoo.client import KazooClient
from kazoo.client import KazooState
import logging
import socket
import yaml
import random
import string

# Random String Generator
def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.digits + string.ascii_letters
    return bytes(''.join(random.choice(letters) for i in range(stringLength)), 'utf-8')

#For sending and reading zookeeper values
def dict_to_bytes(the_dict):
    b = bytes(yaml.dump(the_dict), 'utf-8')
    return b
def bytes_to_dict(the_binary):
    d = yaml.load(the_binary)
    return d

logging.basicConfig(level=logging.DEBUG)

# Connect to zookeeper
zk = KazooClient(hosts="zoo1:2181,zoo2:2181,zoo3:2181")
zk.start()

# Listen to connection
def zklistener(state):
    if state == KazooState.LOST:
        print("Zookeeper Connection Lost")
    elif state == KazooState.SUSPENDED:
        print("Zookeeper Connection Suspended")
    else:
        #Create personal ZNode
        try:
            zk.delete("/storage/storage_"+str(settings.FS_ID))
        except:
            pass
        finally:
            zk.create("/storage/storage_"+str(settings.FS_ID),dict_to_bytes(zkdata), ephemeral=True)
        print("Zookeeper Connected AND UPDATED")

# Make sure path exists
zk.ensure_path("/storage")
# Add listener
zk.add_listener(zklistener)
# Add watcher for hashing key
@zk.DataWatch("/storage")
def watch_node(data, stat):
    print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))
    settings.GLOBALS["hash_key"] = data.decode("utf-8")


# Data for personal zNode
zkdata = {
    "ID" : settings.FS_ID,
    "hostname" : socket.gethostname(),
    "EXT_URL" : settings.EXT_URL
}

# Update Hash Key
zk.set("/storage", randomString(30))
#Create personal ZNode
try:
    zk.delete("/storage/storage_"+str(settings.FS_ID))
except:
    pass
finally:
    zk.create("/storage/storage_"+str(settings.FS_ID),dict_to_bytes(zkdata), ephemeral=True)
# Add listener
zk.add_listener(zklistener)


print("EXISTS------------------------------------------------------------------------------")
print(zk.exists("/storage/storage_"+str(settings.FS_ID)))



# index page
def index(request):
    ID = settings.FS_ID
    responce = "<HEAD><TITLE>Storage Server</TITLE></HEAD>" \
               "<BODY><H1> Storage Server " + "</H1>"+ \
               "<P> Storage server ID: " + str(ID) + "</P>"+ \
               "<P> ZK State: " + str(zk.state) + "</P></BODY>" \
               "<P> Hostname: " + socket.gethostname() + "</P></BODY>"
               
    return HttpResponse(responce)