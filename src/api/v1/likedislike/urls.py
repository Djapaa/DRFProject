from django.urls import path, re_path

from . import views
from .models import LikeDislike
from ..chapter.models import Chapter

urlpatterns = [
    re_path(r'^chapter/(?P<pk>\d+)/like/$', views.VotesView.as_view(model=Chapter, vote_type=LikeDislike.LIKE),
            name='chapter_like'),
]
