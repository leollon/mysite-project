from rest_framework import pagination


class CustomizedCursorPagination(pagination.CursorPagination):

    page_size = 10
    ordering = '-created_time'
