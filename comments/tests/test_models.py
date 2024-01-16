from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from comments.models import User, Comment


class UserModelTests(TestCase):
    def test_create_user(self) -> None:
        user = User.objects.create(
            username="testuser", email="test@example.com"
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")

    def test_unique_email_constraint(self) -> None:
        User.objects.create(username="user1", email="user@example.com")
        with self.assertRaises(IntegrityError):
            User.objects.create(username="user2", email="user@example.com")

    def test_clean_method(self) -> None:
        User.objects.create(username="user1", email="user@example.com")
        user2 = User(username="user2", email="user@example.com")
        with self.assertRaises(ValidationError):
            user2.clean()

    def test_str_method(self) -> None:
        user = User(username="testuser", email="test@example.com")
        self.assertEqual(str(user), "testuser")


class CommentModelTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            username="testuser", email="test@example.com"
        )

    def test_create_comment(self) -> None:
        comment = Comment.objects.create(user=self.user, text="Test comment")
        self.assertEqual(comment.text, "Test comment")
        self.assertEqual(comment.user, self.user)

    def test_str_method(self) -> None:
        comment = Comment.objects.create(user=self.user, text="Test comment")
        self.assertEqual(str(comment), f"testuser - {comment.created_at}")

    def test_create_reply(self) -> None:
        parent_comment = Comment.objects.create(
            user=self.user, text="Parent comment"
        )
        reply = Comment.objects.create(
            user=self.user,
            text="Reply to parent",
            parent_comment=parent_comment,
        )
        self.assertEqual(reply.text, "Reply to parent")
        self.assertEqual(reply.parent_comment, parent_comment)

    def test_ordering(self) -> None:
        comment1 = Comment.objects.create(user=self.user, text="Comment 1")
        comment2 = Comment.objects.create(user=self.user, text="Comment 2")
        self.assertGreater(comment2.created_at, comment1.created_at)
