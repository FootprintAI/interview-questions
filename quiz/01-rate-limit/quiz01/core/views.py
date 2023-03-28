# Create your views here.

from django.http import HttpResponse,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from core.models import GET_Model, POST_Model

import functools
from django.conf import settings
from django.core.cache import caches
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

# django_ratelimit
from django_ratelimit.exceptions import Ratelimited
from django_ratelimit.decorators import ratelimit
from django_ratelimit.core import get_usage, _SIMPLE_KEYS, _ACCESSOR_KEYS, _get_window, _make_cache_key, _split_rate
from django_ratelimit import ALL, UNSAFE


@method_decorator(csrf_exempt, name='dispatch')
class RateLimitAPI(View):
    @method_decorator(ratelimit(group = 'get',key='ip', rate='100/s', method='GET'))
    def get(self,request):
        block_info = get_usage(group = 'get', request=request ,key='ip', rate='100/s', method='GET', increment =False)
        response = ratelimit_response(block_info)
        headerfiled_get_db(request,block_info)

        return response
    
    @method_decorator(ratelimit(group = 'post', key='ip', rate='1/s', method='POST'))
    def post(self,request):
        block_info = get_usage(group = 'post', request=request ,key='ip', rate='1/s', method='POST', increment =False)
        response = ratelimit_response(block_info)
        headerfiled_post_db(request,block_info)
        
        return response
    
def reset(request, group=None, fn=None, key=None, rate=None, method=ALL, increment=False):
    group = request.POST['group']
    key = request.POST['key']
    rate = request.POST['rate']
    method = request.POST['method']
    if group is None and fn is None:
        raise ImproperlyConfigured('get_usage must be called with either '
                                   '`group` or `fn` arguments')

    if not getattr(settings, 'RATELIMIT_ENABLE', True):
        return None

    if group is None:
        parts = []

        if isinstance(fn, functools.partial):
            fn = fn.func

        # Django <2.1 doesn't use a partial. This is ugly and inelegant, but
        # throwing __qualname__ into the list below helps.
        if fn.__name__ == 'bound_func':
            fn = fn.__closure__[0].cell_contents

        if hasattr(fn, '__module__'):
            parts.append(fn.__module__)

        if hasattr(fn, '__self__'):
            parts.append(fn.__self__.__class__.__name__)

        parts.append(fn.__qualname__)
        group = '.'.join(parts)
    
    if callable(rate):
        rate = rate(group, request)
    elif isinstance(rate, str) and '.' in rate:
        ratefn = import_string(rate)
        rate = ratefn(group, request)

    if rate is None:
        return HttpResponse('Ratelimit rate is None)',status=200)
    limit, period = _split_rate(rate)
    if period <= 0:
        raise ImproperlyConfigured('Ratelimit period must be greater than 0')
    
    if not key:
        raise ImproperlyConfigured('Ratelimit key must be specified')
    if callable(key):
        value = key(group, request)
    elif key in _SIMPLE_KEYS:
        value = _SIMPLE_KEYS[key](request)
    elif ':' in key:
        accessor, k = key.split(':', 1)
        if accessor not in _ACCESSOR_KEYS:
            raise ImproperlyConfigured('Unknown ratelimit key: %s' % key)
        value = _ACCESSOR_KEYS[accessor](request, k)
    elif '.' in key:
        keyfn = import_string(key)
        value = keyfn(group, request)
    else:
        raise ImproperlyConfigured(
            'Could not understand ratelimit key: %s' % key)
    
    window = _get_window(value, period)

    cache_name = getattr(settings, 'RATELIMIT_USE_CACHE', 'default')
    cache = caches[cache_name]
    cache_key = _make_cache_key(group, window, rate, value, method)
    cache.get(cache_key)
    if cache.delete(cache_key) == True:
        return HttpResponse('Reseted',status=205)
    return HttpResponse('An error occurred from reset',status=400)
    

#build ratelimit response
def ratelimit_response(block_info):
    response = HttpResponse('X-RateLimit-Limit: '+str(block_info['limit'])+'\n'
                                + 'X-RateLimit-Remaining: '+ str(block_info['limit'] - block_info['count'] )+'\n'
                                + 'X-RateLimit-Reset: '+ str(block_info['time_left']))
    #header filed
    response['X-RateLimit-Limit'] = block_info['limit']
    response['X-RateLimit-Remaining'] = block_info['limit'] - block_info['count']
    response['X-RateLimit-Reset'] = block_info['time_left']
    # print(block_info)
    return response

def headerfiled_post_db(request,block_info):
    client_id = get_client_ip_address(request)
    if POST_Model.objects.filter(customer_ID=client_id).exists():
        try:
            db_info = POST_Model.objects.filter(customer_ID = client_id)
            db_info.update(Limit = block_info['limit'],
                       Remaining = block_info['limit'] - block_info['count'],
                       Reset =block_info['time_left'],
                       RetryAt = block_info['time_left'])
        except Exception as ex:
            print("Error during update data of post (Possibly unsupported):", ex)
    else:
        try:
            POST_Model.objects.create(customer_ID = client_id,
                                  Limit = block_info['limit'],
                                  Remaining = block_info['limit'] - block_info['count'],
                                  Reset =block_info['time_left'],
                                  RetryAt = block_info['time_left'])
        except Exception as ex:
            print("Error during create data of post(Possibly unsupported):", ex)
        

def headerfiled_get_db(request,block_info):
    client_id = get_client_ip_address(request)
    if GET_Model.objects.filter(customer_ID=client_id).exists():
        try:
            db_info = GET_Model.objects.filter(customer_ID = client_id)
            db_info.update(Limit = block_info['limit'],
                       Remaining = block_info['limit'] - block_info['count'],
                       Reset =block_info['time_left'],
                       RetryAt = block_info['time_left'])
        except Exception as ex:
            print("Error during update data of post (Possibly unsupported):", ex)
    else:
        try:
            GET_Model.objects.create(customer_ID = client_id,
                                  Limit = block_info['limit'],
                                  Remaining = block_info['limit'] - block_info['count'],
                                  Reset =block_info['time_left'],
                                  RetryAt = block_info['time_left'])
        except Exception as ex:
            print("Error during create data of get(Possibly unsupported):", ex)
        
        
def get_client_ip_address(request):
    req_headers = request.META
    x_forwarded_for_value = req_headers.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for_value:
        ip_addr = x_forwarded_for_value.split(',')[-1].strip()
    else:
        ip_addr = req_headers.get('REMOTE_ADDR')
    return ip_addr

#if over rate limit will redirect 403 to 429
def handler403(request, exception=None):
    if isinstance(exception, Ratelimited):
        print("Over Rating")
        if request.method == 'POST':
            block_info = get_usage(group = 'post', request=request ,key='ip', rate='1/s', method='POST', increment =False)
        elif request.method == 'GET':
            block_info = get_usage(group = 'get', request=request ,key='ip', rate='100/s', method='GET', increment =False)
        headerfiled_get_db(request,block_info)
        response = HttpResponse('Too Many Requests'+'\n'
                                + 'Retry-At: ' + str(block_info['time_left']), status=429)
        response['Retry-At'] = block_info['time_left']
        return response
    return HttpResponseForbidden('Forbidden')    




