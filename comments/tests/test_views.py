from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from comments.models import Comment


class CommentViewsTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@example.com"
        )
        self.comment = Comment.objects.create(
            user=self.user, text="Test comment"
        )
        from captcha.conf import settings as captcha_settings

        captcha_settings.CAPTCHA_TEST_MODE = True

    def test_add_comment_view(self) -> None:
        url = reverse("comments:add_comment")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            url,
            {
                "username": "newuser",
                "email": "new@example.com",
                "captcha_0": "test",
                "captcha_1": "PASSED",
                "text": "New comment",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 2)

    def test_comment_list_view(self) -> None:
        url = reverse("comments:comment_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "comments/comment_list.html")

        for i in range(30):
            Comment.objects.create(
                user=self.user, text=f"Test comment {i + 2}"
            )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["comments"]), 25)

    def test_comment_detail_view(self) -> None:
        url = reverse("comments:comment_detail", args=[self.comment.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "comments/comment_detail.html")

        response = self.client.post(
            url,
            {
                "username": "replyuser",
                "email": "reply@example.com",
                "captcha_0": "test",
                "captcha_1": "PASSED",
                "text": "Reply to comment",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.comment.replies.count(), 1)
