from django.shortcuts import render,redirect , get_object_or_404
# Create your views here.
from django.contrib import messages
from .models import Photo, Gallery, GalleryReaction, PhotoReaction, Follow,Profile, GalleryComment, PhotoComment
from .forms import GalleryForm, PhotoForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . import api_client
from django.http import Http404
from django.core.files.temp import NamedTemporaryFile

def get_api_objects_or_404(objects):

    if len(objects) == 0:
        raise Http404('No matches the given query.')
    return objects

# Responsible to show all galleries. Currently not used and will be deleted.Just for test purposes
@login_required(login_url='users:login')
def index(request):

    all_galleries = api_client.get_gallery()

    context = {
            'all_galleries': all_galleries,
    }
    return render(request, 'webmain/index.html', context)

# This is currently used as our home feed.
# TODO REVERSE FRIEND CONDITION
@login_required(login_url='users:login')
def home_view(request):
    # People that have me as a friend can show me their photos
    galleries = api_client.get_shared_galleries(requsername=str(request.user.username))
    comments = api_client.get_gallery_comment()

    context = {
        'all_galleries': galleries,
        'comments': comments,
        # 'profile':profile,
    }

    return render(request, "webmain/index.html", context)

# Shows details of a specific gallery
@login_required(login_url='users:login')
def detail(request, gallery_id):
    user = request.user

    gallery = get_api_objects_or_404(api_client.get_gallery(id=gallery_id, requsername=user.username))[0]
    comments = api_client.get_gallery_comment(requsername=user.username)
    photos = api_client.get_photo(requsername=user.username,galleryid=gallery_id)


    print("\n\nDETAILS\n"+str(gallery)+"\n")

    context = {
        'gallery': gallery,
        'user': user,
        'comments': comments,
        'photos' : photos
    }

    return render(request, 'webmain/detail.html', context)

# Shows details of a specific gallery
@login_required(login_url='users:login')
def photo_detail(request, gallery_id, photo_id):
    user = request.user

    gallery = get_api_objects_or_404(api_client.get_gallery(requsername=user.username, id=gallery_id))[0]
    comments = api_client.get_photo_comment()

    photο = get_api_objects_or_404(api_client.get_photo(requsername=request.user.username,id=photo_id))[0]

    context = {
        'phot': photο,
        'gallery': gallery,
        'comments':comments,
    }
        # return JsonResponse(data, safe=False)
        # return render(request, 'webmain/photo_detail.html', context)
    return render(request, 'webmain/photo_detail.html', context)

# Create a new gallery. NOTE: You cannot add two galleries with the same name
import base64

@login_required(login_url='users:login')
def create_gallery(request):
    form = GalleryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        gallery = form.save(commit=False)
        gallery.GalleryOwner = request.user

        responce = api_client.post_gallery(gallery, request.user.username)

        status_code = responce.status_code
        if status_code == 406:
            messages.error(request, 'You have already added a Gallery with the same name')

            print("\n\nALREADY ADDED" + "=" * 80 + "You have already added a Gallery with the same name\n\n")

            context = {
                'album': gallery,
                'form': form,
            }
            return render(request, 'webmain/create_gallery.html', context)  # TODO CHANGE THAT. SHOW MESSAGE CORRECTLY
        elif status_code == 403:
            messages.error(request, 'Authorization Error')

            context = {
                'album': gallery,
                'form': form,
            }
            return render(request, 'webmain/create_gallery.html', context)  # TODO CHANGE THAT. SHOW MESSAGE CORRECTLY

        messages.success(request, 'Form submission successful')
        # return redirect(request, 'webmain/index.html')    # TODO REDIRECT ANYWHERE YOu WISH?
        return redirect('users:profile')    # TODO REDIRECT ANYWHERE YOu WISH

    context = {
        "form": form,
    }

    return render(request, 'webmain/create_gallery.html',context)

# Updates photo that belongs on a gallery. NOTE: Only if the requested user is the galleryowner an update can occur
@login_required(login_url='users:login')     #@ declarator adds extra functionality on an extisting function
def update_gallery(request, gallery_id):

    # u_galleries = Gallery.objects.filter(id=gallery_id).first()
    u_galleries = get_api_objects_or_404(api_client.get_gallery(requsername=request.user.username,id=gallery_id))[0]

    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES, instance=u_galleries)  # request.files for images

        if form.is_valid():
            gallery = form.save(commit=False)
            api_client.put_gallery(gallery, request.user.username)
            messages.success(request, f'Your gallery has been updated')
            return redirect('webmain:detail', gallery_id)

    else:
        form = GalleryForm(instance=u_galleries)

    context = {
        "form": form,
    }

    return render(request, 'webmain/create_gallery.html', context)


