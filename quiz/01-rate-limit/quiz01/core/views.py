# Create your views here.

# from core.models import CoreModel
from django_ratelimit.decorators import ratelimit
from django.http import HttpResponse,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from django_ratelimit.exceptions import Ratelimited
from django_ratelimit.core import get_usage, is_ratelimited

@method_decorator(csrf_exempt, name='dispatch')
class RateLimitAPI(View):

    @classmethod
    @method_decorator(ratelimit(key='ip', rate='100/s', method='GET'))
    def get(cls, request):
        block_info = ratelimit_tracking(cls,request,'100/s')
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
    # print(block_info)
    return block_info

#if over rate limit will redirect 403 to 429
def handler403(request, exception=None):
    if isinstance(exception, Ratelimited):

        if request.method == 'POST':
            block_info = ratelimit_tracking(RateLimitAPI.post,request,'1/s')
        elif request.method == 'GET':
            block_info = ratelimit_tracking(RateLimitAPI.get,request,'100/s')
        
        response = HttpResponse('Too Many Requests'+'\n'
                                + 'Retry-At: ' + str(block_info['time_left']), status=429)
        response['Retry-At'] = block_info['time_left']
        return response
    return HttpResponseForbidden('Forbidden')    




