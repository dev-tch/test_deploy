from .models import Window, CustomUser, Office
from rest_framework import serializers


class WindowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Window
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = '__all__'
