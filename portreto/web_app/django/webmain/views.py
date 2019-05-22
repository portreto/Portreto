from django.shortcuts import render
from django.contrib import messages
from .models import Follow, GalleryComment, PhotoComment
from .forms import GalleryForm, PhotoForm
from django.contrib.auth.models import User
from . import api_client
from django.http import Http404
from users.UserConnection import *

def get_api_objects_or_404(objects):

    if len(objects) == 0:
        raise Http404('No matches the given query.')
    return objects

@my_login_required()
def home_view(request, username=None, token=None):
    requsername = username

    # People that have me as a friend can show me their photos
    galleries = api_client.get_shared_galleries(requsername=requsername)
    comments = api_client.get_gallery_comment()

    context = {
        'all_galleries': galleries,
        'comments': comments,
        'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername))[0]
    }

    return render(request, "webmain/index.html", context)

# Shows details of a specific gallery
@my_login_required()
def detail(request, gallery_id, username=None, token=None):
    requsername = username

    user = get_api_objects_or_404(api_client.get_user(username=requsername))[0]
    gallery = get_api_objects_or_404(api_client.get_gallery(id=gallery_id, requsername=requsername))[0]
    comments = api_client.get_gallery_comment(requsername=requsername,galleryid=gallery_id)
    photos = api_client.get_photo(requsername=requsername,galleryid=gallery_id)

    # print("\n\nDETAILS\n  "+str(gallery.GalleryOwner.username)+"\n  "+str(user.username))

    context = {
        'gallery': gallery,
        'user': user,
        'comments': comments,
        'photos' : photos,
        'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername))[0]
    }

    return render(request, 'webmain/detail.html', context)

# Shows details of a specific gallery
@my_login_required()
def photo_detail(request, gallery_id, photo_id, username=None, token=None):
    requsername = username

    gallery = get_api_objects_or_404(api_client.get_gallery(requsername=requsername, id=gallery_id))[0]
    comments = api_client.get_photo_comment(requsername=requsername,photoid=photo_id)

    photο = get_api_objects_or_404(api_client.get_photo(requsername=requsername,id=photo_id))[0]

    context = {
        'phot': photο,
        'gallery': gallery,
        'comments':comments,
        'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername))[0]
    }
        # return JsonResponse(data, safe=False)
        # return render(request, 'webmain/photo_detail.html', context)
    return render(request, 'webmain/photo_detail.html', context)

# Create a new gallery. NOTE: You cannot add two galleries with the same name
import base64

@my_login_required()
def create_gallery(request, username=None, token=None):
    requsername = username

    form = GalleryForm(request.POST or None, request.FILES or None)

    user = get_api_objects_or_404(api_client.get_user(username=requsername))[0]

    if form.is_valid():
        # form.GalleryOwner = user
        gallery = form.save(commit=False)

        user2 = User(id=user.id,username=user.username)
        gallery.GalleryOwner = user2

        responce = api_client.post_gallery(gallery, requsername)

        status_code = responce.status_code
        if status_code == 406:
            messages.error(request, 'You have already added a Gallery with the same name')

            print("\n\nALREADY ADDED" + "=" * 80 + "You have already added a Gallery with the same name\n\n")

            context = {
                'album': gallery,
                'form': form,
                'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername))[0]
            }
            return render(request, 'webmain/create_gallery.html', context)  # TODO CHANGE THAT. SHOW MESSAGE CORRECTLY
        elif status_code == 403:
            messages.error(request, 'Authorization Error')

            context = {
                'album': gallery,
                'form': form,
                'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername))[0]
            }
            return render(request, 'webmain/create_gallery.html', context)  # TODO CHANGE THAT. SHOW MESSAGE CORRECTLY

        messages.success(request, 'Form submission successful')
        # return redirect(request, 'webmain/index.html')    # TODO REDIRECT ANYWHERE YOu WISH?
        return redirect('users:profile')    # TODO REDIRECT ANYWHERE YOu WISH

    context = {
        "form": form,
        'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername))[0]
    }

    return render(request, 'webmain/create_gallery.html',context)

