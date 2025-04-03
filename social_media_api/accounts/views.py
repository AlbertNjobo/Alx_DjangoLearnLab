from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import UserSerializer, ProfileSerializer

class RegisterView(generics.CreateAPIView):
    """API view for user registration
        Creates a new user and returns user data along with the auth token

    """
    queryset = CustomUser.objects.all
    permission_classes = [permissions.AllowAny] #Anyone can register
    serializer_class = UserSerializer

    def create(self,request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save() #Calls serializer.create

        #--- Create token for the user using rest_framework.authtoken
        token, created = Token.objects.get_or_create(user=user)
        token_data = {'token': token.key}

        #--- Return user data and token in the response

        #---Prepare Response Data ---

        response_data = serializer.data
        response_data.pop('password',None)
        response_data.pop('password2',None)
        response_data.update(token_data) #Add token to response

        headers = self.get_success_headers(serializer.data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
    
    #Note : Login is handled by build-in view imported in urls.py

class ProfileView(generics.RetrieveUpdateAPIView):
    """API view for user profile
        Allows users to view and update their profile information

    """
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated] #Only authenticated users can access this view
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user #Get the current logged-in user

class CustomLoginView(APIView):
    """
    Custom login view to handle both GET and POST requests.
    """
    def get(self, request, *args, **kwargs):
        # Provide instructions for using the login endpoint
        return Response({
            "detail": "Send a POST request with 'username' and 'password' to obtain an auth token.",
            "example_body": {
                "username": "your_username",
                "password": "your_password"
            }
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Handle login and token generation
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        if target_user == request.user:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.following.add(target_user)
        return Response({"detail": f"You are now following {target_user.username}."}, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        request.user.following.remove(target_user)
        return Response({"detail": f"You have unfollowed {target_user.username}."}, status=status.HTTP_200_OK)

# Create your views here.
