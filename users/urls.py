from django.urls import path
from . import views

urlpatterns = [
    path('signup/',  views.signup_view,  name='signup'),
    path('login/',   views.login_view,   name='login'),
    path('logout/',  views.logout_view,  name='logout'),

    path(
        'forgot-password/',
        views.forgot_password_view,
        name='forgot_password'
    ),
    path(
        'forgot-password/sent/',
        views.password_reset_sent_view,
        name='password_reset_sent'
    ),
    path(
        'reset-password/<uidb64>/<token>/',
        views.reset_password_view,
        name='reset_password'
    ),
    path(
        'reset-password/done/',
        views.reset_password_done_view,
        name='reset_password_done'
    ),
]