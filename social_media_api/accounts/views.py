from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
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

# Create your views here.
