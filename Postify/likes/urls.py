from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LikeViewSet

app_name = 'likes'

router = DefaultRouter()
router.register(r'likes', LikeViewSet, basename='like')  # Registering the viewset

urlpatterns = [
    path('like/', LikeViewSet.as_view({'post': 'create'}), name='like_post'),  # POST to like a post
    path('unlike/', LikeViewSet.as_view({'post': 'destroy'}), name='unlike_post'),    # POST to unlike a post

]
