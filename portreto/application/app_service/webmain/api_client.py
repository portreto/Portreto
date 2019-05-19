import requests
from .models import *
from api.serializers import *
from rest_framework.parsers import JSONParser

base_url="http://localhost:8000/api"


#def get gallery

def get_gallery_reaction(requsername=None,id=None,galleryid=None):
    params={}
    url = base_url+'/basic/gallery_reactions'
    if id is not None:
        url += "/" + str(id)
    if galleryid is not None:
        params["galleryid"]=galleryid
    if requsername is not None:
        params["requsername"] = requsername

    r = requests.get(url,params=params)
    data = r.json()

    if id is not None:
        d2 = data
        data = []
        data.append(d2)
    objects=[]

    for dt in data:
        serializer = GalleryReactionSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

#def get photo

def get_photo_reaction(requsername=None, id=None, photoid=None):
    params={}
    url = base_url+'/basic/photo_reactions'
    if id is not None:
        url += "/" + str(id)
    if photoid is not None:
        params["photoid"]=photoid
    if requsername is not None:
        params["requsername"] = requsername

    r = requests.get(url,params=params)
    data = r.json()

    if id is not None:
        d2 = data
        data = []
        data.append(d2)
    objects=[]

    for dt in data:
        serializer = PhotoReactionSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_gallery_comment(requsername=None,id=None,galleryid=None):
    params={}
    url = base_url+'/basic/gallery_comments'
    if id is not None:
        url += "/" + str(id)
    if galleryid is not None:
        params["galleryid"]=galleryid
    if requsername is not None:
        params["requsername"] = requsername

    r = requests.get(url,params=params)
    data = r.json()

    if id is not None:
        d2 = data
        data = []
        data.append(d2)
    objects=[]

    for dt in data:
        serializer = GalleryCommentSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_photo_comment(requsername=None, id=None, photoid=None):
    params={}
    url = base_url+'/basic/photo_comments'
    if id is not None:
        url += "/" + str(id)
    if photoid is not None:
        params["photoid"]=photoid
    if requsername is not None:
        params["requsername"] = requsername

    r = requests.get(url,params=params)
    data = r.json()

    if id is not None:
        d2 = data
        data = []
        data.append(d2)
    objects=[]

    for dt in data:
        serializer = PhotoReactionSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_follow(id=None,requsername=None):
    params={}
    url = base_url+'/basic/follows'
    if id is not None:
        url += "/" + str(id)
    if requsername is not None:
        params["requsername"] = requsername

    r = requests.get(url,params=params)
    data = r.json()

    if id is not None:
        d2 = data
        data = []
        data.append(d2)
    objects=[]

    for dt in data:
        serializer = FollowSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_profile(id=None,username=None):
    params={}
    url = base_url+'/basic/profiles'
    if id is not None:
        url += "/" + str(id)
    if username is not None:
        params["username"] = username

    r = requests.get(url)
    data = r.json()



    if id is not None:
        d2 = data
        data = []
        data.append(d2)
    objects=[]

    # print("\n\nDATA_PROFILES"+"="*40+"\n"+str(data)+"\n\n")
    for dt in data:
        serializer = ProfileDeserializer(data=dt)
        serializer.is_valid()
        # print("\n\nIS_VALID" + "=" * 40 + "\n" + str(serializer.errors) + "\n\n")
        obj = serializer.create()
        objects.append(obj)

    return objects

def get_user(id=None,username=None):
    params={}
    url = base_url+'/basic/users'
    if id is not None:
        url += "/" + str(id)
    if username is not None:
        params["username"] = username

    r = requests.get(url)
    data = r.json()

    if id is not None:
        d2 = data
        data = []
        data.append(d2)
    objects=[]

    for dt in data:
        serializer = UserSerializer(data=dt)
        serializer.is_valid()
        # print(serializer.errors)
        obj = serializer.create()
        objects.append(obj)
    return objects

#def get shared galleries

def get_followers(username):
    params={}
    url = base_url+'/advanced/followers'

    params["username"] = username

    r = requests.get(url,params=params)
    data = r.json()

    objects=[]

    for dt in data:
        serializer = UserSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

# def get_followers_profiles

def get_following(username):
    params={}
    url = base_url+'/advanced/following'

    params["username"] = username

    r = requests.get(url,params=params)
    data = r.json()

    objects=[]

    for dt in data:
        serializer = UserSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

# def get_following_profiles