from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class User(AbstractUser):
    """Authentication using a unique combination of email and username"""

    email = models.EmailField(_("email address"), unique=True)
    home_page = models.URLField(
        max_length=200, help_text="Enter a valid URL", blank=True
    )

    class Meta:
        ordering = ["username"]

    def clean(self) -> None:
        super().clean()
        existing_user_with_email = (
            User.objects.filter(email=self.email)
            .exclude(username=self.username)
            .first()
        )
        if existing_user_with_email:
            raise ValidationError(
                {
                    "email": _(
                        "This email address is already "
                        "associated with another username."
                    )
                }
            )

    def __str__(self) -> str:
        return self.username


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    parent_comment = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user.username} - {self.created_at}"
