# Create your views here.
from core.models import CoreModel
from core.serializers import CoreSerializers

from rest_framework import viewsets


# Create your views here.
class CoreViewSet(viewsets.ModelViewSet):
    queryset = CoreModel.objects.all()
    serializer_class = CoreSerializers
