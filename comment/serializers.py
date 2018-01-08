from rest_framework import serializers

from comment.models import Comment


class CommentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('username', 'email', 'link', 'comment_text', 'created_time',
                  'post')
