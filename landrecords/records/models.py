from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class UserProfile(models.Model):
    """Extended user profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class DocumentCategory(models.Model):
    """Categories for land records documents"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Document Categories'
    
    def __str__(self):
        return self.name

class LandRecord(models.Model):
    """Land record document model"""
    title = models.CharField(max_length=200)
    property_address = models.TextField()
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='land_records')
    category = models.ForeignKey(DocumentCategory, on_delete=models.SET_NULL, null=True, related_name='records')
    document = models.FileField(upload_to='land_records/')
    survey_number = models.CharField(max_length=100, blank=True, null=True)
    property_size = models.CharField(max_length=100, blank=True, null=True)
    property_type = models.CharField(max_length=100, blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_added']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('record-detail', kwargs={'pk': self.pk})
    
    def get_file_extension(self):
        """Return the file extension of the uploaded document"""
        name, extension = self.document.name.split('.')[-2:]
        return extension.lower()
    
    def is_pdf(self):
        """Check if the document is a PDF file"""
        return self.get_file_extension() == 'pdf'
    
    def is_image(self):
        """Check if the document is an image file"""
        image_extensions = ['jpg', 'jpeg', 'png', 'gif']
        return self.get_file_extension() in image_extensions
