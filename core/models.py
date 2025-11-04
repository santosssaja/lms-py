from django.db import models
from django.contrib.auth.models import User
import datetime

# 1. Memperluas User bawaan untuk membedakan peran
class Profile(models.Model):
    # 'User' dari Django sudah punya username, password, email, first_name, last_name
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    ROLE_CHOICES = (
        ('SISWA', 'Siswa'),
        ('GURU', 'Guru'),
    )
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='SISWA')

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

# 2. Model untuk Ruangan/Kelas (Course)
class Ruangan(models.Model):
    nama_ruangan = models.CharField(max_length=200)
    # Kita tautkan Guru ke Ruangan. Satu ruangan bisa diajar banyak guru.
    guru_pengajar = models.ManyToManyField(User, related_name='ruangan_diajar')
    # Siswa yang terdaftar di ruangan ini
    siswa_terdaftar = models.ManyToManyField(User, related_name='ruangan_diikuti', blank=True)
    
    def __str__(self):
        return self.nama_ruangan

# 3. Model untuk Materi
class Materi(models.Model):
    # Menautkan materi ini ke satu ruangan spesifik
    ruangan = models.ForeignKey(Ruangan, on_delete=models.CASCADE, related_name='materi_list')
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField(blank=True)
    file = models.FileField(upload_to='materi_files/', blank=True, null=True) # Untuk upload PDF, PPT, dll.
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.ruangan.nama_ruangan} - {self.judul}"

# 4. Model untuk Jam/Jadwal
class Jadwal(models.Model):
    HARI_CHOICES = (
        ('SENIN', 'Senin'),
        ('SELASA', 'Selasa'),
        ('RABU', 'Rabu'),
        ('KAMIS', 'Kamis'),
        ('JUMAT', 'Jumat'),
        ('SABTU', 'Sabtu'),
        ('MINGGU', 'Minggu'),
    )
    ruangan = models.ForeignKey(Ruangan, on_delete=models.CASCADE, related_name='jadwal_list')
    judul = models.CharField(max_length=200, default='Tanpa Judul')
    hari = models.CharField(max_length=10, choices=HARI_CHOICES) # Misal: "Senin", "Selasa"
    tanggal = models.DateField(default=datetime.date.today)
    jam_mulai = models.TimeField()
    jam_selesai = models.TimeField()
    
    def __str__(self):
        return f"{self.ruangan.nama_ruangan} | {self.hari} ({self.jam_mulai} - {self.jam_selesai})"