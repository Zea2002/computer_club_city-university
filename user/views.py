from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from .models import User
from .serializers import UserSerializer, RegistrationSerializer, UserLoginSerializer
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/users/activate/{uid}/{token}/"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_mail.html', {"confirm_link": confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response({"message": "User registered successfully. Please check your email to activate your account."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        context = {'success': True, 'message': 'User activated successfully.'}
    else:
        context = {'success': False, 'message': 'Activation link is invalid.'}
    
    # Check if the request is AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(context)
    return render(request, 'activation_response.html', context)   
   


class UserLoginApiView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token': token.key, 'user_id': user.id, 'username': user.username}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
