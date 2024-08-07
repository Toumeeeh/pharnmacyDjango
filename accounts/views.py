from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.serializer import CustomUserSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken


@api_view(['POST'])
def register(request):
    try:
        with transaction.atomic():
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.set_password(request.data['password'])
                user.save()
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': serializer.data
                }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = get_user_model()

    try:
        users = user.objects.get(username=username)
    except user.DoesNotExist:
        return JsonResponse({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if not users.check_password(password):
        return JsonResponse({"detail": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)

    refresh = RefreshToken.for_user(users)
    access = str(refresh.access_token)

    return JsonResponse({
        'refresh': str(refresh),
        'access': access,
        'user': {
            'username': user.username,
            'email': user.email,
            'user_type': user.user_type
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
    except InvalidToken as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)