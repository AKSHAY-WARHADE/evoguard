from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('services',views.services,name='services'),
    path('register',views.register,name='register'),
    path('login/',views.login_page,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('complaint',views.complaint,name='complaint'),
    path('user/dashboard', views.user_dashboard, name='user_dashboard'),
    path('user/complaints',views.user_complaints,name='user_complaints'),
    path('user/profile', views.user_profile, name='user_profile'),
    path('user/settings', views.user_settings, name='user_settings'),
    path('queries',views.queries,name='queries'),
    path('employee/login',views.employee_login,name='employee_login'),
    path('employee/dashboard',views.emp_main,name='emp_main'),
    path('new/complaints',views.new_complaints,name='new_complaints'),
    path('pending/complaints',views.pending_complaints,name='pending_complaints'),
    path('solved/complaints',views.solved_complaints,name='solved_complaints'),
    path('update/new/complaints/<str:pk>',views.update_new_complaints,name='update_new_complaints'),
    path('update/pending/complaints/<str:pk>',views.update_pending_complaints,name='update_pending_complaints'),
    path('update/solved/complaints/<str:pk>',views.update_solved_complaints,name='update_solved_complaints'),
    path('check/status',views.check_status,name='check_status'),
    path('complaint/success/', views.complaint_success, name='complaint_success'),
    path('save/profile/', views.save_profile, name='save_profile'),
    path('user/settings/', views.user_settings, name='user_settings'),
    path('search/', views.search_complaints, name='complaint_search_results'),
   
   
    
]