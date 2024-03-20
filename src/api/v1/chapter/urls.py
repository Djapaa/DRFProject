from django.urls import path, include


from . import views


chapter_detail = views.ChapterView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})




urlpatterns = [
    path('<int:pk>/chapters-list/', views.ChapterListView.as_view(), name='composition-chapters'),
    path('chapters/<int:pk>/', chapter_detail, name='chapter'),
    path('<int:composition_id>/chapters/create/', views.ChapterCreateView.as_view(), name='chapter-create'),

]