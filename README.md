---

### **README.md (BAGIAN 1 DARI 3): Pengenalan, Fitur Utama, dan Arsitektur Proyek**

```markdown
# Smart Expense Data Generator

## 1. Pengenalan Proyek

`Smart Expense Data Generator` adalah aplikasi web full-stack yang dirancang untuk mengatasi masalah fundamental dalam analisis data dan machine learning: kelangkaan data transaksi yang realistis. Aplikasi ini berfungsi sebagai "mesin" untuk menghasilkan dataset pengeluaran harian sintetis yang tidak hanya terlihat natural, tetapi juga terkontrol secara presisi untuk memenuhi target finansial bulanan yang telah ditentukan.

Proyek ini dibangun menggunakan **Python (Flask)** untuk backend dan **Vanilla JavaScript** untuk frontend, menjadikannya ringan, mudah dipahami, dan dapat di-deploy di mana saja.

**Masalah yang Dipecahkan:**
- Kebutuhan data dummy untuk Business Intelligence (BI) Dashboards.
- Pengujian skenario dan model perencanaan keuangan.
- Data training untuk model deteksi anomali atau forecasting.
- Mengisi database untuk pengembangan dan demo aplikasi.

**Solusi yang Ditawarkan:**
- **Generator Hibrida**: Menggabungkan naturalitas perilaku belanja *bottom-up* dengan kontrol target *top-down*.
- **Output Terkontrol**: Menghasilkan data yang total akhirnya (per kategori) selalu akurat (95-100%) terhadap target yang ditetapkan.
- **Antarmuka Sederhana**: UI berbasis web yang intuitif untuk memilih periode dan menghasilkan data dengan beberapa klik.

---

## 2. Fitur Utama

- **UI Berbasis Web**: Antarmuka pengguna yang bersih untuk memilih Tahun dan Bulan.
- **Tampilan Target Dinamis**: Menampilkan ringkasan target finansial untuk periode yang dipilih sebelum data digenerate.
- **Generasi Transaksi Natural**: Menggunakan **Logika "Keranjang Belanja"** untuk membuat keterangan transaksi yang realistis (`susu/gula/kopi/lpg`).
- **Simulasi Perilaku Manusia**:
    - Tumpang tindih kategori (item operasional dalam belanja bahan baku).
    - Frekuensi transaksi yang bervariasi (belanja harian vs. pembayaran tagihan bulanan).
    - Penanganan hari libur untuk transaksi terjadwal seperti gaji.
- **Mesin Kontrol Adaptif**:
    - **Penyesuaian Harian**: Sistem secara otomatis "mengerem" atau "menginjak gas" pengeluaran harian untuk tetap berada di jalur menuju target bulanan.
    - **Kalibrasi Presisi 100%**: Mekanisme final untuk memastikan tidak ada selisih antara hasil yang digenerate dan target awal.
- **Struktur Kode Modular**: Pemisahan yang jelas antara routing (Flask), logika inti (Kelas Generator), dan presentasi (Frontend).

---

## 3. Arsitektur & Teknologi

Proyek ini menggunakan arsitektur client-server yang sederhana dan efektif.

### Komponen Utama:

1.  **Backend Server (Flask - `app.py`)**
    - Bertanggung jawab untuk menyajikan frontend (`index.html`).
    - Menyediakan dua API endpoint utama:
        - `POST /get-target`: Untuk mengambil data target dari database internal.
        - `POST /generate-data`: Untuk memicu proses generasi data.
    - Berperan sebagai orkestrator yang menerima permintaan dari klien dan memanggil modul generator.

2.  **Mesin Generator (Python Class - `expense_generator.py`)**
    - Ini adalah "otak" dari aplikasi.
    - Berisi kelas `SmartExpenseGenerator` yang merangkum semua logika kompleks untuk pembuatan data.
    - Mengelola *state*, memproses aturan tetap, menjalankan loop harian adaptif, dan melakukan kalibrasi akhir.
    - Sepenuhnya terpisah dari lapisan web, membuatnya dapat diuji dan digunakan kembali di lingkungan lain.

3.  **Frontend Client (HTML/CSS/JS)**
    - Berjalan sepenuhnya di browser pengguna.
    - Menyediakan UI untuk interaksi.
    - Menggunakan **JavaScript `fetch` API** untuk berkomunikasi dengan backend Flask secara asinkron (tanpa refresh halaman).
    - Bertanggung jawab untuk merender data target dan hasil transaksi ke dalam tabel yang mudah dibaca.

### Stack Teknologi:

```
- Bahasa Backend: Python 3.8+
- Framework Backend: Flask
- Library Data: Pandas, NumPy
- Bahasa Frontend: JavaScript (ES6+)
- Struktur Frontend: HTML5
- Styling Frontend: CSS3```
```


