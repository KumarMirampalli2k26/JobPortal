from django.test import TestCase
from django.contrib.auth.models import User
from .models import Company, Job, Application, SavedJob
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

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
        with self.assertRaises(Exception):
            SavedJob.objects.create(user=self.candidate, job=self.job)
            
        pdf_resume = SimpleUploadedFile("resume.pdf", b"file_content", content_type="application/pdf")
        Application.objects.create(job=self.job, candidate=self.candidate, resume=pdf_resume)
        with self.assertRaises(Exception):
            Application.objects.create(job=self.job, candidate=self.candidate, resume=pdf_resume)
