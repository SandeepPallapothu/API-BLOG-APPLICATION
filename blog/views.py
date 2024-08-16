from django.shortcuts import render
from .models import *
from .serializer import *
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView,GenericAPIView


#post operations
class BlogList(ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

class BlogUpdate(RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


#comment operations
class CommentList(ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

class CommentRetrieve(RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

#Register form
class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

#login form
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username = username, password = password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user' : user_serializer.data
            })
        else:
            return Response({'detail':'Invalid Credentials'}, status=401)