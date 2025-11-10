# LMS Proyek

## Deskripsi Proyek
LMS Proyek adalah Sistem Manajemen Pembelajaran (LMS) sederhana yang dibangun menggunakan kerangka kerja web Django. Aplikasi ini dirancang untuk memfasilitasi interaksi antara guru dan siswa dalam lingkungan pembelajaran online. Guru dapat membuat kelas, mengelola jadwal, mengunggah materi pembelajaran, dan mendaftarkan siswa ke kelas mereka. Siswa, di sisi lain, dapat melihat jadwal mereka, mengakses materi pembelajaran yang diunggah oleh guru, dan mengelola profil mereka.

## Fitur Utama
-   **Autentikasi Pengguna:** Sistem login dan registrasi yang aman untuk guru dan siswa.
-   **Dashboard Berbasis Peran:** Dashboard terpisah dengan fungsionalitas yang relevan untuk guru dan siswa.
-   **Manajemen Ruangan/Kelas:** Guru dapat membuat, mengelola, dan melihat detail kelas yang mereka ajar.
-   **Manajemen Jadwal:** Guru dapat membuat jadwal pelajaran dan siswa dapat melihat jadwal mereka.
-   **Unggah Materi:** Guru dapat mengunggah berbagai jenis materi pembelajaran (misalnya, PDF, presentasi) ke kelas mereka.
-   **Pendaftaran Siswa:** Guru dapat mendaftarkan siswa ke kelas yang mereka buat.
-   **Manajemen Profil:** Pengguna dapat melihat dan mengelola informasi profil mereka.
-   **Halaman About:** Informasi tentang proyek dan detail teknis implementasi.

## Tumpukan Teknologi
-   **Backend:** Python 3.x dengan Django 5.x
-   **Database:** SQLite (untuk pengembangan, dapat diganti dengan PostgreSQL/MySQL untuk produksi)
-   **Frontend:** HTML dengan styling menggunakan Tailwind CSS (melalui CDN untuk kemudahan)
-   **JavaScript:** Vanilla JavaScript untuk interaktivitas dasar (misalnya, modal jadwal).

## Struktur Kode
-   `core/models.py`: Definisi skema database untuk `Profile`, `Ruangan`, `Materi`, dan `Jadwal`.
-   `core/views.py`: Logika untuk menangani permintaan web, rendering template, dan interaksi database. Dipecah menjadi fungsi-fungsi terpisah untuk setiap peran (misalnya, `guru_dashboard`, `siswa_dashboard`).
-   `core/forms.py`: Formulir kustom untuk registrasi pengguna, pembuatan ruangan, pembuatan jadwal dan materi, serta penambahan siswa ke ruangan.
-   `core/urls.py`: Konfigurasi URL routing untuk aplikasi.
-   `core/templates/`: Direktori yang berisi semua template HTML, dengan `base.html` sebagai template dasar untuk konsistensi tata letak.

## Instalasi dan Setup

### Prasyarat
-   Python 3.x
-   pip (manajer paket Python)

### Langkah-langkah Instalasi
1.  **Clone repositori:**
    ```bash
    git clone https://github.com/santosssaja/lms-py
    cd lms-py
    ```

2.  **Buat dan aktifkan virtual environment:**
    ```bash
    python -m venv venv
    # Di Windows
    .\venv\Scripts\activate
    # Di macOS/Linux
    source venv/bin/activate
    ```

3.  **Instal dependensi:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Catatan: Anda mungkin perlu membuat `requirements.txt` terlebih dahulu jika belum ada, dengan menjalankan `pip freeze > requirements.txt`)*

4.  **Jalankan migrasi database:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Buat superuser (opsional, untuk akses admin Django):**
    ```bash
    python manage.py createsuperuser
    ```
    Ikuti petunjuk untuk membuat username dan password.

6.  **Jalankan server pengembangan:**
    ```bash
    python manage.py runserver
    ```

    Aplikasi akan tersedia di `http://127.0.0.1:8000/`.

## Penggunaan

### Sebagai Guru
1.  Daftar atau login sebagai guru.
2.  Dari dashboard, Anda dapat:
    -   Membuat ruangan/kelas baru.
    -   Membuat jadwal dan mengunggah materi untuk kelas Anda.
    -   Menambahkan siswa ke kelas Anda.
    -   Melihat semua jadwal yang Anda ajar.

### Sebagai Siswa
1.  Daftar atau login sebagai siswa.
2.  Dari dashboard, Anda dapat:
    -   Melihat jadwal pelajaran Anda.
    -   Mengakses materi pembelajaran yang diunggah oleh guru.

## Lisensi
Proyek ini dilisensikan di bawah Lisensi MIT. Lihat file `LICENSE` untuk detail lebih lanjut.
