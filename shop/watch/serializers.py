from rest_framework import serializers
#
from .models import Watches

class WatchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watches
        fields = '__all__'