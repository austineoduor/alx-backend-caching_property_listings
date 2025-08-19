from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .utils import get_all_properties,get_redis_cache_metrics
from .serializers import PropertySerializer

@cache_page(60 * 15) # 15 minutes
@api_view(['GET'])
def property_list(request):
    properties = get_all_properties()
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)

from django.http import JsonResponse

def cache_metrics(request):
    metrics = get_redis_cache_metrics()
    return JsonResponse(metrics)