### **README.md (BAGIAN 2 DARI 3): Struktur Proyek, Instalasi, dan Cara Menjalankan**

```markdown
---

## 4. Struktur Direktori Proyek

Proyek ini diorganisir dengan struktur yang bersih untuk memisahkan logika, antarmuka, dan aset statis.

```
/smart-expense-generator/
│
├── app.py
│   └── File utama aplikasi Flask. Mengandung semua route (API endpoints)
│       dan bertindak sebagai controller yang menghubungkan frontend
│       dengan mesin generator.
│
├── expense_generator.py
│   └── Modul inti aplikasi. Berisi kelas `SmartExpenseGenerator`
│       yang menangani semua logika kompleks untuk pembuatan data
│       sintetis.
│
├── /templates/
│   └── index.html
│       └── Satu-satunya file HTML untuk antarmuka pengguna (UI).
│           Ditampilkan oleh Flask saat pengguna mengakses root URL.
│
└── /static/
    ├── style.css
    │   └── File CSS untuk memberikan styling pada `index.html`.
    │
    └── script.js
        └── File JavaScript yang berisi semua logika frontend.
            Menangani interaksi pengguna, panggilan API ke backend,
            dan rendering data yang diterima.
```

---

## 5. Panduan Instalasi & Pengaturan

Untuk menjalankan aplikasi ini di lingkungan lokal Anda, ikuti langkah-langkah berikut.

### Prasyarat

- **Python**: Pastikan Anda memiliki Python versi **3.8** atau yang lebih baru terinstal. Anda dapat memeriksanya dengan menjalankan `python --version` atau `python3 --version`.
- **pip**: Manajer paket Python, biasanya sudah terinstal bersama Python.

### Langkah-langkah Instalasi

1.  **Clone Repositori**

    Buka terminal atau Git Bash Anda dan clone repositori ini ke mesin lokal Anda.
    ```bash
    git clone https://github.com/your-username/smart-expense-generator.git
    cd smart-expense-generator
    ```

2.  **Buat dan Aktifkan Lingkungan Virtual (*Virtual Environment*)**

    Menggunakan lingkungan virtual adalah praktik terbaik untuk mengisolasi dependensi proyek dan menghindari konflik dengan paket Python global.

    -   **Untuk macOS / Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

    -   **Untuk Windows (Command Prompt / PowerShell):**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    Setelah diaktifkan, Anda akan melihat `(venv)` di awal baris prompt terminal Anda.

3.  **Instal Dependensi yang Diperlukan**

    Proyek ini memerlukan beberapa library Python. Instal semuanya dengan satu perintah:
    ```bash
    pip install Flask pandas numpy
    ```
    -   `Flask`: Kerangka kerja web untuk backend.
    -   `pandas`: Untuk manipulasi data dan struktur DataFrame.
    -   `numpy`: Untuk operasi numerik, terutama dalam menghasilkan variasi acak.

---

## 6. Cara Menjalankan Aplikasi

Setelah semua dependensi terinstal, Anda dapat menjalankan server pengembangan Flask.

1.  **Jalankan Server**

    Pastikan Anda berada di direktori root proyek (`/smart-expense-generator/`) dan lingkungan virtual Anda aktif. Kemudian, jalankan perintah berikut:
    ```bash
    python app.py
    ```

2.  **Akses Aplikasi**

    Anda akan melihat output di terminal yang menandakan bahwa server sedang berjalan, biasanya pada `http://127.0.0.1:5000`.
    ```
     * Serving Flask app 'app'
     * Debug mode: on
     * Running on http://127.0.0.1:5000
    Press CTRL+C to quit
    ```
    Buka browser web pilihan Anda dan kunjungi alamat **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.

