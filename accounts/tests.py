from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

class AccountsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testcandidate', password='password')
        self.user.profile.role = 'CANDIDATE'
        self.user.profile.save()

    def test_profile_created(self):
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(self.user.profile.role, 'CANDIDATE')

    def test_login_view(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_access(self):
        self.client.login(username='testcandidate', password='password')
        response = self.client.get('/accounts/dashboard/')
        self.assertEqual(response.status_code, 200)
