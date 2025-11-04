# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Ruangan, Materi

class AddSiswaToRoomForm(forms.Form):
    siswa = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(profile__role='SISWA'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def __init__(self, *args, **kwargs):
        ruangan = kwargs.pop('ruangan', None)
        super().__init__(*args, **kwargs)
        if ruangan:
            self.fields['siswa'].initial = ruangan.siswa_terdaftar.all()

class JadwalMateriForm(forms.Form):
    ruangan = forms.ModelChoiceField(queryset=Ruangan.objects.all())
    tanggal = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    jam_mulai = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    jam_selesai = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    judul = forms.CharField(max_length=200)
    deskripsi = forms.CharField(widget=forms.Textarea, required=False)
    file = forms.FileField(required=False)

class RuanganForm(forms.ModelForm):
    class Meta:
        model = Ruangan
        fields = ['nama_ruangan']

class MateriForm(forms.ModelForm):
    class Meta:
        model = Materi
        fields = ['judul', 'deskripsi', 'file']

class RegistrasiForm(UserCreationForm):
    # Tambahkan field baru untuk First Name, Last Name, dan Role
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}))

    ROLE_CHOICES = (
        ('SISWA', 'Saya seorang Siswa'),
        ('GURU', 'Saya seorang Guru'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect(attrs={'class': 'mr-2'}))

    class Meta(UserCreationForm.Meta):
        model = User
        # Tentukan field apa saja yang muncul di form
        # fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super(RegistrasiForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'})
        # UserCreationForm provides 'password1' and 'password2' fields
        self.fields['password1'].widget.attrs.update({'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'})
        self.fields['password2'].widget.attrs.update({'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'})

    # Kita 'override' method save()
    def save(self, commit=True):
        # 1. Simpan data User (username, password)
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save() # Simpan user

            # 2. Buat Profile yang terhubung dengan User tadi
            profile = Profile.objects.create(
                user=user,
                role=self.cleaned_data['role']
            )
            profile.save()

        return user