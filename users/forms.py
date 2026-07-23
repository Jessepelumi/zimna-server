from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """
    The stock UserCreationForm calls
        User.objects.create_user(username=..., password=...)
    which doesn't match our manager's signature
        create_user(self, email, password=None, **extra_fields)
    and our model doesn't require a manually-entered username (it's
    auto-generated in User.save()). This override fixes both.
    """
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "first_name", "last_name", "gender")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = "__all__"
        