from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Job, Application, Company
from .forms import ApplicationForm
from django.utils.decorators import method_decorator
from accounts.decorators import recruiter_required, candidate_required

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

@method_decorator(recruiter_required, name='dispatch')
class JobCreateView(CreateView):
    model = Job
    template_name = 'jobs/job_form.html'
    fields = ['title', 'description', 'skills', 'location', 'salary']
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.recruiter = self.request.user
        messages.success(self.request, "Job posted successfully!")
        return super().form_valid(form)

@method_decorator(recruiter_required, name='dispatch')
class JobUpdateView(UpdateView):
    model = Job
    template_name = 'jobs/job_form.html'
    fields = ['title', 'description', 'skills', 'location', 'salary']
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Job updated successfully!")
        return super().form_valid(form)

@method_decorator(recruiter_required, name='dispatch')
class JobDeleteView(DeleteView):
    model = Job
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user)
        
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Job deleted successfully!")
        return super().delete(request, *args, **kwargs)

@method_decorator(recruiter_required, name='dispatch')
class JobToggleActiveView(View):
    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk, recruiter=request.user)
        job.is_active = not job.is_active
        job.save()
        status = "activated" if job.is_active else "deactivated"
        messages.success(request, f"Job {status} successfully!")
        return redirect('dashboard')

@method_decorator(recruiter_required, name='dispatch')
class CompanyUpdateView(UpdateView):
    model = Company
    template_name = 'jobs/company_form.html'
    fields = ['name', 'logo', 'website', 'location', 'description']
    success_url = reverse_lazy('dashboard')

    def get_object(self, queryset=None):
        company, created = Company.objects.get_or_create(owner=self.request.user, defaults={'name': 'Your Company Name'})
        return company

    def form_valid(self, form):
        messages.success(self.request, "Company profile updated successfully!")
        return super().form_valid(form)

@candidate_required
def apply_to_job(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    
    if Application.objects.filter(job=job, candidate=request.user).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.candidate = request.user
            application.save()
            messages.success(request, f"You have successfully applied to {job.title}!")
            return redirect('dashboard')
    else:
        form = ApplicationForm()
    
    return render(request, 'jobs/apply.html', {'job': job, 'form': form})

@method_decorator(recruiter_required, name='dispatch')
class JobApplicantsView(DetailView):
    model = Job
    template_name = 'jobs/job_applicants.html'
    context_object_name = 'job'
    
    def get_queryset(self):
        return Job.objects.filter(recruiter=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['applications'] = self.object.applications.all()
        return context
