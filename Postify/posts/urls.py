from django.urls import path
from .views import PostList, PostUserDetail, PostUserUpdate, PostUserDestroy, PostUserCreate
from rest_framework import routers
from .tags import TagView

app_name = 'Posts'

simple_router = routers.SimpleRouter()
List_Post = PostList.as_view({'post': 'list'})
Update_Post = PostUserUpdate.as_view({'post': 'update'})
Delete_Post = PostUserDestroy.as_view({'post': 'delete'})
User_ID = PostUserDetail.as_view({'post': 'create'})
Create_Post = PostUserCreate.as_view({'post': 'create'})
# Tags = TagView.as_view({'post': 'create'})

urlpatterns = simple_router.urls

urlpatterns = urlpatterns + [
    path('posts/list/', List_Post, name='List_Posts'),
    path('posts/create/', Create_Post, name='Create_Post'),
    path('posts/update/', Update_Post, name='Update_Post'),
    path('posts/delete/', Delete_Post, name='Delete_Post'),
    path('posts/id/', User_ID, name='User_ID'),

    #   endpoints for tag
    path('posts/tag/<str:tag_name>/', TagView.as_view(), name='single-tag-filter'),
    path('posts/tag/', TagView.as_view(), name='multi-tag-filter'),
]
