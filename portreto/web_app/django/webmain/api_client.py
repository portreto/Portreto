import requests
from rest_framework.utils import json

from .serializers import *

base_url="http://appservice/api"

def append_params(**kwargs):
    params = {}
    if kwargs is not None:
        for key, value in kwargs.items():
            if value is not None:
                params[key]=value;

    return params;

# Basic API
def get_gallery(requsername=None,id=None,username=None,token=None):
    url = base_url+'/basic/gallery/'
    params = append_params(requsername=requsername, username=username)
    
    if id is not None:
        url += str(id) + '/'

    headers= {"TOKEN":token}
    r = requests.get(url, params=params, data='token='+token,headers=headers)

    data = r.json()

    # Data is a single object, make it iterable
    if id is not None: data=[data]

    objects=[]
    for dt in data:
        serializer = GalleryDeserializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)

    return objects

def get_gallery_reaction(requsername=None,id=None,galleryid=None,token=None):
    params = append_params(requsername=requsername, galleryid=galleryid)
    url = base_url+'/basic/gallery_reactions/'
    if id is not None:
        url += str(id) + '/'

    headers= {"TOKEN":token}

    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    # Data is a single object, make it iterable
    if id is not None: data = [data]
    objects=[]

    for dt in data:
        serializer = GalleryReactionSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_photo(requsername=None,id=None,galleryid=None,token=None):
    params = append_params(requsername=requsername, galleryid=galleryid)
    url = base_url+'/basic/photos/'
    if id is not None:
        url += str(id) + '/'

    headers= {"TOKEN":token}

    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    # Data is a single object, make it iterable
    if id is not None: data = [data]
    objects=[]

    for dt in data:
        serializer = PhotoDeserializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_photo_reaction(requsername=None, id=None, photoid=None,token=None):
    params = append_params(requsername=requsername, photoid=photoid)
    url = base_url+'/basic/photo_reactions/'
    if id is not None:
        url += str(id) + '/'

    headers= {"TOKEN":token}

    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    # Data is a single object, make it iterable
    if id is not None: data = [data]
    objects=[]

    for dt in data:
        serializer = PhotoReactionSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_gallery_comment(requsername=None,id=None,galleryid=None,token=None):
    params = append_params(requsername=requsername, galleryid=galleryid)
    url = base_url+'/basic/gallery_comments/'
    if id is not None:
        url += str(id) + '/'

    headers= {"TOKEN":token}

    r = requests.get(url, params=params, headers=headers)
    data = r.json()



    # Data is a single object, make it iterable
    if id is not None: data = [data]
    objects=[]



    for dt in data:

        serializer = GalleryCommentDeserializer(data=dt)

        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_photo_comment(requsername=None, id=None, photoid=None,token=None):
    params = append_params(requsername=requsername, photoid=photoid)
    url = base_url+'/basic/photo_comments/'
    if id is not None:
        url += str(id) + '/'
    headers= {"TOKEN":token}

    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    # Data is a single object, make it iterable
    if id is not None: data = [data]
    objects=[]

    for dt in data:
        serializer = PhotoCommentDeserializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_follow(id=None,FC_1_Username=None,FC_2_Username=None,token=None):
    params = append_params(fc1username=FC_1_Username,fc2username=FC_2_Username)

    url = base_url+'/basic/follows/'
    if id is not None:
        url += str(id) + '/'

    headers= {"TOKEN":token}

    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    if id is not None: data = [data]
    objects=[]

    for dt in data:
        serializer = FollowSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_profile(id=None,username=None,token=None):
    params = append_params(username=username)
    url = base_url+'/basic/profiles/'
    if id is not None:
        url += str(id) + '/'

    headers= {"TOKEN":token}

    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    # Data is a single object, make it iterable
    if id is not None: data = [data]
    objects=[]


    for dt in data:
        serializer = ProfileDeserializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)

    return objects

def get_user(id=None,username=None,token=None):
    params = append_params(username=username)

    url = base_url+'/basic/users/'
    if id is not None:
        url += str(id) + '/'

    headers= {"TOKEN":token}

    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    # Data is a single object, make it iterable
    if id is not None: data = [data]
    objects=[]

    for dt in data:
        serializer = UserSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

#Advance API

