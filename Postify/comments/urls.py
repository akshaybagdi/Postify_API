from django.urls import path
from rest_framework import routers
from .views import CommentList, CommentCreate, CommentUpdate, CommentDelete

app_name = 'comments'

# Explicitly map views to their methods using as_view()
simple_router = routers.SimpleRouter()

# Map the views to specific actions
List_Comments = CommentList.as_view({'post': 'list'})  # POST method for filtering and listing
Create_Comment = CommentCreate.as_view({'post': 'create'})  # POST method for creating
Update_Comment = CommentUpdate.as_view({'post': 'update'})  # POST method for updating
Delete_Comment = CommentDelete.as_view({'post': 'destroy'})  # POST method for deleting

urlpatterns = simple_router.urls

# Explicitly map the URLs to the views
urlpatterns += [
    path('comments/list/', List_Comments, name='comment_list'),  # List comments or filter by IDs
    path('comments/create/', Create_Comment, name='comment_create'),  # List comments or filter by IDs
    path('comments/update/', Update_Comment, name='comment_update'),  # Update comment by ID
    path('comments/delete/', Delete_Comment, name='comment_delete'),  # Delete comment by ID
]
