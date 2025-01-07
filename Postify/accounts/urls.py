from .views import user_registration, user_login, user_logout
from django.urls import path

urlpatterns = [
    path('account/register/', user_registration, name='register'),
    path('account/login/', user_login, name='token_obtain_pair'),
    path('account/logout/', user_logout, name='logout'),
]
