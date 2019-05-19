from django.shortcuts import render,redirect , get_object_or_404
# Create your views here.
from django.contrib import messages
from .models import Photo, Gallery, GalleryReaction, PhotoReaction, Follow,Profile, GalleryComment, PhotoComment
from .forms import GalleryForm, PhotoForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .api_client import *


# Responsible to show all galleries. Currently not used and will be deleted.Just for test purposes
@login_required(login_url='users:login')
def index(request):

    all_galleries = Gallery.objects.all()

    context = {
            'all_galleries': all_galleries,
    }
    return render(request, 'webmain/index.html', context)

# This is currently used as our home feed.
# TODO REVERSE FRIEND CONDITION
@login_required(login_url='users:login')
def home_view(request):

    print("\n\nGETING_GALLERY_REACTION"+"="*40+"\n"+str( get_gallery_reaction())+"\n\n")
    print("\n\nGETING_PHOTO_REACTION"+"="*40+"\n"+str(get_photo_reaction() )+"\n\n")
    print("\n\nGETING_GALERY_COMMENT"+"="*40+"\n"+str( get_gallery_comment())+"\n\n")
    print("\n\nGETING_PHOTO_COMMENT"+"="*40+"\n"+str(get_photo_comment() )+"\n\n")
    print("\n\nGETING_FOLLOW"+"="*40+"\n"+str(get_follow() )+"\n\n")
    print("\n\nGETING_USER"+"="*40+"\n"+str( get_user())+"\n\n")
    print("\n\nGETING_FOLLOWING"+"="*40+"\n"+str( get_following("admin"))+"\n\n")
    print("\n\nGETING_FOLLOWERS"+"="*40+"\n"+str( get_followers("admin"))+"\n\n")
    print("\n\nGETING_PROFILES"+"="*40+"\n"+str(get_profile())+"\n\n")

    # People that have me as a friend can show me their photos
    friends = Follow.objects.filter(FollowCond2__id=request.user.id).all().values_list('FollowCond1', flat=True)
    galleries = Gallery.objects.filter(GalleryOwner__in=friends).all().order_by('-UploadDateTime')

    context = {
        'all_galleries': galleries,
        # 'profile':profile,
    }

    return render(request, "webmain/index.html", context)

# Shows details of a specific gallery
@login_required(login_url='users:login')
def detail(request, gallery_id):
    user = request.user
    gallery = get_object_or_404(Gallery, pk=gallery_id)

    if request.user == gallery.GalleryOwner:
        messages.success(request, 'You can view details of this gallery')
        context = {
            'gallery': gallery,
            'user': user,
        }

        return render(request, 'webmain/detail.html', context)
    else:
        messages.error(request, 'You do not have permission to view this gallery ')
        return redirect('webmain:index')  # TODO REDIRECT ANYWHERE YOu WISH

# Create a new gallery. NOTE: You cannot add two galleries with the same name
@login_required(login_url='users:login')
def create_gallery(request):
    form = GalleryForm(request.POST or None, request.Files or None)
    if form.is_valid():
        gallery = form.save(commit=False)
        gallery.GalleryOwner = request.user

        user_galleries = Gallery.objects.filter(GalleryOwner=request.user)

        for gal in user_galleries:
            if gal.Name == form.cleaned_data.get("Name"):
                context = {
                    'album': gallery,
                    'form': form,
                    # 'error_message': 'You already added that song',
                }
                messages.error(request, 'You have already added a Gallery with the same name')
                return render(request, 'webmain/create_gallery.html', context) #TODO CHANGE THAT. SHOW MESSAGE CORRECTLY

        gallery.save()
        messages.success(request, 'Form submission successful')
        return render(request, 'webmain/index.html')    # TODO REDIRECT ANYWHERE YOu WISH

    context = {
        "form": form,
    }

    return render(request, 'webmain/create_gallery.html',context)


# Updates photo that belongs on a gallery. NOTE: Only if the requested user is the galleryowner an update can occur
@login_required(login_url='users:login')     #@ declarator adds extra functionality on an extisting function
def update_gallery(request, gallery_id):

    u_galleries = Gallery.objects.filter(id=gallery_id).first()

    if request.user == u_galleries.GalleryOwner:    # TODO CHECK ERROR WHEN THERE IS NOT THIS GALLERY
        messages.success(request, f'You can update the gallery ')

        if request.method == 'POST':
            form = GalleryForm(request.POST, request.FILES, instance=u_galleries)  # request.files for images

            if form.is_valid():
                form.save()
                messages.success(request, f'Your gallery has been updated')
                return redirect('users:profile')

        else:
            form = GalleryForm(instance=u_galleries)

        context = {
            "form": form,
        }

        return render(request, 'webmain/create_gallery.html', context)
    else:
        messages.error(request, f'You cannot update the gallery ')
        return redirect('webmain:index')