# Updates photo that belongs on a gallery. NOTE: Only if the requested user is the galleryowner an update can occur
@my_login_required()
def update_gallery(request, gallery_id, username=None, token=None):
    requsername = username

    # u_galleries = Gallery.objects.filter(id=gallery_id).first()
    u_galleries = get_api_objects_or_404(api_client.get_gallery(requsername=requsername,id=gallery_id))[0]

    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=u_galleries)  # request.files for images

        if form.is_valid():
            gallery = form.save(commit=False)
            api_client.put_gallery(gallery, requsername)
            messages.success(request, f'Your gallery has been updated')
            return redirect('webmain:detail', gallery_id)

    else:
        form = GalleryForm(instance=u_galleries)

    context = {
        "form": form,
        'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername))[0]
    }

    return render(request, 'webmain/create_gallery.html', context)


# Create a new photo. NOTE: You cannot add two photos with the same name
@my_login_required()
def add_photo(request, gallery_id, username=None, token=None):
    requsername = username

    form = PhotoForm(request.POST or None, request.FILES or None)
    gallery = get_api_objects_or_404(api_client.get_gallery(requsername=requsername,id=gallery_id))[0]

    if form.is_valid():
        photo = form.save(commit=False)
        photo.Gallery = gallery.id
        api_client.post_photo(photo, requsername)

        return redirect('webmain:detail', gallery_id)
    context = {
        'gallery': gallery,
        'form': form,
        'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername))[0]
    }
    return render(request, 'webmain/add_photo.html', context)

@my_login_required()
# Updates photo that belongs on a gallery. NOTE: Only if the requested user is the galleryowner an update can occur
def update_photo(request, gallery_id, photo_id, username=None, token=None):
    requsername = username

    gallery = get_api_objects_or_404(api_client.get_gallery(requsername=requsername,id=gallery_id))[0]

    u_photos = get_api_objects_or_404(api_client.get_photo(requsername=requsername, id=photo_id))[0]

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=u_photos)  # request.files for images

        if form.is_valid():
            form.save()
            photo = form.save(commit=False)
            api_client.put_photo(photo, requsername)

            messages.success(request, f'Your photo has been updated')
            return redirect('webmain:detail', gallery_id)
    else:
        form = PhotoForm(instance=u_photos)

    context = {
        'form': form,
        'gallery': gallery,
        'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername))[0]
    }

    return render(request, 'webmain/add_photo.html', context)


# Delete gallery. NOTE: Only the gallery owner has the permission to delete
@my_login_required()
def delete_gallery(request, gallery_id, username=None, token=None):
    requsername = username

    get_api_objects_or_404(api_client.get_gallery(requsername=requsername, id=gallery_id))[0]
    api_client.delete_gallery(requsername=requsername,id=gallery_id)
    # return render(request, 'webmain/index.html')    # TODO REDIRECT CORRECTLY

    return redirect('users:profile')

# Delete photo. NOTE: Only the gallery owner, in which the photo belongs has the permission to delete
@my_login_required()
def delete_photo(request, gallery_id, photo_id, username=None, token=None):
    requsername = username
    gallery = get_api_objects_or_404(api_client.get_gallery(requsername=requsername, id=gallery_id))[0]

    if request.user == gallery.GalleryOwner:
        messages.success(request, 'You can delete this photo')

        api_client.delete_photo(requsername=requsername, id=photo_id)

        messages.success(request, 'Photo successfully deleted ')

    else:
        messages.error(request, 'You cannot delete this photo')

    return redirect('webmain:detail',gallery_id)            # TODO REDIRECT ANYWHERE YOU WISH


# Follow and unfollow users. NOTE: Added condition so that you cannot follow or unfollow yourself
@my_login_required()
def follow(request, user_id, username=None, token=None):
    requsername = username

    user_follow = get_api_objects_or_404(api_client.get_user(id=user_id))[0]
    user = get_api_objects_or_404(api_client.get_user(username=requsername))[0]

    if user_follow.id == user.id:
        messages.error(request, 'You cannot follow yourself')

    else:
        check = api_client.get_follow(FC_1_Username=requsername,FC_2_Username=user_follow.username)

        #friendship existed
        if len(check) > 0:
            follow = check[0]
            print("\n\nFOLLOW" + "=" * 30 + str(follow))

            api_client.delete_follow(id=follow.id ,requsername=requsername)
            messages.success(request, 'Unshared Content ')

        # no friendship existed
        else:
            follow = Follow(FollowCond1=user.id, FollowCond2=user_follow.id,)
            api_client.post_follow(follow,requsername)
            messages.success(request, 'Shared Content')

    # return redirect('/' + str(id))
    return redirect('users:getProfile', user_follow.username)  # TODO FIX REDIRECTION


