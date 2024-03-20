from rest_framework import serializers
from .models import Comment
from ..accounts.serializers import UserSerializer


class CommentCreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField(min_length=5, max_length=500)
    parent_id = serializers.IntegerField(min_value=0, required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = ('parent_id', 'content')



