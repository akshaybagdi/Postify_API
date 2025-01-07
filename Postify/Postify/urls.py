
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('posts.urls', namespace='Posts')),
    path('api/', include('comments.urls', namespace='Comments')),
    path('api/', include('likes.urls', namespace='likes')),

]
