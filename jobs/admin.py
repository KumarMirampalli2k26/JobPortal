from django.contrib import admin
from .models import Job, Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'recruiter', 'job_type', 'is_active', 'created_at']
    list_filter = ['is_active', 'job_type']
    search_fields = ['title', 'description', 'location']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'job', 'status', 'applied_at']
    list_filter = ['status']
    search_fields = ['candidate__username', 'job__title']
