from django.utils import timezone
from rest_framework import serializers

from .models import Comment


class CommentModelSerializer(serializers.ModelSerializer):

    created_time = serializers.DateTimeField(format="%a, %d %b %Y %H:%M:%S %z", default=timezone.now)

    class Meta:
        model = Comment
        exclude = ('id', )
        read_only_fields = ('created_time',)
        extra_kwargs = {'email': {'write_only': True}}
