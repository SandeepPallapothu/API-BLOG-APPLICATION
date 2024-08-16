from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Posts
from django.contrib.auth.models import User

class BlogPostTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post_data = {'title': 'Test Title', 'content': 'Test Content','author':self.user.id}
        self.post_url = reverse('post-list-create')

    def test_create_blog_post(self):
        response = self.client.post(self.post_url, self.post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_blog_posts(self):
        response = self.client.get(self.post_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CommentTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post = Posts.objects.create(title='Test Title', content='Test Content', author=self.user)
        self.comment_data = {'post': self.post.id, 'content': 'Test Comment','author':self.user.id}
        self.comment_url = reverse('comment-list-create')

    def test_create_comment(self):
        response = self.client.post(self.comment_url, self.comment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_comments(self):
        response = self.client.get(self.comment_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser',password='testpassword')
        self.register_url = reverse('auth_register')
        self.login_url = reverse('auth_login')
        self.user_data = {'username': 'newuser','email':'newemail@gmail.com', 'password': 'password'}
        self.login_data = {'username': 'testuser', 'password': 'testpassword'}


    def test_user_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        self.client.post(self.login_url, self.user_data, format='json')
        response = self.client.post(self.login_url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

class BlogCommentIntegrationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.post_url = reverse('post-list-create')
        self.comment_url = reverse('comment-list-create')
        self.post_data = {'title': 'Integration Test Title', 'content': 'Integration Test Content','author': self.user.id}
        self.post_response = self.client.post(self.post_url, self.post_data, format='json')
        self.comment_data = {'post': self.post_response.data['id'], 'content': 'Integration Test Comment','author': self.user.id}

    def test_blog_and_comment_creation(self):
        # Test creating a blog post
        self.assertEqual(self.post_response.status_code, status.HTTP_201_CREATED)

        # Test creating a comment on the blog post
        comment_response = self.client.post(self.comment_url, self.comment_data, format='json')
        self.assertEqual(comment_response.status_code, status.HTTP_201_CREATED)

        # Test retrieving the post with its comments
        post_detail_url = reverse('post-retrieve-update-delete', args=[self.post_response.data['id']])
        post_detail_response = self.client.get(post_detail_url, format='json')
        self.assertEqual(post_detail_response.status_code, status.HTTP_200_OK)
        #self.assertEqual(len(post_detail_response.data['comments']), 1)
