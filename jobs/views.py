from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Job, Application

class JobListView(ListView):
    model = Job
    template_name = 'jobs/job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(location__icontains=query)
            )
        return queryset

class JobDetailView(DetailView):
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['has_applied'] = Application.objects.filter(job=self.object, candidate=self.request.user).exists()
        return context

class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Job
    template_name = 'jobs/job_form.html'
    fields = ['title', 'description', 'skills', 'location', 'salary']
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.recruiter = self.request.user
        messages.success(self.request, "Job posted successfully!")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.profile.role == 'RECRUITER'

@login_required
def apply_to_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    
    if request.user.profile.role != 'CANDIDATE':
        messages.error(request, "Only candidates can apply for jobs.")
        return redirect('job_detail', pk=pk)

    if Application.objects.filter(job=job, candidate=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('job_detail', pk=pk)

    if request.method == 'POST':
        if 'resume' in request.FILES:
            resume = request.FILES['resume']
            Application.objects.create(
                job=job,
                candidate=request.user,
                resume=resume
            )
            messages.success(request, f"You have successfully applied to {job.title}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Please upload a resume (PDF format).")
    
    return render(request, 'jobs/apply.html', {'job': job})
