from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import BlogPost

User = get_user_model()


class BlogAuthorizationTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user("author", password="strong-test-pass-1")
        self.other_user = User.objects.create_user("other", password="strong-test-pass-2")
        self.post = BlogPost.objects.create(
            title="Owned post", content="Private editing rights", author=self.author
        )

    def test_anonymous_user_can_read_posts(self):
        self.assertEqual(
            self.client.get(reverse("post_detail", args=[self.post.pk])).status_code, 200
        )

    def test_create_requires_login(self):
        response = self.client.get(reverse("create_post"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('create_post')}")

    def test_post_author_is_set_from_authenticated_user(self):
        self.client.force_login(self.author)
        response = self.client.post(
            reverse("create_post"), {"title": "New post", "content": "Body"}
        )
        created = BlogPost.objects.get(title="New post")
        self.assertEqual(created.author, self.author)
        self.assertRedirects(response, reverse("post_detail", args=[created.pk]))

    def test_user_cannot_edit_another_authors_post(self):
        self.client.force_login(self.other_user)
        response = self.client.post(
            reverse("edit_post", args=[self.post.pk]),
            {"title": "Hijacked", "content": "Changed"},
        )
        self.assertEqual(response.status_code, 404)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Owned post")

    def test_user_cannot_delete_another_authors_post(self):
        self.client.force_login(self.other_user)
        response = self.client.post(reverse("delete_post", args=[self.post.pk]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(BlogPost.objects.filter(pk=self.post.pk).exists())

    def test_author_can_edit_and_delete_own_post(self):
        self.client.force_login(self.author)
        edit = self.client.post(
            reverse("edit_post", args=[self.post.pk]),
            {"title": "Updated", "content": "Changed"},
        )
        self.assertRedirects(edit, reverse("post_detail", args=[self.post.pk]))
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated")
        delete = self.client.post(reverse("delete_post", args=[self.post.pk]))
        self.assertRedirects(delete, reverse("home"))
        self.assertFalse(BlogPost.objects.filter(pk=self.post.pk).exists())

    def test_logout_rejects_get_requests(self):
        self.client.force_login(self.author)
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
