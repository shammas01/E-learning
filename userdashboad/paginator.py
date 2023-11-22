from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination

class CustomUserListPagination(PageNumberPagination):
    page_size = 1 
    page_query_param = "page"