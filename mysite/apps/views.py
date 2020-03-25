from django.http import JsonResponse
from utils import cache


def online(request):
    online_ips = cache.get('online_ips')
    return JsonResponse({'online_statistics': len(online_ips)})
