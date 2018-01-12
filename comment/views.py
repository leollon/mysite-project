from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from comment.serializers import CommentSerializers

FORMAT_STRING = "%b %d %Y %a %H:%M:%S"


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
            return JsonResponse(success_msg, status=201)
        return JsonResponse(serializers.errors, status=400)
    else:
        error_msg = {'errMsg': 'Forbidden'}
        return JsonResponse(error_msg, status=400)
