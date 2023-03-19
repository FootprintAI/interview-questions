# Create your views here.

# from core.models import CoreModel
from django_ratelimit.decorators import ratelimit
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View

@method_decorator(csrf_exempt, name='dispatch')
class RateLimitAPI(View):
    @method_decorator(ratelimit(key='ip', rate='100/s', method='GET'))
    def get(self, request):
        response = HttpResponse()
        return response
    
    @method_decorator(ratelimit(key='ip', rate='1/s', method='Post'))
    def post(self, request):
        response = HttpResponse()
        return response




