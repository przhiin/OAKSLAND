from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model, authenticate, login, logout
from .models import CustomUser

User = get_user_model()


# -------------------- LOGIN --------------------
class LoginRequest(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful", "user_id": user.id})
        else:
            return Response({"error": "Invalid username or password"}, status=400)


# -------------------- REGISTER --------------------
class RegisterRequest(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")
        phone = request.data.get("phone")
        address = request.data.get("address")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address
        )

        return Response({"message": "Registration complete", "user_id": user.id})


# -------------------- LOGOUT --------------------
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=200)


# -------------------- PROFILE --------------------
class ViewProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "address": user.address,
        }
        return Response({"profile": data})


class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        # Update fields if present
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.email = data.get("email", user.email)
        user.phone = data.get("phone", user.phone)
        user.address = data.get("address", user.address)

        user.save()
        return Response({"message": "Profile updated successfully"})


# -------------------- SUPERUSER LOGIN --------------------
class SuperuserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user and user.is_superuser:
            login(request, user)
            return Response({"success": True, "message": "Superuser logged in!"})
        return Response({"success": False, "message": "Invalid superuser credentials"})







# import json
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth import get_user_model, authenticate, login, logout
# from django.contrib.auth.decorators import login_required
# from .models import CustomUser

# User = get_user_model()

# # -------------------- LOGIN --------------------
# @csrf_exempt
# def login_request(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         username = data.get("username")
#         password = data.get("password")

#         if not username or not password:
#             return JsonResponse({"error": "Username and password required"}, status=400)

#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return JsonResponse({"message": "Login successful", "user_id": user.id})
#         else:
#             return JsonResponse({"error": "Invalid username or password"}, status=400)


# # -------------------- REGISTER --------------------
# @csrf_exempt
# def register_request(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         username = data.get("username")
#         password = data.get("password")
#         first_name = data.get("first_name")
#         last_name = data.get("last_name")
#         email = data.get("email")
#         phone = data.get("phone")
#         address = data.get("address")

#         if not username or not password:
#             return JsonResponse({"error": "Username and password required"}, status=400)

#         if User.objects.filter(username=username).exists():
#             return JsonResponse({"error": "Username already exists"}, status=400)

#         user = User.objects.create_user(
#             username=username,
#             password=password,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             phone=phone,
#             address=address
#         )

#         return JsonResponse({"message": "Registration complete", "user_id": user.id})


# # -------------------- LOGOUT --------------------
# @csrf_exempt
# def logout_view(request):
#     if request.method == "POST":
#         logout(request)
#         return JsonResponse({"message": "Logout successful"}, status=200)
#     return JsonResponse({"error": "Invalid request"}, status=400)


# # -------------------- PROFILE --------------------
# @login_required
# def view_profile(request):
#     user = request.user
#     data = {
#         "username": user.username,
#         "email": user.email,
#         "first_name": user.first_name,
#         "last_name": user.last_name,
#         "phone": user.phone,
#         "address": user.address,
#     }
#     return JsonResponse({"profile": data})


# @login_required
# @csrf_exempt
# def update_profile(request):
#     if request.method == "POST":
#         data = json.loads(request.body.decode("utf-8"))
#         user = request.user

#         # Update fields if present
#         user.first_name = data.get("first_name", user.first_name)
#         user.last_name = data.get("last_name", user.last_name)
#         user.email = data.get("email", user.email)
#         user.phone = data.get("phone", user.phone)
#         user.address = data.get("address", user.address)

#         user.save()
#         return JsonResponse({"message": "Profile updated successfully"})
#     return JsonResponse({"error": "Invalid request"}, status=400)


# # -------------------- SUPERUSER LOGIN --------------------
# @csrf_exempt
# def superuser_login(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         username = data.get("username")
#         password = data.get("password")

#         user = authenticate(username=username, password=password)
#         if user and user.is_superuser:
#             login(request, user)
#             return JsonResponse({"success": True, "message": "Superuser logged in!"})
#         return JsonResponse({"success": False, "message": "Invalid superuser credentials"})


