from django.urls import path
from . import views
from ml_engine.scoring_api import api_get_propensity_score

urlpatterns = [
    # Public Gateway
    path('', views.process_donation, name='public_portal'),
    
    # Reporting Dashboard
    path('admin-dashboard/', views.donor_list, name='admin_dashboard'),
    
    # Donor CRUD
    path('donors/create/', views.donor_create, name='donor_create'),
    path('donors/<int:pk>/', views.donor_detail, name='donor_detail'),
    path('donors/<int:pk>/update/', views.donor_update, name='donor_update'),
    path('donors/<int:pk>/delete/', views.donor_delete, name='donor_delete'),
    
    # Manual Donation
    path('donations/manual/', views.manual_donation, name='manual_donation'),
    
    # Volunteer Tracking
    path('volunteers/', views.volunteer_list, name='volunteer_list'),
    path('volunteers/create/', views.volunteer_create, name='volunteer_create'),
    path('volunteers/<int:pk>/update/', views.volunteer_update, name='volunteer_update'),
    
    # Admin User Management
    path('admins/', views.admin_user_list, name='admin_user_list'),
    path('admins/create/', views.admin_user_create, name='admin_user_create'),

    # Campaign Management
    path('campaigns/', views.campaign_list, name='campaign_list'),
    path('campaigns/create/', views.campaign_create, name='campaign_create'),
    path('campaigns/<int:pk>/', views.campaign_detail, name='campaign_detail'),
    path('campaigns/<int:pk>/update/', views.campaign_update, name='campaign_update'),
    path('campaigns/<int:pk>/delete/', views.campaign_delete, name='campaign_delete'),

    # AI Scoring API
    path('api/score/<int:donor_id>/', api_get_propensity_score, name='api_score_donor'),
]
