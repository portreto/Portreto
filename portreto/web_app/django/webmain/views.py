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
    galleries = api_client.get_shared_galleries(requsername=requsername,token=token)

    # Add gallery owner photos
    for gallery in galleries:
        gallery.GalleryOwnerPhoto = get_api_objects_or_404(api_client.get_profile(username=gallery.GalleryOwner.username, token=token))[0].ProfilePhoto
        gallery.isLiked = len(api_client.get_gallery_reaction(requsername=requsername,galleryid=gallery.id,token=token))>0
        gallery.comments = api_client.get_gallery_comment(requsername=requsername,galleryid=gallery.id,token=token)


    context = {
        'all_galleries': galleries,
        'requsername':requsername,
        'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername,token=token))[0]
    }

    return render(request, "webmain/index.html", context)

# Shows details of a specific gallery
@my_login_required()
def detail(request, gallery_id, username=None, token=None):
    requsername = username

    user = get_api_objects_or_404(api_client.get_user(username=requsername,token=token))[0]
    gallery = get_api_objects_or_404(api_client.get_gallery(id=gallery_id, requsername=requsername,token=token))[0]
    comments = api_client.get_gallery_comment(requsername=requsername,galleryid=gallery_id,token=token)
    photos = api_client.get_photo(requsername=requsername,galleryid=gallery_id,token=token)

    reactions = api_client.get_gallery_reaction(requsername=requsername, galleryid=gallery_id,token=token)

    is_liked = False
    for like in reactions:
        if like.User == user.id:
            is_liked = True
            break

    context = {
        'gallery': gallery,
        'user': user,
        'comments': comments,
        'photos' : photos,
        'is_liked': is_liked,
        'like_count': len(reactions),
        'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername,token=token))[0]
    }

    return render(request, 'webmain/detail.html', context)

# Shows details of a specific photo
@my_login_required()
def photo_detail(request, gallery_id, photo_id, username=None, token=None):
    requsername = username

    user = get_api_objects_or_404(api_client.get_user(username=requsername,token=token))[0]
    gallery = get_api_objects_or_404(api_client.get_gallery(requsername=requsername, id=gallery_id,token=token))[0]
    comments = api_client.get_photo_comment(requsername=requsername,photoid=photo_id,token=token)
    photο = get_api_objects_or_404(api_client.get_photo(requsername=requsername,id=photo_id,token=token))[0]

    reactions = api_client.get_photo_reaction(requsername=requsername,photoid = photo_id,token=token)

    is_liked = False
    for like in reactions:
        if like.User == user.id:
            is_liked = True
            break
    context = {
        'phot': photο,
        'gallery': gallery,
        'comments':comments,
        'requsername':requsername,
        'user' : user,
        'is_liked':is_liked,
        'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername,token=token))[0]
    }
    return render(request, 'webmain/photo_detail.html', context)

# Create a new gallery. NOTE: You cannot add two galleries with the same name
@my_login_required()
def create_gallery(request, username=None, token=None):
    requsername = username

    form = GalleryForm(request.POST or None, request.FILES or None)

    user = get_api_objects_or_404(api_client.get_user(username=requsername,token=token))[0]

    if form.is_valid():
        # form.GalleryOwner = user
        gallery = form.save(commit=False)

        user2 = User(id=user.id,username=user.username)
        gallery.GalleryOwner = user2

        responce = api_client.post_gallery(gallery, requsername,token=token)

        status_code = responce.status_code
        if status_code == 406:
            messages.error(request, 'You have already added a Gallery with the same name')

            print("\n\nALREADY ADDED" + "=" * 80 + "You have already added a Gallery with the same name\n\n")

            context = {
                'album': gallery,
                'form': form,
                'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername,token=token))[0]
            }
            return render(request, 'webmain/create_gallery.html', context)  # TODO CHANGE THAT. SHOW MESSAGE CORRECTLY
        elif status_code == 403:
            messages.error(request, 'Authorization Error')

            context = {
                'album': gallery,
                'form': form,
                'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername,token=token))[0]
            }
            return render(request, 'webmain/create_gallery.html', context)  # TODO CHANGE THAT. SHOW MESSAGE CORRECTLY

        messages.success(request, 'Form submission successful')
        # return redirect(request, 'webmain/index.html')    # TODO REDIRECT ANYWHERE YOu WISH?
        return redirect('users:profile')    # TODO REDIRECT ANYWHERE YOu WISH

    context = {
        "form": form,
        'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername,token=token))[0]
    }

    return render(request, 'webmain/create_gallery.html',context)

