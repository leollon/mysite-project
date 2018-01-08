from django.template.library import Library


from comment.models import Comment

register = Library()


@register.simple_tag(name='get_comments')
def get_post_comments(post_id):
    return Comment.objects.order_by('-created_time').filter(post_id=post_id)
