from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.home_view, name='home'),
    path('events/', views.events_list_view, name='events'),
    path('events/<int:pk>/', views.event_detail_view, name='event_detail'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),  # ← ADD
    path('faq/', views.faq_view, name='faq'),              # ← ADD

    # Professor
    path('professor/dashboard/', views.professor_dashboard_view, name='professor_dashboard'),
    path('professor/events/', views.professor_events_view, name='professor_events'),
    path('professor/events/add/', views.add_event_view, name='add_event'),
    path('professor/events/edit/<int:pk>/', views.edit_event_view, name='edit_event'),
    path('professor/events/delete/<int:pk>/', views.delete_event_view, name='delete_event'),
    path('professor/events/<int:pk>/registrations/', views.event_registrations_view, name='event_registrations'),

    # Student
    path('student/dashboard/', views.student_dashboard_view, name='student_dashboard'),
    path('student/registrations/', views.my_registrations_view, name='my_registrations'),

    # Profile
    path('profile/', views.profile_view, name='profile'),
]