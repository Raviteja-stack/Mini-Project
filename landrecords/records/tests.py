from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import LandRecord, DocumentCategory, UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile

class ModelsTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Create profile for user
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone_number='1234567890',
            address='123 Test St'
        )
        
        # Create document category
        self.category = DocumentCategory.objects.create(
            name='Deed',
            description='Property deed documents'
        )
        
        # Create a test document
        self.document = SimpleUploadedFile(
            "test_doc.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        
        # Create land record
        self.record = LandRecord.objects.create(
            title='Test Property',
            property_address='123 Test Avenue',
            description='Test property description',
            owner=self.user,
            category=self.category,
            document=self.document,
            survey_number='TEST123',
            property_size='1000 sq.ft',
            property_type='Residential'
        )
    
    def test_user_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.phone_number, '1234567890')
        
    def test_document_category_creation(self):
        self.assertEqual(self.category.name, 'Deed')
        
    def test_land_record_creation(self):
        self.assertEqual(self.record.title, 'Test Property')
        self.assertEqual(self.record.owner, self.user)
        self.assertEqual(self.record.category, self.category)

class ViewsTestCase(TestCase):
    def setUp(self):
        # Create client
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        
        # Create profile for user
        self.profile = UserProfile.objects.create(
            user=self.user,
            phone_number='1234567890',
            address='123 Test St'
        )
        
        # Create document category
        self.category = DocumentCategory.objects.create(
            name='Deed',
            description='Property deed documents'
        )
    
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/home.html')
    
    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'records/register.html')
        
        # Test user registration
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'testpassword456',
            'password2': 'testpassword456'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        
    def test_login_required(self):
        # Test that dashboard requires login
        response = self.client.get(reverse('dashboard'))
        self.assertNotEqual(response.status_code, 200)
        
        # Login and test again
        self.client.login(username='testuser', password='testpassword123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