3.  **Gunakan Aplikasi**
    - Pilih Tahun dan Bulan dari dropdown.
    - Klik tombol **"Tampilkan Target"**. Tabel target akan muncul.
    - Klik tombol **"Generate Data Transaksi"**. Tabel verifikasi dan tabel detail transaksi akan muncul di bawahnya.

4.  **Hentikan Server**

    Untuk menghentikan server, kembali ke terminal Anda dan tekan `CTRL+C`.
```


### **README.md (BAGIAN 3 DARI 3): Detail Logika Inti & Spesifikasi API**

```markdown
---

## 7. Penjelasan Mendalam: Logika Inti Generator

Inti dari aplikasi ini adalah kelas `SmartExpenseGenerator` dalam file `expense_generator.py`. Kelas ini mengimplementasikan **arsitektur hibrida** untuk menghasilkan data yang realistis namun terkontrol.

### Fase 1: Generasi Transaksi Tetap (`_generate_fixed_transactions`)

Proses dimulai dengan membuat semua transaksi yang polanya dapat diprediksi. Ini membangun "tulang punggung" data bulanan.

-   **Input**: `monthly_target` (dictionary target bulanan).
-   **Proses**:
    -   **Gaji**: Dibuat satu kali pada tanggal 10, dengan logika untuk menghindari akhir pekan (jika tanggal 10 jatuh pada hari Sabtu, gaji dibayarkan Senin; jika Minggu, dibayarkan Jumat).
    -   **Sewa, Marketing, Depresiasi**: Dibuat satu kali pada tanggal-tanggal yang telah ditentukan (misalnya, awal bulan).
    -   **Iuran Lingkungan**: Dipecah menjadi dua jenis transaksi:
        1.  `Iuran Warga` (Rp 80.000): Satu kali di awal bulan.
        2.  `Iuran Sampah` (Rp 20.000): Dibuat pada **setiap hari Sabtu** dalam bulan tersebut.
    -   **Utilitas Tetap**: Komponen Utilitas yang dapat diprediksi (WIFI dan PDAM) dibuat terlebih dahulu. Sisa dari total target `Utilitas` kemudian dihitung dan diteruskan sebagai target baru untuk `Listrik` yang akan diproses secara fleksibel.
-   **Output**: Sebagian dari daftar transaksi dan sisa target untuk kategori fleksibel.

### Fase 2: Generasi Transaksi Fleksibel (`_generate_daily_flexible_transactions`)

Ini adalah fase paling dinamis, di mana mesin kontrol adaptif bekerja.

-   **Input**: `flexible_targets` (kamus berisi sisa target untuk COGS, Maintenance, Listrik, dll.).
-   **Proses**:
    -   Generator memasuki **loop harian** dari tanggal 1 hingga akhir bulan.
    -   **Pada setiap hari:**
        1.  **Analisis Pro-rata**: Sistem menghitung posisi ideal pengeluaran (`target_pro_rata`). Ini adalah jumlah pengeluaran yang seharusnya sudah terjadi hingga hari ini untuk mencapai target bulanan secara linear.
        2.  **Kalkulasi `adjustment_factor`**: Sistem membandingkan `target_pro_rata` dengan pengeluaran aktual (`actual_spending`).
           -   `discrepancy = target_pro_rata - actual_spending`
           -   Jika `discrepancy` positif (tertinggal), `adjustment_factor` akan menjadi `> 1`.
           -   Jika `discrepancy` negatif (terlalu boros), `adjustment_factor` akan menjadi `< 1`.
        3.  **Generasi Perilaku yang Dimodulasi**: Transaksi harian dibuat menggunakan **Algoritma Keranjang Belanja**, di mana `adjustment_factor` secara aktif memengaruhi hasilnya:
           -   `jumlah_item_di_keranjang = round(jumlah_dasar * adjustment_factor)`
           -   Ini secara cerdas meningkatkan atau mengurangi volume dan nilai belanja harian untuk "menyetir" total kumulatif kembali ke jalur target.