# TODO ADD LIKE COUNTER
# Like and unlike a gallery content. NOTE: ONLY friends of current user or the user himself can like
@my_login_required()
def like_gallery(request, gallery_id, username=None, token=None):
    requsername = username


    responce = api_client.gallery_reaction_toggle(requsername, gallery_id)

    status_code = responce.status_code

    if status_code == 302 :
        messages.success(request, 'Unliked ')
    elif status_code == 2001:
        messages.success(request, 'Liked')
    # count = getLike(postId)
    context = {
        'like_gallery': like_gallery,
        'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername))[0]
    }
    # return JsonResponse(data, safe=False)
    return redirect('webmain:detail', gallery_id)   #TODO CHECK REDIRECTION


# TODO ADD LIKE COUNTER
# Like and unlike a photo content. NOTE: ONLY friends of current user or the user himself can like
@my_login_required()
def like_photo(request, gallery_id, photo_id, username=None, token=None):
    requsername = username

    responce = api_client.photo_reaction_toggle(requsername,photo_id)

    status_code = responce.status_code

    if status_code == 302 :
        messages.success(request, 'Unliked ')
    elif status_code == 201:
        messages.success(request, 'Liked')
    # count = getLike(postId)
    # return JsonResponse(data, safe=False)
    return redirect('webmain:detail', gallery_id)   #TODO CHECK REDIRECTION


# This is a function to find if there is a friend connection between gallery owner and request user.
# Used in likes, comments.
# Returns boolean
def is_friend(request, user_id, username=None, token=None):
    friends = Follow.objects.filter(FollowCond2__id=request.user.id).filter(FollowCond1__id=user_id).all()

    if friends.count() == 0:
        return False

    return True

# Something like a like counter on photos. Not tested yet
# def num_photo_like(id):
#     like = PhotoReaction.objects.filter(p=id).count()
#     return like

# TODO ADD MORE FUNCTIONALITY. CURRENTY SUPPORTS ONLY SEARCH BASED ON USERNAME
# This is our search function
@my_login_required()
def search(request, username=None, token=None):

    # instance = User.objects.get(username=)
    # albums = Album.objects.filter(user=request.user)
    # song_results = Song.objects.all()

    query = request.GET.get("q")

    profiles = api_client.get_search_profiles(query=query)

    if query == "":
        messages.error(request, 'No Items to search ')
        return render(request, 'webmain/index.html')
    else:
        return render(request, 'webmain/search.html', {
            'profiles': profiles,
        })



@my_login_required()
def comment_gallery(request, gallery_id, username=None, token=None):
    requsername = username

    # if user cant access gallery this will return 404
    gallery = get_api_objects_or_404(api_client.get_gallery(requsername=requsername,id=gallery_id))[0]
    user = get_api_objects_or_404(api_client.get_user(username=requsername))[0]

    comment = GalleryComment(User=user.id, Gallery=gallery_id, Comment=request.GET['comment'])
    responce = api_client.post_gallery_comment(comment,requsername=requsername)

    return redirect('webmain:detail', gallery_id)


@my_login_required()
def comment_photo(request, photo_id, username=None, token=None):
    requsername = username

    # if user cant access photo this will return 404
    photo = get_api_objects_or_404(api_client.get_photo(requsername=requsername,id=photo_id))[0]
    user = get_api_objects_or_404(api_client.get_user(username=requsername))[0]
    comment = PhotoComment(User=user.id, Photo=photo_id, Comment=request.GET['comment'])
    responce = api_client.post_photo_comment(comment,requsername=requsername)

    return redirect('webmain:detail', photo.Gallery.id)

@my_login_required()
def delete_comment_photo(request, comment_id, photo_id, username=None, token=None):
    requsername = username

    responce = api_client.delete_photo_comment(id=comment_id,requsername=requsername)

    print("\n\nPHOTO COMMENT DELETE RESPONSE"+"="*60+"\n"+str(responce))

    return redirect('webmain:index')

@my_login_required()
def delete_comment_gallery(request, comment_id, gallery_id, username=None, token=None):
    requsername = username

    responce = api_client.delete_gallery_comment(id=comment_id,requsername=requsername)

    print("\n\nGALLERY COMMENT DELETE RESPONSE"+"="*60+"\n"+str(responce))


    return redirect('webmain:index')