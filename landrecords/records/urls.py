from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home and authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='records/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard and profile
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Land records CRUD
    path('records/', views.RecordListView.as_view(), name='record-list'),
    path('records/<int:pk>/', views.RecordDetailView.as_view(), name='record-detail'),
    path('records/new/', views.RecordCreateView.as_view(), name='record-create'),
    path('records/<int:pk>/update/', views.RecordUpdateView.as_view(), name='record-update'),
    path('records/<int:pk>/delete/', views.RecordDeleteView.as_view(), name='record-delete'),
    
    # Document actions
    path('records/<int:pk>/download/', views.download_document, name='download-document'),
    path('records/<int:pk>/preview/', views.preview_document, name='preview-document'),
    
    # Password reset
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='records/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='records/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='records/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='records/password_reset_complete.html'),
         name='password_reset_complete'),
]
