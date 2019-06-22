import requests
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
def get_gallery(requsername=None,id=None,username=None):
    url = base_url+'/basic/gallery'
    params = append_params(requsername=requsername, username=username)

    if id is not None:
        url += "/" + str(id)

    r = requests.get(url,params=params)
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

def get_gallery_reaction(requsername=None,id=None,galleryid=None):
    params = append_params(requsername=requsername, galleryid=galleryid)
    url = base_url+'/basic/gallery_reactions'
    if id is not None:
        url += "/" + str(id)

    r = requests.get(url,params=params)
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

def get_photo(requsername=None,id=None,galleryid=None):
    params = append_params(requsername=requsername, galleryid=galleryid)
    params={}
    url = base_url+'/basic/photos'
    if id is not None:
        url += "/" + str(id)

    r = requests.get(url,params=params)
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

def get_photo_reaction(requsername=None, id=None, photoid=None):
    params = append_params(requsername=requsername, photoid=photoid)
    url = base_url+'/basic/photo_reactions'
    if id is not None:
        url += "/" + str(id)

    r = requests.get(url,params=params)
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

def get_gallery_comment(requsername=None,id=None,galleryid=None):
    params = append_params(requsername=requsername, galleryid=galleryid)
    url = base_url+'/basic/gallery_comments'
    if id is not None:
        url += "/" + str(id)

    r = requests.get(url,params=params)
    data = r.json()

    # Data is a single object, make it iterable
    if id is not None: data = [data]
    objects=[]

    for dt in data:
        serializer = GalleryCommentSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_photo_comment(requsername=None, id=None, photoid=None):
    params = append_params(requsername=requsername, photoid=photoid)
    url = base_url+'/basic/photo_comments'
    if id is not None:
        url += "/" + str(id)
    r = requests.get(url,params=params)
    data = r.json()

    # Data is a single object, make it iterable
    if id is not None: data = [data]
    objects=[]

    for dt in data:
        serializer = PhotoCommentSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_follow(id=None,requsername=None,FC_1_Username=None,FC_2_Username=None):
    params = append_params(requsername=requsername, FC_1_Username=FC_1_Username,FC_2_Username=FC_2_Username)

    url = base_url+'/basic/follows'
    if id is not None:
        url += "/" + str(id)

    r = requests.get(url,params=params)
    data = r.json()

    # Data is a single object, make it iterable
    if id is not None: data = [data]
    objects=[]

    for dt in data:
        serializer = FollowSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_profile(id=None,username=None):
    params = append_params(username=username)
    url = base_url+'/basic/profiles'
    if id is not None:
        url += "/" + str(id)

    r = requests.get(url, params=params)
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

def get_user(id=None,username=None):
    params = append_params(username=username)

    url = base_url+'/basic/users'
    if id is not None:
        url += "/" + str(id)

    r = requests.get(url, params=params)
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

def get_shared_galleries(requsername):
    params = append_params(requsername=requsername)
    url = base_url+'/advanced/shared_galleries'
    r = requests.get(url,params=params)
    data = r.json()
    objects=[]

    for dt in data:
        serializer = GalleryDeserializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_followers(username):
    params = append_params(username=username)
    url = base_url+'/advanced/followers'
    r = requests.get(url,params=params)
    data = r.json()

    objects=[]

    for dt in data:
        serializer = UserSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_followers_profiles(username):
    params = append_params(username=username)
    url = base_url+'/advanced/followers_profiles'
    r = requests.get(url,params=params)
    data = r.json()

    objects=[]

    for dt in data:
        serializer = ProfileDeserializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_following(username):
    params = append_params(username=username)
    url = base_url+'/advanced/following'
    r = requests.get(url,params=params)
    data = r.json()

    objects=[]

    for dt in data:
        serializer = UserSerializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_following_profiles(username):
    params = append_params(username=username)
    url = base_url+'/advanced/following'
    r = requests.get(url,params=params)
    data = r.json()

    objects=[]

    for dt in data:
        serializer = ProfileDeserializer(data=dt)
        serializer.is_valid()
        obj = serializer.create()
        objects.append(obj)
    return objects

def get_search_profiles(query):
    params = append_params(query=query)
    url = base_url+'/advanced/profile_search'
    r = requests.get(url,params=params)
    data = r.json()

    objects=[]

    for dt in data:
        serializer = ProfileDeserializer(data=dt)
        serializer.is_valid()

        obj = serializer.create()
        objects.append(obj)

    return objects

def photo_reaction_toggle(requsername,photoid):
    params = append_params(requsername=requsername,photoid=photoid)
    url = base_url+'/photo_reaction_toggle'
    r = requests.get(url,params=params)
    return r

def gallery_reaction_toggle(requsername, galleryid):
    params = append_params(requsername=requsername,galleryid=galleryid)
    url = base_url+'/gallery_reaction_toggle'
    r = requests.get(url,params=params)
    return r

# Post API
def post_gallery(object,requsername):
    params = append_params(requsername=requsername)
    serializer = GallerySerializer(object)

    data = serializer.data
    data["GalleryOwner"]=object.GalleryOwner.username

    r = requests.post(base_url + '/basic/gallery/', data=data, params=params, files=dict(AlbumCover=object.AlbumCover))
    return r

def post_gallery_reaction(object,requsername):
    params = append_params(requsername=requsername)
    serializer = GalleryReactionSerializer(object)
    return requests.post(base_url + '/basic/gallery_reactions/', data=serializer.data ,params=params)

