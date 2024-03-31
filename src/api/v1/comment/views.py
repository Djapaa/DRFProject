from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum, Count, Prefetch
from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model


from .serializers import CommentUpdateSerializer, CommentSerializer
from .models import Comment
from ..viewsets.paginators import TwentyObjectsSetPagination
from ..viewsets.permissions import IsOwner

User = get_user_model()


class CommentView(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """ CRUD комментариев """

    model = None  # Модель данных

    filter_backends = [OrderingFilter]
    ordering_fields = ['time_create', 'score']
    ordering = ['-time_create']
    pagination_class = TwentyObjectsSetPagination

    def get_object(self):
        return get_object_or_404(self.model.objects.only('id'), pk=self.kwargs['pk'])

    def get_queryset(self):
        obj = self.get_object()
        return Comment.objects.filter(
            parent=None,
            object_id=obj.id,
            content_type=ContentType.objects.get_for_model(obj),
        ).annotate(
            score=Coalesce(Sum('votes'), 0),
            count_replies=Count('children')
        ).prefetch_related('author')

    def create(self, request, model_instance_pk, *args, **kwargs):
        """Добавление комментариев к обькту"""

        obj = self.get_object()
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        comment = Comment(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id,
            author=request.user
        )
        comment.content = serializer.validated_data.get('content')
        parent_id = serializer.validated_data.get('parent_id')
        if parent_id:
            try:
                comment.parent = Comment.objects.get(id=parent_id)
            except:
                return Response({'parant': 'object does not exists'}, status=status.HTTP_400_BAD_REQUEST)

        comment.save()
        return Response(

            {
                'msg': 'Комментарий был добавлен',
                'id': comment.id,
                'content': comment.content,
                'score': comment.votes.sum_rating(),
                'count_replies': comment.get_children().count(),
                'author': {
                    'id': comment.author.id,
                    'username': comment.author.username,
                    'avatar': comment.author.avatar.url
                }

            }, status=status.HTTP_201_CREATED)

    def update(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)

        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        comment.content = serializer.validated_data.get('content', comment.content)
        return Response(

            {
                'msg': 'Комментарий был изменён',
                'id': comment.id,
                'content': comment.content,
                'score': comment.votes.sum_rating(),
                'count_replies': comment.get_children().count(),
                'author': {
                    'id': comment.author.id,
                    'username': comment.author.username,
                    'avatar': comment.author.avatar.url
                }

            }, status=status.HTTP_200_OK)

    def destroy(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        self.perform_destroy(comment)
        return Response({'msg': 'Комментарий был удалён'}, status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.action == 'update':
            return CommentUpdateSerializer
        return CommentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), ]
        return [IsOwner(), ]


class CommentReplyView(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    serializer_class = CommentSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['time_create']
    ordering = ['time_create']

    def get_object(self):
        return get_object_or_404(Comment, pk=self.kwargs['pk'])

    def get_queryset(self):
        return self.get_object().get_children().annotate(
            score=Coalesce(Sum('votes'), 0),
            count_replies=Count('children')
        ).prefetch_related(
            Prefetch(
                'author',
                queryset=User.objects.all().only('id', 'username', 'avatar')
            )
        )
