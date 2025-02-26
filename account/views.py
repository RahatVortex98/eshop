from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer, UserSerializer

from django.utils.crypto import get_random_string
from datetime import datetime,timedelta
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from .models import Profile



# Create your views here.
@api_view(["POST"])
def register(request):
    data=request.data

    user = SignUpSerializer(data=data)

    if user.is_valid():
        if not User.objects.filter(username=data['email']).exists():

            user = User.objects.create(
                first_name = data['first_name'],
                last_name = data['last_name'],
                email = data['email'],
                username = data['email'],
                password = make_password(data['password']),

            )
            return Response({'details':'User Registered'},status=status.HTTP_201_CREATED)
        else:
            return Response({'error':'User Already Exist'},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user.errors)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def currentUser(request):
    user = UserSerializer(request.user)
    return Response(user.data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateUser(request):

    user = request.user
    data = request.data 

    user.first_name = data['first_name']
    user.last_name =data['last_name']
    user.username = data['email']
    user.email = data['email']

    if data['password'] != "":
        user.password = make_password(data['password'])

        user.save()
        serializer =UserSerializer(user,many=False)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

#FORGOT Pasword and send token to email address>>>>>

def get_current_host(request):
    """
    Returns the current host URL with the correct protocol (http or https).
    """
    protocol = "https" if request.is_secure() else "http"  # Check if the request is secure
    host = request.get_host()  # Get the domain (e.g., example.com)
    return "{protocol}://{host}/".format(protocol=protocol, host=host)  # Return full base URL

@api_view(['POST'])  # This function handles POST requests
def forgot_password(request):
    """
    Generates a password reset token, saves it in the user's profile, and sends an email with the reset link.
    """
    data = request.data  # Get JSON data from the request (contains user email)
    user = get_object_or_404(User, email=data['email'])  # Fetch user by email or return 404 if not found

    # Generate a random 40-character reset token
    token = get_random_string(40)  
    expire_date = datetime.now() + timedelta(minutes=30)  # Token expires in 30 minutes

    # Store the token and expiry time in the user's profile
    user.profile.reset_password_token = token
    user.profile.reset_password_expire = expire_date
    user.profile.save()  # Save changes to the database

    # Generate password reset link with user ID and token
    host = get_current_host(request)  
    link = "{host}api/reset_password/{user_id}/{token}".format(host=host, user_id=user.id, token=token)

    # Email message body
    body = "Your Password Reset Link Is: {link}".format(link=link)

    # Send email to user
    send_mail(
        "Password Reset For eShop",  # Email subject
        body,  # Email body
        "noreply@eshop.com",  # Sender email
        [data['email']]  # Recipient list
    )

    # Return success response
    return Response({'details': 'Password reset email sent to: {email}'.format(email=data['email'])})


@api_view(['POST'])  # This API only accepts POST requests
def reset_password(request, token):  # Function to reset password, takes request and token as arguments
    data = request.data  # Extracts the request data (contains new password)
    new_password = data.get('password')  # Gets the new password from request data

    profile = get_object_or_404(Profile, reset_password_token=token)  # Fetch profile using the reset token, or return 404 if not found

    if profile.reset_password_expire < datetime.now():  # Checks if the reset token has expired
        return Response({'error': 'Reset token has expired'}, status=status.HTTP_400_BAD_REQUEST)  # Returns error if expired

    if not new_password or len(new_password) < 6:  # Checks if the password is empty or too short
        return Response({'error': 'Password must be at least 6 characters'}, status=status.HTTP_400_BAD_REQUEST)  # Returns error if invalid

    user = profile.user  # Gets the associated user from the profile
    user.password = make_password(new_password)  # Hashes and updates the user's password
    user.save()  # Saves the updated password to the database

    profile.reset_password_token = ""  # Clears the reset token so it can't be used again
    profile.reset_password_expire = None  # Clears the expiration time
    profile.save()  # Saves the updated profile

    return Response({'detail': 'Password reset successful'})  # Returns a success message