-   **Output**: Sebagian besar dari daftar transaksi harian yang natural.

### Fase 3: Kalibrasi Final (`_run_final_calibration`)

Ini adalah langkah penjaminan kualitas untuk mencapai akurasi 100%.

-   **Input**: DataFrame dari semua transaksi yang telah dibuat dan `final_targets`.
-   **Proses**:
    -   Setelah loop harian selesai, mungkin masih ada sedikit selisih antara total yang dihasilkan dan target.
    -   Fungsi ini menghitung selisih akhir (`discrepancy`) untuk **setiap kategori**.
    -   Selisih ini kemudian didistribusikan dengan menambahkannya ke **transaksi dengan nominal terbesar** dalam kategori tersebut. Strategi ini efektif menyembunyikan penyesuaian kecil.
-   **Output**: DataFrame akhir yang totalnya per kategori sama persis dengan target.

---

## 8. Spesifikasi API Endpoint

Aplikasi ini berjalan pada dua endpoint Flask sederhana yang berkomunikasi melalui JSON.

### `POST /get-target`

-   **Deskripsi**: Mengambil data target finansial untuk satu periode (bulan/tahun) tertentu dari sumber data internal.
-   **URL**: `/get-target`
-   **Metode**: `POST`
-   **Request Body**:
    ```json
    {
      "year": 2024,
      "month": 9
    }
    ```
-   **Response 200 (OK)**:
    ```json
    {
      "Tanggal Laporan": "2024-09-30",
      "Belanja Bahan Baku (COGS)": 10452000.0,
      "Operasional|Gaji Pegawai": 4800000.0,
      "...": "..."
    }
    ```
-   **Response 404 (Not Found)**:
    ```json
    {
      "error": "Data target tidak ditemukan untuk periode yang dipilih."
    }
    ```

### `POST /generate-data`

-   **Deskripsi**: Memicu proses pembuatan data transaksi sintetis berdasarkan data target yang diberikan.
-   **URL**: `/generate-data`
-   **Metode**: `POST`
-   **Request Body**: Objek JSON lengkap yang diterima dari endpoint `/get-target`.
    ```json
    {
      "Tanggal Laporan": "2024-09-30",
      "Belanja Bahan Baku (COGS)": 10452000.0,
      "Operasional|Gaji Pegawai": 4800000.0,
      "...": "..."
    }
    ```
-   **Response 200 (OK)**: Sebuah array JSON yang berisi semua objek transaksi yang telah dibuat.
    ```json
    [
      {
        "ID_Transaksi": "TXN0001",
        "Tanggal_Transaksi": "2024-09-01",
        "Bulan": 9,
        "PIC": "SYSTEM",
        "Kategori_Utama": "Operasional",
        "Sub_Kategori": "Operasional|Sewa Tempat (Cadangan)",
        "Keterangan": "Alokasi Dana Cadangan Sewa",
        "Nominal": 2670000.0
      },
      {
        "ID_Transaksi": "TXN0002",
        "Tanggal_Transaksi": "2024-09-01",
        "Bulan": 9,
        "PIC": "SYSTEM",
        "Kategori_Utama": "Bahan Baku",
        "Sub_Kategori": "Belanja Bahan Baku (COGS)",
        "Keterangan": "pasar/gula/telur/susu/kopi/dampit",
        "Nominal": 345600.0
      }
    ]
    ```
-   **Response 400 (Bad Request)**:
    ```json
    {
      "error": "Data target tidak diterima."
    }
    ```
```

