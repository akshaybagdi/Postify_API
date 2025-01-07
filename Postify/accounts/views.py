import logging
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from .middleware.middleware import TokenGenerationMiddleware
from django.http import JsonResponse
    
logger=logging.getLogger('__name__')

# User Registration Function
# @api_view(['POST'])
# @permission_classes([AllowAny])  # Allow any user to register
# def user_registration(request):
#     data = request.data
#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')
#
#     # Ensure all required fields are provided
#     if not username or not email or not password:
#         return Response({"Error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
#
#     if User.objects.filter(username=username).exists():
#         return Response({"Error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
#
#     if User.objects.filter(email=email).exists():
#         return Response({"Error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
#
#     user = User.objects.create_user(username=username, email=email, password=password)
#     user.is_active = True  # Ensure the user is active
#     user.save()
#     return Response({"Message": "User registered successfully."}, status=status.HTTP_201_CREATED)


def required_fields(func):
    def wrapper(request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        # Ensure all required fields are provided
        if not username or not email or not password:
            logger.warning("Validation failed: Missing required fields")
            return Response({"Error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)
        return func(request, *args, **kwargs)  # Call the original function if validation passes
    return wrapper


# Custom decorator to check if the username and email already exist
def check_existing_user(func):
    def wrapper(request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(username=username).exists():
            logger.warning(f"Registration attempt with existing username: {username}")
            return Response({"Error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            logger.warning(f"Registration attempt with existing email: {email}")
            return Response({"Error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        return func(request, *args, **kwargs)  # Call the original function if checks pass
    return wrapper


# The registration function-based view
@api_view(['POST'])  # This decorator makes it a view that can handle POST requests
@permission_classes([AllowAny])
@required_fields  # Apply the first decorator to validate the fields
@check_existing_user  # Apply the second decorator to check if the user already exists
def user_registration(request):
    logger.info("User registration endpoint accessed.")
    try:
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = True
        user.save()
        logger.info(f"User {username} registered successfully.")
        return Response({"Message": "User registered successfully."}, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"User registration failed: {str(e)}")
        return Response({"Error": "User registration failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# User Logout Function
@api_view(['POST'])
@permission_classes([AllowAny])
def user_logout(request):
    logger.info("User logout endpoint accessed.")
    try:
        # Log incoming request body
        # print("Request body:", request.data)
        logger.debug(f"Request body: {request.data}")
        refresh_token = request.data.get("refresh_token")
        print("\n _____________________________________________________")
        print("refresh_token:", refresh_token)
        print("\n _____________________________________________________")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info("Refresh token blacklisted successfully.")
        access_token = request.data.get("access_token")
        # print("\n _____________________________________________________")
        #
        # print("access_token:", access_token)
        # print("\n _____________________________________________________")
        if access_token:
            token = AccessToken(access_token)
            token.blacklist()
            logger.info("Access token blacklisted successfully.")
        return Response({"Message": "Successfully logged out."}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Logout failed: {str(e)}")
        return Response({"Error": f"Logout failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


# Login Function
@api_view(['POST'])
@permission_classes([AllowAny])  # Allow any user to login
@required_fields
def user_login(request):
    logger.info("User login endpoint accessed.")
    try:
        data = request.data
        if 'username' in data and 'password' in data:
            middleware = TokenGenerationMiddleware(None)  # Call the middleware method for token generation
            response = middleware.process_request(request)
            if isinstance(response, JsonResponse):
                logger.info("Token generated successfully.")
                return response  # Return the middleware's response if it handled the request
            logger.warning("Login failed: Invalid credentials.")
            return JsonResponse(
                {'Error': 'Invalid credentials.'}, status=400)
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        return JsonResponse({'Error': 'Login failed.'}, status=500)