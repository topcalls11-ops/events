from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from .forms import SignupForm, LoginForm, SetNewPasswordForm

User = get_user_model()


def signup_view(request):
    if request.user.is_authenticated:
        if request.user.is_professor():
            return redirect('professor_dashboard')
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            try:
                html_message = render_to_string(
                    'users/emails/welcome_email.html',
                    {'user': user}
                )
                plain_message = strip_tags(html_message)
                send_mail(
                    subject='Welcome to EventSphere! 🎉',
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(
                request,
                f'Welcome {user.first_name}! '
                f'Check your email for confirmation.'
            )
            if user.is_professor():
                return redirect('professor_dashboard')
            return redirect('student_dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = SignupForm()

    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_professor():
            return redirect('professor_dashboard')
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(
                request,
                f'Welcome back, '
                f'{user.first_name or user.username}! 👋'
            )
            if user.is_professor():
                return redirect('professor_dashboard')
            return redirect('student_dashboard')
        else:
            messages.error(
                request,
                'Invalid username or password.'
            )
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(
        request,
        'Logged out successfully. See you soon! 👋'
    )
    return redirect('home')


@login_required
def profile_view(request):
    return render(
        request,
        'users/profile.html',
        {'user': request.user}
    )


def forgot_password_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()

        if not email:
            messages.error(request, 'Please enter your email.')
            return render(request, 'users/forgot_password.html')

        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid   = urlsafe_base64_encode(force_bytes(user.pk))

            reset_link = (
                f"{request.scheme}://{request.get_host()}"
                f"/users/reset-password/{uid}/{token}/"
            )

            try:
                html_message = render_to_string(
                    'users/emails/reset_password_email.html',
                    {
                        'user': user,
                        'reset_link': reset_link,
                    }
                )
                plain_message = strip_tags(html_message)
                send_mail(
                    subject='Reset Your EventSphere Password 🔐',
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
            except Exception as e:
                messages.error(
                    request,
                    f'Could not send email: {str(e)}'
                )
                return render(
                    request,
                    'users/forgot_password.html'
                )

        except User.DoesNotExist:
            pass  # Security ke liye same page

        return redirect('password_reset_sent')

    return render(request, 'users/forgot_password.html')


def password_reset_sent_view(request):
    return render(request, 'users/password_reset_sent.html')


def reset_password_view(request, uidb64, token):
    try:
        uid  = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    token_valid = (
        user is not None and
        default_token_generator.check_token(user, token)
    )

    if not token_valid:
        return render(
            request,
            'users/reset_password_invalid.html'
        )

    if request.method == 'POST':
        form = SetNewPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()

            try:
                html_message = render_to_string(
                    'users/emails/password_changed_email.html',
                    {'user': user}
                )
                plain_message = strip_tags(html_message)
                send_mail(
                    subject='Password Changed Successfully ✅',
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    html_message=html_message,
                    fail_silently=True,
                )
            except Exception:
                pass

            return redirect('reset_password_done')
    else:
        form = SetNewPasswordForm()

    return render(request, 'users/reset_password.html', {
        'form': form,
        'uidb64': uidb64,
        'token': token,
    })


def reset_password_done_view(request):
    return render(request, 'users/reset_password_done.html')