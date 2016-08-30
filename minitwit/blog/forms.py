from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField
from django.utils.translation import ugettext_lazy as _
from .models import User
from werkzeug import generate_password_hash


class UserForm(UserCreationForm):
    email = EmailField(label=_("Email address"), required=True, help_text=_("Required."))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self):
        current_email = self.cleaned_data["email"]
        current_username = self.cleaned_data["username"]
        current_password = self.cleaned_data["password1"]
        current_user = User(username=current_username, email=current_email,
                            pw_hash=generate_password_hash(current_password))
        current_user.save()