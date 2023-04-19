from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Молель пагинации"""

    page_size_query_param = 'limit'
