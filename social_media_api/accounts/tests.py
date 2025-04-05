from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class FollowSystemTests(APITestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username='testuser1', password='testpass123')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass123')
        # Authenticate user1
        self.client.force_authenticate(user=self.user1)

    def test_follow_user(self):
        url = reverse('follow-user', kwargs={'user_id': self.user2.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user1.following.filter(id=self.user2.id).exists())

    def test_unfollow_user(self):
        # First follow the user
        self.user1.following.add(self.user2)
        url = reverse('unfollow-user', kwargs={'user_id': self.user2.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.user1.following.filter(id=self.user2.id).exists())

    def test_cannot_follow_self(self):
        url = reverse('follow-user', kwargs={'user_id': self.user1.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class FeedTests(APITestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username='testuser1', password='testpass123')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass123')
        self.user3 = User.objects.create_user(username='testuser3', password='testpass123')
        
        # User1 follows User2 but not User3
        self.user1.following.add(self.user2)
        
        # Create some posts
        self.post1 = Post.objects.create(author=self.user2, title='Test Post 1', content='Content 1')
        self.post2 = Post.objects.create(author=self.user3, title='Test Post 2', content='Content 2')
        
        # Authenticate user1
        self.client.force_authenticate(user=self.user1)

    def test_feed_content(self):
        url = reverse('feed')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Should only see user2's post
        self.assertEqual(response.data['results'][0]['title'], 'Test Post 1')
