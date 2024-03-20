from django.contrib.contenttypes.models import ContentType
from rest_framework import mixins, viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import CommentCreateSerializer
from .models import Comment

CreateAPIView


class CommentView(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = CommentCreateSerializer
    model = None  # Модель данных

    def create(self, request, composition_pk, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=composition_pk)
        serializer = CommentCreateSerializer(data=self.request.data)
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

    def update(self, request, *args, **kwargs):
        pass


    # def post(self, request, pk):
    #     obj = self.model.objects.get(pk=pk)
    #     form = CommentCreateForm(request.POST)
    #     if form.is_valid():
    #         comment = Comment.objects.create(content_type=ContentType.objects.get_for_model(obj),
    #                                              object_id=obj.id,
    #                                              author=request.user)
    #         comment.content = form.cleaned_data.get('content', '')
    #         parent_id = form.cleaned_data.get('parent', None)
    #         if parent_id:
    #             try:
    #                 comment.parent = Comment.objects.get(id=parent_id)
    #                 comment.save()
    #             except:
    #                 comment.delete()
    #
    #         else:
    #             comment.save()
