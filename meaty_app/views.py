from django.shortcuts import render
from meaty_app.serializers import UserSerializer
from django.contrib.auth import authenticate

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from meaty_app.models import UploadedImage
from meaty_app.serializers import UploadedImageSerializer, UserUploadHistorySerializer
from tensorflow import keras
from PIL import Image
import numpy as np

from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['POST'])
def user_register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response_data = {
            'error': False,
            'message': 'User Created'
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        response_data = {
            'error': True,
            'message': serializer.errors
        }
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        response_data = {
            'error': False,
            'message': 'success',
            'loginResult': {
                'userId': user.id,
                'name': user.first_name,
                'token': str(refresh.access_token)
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            'error': True,
            'message': 'failed',
            'loginResult': None
        }
        return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

User = get_user_model()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_image(request):
    try:
        uploaded_file = request.FILES['image']
        notes = request.data.get('notes')  # Ambil nilai notes dari permintaan POST

        # Memuat model H5
        model = keras.models.load_model('meaty_app/model_meaty.h5')

        # Memproses gambar dan melakukan prediksi
        img = Image.open(uploaded_file)
        img = img.resize((150, 150))  # Ubah ukuran gambar menjadi 150x150
        img_array = np.array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        prediction = model.predict(img_array)
        predicted_class = np.argmax(prediction)

        # Menentukan hasil prediksi
        if predicted_class == 0:
            prediction_result = 'Fresh'
        else:
            prediction_result = 'Spoiled'

        # Simpan uploaded_file ke database
        uploaded_image = UploadedImage(image=uploaded_file, user=request.user, prediction=prediction_result, notes=notes)
        uploaded_image.save()

        # Serialize uploaded_image
        serializer = UploadedImageSerializer(uploaded_image)

        # Mengirimkan respons JSON dengan result sebagai boolean
        return Response({'result': True, 'prediction': prediction_result})
    except Exception as e:
        # Jika terjadi kesalahan, mengirimkan respons JSON dengan result sebagai boolean False
        return Response({'result': False, 'error': str(e)})

@api_view(['GET'])
def user_upload_history(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        uploaded_images = UploadedImage.objects.filter(user=user)
        serializer = UserUploadHistorySerializer(uploaded_images, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

