from django.urls import path

from . import views

notifications = views.NotificationView.as_view(
    {'get': 'list',
     'post': 'destroy'}
)

urlpatterns = [
    path('', notifications, name='notification_of_user')
]
