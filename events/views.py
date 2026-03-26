
from django.core.mail import send_mail
from django.conf import settings

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Event, Registration
from .forms import EventForm, RegistrationForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


# ═══ PUBLIC VIEWS ══════════════════════════════

def home_view(request):
    """Homepage - logged in ho to dashboard pe bhejo"""
    if request.user.is_authenticated:
        if request.user.is_professor():
            return redirect('professor_dashboard')
        return redirect('student_dashboard')

    featured_events = Event.objects.filter(
        approved=True
    ).order_by('-created_at')[:6]

    stats = {
        'total_events': Event.objects.filter(approved=True).count(),
        'total_colleges': Event.objects.filter(
            approved=True
        ).values('college').distinct().count(),
        'total_registrations': Registration.objects.count(),
    }

    return render(request, 'events/home.html', {
        'featured_events': featured_events,
        'stats': stats,
    })


def events_list_view(request):
    """All events with search and filter"""
    events = Event.objects.filter(approved=True)

    search_query = request.GET.get('search', '')
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(college__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    category = request.GET.get('category', '')
    if category:
        events = events.filter(category=category)

    categories = Event.CATEGORY_CHOICES

    return render(request, 'events/events.html', {
        'events': events,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category,
    })

# Ye do views add karo existing views ke saath

def contact_view(request):
    sent = False

    if request.method == 'POST':
        name    = request.POST.get('name', '').strip()
        email   = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and message:
            try:
                # Admin ko email bhejo
                send_mail(
                    subject=f'EventSphere Contact: {subject}',
                    message=(
                        f'Name: {name}\n'
                        f'Email: {email}\n'
                        f'Subject: {subject}\n\n'
                        f'Message:\n{message}'
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=['theholara0@gmail.com'],
                    fail_silently=True,
                )
                sent = True
            except Exception:
                sent = True  # Form clear karo anyway

    return render(request, 'events/contact.html', {'sent': sent})


def faq_view(request):
    return render(request, 'events/faq.html')

def event_detail_view(request, pk):
    event = get_object_or_404(Event, pk=pk, approved=True)
    already_registered = False
    if request.user.is_authenticated:
        already_registered = Registration.objects.filter(
            event=event,
            user=request.user
        ).exists()

    form = RegistrationForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to register.')
            return redirect('login')

        if request.user.is_professor():
            messages.error(request, 'Professors cannot register.')
            return redirect('event_detail', pk=pk)

        if already_registered:
            messages.warning(request, 'Already registered!')
            return redirect('event_detail', pk=pk)

        if event.is_full():
            messages.error(request, 'Event is full!')
            return redirect('event_detail', pk=pk)

        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.user = request.user
            registration.save()

            # ── Student Ko Email ──────────────────
            try:
                html_msg = render_to_string(
                    'events/emails/registration_confirmation.html',
                    {
                        'user': request.user,
                        'event': event,
                        'registration': registration,
                    }
                )
                send_mail(
                    subject=f'Registered: {event.title} ✅',
                    message=strip_tags(html_msg),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[request.user.email],
                    html_message=html_msg,
                    fail_silently=True,
                )
            except Exception:
                pass

            # ── Professor Ko Email ────────────────
            try:
                prof_msg = render_to_string(
                    'events/emails/new_registration_notify.html',
                    {
                        'professor': event.created_by,
                        'event': event,
                        'registration': registration,
                        'student': request.user,
                    }
                )
                send_mail(
                    subject=f'New Registration: {event.title} 🎉',
                    message=strip_tags(prof_msg),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[event.created_by.email],
                    html_message=prof_msg,
                    fail_silently=True,
                )
            except Exception:
                pass

            messages.success(
                request,
                f'Successfully registered for {event.title}!'
            )
            return redirect('event_detail', pk=pk)

    return render(request, 'events/event_detail.html', {
        'event': event,
        'form': form,
        'already_registered': already_registered,
        'registered_count': event.registered_count(),
    })

def about_view(request):
    """About page"""
    return render(request, 'events/about.html')


# ═══ PROFESSOR VIEWS ═══════════════════════════

@login_required
def professor_dashboard_view(request):
    """Professor main dashboard"""
    if not request.user.is_professor():
        return redirect('student_dashboard')

    my_events = Event.objects.filter(created_by=request.user)
    total_registrations = sum(
        event.registered_count() for event in my_events
    )
    recent_regs = Registration.objects.filter(
        event__created_by=request.user
    ).order_by('-registered_at')[:5]

    return render(request, 'events/professor_dashboard.html', {
        'my_events': my_events,
        'total_registrations': total_registrations,
        'recent_regs': recent_regs,
        'active_page': 'dashboard',
    })


@login_required
def professor_events_view(request):
    """Professor - all my events"""
    if not request.user.is_professor():
        return redirect('student_dashboard')

    my_events = Event.objects.filter(created_by=request.user)

    return render(request, 'events/professor_events.html', {
        'my_events': my_events,
        'active_page': 'events',
    })


@login_required
def add_event_view(request):
    """Add new event - Professor only"""
    if not request.user.is_professor():
        messages.error(request, 'Only professors can add events.')
        return redirect('home')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(
                request,
                'Event submitted! Waiting for admin approval.'
            )
            return redirect('professor_events')
    else:
        form = EventForm()

    return render(request, 'events/add_event.html', {
        'form': form,
        'active_page': 'add_event',
    })


@login_required
def edit_event_view(request, pk):
    """Edit event - Only owner"""
    event = get_object_or_404(Event, pk=pk)

    if event.created_by != request.user:
        messages.error(request, 'You can only edit your own events.')
        return redirect('professor_events')

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('professor_events')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/edit_event.html', {
        'form': form,
        'event': event,
        'active_page': 'events',
    })


