from django.test import TestCase
from posts.models import Post
from profiles.models import Profile


class TestAppModels(TestCase):

    def test_model_str(self):
        author1 = Profile.objects.get(pk=3)
        post = Post.objects.create(content="test content",author=author1)
        self.assertEqual(str(post),"test content")


