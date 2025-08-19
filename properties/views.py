from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Property
from .utils import get_all_properties
from .serializers import PropertySerializer

@method_decorator(cache_page(60 * 15), name='dispatch')  # 15 minutes
@api_view(['GET'])
def property_list(request):
    properties = get_all_properties()
    serializer = PropertySerializer(properties, many=True)
    return Response(serializer.data)