# # Updates photo that belongs on a gallery. NOTE: Only if the requested user is the galleryowner an update can occur
# @my_login_required()
# def update_gallery(request, gallery_id, username=None, token=None):
#     requsername = username
#
#     # u_galleries = Gallery.objects.filter(id=gallery_id).first()
#     u_galleries = get_api_objects_or_404(api_client.get_gallery(requsername=requsername,id=gallery_id,token=token))[0]
#
#     if request.method == 'POST':
#         form = GalleryForm(request.POST, request.FILES, instance=u_galleries)  # request.files for images
#
#         if form.is_valid():
#             gallery = form.save(commit=False)
#             api_client.put_gallery(gallery, requsername,token=token)
#             messages.success(request, f'Your gallery has been updated')
#             return redirect('webmain:detail', gallery_id)
#
#     else:
#         form = GalleryForm(instance=u_galleries)
#
#     context = {
#         "form": form,
#         'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername,token=token))[0]
#     }
#
#     return render(request, 'webmain/create_gallery.html', context)

# Create a new photo. NOTE: You cannot add two photos with the same name
@my_login_required()
def add_photo(request, gallery_id, username=None, token=None):
    requsername = username

    form = PhotoForm(request.POST or None, request.FILES or None)
    gallery = get_api_objects_or_404(api_client.get_gallery(requsername=requsername,id=gallery_id,token=token))[0]
    comments = api_client.get_gallery_comment(requsername=requsername,galleryid=gallery_id,token=token)

    if form.is_valid():
        photo = form.save(commit=False)
        photo.Gallery = gallery.id
        api_client.post_photo(photo, requsername,token=token)
        return redirect('webmain:detail', gallery_id)
    context = {
        'gallery': gallery,
        'form': form,
        'comments' : comments,
        'requsername' : requsername,
        'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername,token=token))[0]
    }
    return render(request, 'webmain/add_photo.html', context)

# # Updates photo that belongs on a gallery. NOTE: Only if the requested user is the galleryowner an update can occur
# @my_login_required()
# def update_photo(request, gallery_id, photo_id, username=None, token=None):
#     requsername = username
#
#     gallery = get_api_objects_or_404(api_client.get_gallery(requsername=requsername,id=gallery_id,token=token))[0]
#
#     u_photos = get_api_objects_or_404(api_client.get_photo(requsername=requsername, id=photo_id,token=token))[0]
#
#     if request.method == 'POST':
#         form = PhotoForm(request.POST, request.FILES, instance=u_photos)  # request.files for images
#
#         if form.is_valid():
#             form.save()
#             photo = form.save(commit=False)
#             api_client.put_photo(photo, requsername,token=token)
#
#             messages.success(request, f'Your photo has been updated')
#             return redirect('webmain:detail', gallery_id)
#     else:
#         form = PhotoForm(instance=u_photos)
#
#     context = {
#         'form': form,
#         'gallery': gallery,
#         'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername,token=token))[0]
#     }
#
#     return render(request, 'webmain/add_photo.html', context)


# Delete gallery. NOTE: Only the gallery owner has the permission to delete
@my_login_required()
def delete_gallery(request, gallery_id, username=None, token=None):
    requsername = username

    get_api_objects_or_404(api_client.get_gallery(requsername=requsername, id=gallery_id,token=token))[0]
    api_client.delete_gallery(requsername=requsername,id=gallery_id,token=token)
    # return render(request, 'webmain/index.html')    # TODO REDIRECT CORRECTLY

    return redirect('users:profile')

# Delete photo. NOTE: Only the gallery owner, in which the photo belongs has the permission to delete
@my_login_required()
def delete_photo(request, gallery_id, photo_id, username=None, token=None):
    requsername = username
    responce = api_client.delete_photo(requsername=requsername, id=photo_id,token=token)

    if responce.status_code == 204:
        messages.success(request, 'Photo successfully deleted ')
    else:
        messages.error(request, 'You cannot delete this photo')
    return redirect('webmain:detail',gallery_id)

# Follow and unfollow users. NOTE: Added condition so that you cannot follow or unfollow yourself
@my_login_required()
def follow(request, user_id, username=None, token=None):
    requsername = username

    user_follow = get_api_objects_or_404(api_client.get_user(id=user_id,token=token))[0]
    user = get_api_objects_or_404(api_client.get_user(username=requsername,token=token))[0]

    if user_follow.id == user.id:
        messages.error(request, 'You cannot follow yourself')

    else:
        check = api_client.get_follow(FC_1_Username=requsername,FC_2_Username=user_follow.username,token=token)
        print("\n\nCHECK"+"=*60"+"\n"+str(check))
        #friendship existed
        if len(check) > 0:
            follow = check[0]
            print("\n\nFOLLOW" + "=" * 30 + str(follow))

            api_client.delete_follow(id=follow.id ,requsername=requsername,token=token)
            messages.success(request, 'Unshared Content ')

        # no friendship existed
        else:
            follow = Follow(FollowCond1=user.id, FollowCond2=user_follow.id,)
            api_client.post_follow(follow,requsername,token=token)
            messages.success(request, 'Shared Content')

    # return redirect('/' + str(id))
    return redirect('users:getProfile', user_follow.username)  # TODO FIX REDIRECTION