def get_shared_galleries(requsername,token=None):
    params = append_params(requsername=requsername)
    url = base_url+'/advanced/shared_galleries/'
    reqdata = {
        'token': token,
    }

    print("\n\n" + "=" * 160 + "\nREQUEST SHARE GALLERY\n" +  "=" * 160)

    headers= {"TOKEN":token}

    r = requests.get(url, params=params, headers=headers)
    data = r.json()
    objects=[]

    for dt in data:
        serializer = GalleryDeserializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_followers(username,token=None):
    params = append_params(username=username)
    url = base_url+'/advanced/followers/'
    headers= {"TOKEN":token}

    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    objects=[]

    for dt in data:
        serializer = UserSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_followers_profiles(username,token=None):
    params = append_params(username=username)
    url = base_url+'/advanced/followers_profiles/'
    headers= {"TOKEN":token}

    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    objects=[]

    for dt in data:
        serializer = ProfileDeserializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_following(username,token=None):
    params = append_params(username=username)
    url = base_url+'/advanced/following/'
    headers= {"TOKEN":token}

    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    objects=[]

    for dt in data:
        serializer = UserSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_following_profiles(username,token=None):
    params = append_params(username=username)
    url = base_url+'/advanced/following/'
    headers= {"TOKEN":token}

    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    objects=[]

    for dt in data:
        serializer = ProfileDeserializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_search_profiles(query,token=None):
    params = append_params(query=query)
    url = base_url+'/advanced/profile_search/'
    headers= {"TOKEN":token}

    r = requests.get(url, params=params, headers=headers)
    data = r.json()

    objects=[]

    for dt in data:
        serializer = ProfileDeserializer(data=dt)
        serializer.is_valid()

        obj = serializer.create()
        objects.append(obj)

    return objects

def photo_reaction_toggle(requsername,photoid,token=None):
    params = append_params(requsername=requsername,photoid=photoid)
    url = base_url+'/photo_reaction_toggle/'
    headers= {"TOKEN":token}

    r = requests.get(url, params=params, headers=headers)
    return r

def gallery_reaction_toggle(requsername, galleryid,token=None):
    params = append_params(requsername=requsername,galleryid=galleryid)
    url = base_url+'/gallery_reaction_toggle/'
    headers= {"TOKEN":token}

    r = requests.get(url, params=params, headers=headers)
    return r

