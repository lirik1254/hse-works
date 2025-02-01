import json
import redis
from celery import shared_task
from django.conf import settings

from codeforces.service import get_user_dict

redis_client = redis.Redis.from_url(settings.CACHES["default"]["LOCATION"], decode_responses=True)


@shared_task
def refresh_cf_data(handle):
    print("рефрешу")
    cf_data = get_user_dict(handle)
    print(cf_data)
    redis_client.set(handle, json.dumps(cf_data))
    refresh_cf_data.apply_async((handle,), countdown=86400)

