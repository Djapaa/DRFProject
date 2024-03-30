from django.urls import path, include

from . import views

urlpatterns = [
    path('bookmarks/', views.BookmarkEditView.as_view({'post': 'create'}), name='user_bookmark_add'),
    path('<int:pk>/bookmarks/', views.BookmarkEditView.as_view({'get': 'list'}), name='user_bookmark'),
    path('notifications/', include('api.v1.notification.urls')),
    path('rating/', views.RatingEditView.as_view({'post': 'create'}), name='user_rating'),

]