# Create a new gallery. NOTE: You cannot add two galleries with the same name
@login_required(login_url='users:login')
def add_photo(request, gallery_id):
    form = PhotoForm(request.POST or None, request.FILES or None)
    gallery = get_object_or_404(Gallery, pk=gallery_id)

    if request.user == gallery.GalleryOwner:
        messages.success(request, 'You can add photo on your gallery')

        if form.is_valid():
            # gallery_photos = gallery.Photo_set.all()

            photo = form.save(commit=False)
            photo.Gallery = gallery

            photo.save()
            # photo.get_remote_image()
            return render(request, 'webmain/add_photo.html', {'gallery': gallery})
        context = {
            'gallery': gallery,
            'form': form,
        }
        return render(request, 'webmain/add_photo.html', context)

    else:
        messages.error(request, 'You cannot add photo on this gallery')
        return redirect('webmain:index')                # TODO REDIRECT ANYWHERE YOu WISH


@login_required(login_url='users:login')     # @ declarator adds extra functionality on an extisting function
# Updates photo that belongs on a gallery. NOTE: Only if the requested user is the galleryowner an update can occur
def update_photo(request, gallery_id, photo_id):

    gallery = get_object_or_404(Gallery, pk=gallery_id)

    if request.user == gallery.GalleryOwner:    # TODO CHECK ERROR WHEN THERE IS NOT THIS GALLERY
        messages.success(request, f'You can update the photo ')

        u_photos = Photo.objects.filter(id=photo_id).filter(Gallery=gallery).first()
        if request.method == 'POST':
            form = PhotoForm(request.POST, request.FILES, instance=u_photos)  # request.files for images

            if form.is_valid():
                form.save()
                messages.success(request, f'Your photo has been updated')
                return redirect('webmain:index')

        else:
            form = PhotoForm(instance=u_photos)

        context = {
            'form': form,
            'gallery': gallery,
        }

        return render(request, 'webmain/add_photo.html', context)
    else:
        messages.error(request, f'You cannot update the photo ')
        return redirect('webmain:index')


# Delete gallery. NOTE: Only the gallery owner has the permission to delete
@login_required(login_url='users:login')
def delete_gallery(request, gallery_id):

    gallery = get_object_or_404(Gallery, pk=gallery_id)

    if request.user == gallery.GalleryOwner:
        messages.success(request, 'You can delete your gallery')
        gallery.delete()
        messages.success(request, 'Gallery successfully deleted ')

    else:
        messages.error(request, 'You cannot delete this gallery')

    # return render(request, 'webmain/index.html')    # TODO REDIRECT CORRECTLY
    return redirect('webmain:index')

# Delete photo. NOTE: Only the gallery owner, in which the photo belongs has the permission to delete
@login_required(login_url='users:login')
def delete_photo(request, gallery_id, photo_id):

    gallery = get_object_or_404(Gallery, pk=gallery_id)

    if request.user == gallery.GalleryOwner:
        messages.success(request, 'You can delete this photo')
        song = Photo.objects.filter(pk=photo_id)  # TODO CHECK IF I NEED TO VERIFY THE USER
        song.delete()
        messages.success(request, 'Photo successfully deleted ')

    else:
        messages.error(request, 'You cannot delete this photo')

    return redirect('webmain:index')            # TODO REDIRECT ANYWHERE YOU WISH


# Follow and unfollow users. NOTE: Added condition so that you cannot follow or unfollow yourself
@login_required(login_url='users:login')
def follow(request, user_id):
    user_follow = get_object_or_404(User, id=user_id)
    if user_follow.id == request.user.id:
        messages.error(request, 'You cannot follow yourself')

    else:
        messages.success(request, 'You can follow that user')
        instance, created = Follow.objects.get_or_create(FollowCond1=request.user, FollowCond2=user_follow)
        if not created:
            messages.success(request, 'Unfollow ')
            instance.delete()
        else:
            messages.success(request, 'Follow')

    # return redirect('/' + str(id))
    return render(request, 'webmain/index.html') # TODO FIX REDIRECTION


# TODO ADD LIKE COUNTER
# Like and unlike a gallery content. NOTE: ONLY friends of current user or the user himself can like
@login_required(login_url='users:login')
def like_gallery(request, gallery_id):
    # postId = request.GET.get('id', None)

    gallery = get_object_or_404(Gallery, id=gallery_id)

    if is_friend(request, gallery.GalleryOwner.id) | gallery.GalleryOwner.id == request.user.id:
        messages.success(request, 'CAN LIKE ')

        instance, created = GalleryReaction.objects.get_or_create(User=request.user, Gallery=gallery)

        if not created:
            messages.success(request, 'Unlike ')
            instance.delete()
        else:
            messages.success(request, 'Like')
        # count = getLike(postId)
        context = {
            'like_gallery': like_gallery,
        }
        # return JsonResponse(data, safe=False)
        return render(request, 'webmain/index.html', context)   #TODO CHECK REDIRECTION

    else:
        messages.error(request, 'CANNOT LIKE ')
        return redirect('webmain:index')  # TODO CHECK REDIRECTION


