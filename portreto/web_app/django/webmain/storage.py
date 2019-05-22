from django.core.files.storage import Storage
from django.db import models

from urllib.request import urlopen
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
import requests
import os
from django.utils.deconstruct import deconstructible

import random
import string

from django.conf import settings
from kazoo.client import KazooClient, KazooState
import yaml
import logging
from django.contrib import admin

import hashlib

class FileEntry(models.Model):
    name = models.TextField()
    storage_1_ID = models.TextField()
    storage_2_ID = models.TextField()

    def __str__(self):
        return self.name

admin.site.register(FileEntry)

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

#For sending and reading zookeeper values
def dict_to_bytes(the_dict):
    b = bytes(yaml.dump(the_dict), 'utf-8')
    return b

def bytes_to_dict(the_binary):
    d = yaml.load(the_binary)
    return d

logging.basicConfig(level=logging.DEBUG)

# Connect to zookeeper
zk = KazooClient(hosts=settings.ZOOCLIENTS)
zk.start()



# Listen to connection
def zklistener(state):
    if state == KazooState.LOST:
        print("Zookeeper Connection Lost")
    elif state == KazooState.SUSPENDED:
        print("Zookeeper Connection Suspended")
    else:
        print("Zookeeper Connected")
zk.add_listener(zklistener)

# Add watcher for hashing key
@zk.DataWatch("/storage")
def watch_node(data, stat):
    settings.GLOBALS["hash_key"] = data.decode("utf-8")

# Add watcher for storage hosts
@zk.ChildrenWatch("/storage")
def watch_children(children):
    if len(children) >0:
        hosts = {}
        for child in children:
            temp_dict = bytes_to_dict(zk.get("/storage/"+child)[0])
            host={temp_dict["ID"]:{'hostname' : temp_dict["hostname"], 'ext_url' : temp_dict["EXT_URL"]}}
            hosts.update(host.copy())
        settings.GLOBALS["hosts"]=hosts

@deconstructible
class ExternalStorage(Storage):
    def __init__(self, key=None):
        if not key:
            key = settings.GLOBALS["hash_key"]
    def _open(self, name, mode='rb'):
        # print("OPENING"+"#"*60)
        # get url
        url = self.url(name=name,internal=True)
        # create temporary image
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(url).read())
        img_temp.flush()
        # return it
        return File(img_temp)

    # Store files in storage servers
    def _save(self, name, content):
        # open image
        data = content.open().read()
        # create content for http post request
        files = {'file': (name, data, "image/jpg", None)}
        # calculate security hash
        hash_object = hashlib.sha256(bytes(settings.GLOBALS["hash_key"], 'utf-8'))
        hash = hash_object.hexdigest()

        # Try to pick 2 random servers
        try:
            servers = random.sample(list(settings.GLOBALS["hosts"]), k=2)
            # Create file entry
            fileInstance = FileEntry(name=name,storage_1_ID=servers[0],storage_2_ID=servers[1])

            #send to second server
            hostname = settings.GLOBALS["hosts"][servers[1]]["hostname"]
            # generate storage server url
            url = "http://" + hostname + "/api/?hash=" + hash
            # send file to storage server
            requests.post(url, files=files)

        # Just use one
        except ValueError:
            servers = list(settings.GLOBALS["hosts"])[0]
            # Create file entry
            fileInstance = FileEntry(name=name,storage_1_ID=servers[0],storage_2_ID=None)

        finally:
            # send to first
            hostname = settings.GLOBALS["hosts"][servers[0]]["hostname"]
            # generate storage server url
            url = "http://" + hostname + "/api/?hash=" + hash
            # send files to storage server
            requests.post(url, files=files)
            # save file instance
            fileInstance.save()

        return name

    # Get url for image
    def url(self, name=None, internal=False):
        # get file instance
        try:
            fileInstance = FileEntry.objects.get(name=name)
        except:
            return
        # get storage IDs for file
        ID=[fileInstance.storage_1_ID,fileInstance.storage_2_ID]

        # calculate security hash
        hash_object = hashlib.sha256(bytes(name + settings.GLOBALS["hash_key"], 'utf-8'))
        hash = hash_object.hexdigest()

        # Try to find external urls for each server ID
        urls=[]
        hostnames = []
        for i in ID:
            try:
                urls.append(settings.GLOBALS["hosts"][i]["ext_url"])
                hostnames.append(settings.GLOBALS["hosts"][i]["hostname"])
            except:
                continue

        # Select and return a url randomly
        try:
            ext_url = random.choice(urls)
            hostname = random.choice(hostnames)
            if internal:
                url = 'http://' + hostname+'/api/?image=' + name + '&hash=' + hash
            else :
                url = ext_url+'/api/?image=' + name + '&hash=' + hash
            return url
        except:
            return ""

    def generate_filename(self, filename="default_filename.jpg"):
        """
        Validate the filename by calling get_valid_name() and return a filename
        to be passed to the save() method.
        """
        # `filename` may include a path as returned by FileField.upload_to.
        dirname, filename = os.path.split(filename)
        return filename

    def exists(self,name):
        return False

    def path(self, name):
        return name

    def get_available_name(self, name, max_length=None):
        # generate random names and make sure there are no duplicates
        extension = name.split('.')[-1]
        rand_name = randomString(stringLength=20) + '.'+extension
        while len(FileEntry.objects.filter(name=rand_name)) > 0 :
            rand_name = randomString(stringLength=20) + '.'+extension
        return rand_name

    # Delete images from all servers they are saved
    def delete(self,name):
        # get file instance
        fileInstance = FileEntry.objects.get(name=name)
        # get storage IDs for file
        ID=[fileInstance.storage_1_ID, fileInstance.storage_2_ID]

        # calculate security hash
        hash_object = hashlib.sha256(bytes(settings.GLOBALS["hash_key"], 'utf-8'))
        hash = hash_object.hexdigest()

        for i in ID :
            if i is not None:
                host = settings.GLOBALS["hosts"][i]["hostname"]
                url = 'http://' + host + '/api/?image=' + name + '&hash=' + hash
                requests.delete(url)

        # Finaly delete file entry
        FileEntry.objects.get(name=name).delete()

        return name

    def size(self,name):
        return name