# Create a new photo. NOTE: You cannot add two photos with the same name
@login_required(login_url='users:login')
def add_photo(request, gallery_id):
    form = PhotoForm(request.POST or None, request.FILES or None)

    gallery = get_api_objects_or_404(api_client.get_gallery(requsername=request.user.username,id=gallery_id))[0]

    if form.is_valid():
        photo = form.save(commit=False)
        photo.Gallery = gallery
        api_client.post_photo(photo, request.user.username)

        return redirect('webmain:detail', gallery_id)
    context = {
        'gallery': gallery,
        'form': form,
    }
    return render(request, 'webmain/add_photo.html', context)

@login_required(login_url='users:login')     # @ declarator adds extra functionality on an extisting function
# Updates photo that belongs on a gallery. NOTE: Only if the requested user is the galleryowner an update can occur
def update_photo(request, gallery_id, photo_id):

    gallery = get_api_objects_or_404(api_client.get_gallery(requsername=request.user.username,id=gallery_id))[0]

    u_photos = get_api_objects_or_404(api_client.get_photo(requsername=request.user.username, id=photo_id))[0]

    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=u_photos)  # request.files for images

        if form.is_valid():
            form.save()
            photo = form.save(commit=False)
            api_client.put_photo(photo, request.user.username)

            messages.success(request, f'Your photo has been updated')
            return redirect('webmain:detail', gallery_id)
    else:
        form = PhotoForm(instance=u_photos)

    context = {
        'form': form,
        'gallery': gallery,
    }

    return render(request, 'webmain/add_photo.html', context)


# Delete gallery. NOTE: Only the gallery owner has the permission to delete
@login_required(login_url='users:login')
def delete_gallery(request, gallery_id):

    get_api_objects_or_404(api_client.get_gallery(requsername=request.user.username, id=gallery_id))[0]
    api_client.delete_gallery(requsername=request.user.username,id=gallery_id)
    # return render(request, 'webmain/index.html')    # TODO REDIRECT CORRECTLY

    return redirect('users:profile')


# Delete photo. NOTE: Only the gallery owner, in which the photo belongs has the permission to delete
@login_required(login_url='users:login')
def delete_photo(request, gallery_id, photo_id):

    gallery = get_api_objects_or_404(api_client.get_gallery(requsername=request.user.username, id=gallery_id))[0]

    # gallery =

    if request.user == gallery.GalleryOwner:
        messages.success(request, 'You can delete this photo')

        api_client.delete_photo(requsername=request.user.username, id=photo_id)

        messages.success(request, 'Photo successfully deleted ')

    else:
        messages.error(request, 'You cannot delete this photo')

    return redirect('webmain:detail',gallery_id)            # TODO REDIRECT ANYWHERE YOU WISH


# Follow and unfollow users. NOTE: Added condition so that you cannot follow or unfollow yourself
@login_required(login_url='users:login')
def follow(request, user_id):

    # user_follow = get_object_or_404(User, id=user_id)
    user_follow = get_api_objects_or_404(api_client.get_user(id=user_id))[0]


    if user_follow.id == request.user.id:
        messages.error(request, 'You cannot follow yourself')

    else:
        check = api_client.get_follow(FC_1_Username=request.user.username,FC_2_Username=user_follow.username)

        #friendship existed
        if len(check) > 0:
            follow = check[0]
            print("\n\nFOLLOW" + "=" * 30 + str(follow))

            api_client.delete_follow(id=follow.id ,requsername=request.user.username)
            messages.success(request, 'Unshared Content ')

        # no friendship existed
        else:
            follow = Follow(FollowCond1=request.user, FollowCond2=user_follow,)
            print("\n\nFOLLOWING" + "=" * 30 + str(follow))

            # api_client.post_follow(follow,request.user.username)
            print("\n\nRESPNCE" + "=" * 30 + str(api_client.post_follow(follow,request.user.username)))
            messages.success(request, 'Shared Content')

    # return redirect('/' + str(id))
    return redirect('users:getProfile', user_follow.username)  # TODO FIX REDIRECTION


# TODO ADD LIKE COUNTER
# Like and unlike a gallery content. NOTE: ONLY friends of current user or the user himself can like
@login_required(login_url='users:login')
def like_gallery(request, gallery_id):

    responce = api_client.gallert_reaction_toggle(request.user.username,gallery_id)

    status_code = responce.status_code

    if status_code == 302 :
        messages.success(request, 'Unliked ')
    elif status_code == 2001:
        messages.success(request, 'Liked')
    # count = getLike(postId)
    context = {
        'like_gallery': like_gallery,
    }
    # return JsonResponse(data, safe=False)
    return redirect('webmain:detail', gallery_id)   #TODO CHECK REDIRECTION


