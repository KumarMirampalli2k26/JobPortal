from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Profile
from jobs.models import Company, Job, Application, SavedJob
from django.core.files.uploadedfile import SimpleUploadedFile

class Command(BaseCommand):
    help = 'Seeds the database with sample recruiters, candidates, companies, jobs, applications, and saved jobs.'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # Create Recruiters
        recruiter1, _ = User.objects.get_or_create(username='r1', email='r1@example.com')
        recruiter1.set_password('password')
        recruiter1.save()
        recruiter1.profile.role = 'RECRUITER'
        recruiter1.profile.save()

        recruiter2, _ = User.objects.get_or_create(username='r2', email='r2@example.com')
        recruiter2.set_password('password')
        recruiter2.save()
        recruiter2.profile.role = 'RECRUITER'
        recruiter2.profile.save()

        # Create Companies
        c1, _ = Company.objects.get_or_create(owner=recruiter1, defaults={'name': 'Tech Corp', 'location': 'New York'})
        c2, _ = Company.objects.get_or_create(owner=recruiter2, defaults={'name': 'Innovate LLC', 'location': 'San Francisco'})

        # Create Candidates
        candidate1, _ = User.objects.get_or_create(username='c1', email='c1@example.com')
        candidate1.set_password('password')
        candidate1.save()
        candidate1.profile.role = 'CANDIDATE'
        candidate1.profile.save()

        candidate2, _ = User.objects.get_or_create(username='c2', email='c2@example.com')
        candidate2.set_password('password')
        candidate2.save()
        candidate2.profile.role = 'CANDIDATE'
        candidate2.profile.save()

        # Create Jobs
        job1, _ = Job.objects.get_or_create(
            recruiter=recruiter1, title='Software Engineer',
            defaults={'skills': 'Python, Django', 'location': 'New York', 'salary': '$120k', 'description': 'Build cool stuff.'}
        )
        job2, _ = Job.objects.get_or_create(
            recruiter=recruiter2, title='Frontend Developer',
            defaults={'skills': 'React, Tailwind', 'location': 'San Francisco', 'salary': '$110k', 'description': 'Build UIs.'}
        )

        # Create Applications
        dummy_resume = SimpleUploadedFile("resume.pdf", b"file_content", content_type="application/pdf")
        Application.objects.get_or_create(job=job1, candidate=candidate1, defaults={'resume': dummy_resume, 'status': 'APPLIED'})
        Application.objects.get_or_create(job=job2, candidate=candidate2, defaults={'resume': dummy_resume, 'status': 'SHORTLISTED'})

        # Create Saved Jobs
        SavedJob.objects.get_or_create(user=candidate1, job=job2)
        SavedJob.objects.get_or_create(user=candidate2, job=job1)

        self.stdout.write(self.style.SUCCESS("Successfully seeded data!"))
