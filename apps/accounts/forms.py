from django import forms
from django.contrib.auth.models import User
from .models import PlayerProfile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'retro-input', 'placeholder': 'Enter Password'}),
        min_length=6
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'retro-input', 'placeholder': 'Confirm Password'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'retro-input', 'placeholder': 'Nokia Gamer Tag'}),
            'email': forms.EmailInput(attrs={'class': 'retro-input', 'placeholder': 'Optional Email'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Gamer Tag already claimed. Choose another.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password_confirm')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = PlayerProfile
        fields = ['nickname', 'bio', 'theme', 'phone_shell', 'sound_enabled', 'sound_volume', 'vibration_enabled', 'scanlines_enabled', 'touch_controls_enabled']
        widgets = {
            'nickname': forms.TextInput(attrs={'class': 'retro-input'}),
            'bio': forms.Textarea(attrs={'class': 'retro-input', 'rows': 3}),
            'theme': forms.Select(attrs={'class': 'retro-select'}),
            'phone_shell': forms.Select(attrs={'class': 'retro-select'}),
            'sound_volume': forms.NumberInput(attrs={'class': 'retro-input', 'min': 0, 'max': 100}),
            'sound_enabled': forms.CheckboxInput(attrs={'class': 'retro-checkbox'}),
            'vibration_enabled': forms.CheckboxInput(attrs={'class': 'retro-checkbox'}),
            'scanlines_enabled': forms.CheckboxInput(attrs={'class': 'retro-checkbox'}),
            'touch_controls_enabled': forms.CheckboxInput(attrs={'class': 'retro-checkbox'}),
        }
