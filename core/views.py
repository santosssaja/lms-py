from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrasiForm, JadwalMateriForm, RuanganForm, MateriForm, AddSiswaToRoomForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Ruangan, Materi, Jadwal
import datetime
from django.http import JsonResponse

# Mapping for English day names to Indonesian day names
DAY_NAME_MAPPING = {
    'MONDAY': 'SENIN',
    'TUESDAY': 'SELASA',
    'WEDNESDAY': 'RABU',
    'THURSDAY': 'KAMIS',
    'FRIDAY': 'JUMAT',
    'SATURDAY': 'SABTU',
    'SUNDAY': 'MINGGU',
}

@login_required
def hapus_jadwal_view(request, jadwal_id):
    jadwal = get_object_or_404(Jadwal, id=jadwal_id)
    if request.user in jadwal.ruangan.guru_pengajar.all():
        jadwal.delete()
    return redirect('semua-jadwal')

@login_required
def jadwal_detail_api(request, jadwal_id):
    jadwal = get_object_or_404(Jadwal, id=jadwal_id)
    materi_list = Materi.objects.filter(ruangan=jadwal.ruangan)
    data = {
        'ruangan': jadwal.ruangan.nama_ruangan,
        'judul': jadwal.judul,
        'hari': DAY_NAME_MAPPING.get(jadwal.tanggal.strftime('%A').upper(), ''),
        'tanggal': jadwal.tanggal.strftime('%d %B %Y') if jadwal.tanggal else '',
        'jam_mulai': jadwal.jam_mulai.strftime('%H:%M'),
        'jam_selesai': jadwal.jam_selesai.strftime('%H:%M'),
        'materi': [
            {
                'judul': materi.judul,
                'file_url': materi.file.url if materi.file else ''
            }
            for materi in materi_list
        ],
        'murid': [f"{siswa.first_name} {siswa.last_name}".strip() or siswa.username for siswa in jadwal.ruangan.siswa_terdaftar.all()]
    }
    return JsonResponse(data)

@login_required
def semua_jadwal_view(request):
    jadwal_list = Jadwal.objects.all()
    context = {
        'jadwal_list': jadwal_list,
    }
    return render(request, 'semua_jadwal.html', context)

@login_required
def enroll_ruangan_view(request, ruangan_id):
    ruangan = get_object_or_404(Ruangan, id=ruangan_id)
    ruangan.siswa_terdaftar.add(request.user)
    return redirect('dashboard') # Redirect to dashboard after enrolling

@login_required
def upload_materi_view(request, ruangan_id):
    ruangan = get_object_or_404(Ruangan, id=ruangan_id)
    if request.method == 'POST':
        form = MateriForm(request.POST, request.FILES)
        if form.is_valid():
            materi = form.save(commit=False)
            materi.ruangan = ruangan
            materi.save()
            return redirect('dashboard') # Redirect to dashboard after uploading
    else:
        form = MateriForm()
    return render(request, 'upload_materi.html', {'form': form, 'ruangan': ruangan})

@login_required
def profil_view(request):
    profile = request.user.profile
    if profile.role == 'GURU':
        ruangan_list = Ruangan.objects.filter(guru_pengajar=request.user)
    else:
        ruangan_list = Ruangan.objects.filter(siswa_terdaftar=request.user)
    
    context = {
        'ruangan_list': ruangan_list
    }
    return render(request, 'profil.html', context)

def registrasi_view(request):
    if request.method == 'POST':
        # Jika form disubmit (metode POST)
        form = RegistrasiForm(request.POST)
        if form.is_valid():
            # Jika form valid:
            user = form.save() # 1. Simpan user & profile (dari logic di forms.py)
            login(request, user) # 2. Langsung login-kan user yang baru daftar
            return redirect('dashboard') # 3. Arahkan ke halaman dashboard (akan kita buat)
    else:
        # Jika halaman baru dibuka (metode GET)
        form = RegistrasiForm()

    return render(request, 'registrasi.html', {'form': form})

# Lindungi halaman ini, hanya bisa diakses oleh yang sudah login
@login_required 
def dashboard_view(request):
    profile = request.user.profile
    if profile.role == 'GURU':
        return guru_dashboard(request)
    elif profile.role == 'SISWA':
        return siswa_dashboard(request)