# TODO ADD LIKE COUNTER
# Like and unlike a gallery content. NOTE: ONLY friends of current user or the user himself can like
@my_login_required()
def like_gallery(request, gallery_id,redirect_target, username=None, token=None):
    requsername = username
    responce = api_client.gallery_reaction_toggle(requsername, gallery_id,token=token)
    status_code = responce.status_code

    if status_code == 302 :
        messages.success(request, 'Unliked ')
    elif status_code == 2001:
        messages.success(request, 'Liked')
    # count = getLike(postId)
    context = {
        'like_gallery': like_gallery,
        'my_prof': get_api_objects_or_404(api_client.get_profile(username=requsername,token=token))[0]
    }
    # Redirect to proper url
    if(redirect_target=='index'):
        return redirect('webmain:'+redirect_target)
    else:
        return redirect('webmain:'+redirect_target, gallery_id)

# TODO ADD LIKE COUNTER
# Like and unlike a photo content. NOTE: ONLY friends of current user or the user himself can like
@my_login_required()
def like_photo(request, gallery_id, photo_id, username=None, token=None):
    requsername = username

    responce = api_client.photo_reaction_toggle(requsername,photo_id,token=token)

    status_code = responce.status_code

    if status_code == 302 :
        messages.success(request, 'Unliked ')
    elif status_code == 201:
        messages.success(request, 'Liked')
    # count = getLike(postId)
    # return JsonResponse(data, safe=False)
    return redirect('webmain:photo_detail', gallery_id, photo_id,token=token)   #TODO CHECK REDIRECTION

# This is our search function
@my_login_required()
def search(request, username=None, token=None):
    query = request.GET.get("q")
    if query == "":
        messages.error(request, 'No Items to search ')
        return render(request, 'webmain/index.html')
    else:
        profiles = api_client.get_search_profiles(query=query,token=token)
        for profile in profiles:
            profile.is_friend = len(api_client.get_follow(FC_1_Username=username,FC_2_Username=profile.user.username,token=token))>0
        context={
            'profiles': profiles,
        }
        return render(request, 'webmain/search.html', context)


@my_login_required()
def comment_gallery(request, redirect_target, gallery_id, username=None, token=None):
    requsername = username

    # if user cant access gallery this will return 404
    gallery = get_api_objects_or_404(api_client.get_gallery(requsername=requsername,id=gallery_id,token=token))[0]
    user = get_api_objects_or_404(api_client.get_user(username=requsername,token=token))[0]

    comment = GalleryComment(User=user, Gallery=gallery_id, Comment=request.GET['comment'])
    response = api_client.post_gallery_comment(comment,requsername=requsername,token=token)

    if(redirect_target=='index'):
        return redirect('webmain:'+redirect_target)
    else:
        return redirect('webmain:'+redirect_target, gallery_id)


@my_login_required()
def comment_photo(request, photo_id, username=None, token=None):
    requsername = username

    # if user cant access photo this will return 404
    photo = get_api_objects_or_404(api_client.get_photo(requsername=requsername,id=photo_id,token=token))[0]
    user = get_api_objects_or_404(api_client.get_user(username=requsername,token=token))[0]
    comment = PhotoComment(User=user, Photo=photo_id, Comment=request.GET['comment'])
    responce = api_client.post_photo_comment(comment,requsername=requsername,token=token)

    return redirect('webmain:photo_detail', photo.Gallery, photo_id)

@my_login_required()
def delete_comment_photo(request, comment_id, photo_id, username=None, token=None):
    requsername = username
    photo = get_api_objects_or_404(api_client.get_photo(requsername=requsername,id=photo_id,token=token))[0]
    responce = api_client.delete_photo_comment(id=comment_id,requsername=requsername,token=token)
    return redirect('webmain:photo_detail', photo.Gallery, photo_id)

@my_login_required()
def delete_comment_gallery(request, comment_id, gallery_id, redirect_target, username=None, token=None):
    requsername = username
    responce = api_client.delete_gallery_comment(id=comment_id,requsername=requsername,token=token)
    if (redirect_target == 'index'):
        return redirect('webmain:' + redirect_target)
    else:
        return redirect('webmain:' + redirect_target, gallery_id)