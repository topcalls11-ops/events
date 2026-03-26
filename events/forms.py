from django import forms
from .models import Event, Registration


class EventForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control glass-input'
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )

    class Meta:
        model = Event
        fields = [
            'title', 'description', 'college',
            'category', 'date', 'venue',
            'max_participants', 'image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control glass-input',
                'placeholder': 'Event title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control glass-input',
                'rows': 5,
                'placeholder': 'Describe your event...'
            }),
            'college': forms.TextInput(attrs={
                'class': 'form-control glass-input',
                'placeholder': 'College name'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control glass-input'
            }),
            'venue': forms.TextInput(attrs={
                'class': 'form-control glass-input',
                'placeholder': 'Event venue / location'
            }),
            'max_participants': forms.NumberInput(attrs={
                'class': 'form-control glass-input',
                'placeholder': 'Max participants'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control glass-input'
            }),
        }


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['name', 'email', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control glass-input',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control glass-input',
                'placeholder': 'Your email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control glass-input',
                'placeholder': 'Phone number'
            }),
        }