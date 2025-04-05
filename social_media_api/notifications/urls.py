from django.urls import path
from . import views

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('mark-read/', views.MarkNotificationReadView.as_view(), name='mark-all-read'),
    path('mark-read/<int:pk>/', views.MarkNotificationReadView.as_view(), name='mark-read'),
]