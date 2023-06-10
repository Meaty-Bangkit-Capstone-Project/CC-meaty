from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'usia', 'domisili', 'pekerjaan', 'gender']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

from .models import UploadedImage

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = '__all__'

class UserUploadHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ['image', 'timestamp', 'prediction', 'notes']
