# serializers.py
from rest_framework import serializers
from .models import CustomUser, OTP
from django.core.mail import send_mail
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "email", "phone", "address", "email_verified"]

# OTP Request Serializer
class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value
    
    def save(self):
        email = self.validated_data['email']
        user = CustomUser.objects.get(email=email)
        otp_obj = OTP.generate_otp(user)
        
        # Send OTP via email
        subject = 'Your Login OTP Code'
        message = f'Your OTP for login is: {otp_obj.otp}. It is valid for 10 minutes.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]
        
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        
        return user

# OTP Verification Serializer
class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    
    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')
        
        try:
            user = CustomUser.objects.get(email=email)
            otp_obj = OTP.objects.filter(user=user, otp=otp, purpose='login').latest('created_at')
            
            if not otp_obj.is_valid():
                raise serializers.ValidationError("OTP has expired.")
                
            data['user'] = user
            return data
            
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")
        except OTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP.")






# from rest_framework import serializers
# from .models import CustomUser
# from django.contrib.auth import authenticate

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ["id", "username", "first_name", "last_name", "email", "phone", "address"]

# # Registration
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ["username", "password", "first_name", "last_name", "email", "phone", "address"]

#     def create(self, validated_data):
#         user = CustomUser.objects.create_user(
#             username=validated_data["username"],
#             password=validated_data["password"],
#             first_name=validated_data.get("first_name", ""),
#             last_name=validated_data.get("last_name", ""),
#             email=validated_data.get("email", ""),
#             phone=validated_data.get("phone", ""),
#             address=validated_data.get("address", "")
#         )
#         return user

# # Login
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)

#     def validate(self, data):
#         user = authenticate(username=data["username"], password=data["password"])
#         if user:
#             return user
#         raise serializers.ValidationError("Invalid username or password")
