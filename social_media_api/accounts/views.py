from rest_framework import generics, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, UserProfileSerializer
from .models import User as CustomUser

class UserListView(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        }, status=status.HTTP_201_CREATED)

class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        if request.user == user_to_follow:
            return Response(
                {'error': 'You cannot follow yourself.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if not request.user.following.filter(id=user_to_follow.id).exists():
            request.user.following.add(user_to_follow)
            return Response(
                {'message': f'You are now following {user_to_follow.username}'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'message': f'You are already following {user_to_follow.username}'},
            status=status.HTTP_400_BAD_REQUEST
        )

class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        if request.user == user_to_unfollow:
            return Response(
                {'error': 'You cannot unfollow yourself.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.user.following.filter(id=user_to_unfollow.id).exists():
            request.user.following.remove(user_to_unfollow)
            return Response(
                {'message': f'You have unfollowed {user_to_unfollow.username}'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'message': f'You are not following {user_to_unfollow.username}'},
            status=status.HTTP_400_BAD_REQUEST
        )
