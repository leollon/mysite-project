from django.contrib import admin

from .models import User


# Register your models here.
class MyUserAdmin(admin.ModelAdmin):
    """
    Managing user's info in admin site
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_valid',
                    'is_staff', 'is_active')
    list_filter = ('is_valid', 'is_active')
    ordering = ('username', )
    search_fields = ('username', 'email')


admin.site.register(User, MyUserAdmin)
