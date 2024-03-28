from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from ..chapter import views as chapter_view

router = DefaultRouter()
router.register('composition', views.CompositionView, basename='composition')

chapter_detail = chapter_view.ChapterView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})




urlpatterns = [
    path('catalog/search/', views.SearchCatalogView.as_view(), name='catalog'),
    path('', include(router.urls)),
    path('composition/', include('api.v1.chapter.urls')),
    path('votes/', include('api.v1.likedislike.urls')),
    path('activity/', include('api.v1.comment.urls')),


]
