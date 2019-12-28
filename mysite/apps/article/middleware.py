import logging
import re
from datetime import datetime

from ipware.ip import get_real_ip
from utils import cache

logger = logging.getLogger(__name__)


class ResponseTimeMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.beg_time = datetime.now().timestamp()
        response = self.get_response(request)
        end_time = datetime.now().timestamp() - self.beg_time
        content = response.content.decode('utf-8')
        response.content = content.replace(
            "RENDER_TIME",
            str(end_time)[:5]).encode('utf-8')
        return response


class OnlineMiddleware(object):
    """访问IP
    统计网站五分钟内容访问的IP
        args:
            :request type: HttpRequest
            :view_func type: Python function
            :view_args type: tuple, positional arguments
            :view_kwargs type: dict, keyword arguments
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        resposne = self.get_response(request)
        return resposne

    def process_view(self, request, view_func, view_args, view_kwargs):
        http_user_agent = request.META.get("HTTP_USER_AGENT", '')
        re_pat = re.compile(
            r".*bot.*|.*spider.*|.*curl.*|.*request.*|.*wget.*")
        if re.search(re_pat, http_user_agent):
            # 不统计爬虫IP
            return

        online_ips = cache.get('online_ips', set())

        ip = get_real_ip(request)
        cache.set(ip, 0, 5 * 60)
        online_ips.add(ip)

        cache.set("online_ips", online_ips)


class VerifyMiddleware(object):
    """
    评论回复验证码
    """
    pass