def guru_dashboard(request):
    if request.method == 'POST':
        if 'create_ruangan' in request.POST:
            return create_ruangan(request)
        elif 'create_jadwal_materi' in request.POST:
            return create_jadwal_materi(request)
        elif 'add_siswa_to_room' in request.POST:
            ruangan_id = request.POST.get('ruangan_id')
            ruangan = get_object_or_404(Ruangan, id=ruangan_id)
            return add_siswa_to_room(request, ruangan)

    today = datetime.date.today()
    hari_ini_english = today.strftime('%A').upper()
    hari_ini_indonesian = DAY_NAME_MAPPING.get(hari_ini_english, '')
    jadwal_hari_ini = Jadwal.objects.filter(tanggal=today, ruangan__guru_pengajar=request.user)

    ruangan_form = RuanganForm()
    jadwal_materi_form = JadwalMateriForm()

    ruangan_diajar = Ruangan.objects.filter(guru_pengajar=request.user)
    ruangan_diajar_data = []
    for ruangan in ruangan_diajar:
        jadwal_list = Jadwal.objects.filter(ruangan=ruangan).order_by('tanggal', 'jam_mulai')
        materi_list = Materi.objects.filter(ruangan=ruangan)
        add_siswa_to_room_form = AddSiswaToRoomForm(ruangan=ruangan)
        ruangan_diajar_data.append({
            'ruangan': ruangan,
            'jadwal_list': jadwal_list,
            'materi_list': materi_list,
            'add_siswa_to_room_form': add_siswa_to_room_form
        })

    context = {
        'jadwal_hari_ini': jadwal_hari_ini,
        'today': today,
        'ruangan_form': ruangan_form,
        'jadwal_materi_form': jadwal_materi_form,
        'hari_ini_indonesian': hari_ini_indonesian,
        'ruangan_diajar_data': ruangan_diajar_data,
    }
    return render(request, 'dashboard_guru.html', context)

def create_ruangan(request):
    ruangan_form = RuanganForm(request.POST)
    if ruangan_form.is_valid():
        ruangan = ruangan_form.save(commit=False)
        ruangan.save()
        ruangan.guru_pengajar.add(request.user)
    return redirect('dashboard')

def create_jadwal_materi(request):
    jadwal_materi_form = JadwalMateriForm(request.POST, request.FILES)
    if jadwal_materi_form.is_valid():
        ruangan = jadwal_materi_form.cleaned_data['ruangan']
        tanggal = jadwal_materi_form.cleaned_data['tanggal']
        hari = DAY_NAME_MAPPING.get(tanggal.strftime('%A').upper(), '')

        Jadwal.objects.create(
            ruangan=ruangan,
            judul=jadwal_materi_form.cleaned_data['judul'],
            hari=hari,
            tanggal=tanggal,
            jam_mulai=jadwal_materi_form.cleaned_data['jam_mulai'],
            jam_selesai=jadwal_materi_form.cleaned_data['jam_selesai'],
        )
        if jadwal_materi_form.cleaned_data['file']:
            Materi.objects.create(
                ruangan=ruangan,
                judul=jadwal_materi_form.cleaned_data['judul'],
                deskripsi=jadwal_materi_form.cleaned_data['deskripsi'],
                file=jadwal_materi_form.cleaned_data['file'],
            )
    return redirect('dashboard')

def add_siswa_to_room(request, ruangan):
    form = AddSiswaToRoomForm(request.POST, ruangan=ruangan)
    if form.is_valid():
        selected_siswa = form.cleaned_data['siswa']
        ruangan.siswa_terdaftar.set(selected_siswa)
    return redirect('dashboard')


def siswa_dashboard(request):
    today = datetime.date.today()
    hari_ini_english = today.strftime('%A').upper()
    hari_ini_indonesian = DAY_NAME_MAPPING.get(hari_ini_english, '')
    jadwal_hari_ini = Jadwal.objects.filter(tanggal=today, ruangan__siswa_terdaftar=request.user)
    context = {
        'jadwal_hari_ini': jadwal_hari_ini,
        'today': today,
        'hari_ini_indonesian': hari_ini_indonesian,
    }
    return render(request, 'dashboard_siswa.html', context)

def about_view(request):
    return render(request, 'about.html')