from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Subject, Doubt, DoubtResponse

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('roll_number', 'full_name', 'role', 'subject', 'is_staff')
    list_filter = ('role', 'subject', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'roll_number', 'role', 'subject')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Doubt)
class DoubtAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'subject', 'status', 'created_at')
    list_filter = ('status', 'subject', 'created_at')
    search_fields = ('title', 'description', 'student__full_name', 'student__roll_number')

@admin.register(DoubtResponse)
class DoubtResponseAdmin(admin.ModelAdmin):
    list_display = ('doubt', 'teacher', 'created_at')
    search_fields = ('response_text', 'teacher__full_name')
