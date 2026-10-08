from django.test import TestCase
from django.contrib.auth.models import User
from .models import Job, Application

class JobsTestCase(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(username='recruiter', password='password')
        self.recruiter.profile.role = 'RECRUITER'
        self.recruiter.profile.save()
        
        self.candidate = User.objects.create_user(username='candidate', password='password')
        self.candidate.profile.role = 'CANDIDATE'
        self.candidate.profile.save()

        self.job = Job.objects.create(
            recruiter=self.recruiter,
            title='Software Engineer',
            description='Test description',
            location='Remote',
            job_type='FULL_TIME'
        )

    def test_job_creation(self):
        self.assertEqual(Job.objects.count(), 1)
        self.assertEqual(self.job.title, 'Software Engineer')

    def test_job_list_view(self):
        response = self.client.get('/jobs/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Software Engineer')

    def test_application_creation(self):
        app = Application.objects.create(
            job=self.job,
            candidate=self.candidate,
            cover_letter='My cover letter'
        )
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(app.status, 'PENDING')
