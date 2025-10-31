from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import FileResponse, HttpResponse
import os
import mimetypes

from .models import LandRecord, DocumentCategory
from .forms import LandRecordForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import logout
def home(request):
    """Home page view"""
    return render(request, 'records/home.html')

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'records/register.html', {'form': form})

@login_required
def dashboard(request):
    """User dashboard view showing recent records and stats"""
    user_records = LandRecord.objects.filter(owner=request.user)
    recent_records = user_records.order_by('-date_added')[:5]
    total_records = user_records.count()
    
    context = {
        'recent_records': recent_records,
        'total_records': total_records,
        'record_categories': DocumentCategory.objects.all(),
    }
    return render(request, 'records/dashboard.html', context)

@login_required
def profile(request):
    """User profile update view"""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.userprofile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('dashboard')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'records/profile.html', context)
def logout_view(request):
    logout(request)
    return redirect('/')
class RecordListView(LoginRequiredMixin, ListView):
    """View for listing all user records with filtering capabilities"""
    model = LandRecord
    template_name = 'records/record_list.html'
    context_object_name = 'records'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = LandRecord.objects.filter(owner=self.request.user)
        
        # Apply search filter if provided
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(property_address__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(survey_number__icontains=search_query)
            )
        
        # Apply category filter if provided
        category_id = self.request.GET.get('category', '')
        if category_id and category_id.isdigit():
            queryset = queryset.filter(category_id=category_id)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = DocumentCategory.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context

class RecordDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """View for viewing details of a specific record"""
    model = LandRecord
    template_name = 'records/record_detail.html'
    context_object_name = 'record'
    
    def test_func(self):
        record = self.get_object()
        return self.request.user == record.owner

class RecordCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new land record"""
    model = LandRecord
    form_class = LandRecordForm
    template_name = 'records/record_form.html'
    success_url = reverse_lazy('record-list')
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Land record created successfully!')
        return super().form_valid(form)

class RecordUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LandRecord
    form_class = LandRecordForm
    template_name = 'records/record_form.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'Land record updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        record = self.get_object()
        return self.request.user == record.owner

class RecordDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting a land record"""
    model = LandRecord
    template_name = 'records/record_confirm_delete.html'
    success_url = reverse_lazy('record-list')
    
    def test_func(self):
        record = self.get_object()
        return self.request.user == record.owner
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Land record deleted successfully!')
        return super().delete(request, *args, **kwargs)

@login_required
def download_document(request, pk):
    """View for downloading a document"""
    record = get_object_or_404(LandRecord, pk=pk, owner=request.user)
    file_path = record.document.path
    
    # Determine content type based on file extension
    content_type, _ = mimetypes.guess_type(file_path)
    if not content_type:
        content_type = 'application/octet-stream'
    
    # Get filename from path
    filename = os.path.basename(file_path)
    
    # Create file response
    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt
def preview_document(request, pk):
    """View for previewing a document"""
    record = get_object_or_404(LandRecord, pk=pk, owner=request.user)
    file_path = record.document.path
    
    # Determine content type based on file extension
    content_type, _ = mimetypes.guess_type(file_path)
    if not content_type:
        content_type = 'application/octet-stream'
    
    # Create file response for inline display
    response = FileResponse(open(file_path, 'rb'), content_type=content_type)
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
    
    return response
