from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserRegistrationView, activate_account, UserLoginApiView, LogoutAPIView

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('users/', include(router.urls)),
    path('users/register/', UserRegistrationView.as_view(), name='register'),
    path('users/activate/<uidb64>/<token>/', activate_account, name='activate-account'),
    path('users/login/', UserLoginApiView.as_view(), name='login'),
    path('users/logout/', LogoutAPIView.as_view(), name='logout'),
]
