from rest_framework.pagination import PageNumberPagination


class TwentyObjectsSetPagination(PageNumberPagination):
    page_size = 20