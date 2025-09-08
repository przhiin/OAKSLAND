# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser, OTP

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view
    list_display = ('email', 'first_name', 'last_name', 'phone', 
                   'email_verified', 'is_staff', 'is_active', 'date_joined')
    
    # Fields that can be used for searching
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    
    # Filter options
    list_filter = ('email_verified', 'is_staff', 'is_active', 'date_joined')
    
    # Ordering
    ordering = ('-date_joined',)
    
    # Fieldsets for the detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'address')}),
        ('Permissions', {'fields': ('email_verified', 'is_active', 'is_staff', 
                                   'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fieldsets for the add view
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 
                      'phone', 'address', 'email_verified', 'is_active', 'is_staff')}
        ),
    )
    
    # Readonly fields
    readonly_fields = ('last_login', 'date_joined')
    
    # Custom actions
    actions = ['mark_email_verified', 'mark_email_unverified']
    
    def mark_email_verified(self, request, queryset):
        updated = queryset.update(email_verified=True)
        self.message_user(request, f'{updated} users marked as email verified.')
    mark_email_verified.short_description = "Mark selected users as email verified"
    
    def mark_email_unverified(self, request, queryset):
        updated = queryset.update(email_verified=False)
        self.message_user(request, f'{updated} users marked as email unverified.')
    mark_email_unverified.short_description = "Mark selected users as email unverified"

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('user', 'otp', 'purpose', 'created_at', 'is_valid_display')
    
    # Fields that can be used for searching
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'otp', 'purpose')
    
    # Filter options
    list_filter = ('purpose', 'created_at')
    
    # Ordering
    ordering = ('-created_at',)
    
    # Readonly fields
    readonly_fields = ('created_at', 'is_valid_display')
    
    # Fieldsets for the detail view
    fieldsets = (
        (None, {'fields': ('user', 'otp', 'purpose')}),
        ('Status', {'fields': ('is_valid_display',)}),
        ('Date Information', {'fields': ('created_at',)}),
    )
    
    def is_valid_display(self, obj):
        return obj.is_valid()
    is_valid_display.boolean = True
    is_valid_display.short_description = 'Is Valid'
    
    # Custom action to delete expired OTPs
    actions = ['delete_expired_otps']
    
    def delete_expired_otps(self, request, queryset):
        # This would work if called from the main OTP list, but for a custom action
        # we need to filter expired OTPs from the entire queryset
        expired_otps = [otp for otp in queryset if not otp.is_valid()]
        count = len(expired_otps)
        for otp in expired_otps:
            otp.delete()
        self.message_user(request, f'{count} expired OTPs deleted.')
    delete_expired_otps.short_description = "Delete expired OTPs"