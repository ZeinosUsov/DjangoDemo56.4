from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import UserProfile, Application
import re

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Электронная почта')
    fio = forms.CharField(max_length=100, required=True, label='ФИО (кириллица, пробелы)')
    phone = forms.CharField(max_length=20, required=True, label='Телефон (формат: 8(XXX)XXX-XX-XX)')

    class Meta:
        model = User
        fields = ['username', 'email', 'fio', 'phone', 'password1', 'password2']

    def clean_fio(self):
        fio = self.cleaned_data['fio']
        if not re.match(r'^[А-Яа-яЁё\s]+$', fio):
            raise ValidationError('ФИО должно содержать только кириллицу и пробелы.')
        return fio

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not re.match(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', phone):
            raise ValidationError('Телефон должен быть в формате 8(XXX)XXX-XX-XX')
        return phone

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже зарегистрирован.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                fio=self.cleaned_data['fio'],
                phone=self.cleaned_data['phone']
            )
        return user

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'event_date', 'genre', 'participation_format']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date'}),
            'title': forms.TextInput(attrs={'placeholder': 'Название концерта, фестиваля...'}),
            'genre': forms.TextInput(attrs={'placeholder': 'Рок, поп, классика, электронная...'}),
            'participation_format': forms.TextInput(attrs={'placeholder': 'Сольное выступление, группа, оркестр...'}),
        }
        labels = {
            'title': 'Название мероприятия',
            'event_date': 'Желаемая дата',
            'genre': 'Жанр музыки',
            'participation_format': 'Формат участия',
        }

class StatusChangeForm(forms.Form):
    status = forms.ChoiceField(choices=Application.STATUS_CHOICES, label='Новый статус')