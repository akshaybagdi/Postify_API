from rest_framework_simplejwt.tokens import RefreshToken  # For JWT token generation
from django.http import JsonResponse  # To return JSON responses
from django.contrib.auth import authenticate  # For user authentication
from django.contrib.auth.models import User  # To fetch user details


class TokenGenerationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self, request):
        try:
            # Use request.data directly
            if "username" in request.data and "password" in request.data:
                username = request.data.get('username')
                password = request.data.get('password')
                try:     # Check if the username exists in the database
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    return JsonResponse({'Error': 'User not found.'}, status=404)
                user = authenticate(username=username, password=password)    # Check if the password is correct for the given user
                if not user:
                    return JsonResponse({'Error': 'Invalid password.'}, status=401)
                refresh = RefreshToken.for_user(user)  # Generate tokens if the username and password are valid
                print("\n _____________________________________________________")
                # print("\n Access Token:", str(refresh.access_token))
                # print("\n Refresh Token:", str(refresh))
                print("\n Username:", str(username))
                print("\n ______________________________________________________")
                return JsonResponse(
                    {
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
                        'username': user.username
                    },
                    status=200
                )
        except Exception as e:
            return JsonResponse({'Error': f'An unexpected error occurred: {str(e)}'}, status=500)
