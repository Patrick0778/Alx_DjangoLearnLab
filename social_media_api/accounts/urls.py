from django.urls import path
from .views import RegisterView, LoginView
from .views import FollowUserView, UnfollowUserView, UserProfileView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
]
# Compare this snippet from social_media_api/accounts/serializers.py: