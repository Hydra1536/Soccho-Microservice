from rest_framework.pagination import CursorPagination
from rest_framework.response import Response

class SocchoCursorPagination(CursorPagination):
    page_size = 10
    page_size_query_param = 'limit'
    cursor_query_param = 'cursor'
    ordering = 'created_at'

    def get_paginated_response(self, data):
        next_link = self.get_next_link()
        end_cursor = None
        if next_link and f"{self.cursor_query_param}=" in next_link:
            end_cursor = next_link.split(f"{self.cursor_query_param}=", 1)[1].split("&", 1)[0]
        return Response({
            'edges': data,
            'pageInfo': {
                'endCursor': end_cursor,
                'hasNextPage': bool(next_link),
            }
        })

