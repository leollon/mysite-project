from collections import OrderedDict

from rest_framework import pagination
from rest_framework.response import Response


class CustomizedCursorPagination(pagination.CursorPagination):

    page_size = 10
    ordering = '-created_time'
    cursor_query_param = 'cur'  # cursor

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('results', data),
            ('count', len(data)),
            ('links', OrderedDict([('next', self.get_next_link()), ('previous', self.get_previous_link())])),
        ]))
