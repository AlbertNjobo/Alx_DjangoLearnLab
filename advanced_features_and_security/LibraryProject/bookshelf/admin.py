from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    """Custom admin interface for CustomUser model"""

    # Fields to display in the admin list view
    list_display = ('email', 'first_name', 'last_name', 'date_of_birth', 'is_staff')

    # Fields to filter by in admin
    list_filter = ('is_staff', 'is_superuser', 'is_active')

    # Fields to search in admin
    search_fields = ('email', 'first_name', 'last_name')

    # Fieldsets for the edit page
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'date_of_birth', 'profile_photo'),
        }),
    )

    # Ordering in admin list view
    ordering = ('email',)

# Register the custom user model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
@admin.register(Book)

class BookAdmin(admin.ModelAdmin):

    list_diplay = ('title', 'author', 'publication_year')

    list_filter = ('author', 'publication_year')

    search_fields = ('title', 'author')

    fieldsets = (('Book Details', {'fields':('title', 'author', 'publication_year')}),)
