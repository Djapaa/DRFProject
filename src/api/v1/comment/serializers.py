from rest_framework import serializers
from .models import Comment
from ..accounts.serializers import UserSerializer



class CommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    parent_id = serializers.IntegerField(min_value=0, required=False, allow_null=True, write_only=True)
    score = serializers.DecimalField(max_digits=7, decimal_places=0, read_only=True)
    count_replies = serializers.IntegerField(read_only=True)
    author = UserSerializer(read_only=True)
    time_create = serializers.DateTimeField(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'content', 'score', 'count_replies', 'time_create', 'author', 'parent_id')


class CommentUpdateSerializer(CommentSerializer):
    parent_id = serializers.IntegerField(min_value=0, required=False, allow_null=True, read_only=True)


