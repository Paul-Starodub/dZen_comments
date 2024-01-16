from typing import Any

import bleach
from captcha.fields import CaptchaField

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext as _

from comments.models import User

alphanumeric_validator = RegexValidator(
    r"^[a-zA-Z0-9]*$",
    "Use correct characters.",
    "invalid_username",
)


class CommentForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(),
        validators=[alphanumeric_validator],
        help_text="Only alphanumeric characters are allowed.",
    )
    email = forms.EmailField(widget=forms.EmailInput(), required=True)
    homepage = forms.URLField(required=False)
    captcha = CaptchaField()
    text = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 4}), max_length=1000
    )
    parent_comment_id = forms.IntegerField(
        required=False, widget=forms.HiddenInput()
    )

    def clean(self) -> dict:
        cleaned_data = super().clean()
        cleaned_data["text"] = self.clean_text()

        email = cleaned_data.get("email", "")
        username = cleaned_data.get("username", "")

        # Check if a user with the provided email already exists
        existing_user_email = (
            User.objects.filter(email=email).exclude(username=username).first()
        )

        if existing_user_email:
            raise ValidationError(
                _(
                    "This email address is already "
                    "associated with another username."
                ),
                code="duplicate_email",
            )

        # Check if a user with the provided username already exists
        existing_user_username = (
            User.objects.filter(username=username).exclude(email=email).first()
        )

        if existing_user_username:
            raise ValidationError(
                _(
                    "This username is already associated "
                    "with another email address."
                ),
                code="duplicate_username",
            )

        return cleaned_data

    def clean_text(self) -> Any:
        text = self.cleaned_data["text"]
        allowed_tags = ["a", "code", "i", "strong"]
        cleaned_text = bleach.clean(text, tags=allowed_tags, strip=True)
        return cleaned_text
