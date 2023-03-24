# Create your views here.

# from core.models import CoreModel
from django_ratelimit.decorators import ratelimit
from django.http import HttpResponse,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from django_ratelimit.exceptions import Ratelimited
from django_ratelimit.core import get_usage, is_ratelimited
from core.models import GET_Model, POST_Model

@method_decorator(csrf_exempt, name='dispatch')
class RateLimitAPI(View):

    @classmethod
    @method_decorator(ratelimit(key='ip', rate='100/s', method='GET'))
    def get(cls, request):
        block_info = ratelimit_tracking(cls,request,'100/s')
        headerfiled_get_db(request,block_info)
        response = HttpResponse('X-RateLimit-Limit: '+str(block_info['limit'])+'\n'
                                + 'X-RateLimit-Remaining: '+ str(block_info['limit'] - block_info['count'] )+'\n'
                                + 'X-RateLimit-Reset: '+ str(block_info['time_left']))
        #header filed
        response['X-RateLimit-Limit'] = block_info['limit']
        response['X-RateLimit-Remaining'] = block_info['limit'] - block_info['count']
        response['X-RateLimit-Reset'] = block_info['time_left']
        return response
    
    @classmethod
    @method_decorator(ratelimit(key='ip', rate='1/s', method='Post'))
    def post(cls, request):
        block_info = ratelimit_tracking(cls,request,'1/s')
        headerfiled_post_db(request,block_info)
        response = HttpResponse('X-RateLimit-Limit: '+str(block_info['limit'])+'\n'
                                + 'X-RateLimit-Remaining: '+ str(block_info['limit'] - block_info['count'] )+'\n'
                                + 'X-RateLimit-Reset: '+ str(block_info['time_left']))
        #header filed
        response['X-RateLimit-Limit'] = block_info['limit']
        response['X-RateLimit-Remaining'] = block_info['limit'] - block_info['count']
        response['X-RateLimit-Reset'] = block_info['time_left']
        return response

#get ratelimit info
def ratelimit_tracking(fun,request,fun_rate):
    block_info = get_usage(request, key="ip",fn=fun, rate=fun_rate,increment =True)
    print(block_info)
    return block_info

def headerfiled_post_db(request,block_info):
    client_id = get_client_ip_address(request)
    if POST_Model.objects.filter(customer_ID=client_id).exists():
        db_info = POST_Model.objects.filter(customer_ID = client_id)
        db_info.update(Limit = block_info['limit'],
                       Remaining = block_info['limit'] - block_info['count'],
                       Reset =block_info['time_left'],
                       RetryAt = block_info['time_left'])
        
    else:
        POST_Model.objects.create(customer_ID = client_id,
                                  Limit = block_info['limit'],
                                  Remaining = block_info['limit'] - block_info['count'],
                                  Reset =block_info['time_left'],
                                  RetryAt = block_info['time_left'])

def headerfiled_get_db(request,block_info):
    client_id = get_client_ip_address(request)
    if GET_Model.objects.filter(customer_ID=client_id).exists():
        db_info = GET_Model.objects.filter(customer_ID = client_id)
        db_info.update(Limit = block_info['limit'],
                       Remaining = block_info['limit'] - block_info['count'],
                       Reset =block_info['time_left'],
                       RetryAt = block_info['time_left'])
        
    else:
        GET_Model.objects.create(customer_ID = client_id,
                                  Limit = block_info['limit'],
                                  Remaining = block_info['limit'] - block_info['count'],
                                  Reset =block_info['time_left'],
                                  RetryAt = block_info['time_left'])
        
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
            block_info = ratelimit_tracking(RateLimitAPI.post,request,'1/s')
        elif request.method == 'GET':
            block_info = ratelimit_tracking(RateLimitAPI.get,request,'100/s')
        headerfiled_get_db(request,block_info)
        response = HttpResponse('Too Many Requests'+'\n'
                                + 'Retry-At: ' + str(block_info['time_left']), status=429)
        response['Retry-At'] = block_info['time_left']
        return response
    return HttpResponseForbidden('Forbidden')    




