from rest_framework import serializers
from ksrtc.models import BusTrip
from django.contrib.auth.models import User


class BusTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusTrip
        fields = '__all__'

        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_superuser']  # Include only these fields

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user