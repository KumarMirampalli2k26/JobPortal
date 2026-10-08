from django.test import TestCase
from django.contrib.auth.models import User
from .models import Company, Job, Application, SavedJob
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from django.db import transaction

class JobsTestCase(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(username='recruiter', password='password')
        self.candidate = User.objects.create_user(username='candidate', password='password')
        
        self.company = Company.objects.create(
            owner=self.recruiter,
            name='Test Company'
        )
        
        self.job = Job.objects.create(
            recruiter=self.recruiter,
            title='Software Engineer',
            location='Remote'
        )

    def test_company_creation(self):
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(self.company.owner, self.recruiter)

    def test_job_creation(self):
        self.assertEqual(Job.objects.count(), 1)
        self.assertEqual(self.job.title, 'Software Engineer')

    def test_application_creation(self):
        pdf_resume = SimpleUploadedFile("resume.pdf", b"file_content", content_type="application/pdf")
        app = Application.objects.create(
            job=self.job,
            candidate=self.candidate,
            resume=pdf_resume
        )
        self.assertEqual(Application.objects.count(), 1)
        self.assertEqual(app.status, 'APPLIED')

    def test_application_pdf_validation(self):
        txt_resume = SimpleUploadedFile("resume.txt", b"file_content", content_type="text/plain")
        app = Application(
            job=self.job,
            candidate=self.candidate,
            resume=txt_resume
        )
        # Should raise ValidationError due to FileExtensionValidator
        with self.assertRaises(ValidationError):
            app.full_clean()

    def test_saved_job_creation(self):
        saved_job = SavedJob.objects.create(user=self.candidate, job=self.job)
        self.assertEqual(SavedJob.objects.count(), 1)
        
    def test_unique_constraints(self):
        SavedJob.objects.create(user=self.candidate, job=self.job)
        with transaction.atomic():
            with self.assertRaises(Exception):
                SavedJob.objects.create(user=self.candidate, job=self.job)
                
        pdf_resume = SimpleUploadedFile("resume.pdf", b"file_content", content_type="application/pdf")
        Application.objects.create(job=self.job, candidate=self.candidate, resume=pdf_resume)
        with transaction.atomic():
            with self.assertRaises(Exception):
                Application.objects.create(job=self.job, candidate=self.candidate, resume=pdf_resume)

class JobCRUDTestCase(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(username='recruiter1', password='password123', email='r1@example.com')
        self.recruiter.profile.role = 'RECRUITER'
        self.recruiter.profile.save()
        
        self.candidate = User.objects.create_user(username='candidate1', password='password123', email='c1@example.com')
        self.candidate.profile.role = 'CANDIDATE'
        self.candidate.profile.save()

        self.job = Job.objects.create(
            recruiter=self.recruiter,
            title='Old Job',
            description='Old Description',
            location='Old Location'
        )

    def test_job_create_view(self):
        self.client.login(username='recruiter1', password='password123')
        response = self.client.post('/jobs/create/', data={
            'title': 'New Job',
            'description': 'New Description',
            'location': 'New Location',
            'skills': 'Python',
            'salary': '$100k'
        })
        self.assertRedirects(response, '/accounts/dashboard/', fetch_redirect_response=False)
        self.assertTrue(Job.objects.filter(title='New Job').exists())

    def test_job_update_view(self):
        self.client.login(username='recruiter1', password='password123')
        response = self.client.post(f'/jobs/{self.job.id}/update/', data={
            'title': 'Updated Job',
            'description': 'Updated Description',
            'location': 'Updated Location'
        })
        self.assertRedirects(response, '/accounts/dashboard/', fetch_redirect_response=False)
        self.job.refresh_from_db()
        self.assertEqual(self.job.title, 'Updated Job')

    def test_job_delete_view(self):
        self.client.login(username='recruiter1', password='password123')
        response = self.client.post(f'/jobs/{self.job.id}/delete/')
        self.assertRedirects(response, '/accounts/dashboard/', fetch_redirect_response=False)
        self.assertFalse(Job.objects.filter(id=self.job.id).exists())

    def test_job_toggle_active_view(self):
        self.client.login(username='recruiter1', password='password123')
        self.assertTrue(self.job.is_active)
        response = self.client.post(f'/jobs/{self.job.id}/toggle/')
        self.assertRedirects(response, '/accounts/dashboard/', fetch_redirect_response=False)
        self.job.refresh_from_db()
        self.assertFalse(self.job.is_active)

    def test_permissions(self):
        self.client.login(username='candidate1', password='password123')
        
        # Candidate tries to create job
        response = self.client.get('/jobs/create/')
        self.assertEqual(response.status_code, 302)
        
        # Candidate tries to edit job
        response = self.client.get(f'/jobs/{self.job.id}/update/')
        self.assertEqual(response.status_code, 302)
