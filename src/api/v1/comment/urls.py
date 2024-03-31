from django.urls import path
from . import views
from ..composition.models import Composition


comment_list_add = views.CommentView.as_view(
    {
        'get': 'list',
        'post': 'create'
    },
    model=Composition
)
comment_update = views.CommentView.as_view(
    {
        'put': 'update',
        'delete': 'destroy',
    }
)

comment_reply = views.CommentReplyView.as_view(
    {
        'get': 'list'
    }
)

urlpatterns = [
    path('composition/<int:pk>/comments/', comment_list_add, name='composition-comments-get-or-add'),
    path('comments/<int:pk>/', comment_update, name='composition-comments-update'),
    path('comments/<int:pk>/reply/', comment_reply, name='comment-reply')
]
