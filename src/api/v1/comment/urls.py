from django.urls import path
from . import views
from ..composition.models import Composition

comments_add = views.CommentView.as_view(
    {
        'post': 'create'
    },
    model=Composition
)

urlpatterns = [
    path('<int:composition_pk>/comments/', comments_add, name='composition-comments-add'),
]
