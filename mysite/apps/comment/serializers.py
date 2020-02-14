from rest_framework import serializers

from .models import Comment


class CommentModelSerializer(serializers.ModelSerializer):

    created_time = serializers.DateTimeField(format="%a, %d %b %Y %H:%M:%S %z")

    class Meta:
        model = Comment
        exclude = ('id', 'post', )