# TODO ADD LIKE COUNTER
# Like and unlike a photo content. NOTE: ONLY friends of current user or the user himself can like
@login_required(login_url='users:login')
def like_photo(request, gallery_id, photo_id):
    # postId = request.GET.get('id', None)
    gallery = get_object_or_404(Gallery, id=gallery_id)
    if is_friend(request, gallery.GalleryOwner.id) | gallery.GalleryOwner.id == request.user.id:

        photo = get_object_or_404(Photo, id=photo_id)
        instance, created = PhotoReaction.objects.get_or_create(User=request.user, Photo=photo)

        if not created:
            messages.success(request, 'Unlike ')
            instance.delete()
        else:
            messages.success(request, 'Like')
        # count = getLike(postId)
        context = {
            'like_photo': like_photo,
        }
        # return JsonResponse(data, safe=False)
        return render(request, 'webmain/index.html', context)
    else:
        messages.error(request, 'CANNOT LIKE ')
        return redirect('webmain:index')  # TODO CHECK REDIRECTION


# This is a function to find if there is a friend connection between gallery owner and request user.
# Used in likes, comments.
# Returns boolean
def is_friend(request, user_id):
    friends = Follow.objects.filter(FollowCond2__id=request.user.id).filter(FollowCond1__id=user_id).all()

    if friends.count() == 0:
        return False

    return True


# Something like a like counter on photos. Not tested yet
def num_photo_like(id):
    like = PhotoReaction.objects.filter(p=id).count()
    return like


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

        messages.success(request, 'Related results found')
        return render(request, 'webmain/search.html', {
            'users': users,
        })

# TODO DECIDE HOW WE ARE GOING TO USE IN HTML.IF WE WILL NOT REDIRECT IN NEW URL THERE IS NO NEED FOR MORE CHECKS.OTHERWISE APPLY SAME CHECKS AS LIKE GALLERY
@login_required(login_url='users:login')
def comment_gallery(request, gallery_id):
    comment = GalleryComment(User_id=request.user.id, Gallery_id=gallery_id, Comment=request.GET['comment'])
    comment.save()

    context = {
        'id': comment.id,
        'userId': comment.User_id,
        'username': comment.user.username,
        'galleryId': comment.Gallery_id,
        'text': comment.Comment
    }

    return render(request, 'webmain/index.html', context)


# TODO DECIDE HOW WE ARE GOING TO USE IN HTML.IF WE WILL NOT REDIRECT IN NEW URL THERE IS NO NEED FOR MORE CHECKS.OTHERWISE APPLY SAME CHECKS AS LIKE GALLERY
@login_required(login_url='users:login')
def comment_photo(request, photo_id):
    comment = GalleryComment(User_id=request.user.id, Photo_id=photo_id, Comment=request.GET['comment'])
    comment.save()

    context = {
        'id': comment.id,       # TODO CHECK THAT. MAYBE WE DONT NEED EVERYTHING
        'userId': comment.User_id,
        'username': comment.user.username,
        'photoId': comment.Photo_id,
        'text': comment.Comment
    }

    return render(request, 'webmain/index.html', context)

# TODO DECIDE HOW WE ARE GOING TO USE IN HTML.IF WE WILL NOT REDIRECT IN NEW URL THERE IS NO NEED FOR MORE CHECKS.OTHERWISE APPLY SAME CHECKS AS LIKE GALLERY
@login_required(login_url='users:login')
def delete_comment_photo(request, comment_id, gallery_id):
    gallery = get_object_or_404(Photo, id=gallery_id)
    comment = get_object_or_404(GalleryComment, id=comment_id)

    if request.user == gallery.GalleryOwner | request.user == comment.User:
        PhotoComment.objects.get(id=comment_id).delete()
    # return render(request) TODO CHECK RETURN


# TODO DECIDE HOW WE ARE GOING TO USE IN HTML.IF WE WILL NOT REDIRECT IN NEW URL THERE IS NO NEED FOR MORE CHECKS.OTHERWISE APPLY SAME CHECKS AS LIKE GALLERY
@login_required(login_url='users:login')
def delete_comment_gallery(request, comment_id, gallery_id):
    gallery = get_object_or_404(Gallery, id=gallery_id)
    comment = get_object_or_404(GalleryComment, id=comment_id)

    if request.user == gallery.GalleryOwner | request.user == comment.User:
        GalleryComment.objects.get(id=comment_id).delete()
    # return render(request) TODO CHECK RETURN









