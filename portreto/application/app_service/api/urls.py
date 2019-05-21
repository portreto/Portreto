from django.urls import path, include
from . import views
from rest_framework import routers

basic_router = routers.DefaultRouter()
basic_router.register('gallery', views.GalleryView)
basic_router.register('gallery_reactions', views.GalleryReactionView)
basic_router.register('photos', views.PhotoView)
basic_router.register('photo_reactions', views.PhotoReactionView)
basic_router.register('gallery_comments', views.GalleryCommentView)
basic_router.register('photo_comments', views.PhotoCommentView)
basic_router.register('follows', views.FollowView)
basic_router.register('profiles', views.ProfileView)
basic_router.register('users', views.UserView)

advanced_router = routers.DefaultRouter()
advanced_router.register('shared_galleries', views.SharedGalleriesView)
advanced_router.register('followers', views.FollowersView)
advanced_router.register('followers_profiles', views.FollowersProfileView)
advanced_router.register('following', views.FollowingView)
advanced_router.register('following_profiles', views.FollowingProfileView)
advanced_router.register('profile_search', views.SearchProfileView)

# advanced_router.register('photo_reaction_toggle', views.PhotoReactionToggle)

urlpatterns = [
    path('basic/', include(basic_router.urls)),
    path('advanced/', include(advanced_router.urls)),
    path('photo_reaction_toggle/', views.PhotoReactionToggle.as_view()),
    path('gallery_reaction_toggle/', views.GalleryReactionToggle.as_view())
]