# Post API
def post_gallery(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = GallerySerializer(object)
    data = serializer.data
    data["GalleryOwner"]=object.GalleryOwner.username
    headers = {"TOKEN": token}

    r = requests.post(base_url + '/basic/gallery/', data=data, params=params,headers=headers, files=dict(AlbumCover=object.AlbumCover))
    return r

def post_gallery_reaction(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = GalleryReactionSerializer(object)
    data=serializer.data
    headers = {"TOKEN": token}
    return requests.post(base_url + '/basic/gallery_reactions/', data=data ,params=params,headers=headers)

def post_photo(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = PhotoSerializer(object)
    data=serializer.data
    headers = {"TOKEN": token}
    r = requests.post(base_url + '/basic/photos/', data=data, params=params,headers=headers, files=dict(Photo=object.Photo))

    return r

def post_photo_reaction(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = PhotoReactionSerializer(object)
    data=serializer.data
    headers = {"TOKEN": token}
    return requests.post(base_url + '/basic/photo_reactions/', data=data, params=params,headers=headers)

def post_gallery_comment(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = GalleryCommentSerializer(object)
    data=serializer.data
    headers = {"TOKEN": token}
    return requests.post(base_url + '/basic/gallery_comments/', data=data, params=params,headers=headers)

def post_photo_comment(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = PhotoCommentSerializer(object)
    data=serializer.data
    headers = {"TOKEN": token}
    return requests.post(base_url + '/basic/photo_comments/', data=data, params=params,headers=headers)

def post_follow(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = FollowSerializer(object)
    data=serializer.data
    headers = {"TOKEN": token}
    response = requests.post(base_url + '/basic/follows/', data=data, params=params,headers=headers)
    return response

def post_profile(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = ProfileSerializer(object)
    data=serializer.data
    headers = {"TOKEN": token}
    return requests.post(base_url + '/basic/profiles/', data=data, params=params,headers=headers, files=dict(ProfilePhoto=object.ProfilePhoto))

def post_user(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = UserSerializer(object)
    data=serializer.data
    headers = {"TOKEN": token}
    return requests.post(base_url + '/basic/users/', data=data, params=params,headers=headers)

# Put API
def put_gallery(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = GallerySerializer(object)
    data=serializer.data
    headers = {"TOKEN": token}
    return requests.put(base_url + '/basic/gallery/'+str(object.id)+"/", data=data, params=params,headers=headers, files=dict(AlbumCover=object.AlbumCover))

def put_gallery_reaction(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = GalleryReactionSerializer(object)
    data=serializer.data
    headers = {"TOKEN": token}
    return requests.put(base_url + '/basic/gallery_reactions/'+str(object.id)+"/", data=data, params=params,headers=headers)

def put_photo(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = PhotoSerializer(object)
    data=serializer.data
    headers = {"TOKEN": token}
    return requests.put(base_url + '/basic/photos/'+str(object.id)+"/", data=data, params=params,headers=headers, files=dict(Photo=object.Photo))

def put_photo_reaction(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = PhotoReactionSerializer(object)
    data=serializer.data
    headers = {"TOKEN": token}
    return requests.put(base_url + '/basic/photo_reactions/'+str(object.id)+"/", data=data, params=params,headers=headers)

def put_gallery_comment(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = GalleryCommentDeserializer(object)
    data=serializer.data
    headers = {"TOKEN": token}
    return requests.put(base_url + '/basic/gallery_comments/'+str(object.id)+"/", data=data, params=params,headers=headers)

def put_photo_comment(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = PhotoCommentDeserializer(object)
    data=serializer.data
    headers = {"TOKEN": token}
    return requests.put(base_url + '/basic/photo_comments/'+str(object.id)+"/", data=data, params=params,headers=headers)

def put_follow(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = FollowSerializer(object)
    data=serializer.data
    headers = {"TOKEN": token}
    return requests.put(base_url + '/basic/follows/'+str(object.id)+"/", data=data, params=params,headers=headers)

def put_profile(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = ProfileSerializer(object)
    # print("\n\n" + "=" * 160 + "\nPUT PROFILE OBJECT \n" + str(object) + "\n" + "=" * 160)
    # print("\n\n" + "=" * 160 + "\nPUT PROFILE PHOTO OBJECT \n" + str(object.ProfilePhoto) + "\n" + "=" * 160)
    data = serializer.data
    # print("\n\n" + "=" * 160 + "\nPUT PROFILE DATA \n" + str(data) + "\n" + "=" * 160)
    # print("\n\n" + "=" * 160 + "\nPUT PROFILE IMAGE FILE TYPE \n" + str(type(object.ProfilePhoto)) + "\n" + "=" * 160)


    if len(str(object.ProfilePhoto))>1:
        files = dict(ProfilePhoto=object.ProfilePhoto)
    else:
        files = None
    headers = {"TOKEN": token}


    response = requests.put(base_url + '/basic/profiles/'+str(object.id)+"/", data=data, params=params,headers=headers,files=files)

    return response

def put_user(object,requsername,token=None):
    params = append_params(requsername=requsername)
    serializer = UserSerializer(object)
    data = serializer.data
    headers = {"TOKEN": token}
    return requests.put(base_url + '/basic/users/'+str(object.id)+"/", data=data, params=params,headers=headers)

# Delete API
def delete_gallery(id,requsername,token=None):
    params = append_params(requsername=requsername)
    headers= {"TOKEN":token}
    return requests.delete(base_url + '/basic/gallery/' + str(id)+"/", params=params,headers=headers)

def delete_gallery_reaction(id,requsername,token=None):
    params = append_params(requsername=requsername)
    headers= {"TOKEN":token}
    return requests.delete(base_url + '/basic/gallery_reactions/' + str(id)+"/", params=params,headers=headers)

def delete_photo(id,requsername,token=None):
    params = append_params(requsername=requsername)
    headers= {"TOKEN":token}
    return requests.delete(base_url + '/basic/photos/' + str(id)+"/", params=params,headers=headers)

def delete_photo_reaction(id,requsername,token=None):
    params = append_params(requsername=requsername)
    headers= {"TOKEN":token}
    return requests.delete(base_url + '/basic/photo_reactions/' + str(id)+"/", params=params,headers=headers)

def delete_gallery_comment(id,requsername,token=None):
    params = append_params(requsername=requsername)
    headers= {"TOKEN":token}
    return requests.delete(base_url + '/basic/gallery_comments/' + str(id)+"/", params=params,headers=headers)

def delete_photo_comment(id,requsername,token=None):
    params = append_params(requsername=requsername)
    headers= {"TOKEN":token}
    return requests.delete(base_url + '/basic/photo_comments/' + str(id)+"/", params=params,headers=headers)

def delete_follow(id,requsername,token=None):
    params = append_params(requsername=requsername)
    headers= {"TOKEN":token}
    return requests.delete(base_url + '/basic/follows/' + str(id)+"/", params=params,headers=headers)