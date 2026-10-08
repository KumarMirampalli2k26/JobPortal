# JobPortal

A complete, modern, and professional Job Portal web application built with Django and Tailwind CSS. The platform connects recruiters with potential candidates, providing seamless tools for posting jobs, managing applications, and discovering opportunities.

## 🚀 Project Overview
JobPortal is designed with a minimal and professional UI/UX, built to industry standards. It features role-based access control, secure authentication, job CRUD operations, application workflows with PDF resume support, and personalized dashboards.

## 🛠️ Tech Stack
- **Backend**: Python 3.12+, Django 5.x
- **Database**: SQLite (Development)
- **Frontend**: HTML5, Tailwind CSS (via CDN), Alpine.js (via CDN)
- **Styling/UI**: Custom minimal design system (Inter font, Indigo accent)
- **File Management**: Pillow (Image processing), Django FileSystemStorage (Resumes/PDFs)
- **Environment**: `python-decouple` for configuration

## ✨ Features
- **Role-based Authentication**: Custom User profiles distinguishing between `CANDIDATE` and `RECRUITER` roles.
- **Recruiter Dashboard**: Manage company profiles, create/edit/delete jobs, and review applicants.
- **Candidate Dashboard**: Browse active jobs, apply with PDF resumes, and track application statuses.
- **Job Applications Flow**: Secure upload and validation of PDF resumes, preventing duplicate applications.
- **Applicant Management**: Recruiters can change application statuses (Shortlisted, Rejected) sending automatic email notifications via the console backend.
- **Search & Filtering**: Search jobs by keywords, title, or location.

### 🌟 Bonus Features Implemented
- **Saved Jobs**: Candidates can bookmark jobs and view them in a dedicated dashboard.
- **Company Profiles**: Recruiters can manage public company profiles (with logos) which are linked from their job postings, providing an aggregated view of all active company jobs.
- **Automated Seed Script**: Command to quickly populate realistic sample data into the database.

## 🗄️ Database Schema
- **User / Profile**: Extends Django's User model via OneToOne relationship to store roles, phone, bio, and avatars.
- **Company**: OneToOne to User (Recruiter), storing name, logo, location, website, and description.
- **Job**: Linked to Recruiter (User FK), storing title, company_name, job_type, skills, description, salary, location, and activity status.
- **Application**: Linked to Job and Candidate. Stores resume (PDF validation), applied date, and application status.
- **SavedJob**: Tracks bookmarked jobs by Candidates (User, Job unique together).

## ⚙️ Setup Instructions

1. **Clone the repository and enter the directory**:
   ```bash
   git clone <repository_url>
   cd Job_Portal
   ```

2. **Create a virtual environment and activate it**:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**:
   Copy `.env.example` to `.env` and configure your `SECRET_KEY` and other settings.
   ```bash
   cp .env.example .env
   ```

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Seed Realistic Sample Data** (Optional but recommended):
   ```bash
   python manage.py seed_data
   ```

7. **Create a Superuser** (For admin access):
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```
   Open `http://localhost:8000` in your browser.

## 🧪 Running Tests
The project includes a comprehensive suite of 29 automated tests verifying models, views, custom permissions, and search functionality.

```bash
python manage.py test
```

To run system checks for potential issues:
```bash
python manage.py check
```

## 📸 Screenshots Checklist
To verify the UI requirements, capture screenshots of the following views:
1. **Home Page** (`/`): Showcasing the hero section and recent jobs.
2. **Job Detail Page** (`/jobs/<id>/`): Highlighting job information and the company link.
3. **Candidate Dashboard** (`/accounts/dashboard/`): Showing application history with colored status badges.
4. **Recruiter Dashboard** (`/accounts/dashboard/`): Highlighting job stats, job management table, and recent applications.
5. **Job Applicants View** (`/jobs/<id>/applicants/`): The recruiter's applicant tracking UI with shortlist/reject actions.
6. **Company Profile** (`/jobs/company/<id>/`): The public-facing company page detailing information and active openings.