def post_photo(object,requsername):
    params = append_params(requsername=requsername)
    serializer = PhotoSerializer(object)

    r = requests.post(base_url + '/basic/photos/', data=serializer.data, params=params, files=dict(Photo=object.Photo))

    return r

def post_photo_reaction(object,requsername):
    params = append_params(requsername=requsername)
    serializer = PhotoReactionSerializer(object)
    return requests.post(base_url + '/basic/photo_reactions/', data=serializer.data, params=params)

def post_gallery_comment(object,requsername):
    params = append_params(requsername=requsername)
    serializer = GalleryCommentSerializer(object)
    return requests.post(base_url + '/basic/gallery_comments/', data=serializer.data, params=params)

def post_photo_comment(object,requsername):
    params = append_params(requsername=requsername)
    serializer = PhotoCommentSerializer(object)
    return requests.post(base_url + '/basic/photo_comments/', data=serializer.data, params=params)

def post_follow(object,requsername):
    params = append_params(requsername=requsername)
    serializer = FollowSerializer(object)
    response = requests.post(base_url + '/basic/follows/', data=serializer.data, params=params)
    return response

def post_profile(object,requsername):
    params = append_params(requsername=requsername)
    serializer = ProfileSerializer(object)
    return requests.post(base_url + '/basic/profiles/', data=serializer.data, params=params, files=dict(ProfilePhoto=object.ProfilePhoto))

def post_user(object,requsername):
    params = append_params(requsername=requsername)
    serializer = UserSerializer(object)
    return requests.post(base_url + '/basic/users/', data=serializer.data, params=params)

# Put API
def put_gallery(object,requsername):
    params = append_params(requsername=requsername)
    serializer = GallerySerializer(object)
    return requests.put(base_url + '/basic/gallery/'+str(object.id)+"/", data=serializer.data, params=params, files=dict(AlbumCover=object.AlbumCover))

def put_gallery_reaction(object,requsername):
    params = append_params(requsername=requsername)
    serializer = GalleryReactionSerializer(object)
    return requests.put(base_url + '/basic/gallery_reactions/'+str(object.id)+"/", data=serializer.data, params=params)

def put_photo(object,requsername):
    params = append_params(requsername=requsername)
    serializer = PhotoSerializer(object)
    return requests.put(base_url + '/basic/photos/'+str(object.id)+"/", data=serializer.data, params=params, files=dict(Photo=object.Photo))

def put_photo_reaction(object,requsername):
    params = append_params(requsername=requsername)
    serializer = PhotoReactionSerializer(object)
    return requests.put(base_url + '/basic/photo_reactions/'+str(object.id)+"/", data=serializer.data, params=params)

def put_gallery_comment(object,requsername):
    params = append_params(requsername=requsername)
    serializer = GalleryCommentSerializer(object)
    return requests.put(base_url + '/basic/gallery_comments/'+str(object.id)+"/", data=serializer.data, params=params)

def put_photo_comment(object,requsername):
    params = append_params(requsername=requsername)
    serializer = PhotoCommentSerializer(object)
    return requests.put(base_url + '/basic/photo_comments/'+str(object.id)+"/", data=serializer.data, params=params)

def put_follow(object,requsername):
    params = append_params(requsername=requsername)
    serializer = FollowSerializer(object)
    return requests.put(base_url + '/basic/follows/'+str(object.id)+"/", data=serializer.data, params=params)

def put_profile(object,requsername):
    params = append_params(requsername=requsername)
    serializer = ProfileSerializer(object)
    response = requests.put(base_url + '/basic/profiles/'+str(object.id)+"/", data=serializer.data, params=params,files=dict(ProfilePhoto=object.ProfilePhoto))
    print("\n\n PUUUUUUUUUUUUUUUUUUUUUUUUUUUUT :  \n\n")
    print("\n\nRESPONSE" + "=" * 80+"\n"+str(response))
    return response

def put_user(object,requsername):
    params = append_params(requsername=requsername)
    serializer = UserSerializer(object)
    return requests.post(base_url + '/basic/users/'+str(object.id)+"/", data=serializer.data, params=params)

# Delete API
def delete_gallery(id,requsername):
    params = append_params(requsername=requsername)
    return requests.delete(base_url + '/basic/gallery/' + str(id)+"/", params=params)

def delete_gallery_reaction(id,requsername):
    params = append_params(requsername=requsername)
    return requests.delete(base_url + '/basic/gallery_reactions/' + str(id)+"/", params=params)

def delete_photo(id,requsername):
    params = append_params(requsername=requsername)
    return requests.delete(base_url + '/basic/photos/' + str(id)+"/", params=params)

def delete_photo_reaction(id,requsername):
    params = append_params(requsername=requsername)
    return requests.delete(base_url + '/basic/photo_reactions/' + str(id)+"/", params=params)

def delete_gallery_comment(id,requsername):
    params = append_params(requsername=requsername)
    return requests.delete(base_url + '/basic/gallery_comments/' + str(id)+"/", params=params)

def delete_photo_comment(id,requsername):
    params = append_params(requsername=requsername)
    return requests.delete(base_url + '/basic/photo_comments/' + str(id)+"/", params=params)

def delete_follow(id,requsername):
    params = append_params(requsername=requsername)
    return requests.delete(base_url + '/basic/follows/' + str(id)+"/", params=params)