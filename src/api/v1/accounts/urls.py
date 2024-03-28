from django.urls import path

from . import views

urlpatterns = [
    path('bookmarks/', views.BookmarkEditView.as_view({'post': 'create'}), name='user_bookmark'),
    path('rating/', views.RatingEditView.as_view({'post': 'create'}), name='user_rating')
]
