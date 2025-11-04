from django.contrib import admin
from .models import Profile, Ruangan, Materi, Jadwal

# Daftarkan model Anda di sini agar muncul di panel admin
admin.site.register(Profile)
admin.site.register(Ruangan)
admin.site.register(Materi)
admin.site.register(Jadwal)