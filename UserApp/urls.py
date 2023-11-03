from django.urls import path
from .views import *

app_name = 'UserApp'

urlpatterns = [
    path('',home,name='home'),
    path('<str:slug>',HomeByTitle,name='HomeByTitle'),
    path('create_profile/user',create_profile,name='create_profile'),
    path('profile/<user>',profile_page,name='profile'),
    path("delete_Comment/<int:id>/<str:slug>",delete_Comment,name='delete_Comment'),
    path('Post/<str:slug>',postView,name='PostView'),
    path('AddComment/<str:slug>',addComment,name='addComment'),
    path('addRemoveLike/<str:slug>',addRemoveLike,name='addRemoveLike'),
    path('follow/<str:profile>',FollowUser,name='followuser'),
    path('new_post/<user>',new_post,name='new_post'),
    path('discover/new',Discover,name='discover'),
    path('search/user',searchUser,name='searchUser'),
    path('search/user/<str:user>',searchUseraxios,name='searchaxios'),
]