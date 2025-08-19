from django.core.cache import cache
from .models import Property
from django_redis import get_redis_connection
import logging


def get_all_properties():
    properties = cache.get('all_properties')

    if properties is None:
        print("Fetching from DB...")  # Debug print
        properties = list(Property.objects.all())  # Evaluate queryset to store safely
        cache.set('all_properties', properties, timeout=3600)
    else:
        print("Fetching from Cache...")  # Debug print

    return properties


logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    try:
        # Get the Redis connection
        redis_conn = get_redis_connection("default")

        # Get cache stats
        info = redis_conn.info()

        hits = info.get('keyspace_hits', 0)
        misses = info.get('keyspace_misses', 0)
        total = hits + misses

        # Calculate hit ratio
        # if total_requests > 0 else 0
        hit_ratio = (hits / total) if total > 0 else 0.0

        metrics = {
            'hits': hits,
            'misses': misses,
            'hit_ratio': round(hit_ratio, 4)
        }

        logger.info(f"Redis Cache Metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error fetching Redis metrics: {e}")
        return {
            'hits': 0,
            'misses': 0,
            'hit_ratio': 0.0,
            'error': str(e)
        }
