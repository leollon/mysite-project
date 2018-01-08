from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from comment.models import Comment
from comment.serializers import CommentSerializers

FORMAT_STRING = "%b %d %Y %a %H:%M:%S"


@csrf_exempt
def comment_list(request, id):
    """
    List all comment, or create a new comment object
    :param request: HttpRequest
    :param id: post's id
    :return: JsonResponse Object
    """
    if request.method == 'GET':
        comments = Comment.objects.filter(post_id=id)
        for comment in comments:
            setattr(comment,
                    'created_time',
                    comment.created_time.strftime(FORMAT_STRING))
        serializers = CommentSerializers(comments, many=True)
        for s in serializers.data:
            s.pop('email')
        return JsonResponse(serializers.data, safe=False)
    else:
        error_msg = {'errorMsg': 'Forbidden'}
        return JsonResponse(error_msg, status=400)


@csrf_exempt
def create_comment(request):
    """
    comment api for post request
    :param request: HttpRequest object
    :return: JsonResponse Object
    """
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializers = CommentSerializers(data=data)
        if serializers.is_valid():
            serializers.save()
            success_msg = {'successMsg': 'success'}
            return JsonResponse(success_msg, status=200)
        return JsonResponse(serializers.errors, status=400)
    else:
        error_msg = {'errMsg': 'Forbidden'}
        return JsonResponse(error_msg, status=400)
