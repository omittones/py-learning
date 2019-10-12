from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Post, CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('birthDate','age',)


class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = UserChangeForm.Meta.fields


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', 'birthDate', 'age']
    list_display_links = ['username']

admin.site.register(Post)
admin.site.register(CustomUser, CustomUserAdmin)
