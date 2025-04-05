from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', views.FeedView.as_view(), name='feed'),
    path('posts/<int:pk>/like/', views.LikeView.as_view(), name='post-like'),
    path('posts/<int:pk>/unlike/', views.LikeView.as_view(), name='post-unlike'),
]