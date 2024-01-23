from django.test import TestCase
from django.contrib.auth import get_user_model

from comments.forms import CommentForm

from captcha.conf import settings as captcha_settings


class CommentFormTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
        )

        captcha_settings.CAPTCHA_TEST_MODE = True

    def test_valid_comment_form(self) -> None:
        form_data = {
            "username": "validusername",
            "email": "valid@example.com",
            "homepage": "http://example.com",
            "captcha_0": "test",
            "captcha_1": "PASSED",
            "text": "Valid comment text",
        }
        form = CommentForm(data=form_data)

        self.assertTrue(form.is_valid())

    def test_duplicate_email(self) -> None:
        get_user_model().objects.create(
            username="existinguser", email="duplicate@example.com"
        )

        form_data = {
            "username": "testuser",
            "email": "duplicate@example.com",
            "homepage": "http://example.com",
            "captcha_0": "test",
            "captcha_1": "PASSED",
            "text": "Valid comment text",
        }
        form = CommentForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "This email address is already associated with another username.",
            form.errors["__all__"],
        )

    def test_duplicate_username(self) -> None:
        form_data = {
            "username": "testuser",
            "email": "test2@example.com",
            "homepage": "http://example.com",
            "captcha_0": "test",
            "captcha_1": "PASSED",
            "text": "Valid comment text",
        }
        form = CommentForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertIn(
            "This username is already associated with another email address.",
            form.errors["__all__"],
        )

    def test_clean_text(self) -> None:
        form_data = {
            "username": "validusername",
            "email": "valid@example.com",
            "homepage": "http://example.com",
            "captcha_0": "test",
            "captcha_1": "PASSED",
            "text": '<a href="#">Test</a><code>Code</code><i>Italic</i><strong>Bold</strong>',
        }
        form = CommentForm(data=form_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.cleaned_data["text"],
            '<a href="#">Test</a><code>Code</code><i>Italic</i><strong>Bold</strong>',
        )
