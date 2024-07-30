from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
class EventPagination(PageNumberPagination):
    page_size = 10  
    page_query_param = 'page'  

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'  

    def paginated_response(self, data):
        return Response({
            'success': 'True',
            'message': 'data retrieved successfully',
            "data":data,
            'pagination_info': {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            }
        })