@login_required
def delete_event_view(request, pk):
    """Delete event - Only owner"""
    event = get_object_or_404(Event, pk=pk)

    if event.created_by != request.user:
        messages.error(request, 'You can only delete your own events.')
        return redirect('professor_events')

    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully.')
        return redirect('professor_events')

    return render(request, 'events/confirm_delete.html', {
        'event': event,
        'active_page': 'events',
    })


@login_required
def event_registrations_view(request, pk):
    """View registrations for an event - Professor only"""
    event = get_object_or_404(Event, pk=pk)

    if event.created_by != request.user:
        messages.error(request, 'Access denied.')
        return redirect('professor_dashboard')

    registrations = Registration.objects.filter(
        event=event
    ).order_by('-registered_at')

    return render(request, 'events/registrations.html', {
        'event': event,
        'registrations': registrations,
        'active_page': 'events',
    })


# ═══ STUDENT VIEWS ═════════════════════════════

@login_required
def student_dashboard_view(request):
    """Student main dashboard"""
    if not request.user.is_student():
        return redirect('professor_dashboard')

    registrations = Registration.objects.filter(
        user=request.user
    ).select_related('event').order_by('-registered_at')

    upcoming = [r for r in registrations if r.event.is_upcoming()]
    past     = [r for r in registrations if not r.event.is_upcoming()]

    all_events = Event.objects.filter(
        approved=True
    ).order_by('-created_at')[:6]

    return render(request, 'events/student_dashboard.html', {
        'registrations': registrations,
        'upcoming': upcoming,
        'past': past,
        'all_events': all_events,
        'active_page': 'dashboard',
    })


@login_required
def my_registrations_view(request):
    """Student - all my registrations"""
    if not request.user.is_student():
        return redirect('professor_dashboard')

    registrations = Registration.objects.filter(
        user=request.user
    ).select_related('event').order_by('-registered_at')

    return render(request, 'events/my_registrations.html', {
        'registrations': registrations,
        'active_page': 'registrations',
    })


def error_404_view(request, exception):
    return render(request, 'events/404.html', status=404)

def error_500_view(request):
    return render(request, 'events/500.html', status=500)

@login_required
def profile_view(request):
    """User profile page"""
    if request.user.is_professor():
        my_events = Event.objects.filter(
            created_by=request.user
        ).count()
        total_regs = sum(
            e.registered_count()
            for e in Event.objects.filter(created_by=request.user)
        )
        context = {
            'my_events_count': my_events,
            'total_registrations': total_regs,
        }
    else:
        registrations = Registration.objects.filter(
            user=request.user
        )
        context = {
            'registrations_count': registrations.count(),
            'upcoming_count': sum(
                1 for r in registrations
                if r.event.is_upcoming()
            ),
        }

    return render(request, 'events/profile.html', context)