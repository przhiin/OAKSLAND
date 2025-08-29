import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser

User = get_user_model()

# -------------------- LOGIN --------------------
@csrf_exempt
def login_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return JsonResponse({"error": "Username and password required"}, status=400)

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful", "user_id": user.id})
        else:
            return JsonResponse({"error": "Invalid username or password"}, status=400)


# -------------------- REGISTER --------------------
@csrf_exempt
def register_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        phone = data.get("phone")
        address = data.get("address")

        if not username or not password:
            return JsonResponse({"error": "Username and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address
        )

        return JsonResponse({"message": "Registration complete", "user_id": user.id})


# -------------------- LOGOUT --------------------
@csrf_exempt
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return JsonResponse({"message": "Logout successful"}, status=200)
    return JsonResponse({"error": "Invalid request"}, status=400)


# -------------------- PROFILE --------------------
@login_required
def view_profile(request):
    user = request.user
    data = {
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "address": user.address,
    }
    return JsonResponse({"profile": data})


@login_required
@csrf_exempt
def update_profile(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        user = request.user

        # Update fields if present
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.email = data.get("email", user.email)
        user.phone = data.get("phone", user.phone)
        user.address = data.get("address", user.address)

        user.save()
        return JsonResponse({"message": "Profile updated successfully"})
    return JsonResponse({"error": "Invalid request"}, status=400)


# -------------------- SUPERUSER LOGIN --------------------
@csrf_exempt
def superuser_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user and user.is_superuser:
            login(request, user)
            return JsonResponse({"success": True, "message": "Superuser logged in!"})
        return JsonResponse({"success": False, "message": "Invalid superuser credentials"})






# import random
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth import get_user_model
# from django.utils import timezone
# import json
# from .models import OTP
# from django.contrib.auth.decorators import login_required
# from .models import CustomUser
# from django.contrib.auth import logout
# from django.contrib.auth import authenticate, login
# from django.http import JsonResponse
# from .models import CustomUser
# import random


# User = get_user_model()


# def generate_otp():
#     return str(random.randint(100000, 999999))


# # -------------------- LOGIN --------------------
# @csrf_exempt
# def login_request_otp(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         phone = data.get("phone")
#         email = data.get("email")

#         if not phone and not email:
#             return JsonResponse({"error": "Phone or Email required"}, status=400)

#         try:
#             user = User.objects.get(phone=phone) if phone else User.objects.get(email=email)
#         except User.DoesNotExist:
#             return JsonResponse({"error": "User does not exist, please register"}, status=404)

#         otp = OTP.objects.create(user=user, code=generate_otp())
#         return JsonResponse({"message": "OTP sent", "otp": otp.code})  # in real case: send via SMS/Email


# @csrf_exempt
# def login_verify_otp(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         phone = data.get("phone")
#         otp_code = data.get("otp")

#         try:
#             user = User.objects.get(phone=phone)
#             otp = OTP.objects.filter(user=user, code=otp_code, is_used=False).last()

#             if not otp:
#                 return JsonResponse({"error": "Invalid or expired OTP"}, status=400)

#             otp.is_used = True
#             otp.save()
#             return JsonResponse({"message": "Login successful", "user_id": user.id})

#         except User.DoesNotExist:
#             return JsonResponse({"error": "User not found"}, status=404)


# # -------------------- REGISTER --------------------
# @csrf_exempt
# def register_request_otp(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         phone = data.get("phone")
#         email = data.get("email")

#         if not phone and not email:
#             return JsonResponse({"error": "Phone or Email required"}, status=400)

#         # Create user if not exists
#         user, created = User.objects.get_or_create(phone=phone, defaults={"email": email})
#         otp = OTP.objects.create(user=user, code=generate_otp())

#         return JsonResponse({"message": "OTP sent", "otp": otp.code})


# @csrf_exempt
# def register_verify_otp(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         phone = data.get("phone")
#         otp_code = data.get("otp")

#         try:
#             user = User.objects.get(phone=phone)
#             otp = OTP.objects.filter(user=user, code=otp_code, is_used=False).last()

#             if not otp:
#                 return JsonResponse({"error": "Invalid or expired OTP"}, status=400)

#             otp.is_used = True
#             otp.save()

#             return JsonResponse({"message": "Phone verified, please complete registration", "user_id": user.id})

#         except User.DoesNotExist:
#             return JsonResponse({"error": "User not found"}, status=404)


# @csrf_exempt
# def complete_registration(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         user_id = data.get("user_id")

#         try:
#             user = User.objects.get(id=user_id)
#             user.email = data.get("email", user.email)
#             user.address = data.get("address", user.address)
#             user.save()

#             return JsonResponse({"message": "Registration complete", "user_id": user.id})

#         except User.DoesNotExist:
#             return JsonResponse({"error": "User not found"}, status=404)

# @csrf_exempt
# def logout_view(request):
#     if request.method == "POST":
#         logout(request)   # Clears the session
#         return JsonResponse({"message": "Logout successful"}, status=200)
#     return JsonResponse({"error": "Invalid request"}, status=400)



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
#         "avatar_url": user.avatar_url
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
#         user.avatar_url = data.get("avatar_url", user.avatar_url)

#         user.save()
#         return JsonResponse({"message": "Profile updated successfully"})
#     return JsonResponse({"error": "Invalid request"}, status=400)
# from django.contrib.auth import authenticate, login


# from django.contrib.auth import authenticate, login
# from django.http import JsonResponse
# from .models import CustomUser

# # -------------------------------
# # Superuser login
# # -------------------------------
# def superuser_login(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(username=username, password=password)
#         if user and user.is_superuser:
#             login(request, user)
#             return JsonResponse({"success": True, "message": "Superuser logged in!"})
#         return JsonResponse({"success": False, "message": "Invalid superuser credentials"})

# # -------------------------------
# # Normal user: Request OTP
# # -------------------------------
# def request_otp(request):
#     if request.method == "POST":
#         phone = request.POST.get("phone")
#         if not phone:
#             return JsonResponse({"success": False, "message": "Phone number required"})
#         try:
#             user = CustomUser.objects.get(phone=phone)
#             otp = user.generate_otp()
#             # In production, send OTP via SMS here
#             return JsonResponse({"success": True, "otp": otp, "message": "OTP sent!"})
#         except CustomUser.DoesNotExist:
#             return JsonResponse({"success": False, "message": "Phone number not found"})

# # -------------------------------
# # Normal user: Verify OTP
# # -------------------------------
# def verify_otp(request):
#     if request.method == "POST":
#         phone = request.POST.get("phone")
#         otp_input = request.POST.get("otp")

#         if not phone or not otp_input:
#             return JsonResponse({"success": False, "message": "Phone and OTP required"})

#         try:
#             user = CustomUser.objects.get(phone=phone)
#             if user.verify_otp(otp_input):
#                 login(request, user)
#                 return JsonResponse({"success": True, "message": "User logged in successfully"})
#             else:
#                 return JsonResponse({"success": False, "message": "Invalid or expired OTP"})
#         except CustomUser.DoesNotExist:
#             return JsonResponse({"success": False, "message": "Phone number not found"})