# TODO ADD LIKE COUNTER
# Like and unlike a photo content. NOTE: ONLY friends of current user or the user himself can like
@login_required(login_url='users:login')
def like_photo(request, gallery_id, photo_id):
    responce = api_client.photo_reaction_toggle(request.user.username,photo_id)

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
def is_friend(request, user_id):
    friends = Follow.objects.filter(FollowCond2__id=request.user.id).filter(FollowCond1__id=user_id).all()

    if friends.count() == 0:
        return False

    return True

# Something like a like counter on photos. Not tested yet
# def num_photo_like(id):
#     like = PhotoReaction.objects.filter(p=id).count()
#     return like

# TODO ADD MORE FUNCTIONALITY.CURRENTY SUPPORTS ONLY SEARCH BASED ON USERNAME
# This is our search function
@login_required(login_url='users:login')
def search(request):

    # instance = User.objects.get(username=)
    # albums = Album.objects.filter(user=request.user)
    # song_results = Song.objects.all()
    queryset_list = Profile.objects.exclude(user=request.user)
    query = request.GET.get("q")

    if query == "":
        messages.error(request, 'No Items to search ')
        return render(request, 'webmain/index.html')
    else:

        # queryset_list = queryset_list.exlude(
        #     Q(user__username__exact=query)
        # )
        users = queryset_list.filter(
            Q(user__username__icontains=query)
            # ~Q(user__username__icontains=request.user)

        ).distinct()

        if not users:
            messages.error(request, 'No related user found. Recommended users to follow ')
            users = queryset_list
            return render(request, 'webmain/search.html', {
                'users': users,
            })

        messages.success(request, 'Related results found')
        return render(request, 'webmain/search.html', {
            'users': users,
        })


@login_required(login_url='users:login')
def comment_gallery(request, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)
    if is_friend(request, gallery.GalleryOwner.id) or gallery.GalleryOwner.id == request.user.id:
        comment = GalleryComment(User_id=request.user.id, Gallery_id=gallery_id, Comment=request.GET['comment'])
        comment.save()

        # return JsonResponse(data, safe=False)
        return redirect('webmain:detail', gallery_id)
        # return redirect('webmain:photo_detail', context)
    else:
        messages.error(request, 'CANNOT COMMENT ')
        return redirect('webmain:index')



# TODO DECIDE HOW WE ARE GOING TO USE IN HTML.IF WE WILL NOT REDIRECT IN NEW URL THERE IS NO NEED FOR MORE CHECKS.OTHERWISE APPLY SAME CHECKS AS LIKE GALLERY
@login_required(login_url='users:login')
def comment_photo(request, photo_id):

    photo = get_object_or_404(Photo, id=photo_id)
    if is_friend(request, photo.Gallery.GalleryOwner.id) or photo.Gallery.GalleryOwner.id == request.user.id:
        comment = PhotoComment(User_id=request.user.id, Photo_id=photo_id, Comment=request.GET['comment'])
        comment.save()
        # return JsonResponse(data, safe=False)

        return redirect('webmain:detail', photo.Gallery.id)
        # return redirect('webmain:photo_detail', context)
    else:
        messages.error(request, 'CANNOT COMMENT ')
        return redirect('webmain:index')

# TODO DECIDE HOW WE ARE GOING TO USE IN HTML.IF WE WILL NOT REDIRECT IN NEW URL THERE IS NO NEED FOR MORE CHECKS.OTHERWISE APPLY SAME CHECKS AS LIKE GALLERY
@login_required(login_url='users:login')
def delete_comment_photo(request, comment_id, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)
    comment = get_object_or_404(PhotoComment, id=comment_id)

    if request.user == photo.Gallery.GalleryOwner or request.user == comment.User:
        PhotoComment.objects.get(id=comment_id).delete()
        return redirect('webmain:detail', photo.Gallery.id)

    messages.error(request, 'CANNOT DELETE ')
    return redirect('webmain:index')
    # return render(request) TODO CHECK RETURN


# TODO DECIDE HOW WE ARE GOING TO USE IN HTML.IF WE WILL NOT REDIRECT IN NEW URL THERE IS NO NEED FOR MORE CHECKS.OTHERWISE APPLY SAME CHECKS AS LIKE GALLERY
@login_required(login_url='users:login')
def delete_comment_gallery(request, comment_id, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)
    comment = get_object_or_404(GalleryComment, id=comment_id)

    if request.user == gallery.GalleryOwner or request.user == comment.User:
        GalleryComment.objects.get(id=comment_id).delete()
        return redirect('webmain:detail', gallery_id)
    # return render(request) TODO CHECK RETURN

    messages.error(request, 'CANNOT DELETE ')
    return redirect('webmain:index')








