from rest_framework import serializers
from rest_framework.settings import api_settings
from core.models import CoreModel

class CoreSerializers(serializers.ModelSerializer):

    last_modify_date = serializers.DateTimeField(format=api_settings.DATETIME_FORMAT, required = False)
    created = serializers.DateTimeField(format=api_settings.DATETIME_FORMAT, required = False)

    class Meta:
        model = CoreModel
        # fields = '__all__'
        fields = ('id', 'song', 'singer', 'last_modify_date', 'created')