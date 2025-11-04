# core/urls.py
from django.urls import path
from .views import (
    registrasi_view, 
    dashboard_view, 
    enroll_ruangan_view,
    upload_materi_view,
    profil_view,
    semua_jadwal_view,
    jadwal_detail_api,
    hapus_jadwal_view,
    about_view,
)

urlpatterns = [
    path('', dashboard_view, name='home'),
    path('about/', about_view, name='about'),
    path('registrasi/', registrasi_view, name='registrasi'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('ruangan/<int:ruangan_id>/enroll/', enroll_ruangan_view, name='enroll-ruangan'),
    path('ruangan/<int:ruangan_id>/upload/', upload_materi_view, name='upload-materi'),
    path('profil/', profil_view, name='profil'),
    path('semua-jadwal/', semua_jadwal_view, name='semua-jadwal'),
    path('api/jadwal/<int:jadwal_id>/', jadwal_detail_api, name='jadwal-detail-api'),
    path('jadwal/<int:jadwal_id>/hapus/', hapus_jadwal_view, name='hapus-jadwal'),
]