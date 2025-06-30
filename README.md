
# 🛑 Drowsiness Detection System with YOLOv8

Deteksi dini **kantuk pada pengemudi kendaraan roda empat** sangat krusial dalam mencegah kecelakaan lalu lintas. Proyek ini mengimplementasikan teknologi **YOLOv8 (You Only Look Once)** untuk mendeteksi tanda-tanda kantuk seperti **durasi mata tertutup** dan **aktivitas menguap** pada wajah pengemudi secara real-time.

---

## 🎯 Tujuan Proyek

Membangun sistem pendeteksi kantuk berbasis *object detection* yang mampu:

* Mendeteksi apakah mata pengemudi tertutup dalam jangka waktu tertentu.
* Mendeteksi apakah pengemudi sedang menguap.
* Memberikan peringatan visual atau suara jika terindikasi kantuk.

---

## 🧠 Teknologi yang Digunakan

* **YOLOv8**: Model deteksi objek real-time untuk mengenali wajah, mata, dan mulut pengemudi.
* **OpenCV**: Untuk pemrosesan video dan pelacakan objek.
* **PyQt / Tkinter (opsional)**: Untuk tampilan antarmuka pengguna.
* **Python**: Bahasa pemrograman utama.

---

## 🗂️ Struktur Proyek

```
📦 Drowsiness-Detection-YOLOv8
├── pendeteksi.py      # Script utama logika pendeteksi kantuk
├── ui.py              # Tampilan antarmuka pengguna (GUI)
├── best.pt            # Model YOLOv8 terlatih
├── requirements.txt   # Daftar library yang dibutuhkan
└── README.md          # Dokumentasi proyek
```

---

## 🚀 Cara Menjalankan

### 1. Install Dependensi

```bash
pip install -r requirements.txt
```

### 2. Jalankan Deteksi (tanpa UI)

```bash
python pendeteksi.py
```

### 3. Jalankan dengan Antarmuka (UI)

```bash
python ui.py
```

> Pastikan kamera sudah terhubung dan berfungsi sebelum menjalankan aplikasi.

---

## 🎥 Cara Kerja Sistem

1. Kamera akan menangkap wajah pengemudi secara real-time.
2. Model YOLOv8 akan mendeteksi area mata dan mulut.
3. Jika mata terdeteksi tertutup selama beberapa frame berturut-turut → dianggap **mengantuk**.
4. Jika mulut terbuka lebar → dianggap **menguap**.
5. Sistem memberikan **peringatan dini** berupa suara atau tampilan visual.

---

## 📥 Unduh Versi Aplikasi (GUI)

Untuk mencoba versi aplikasi dengan antarmuka pengguna, kamu bisa mengunduhnya melalui Google Drive:

🔗 [Download Aplikasi Drowsiness Detection (GUI)](https://drive.google.com/file/d/12nDrbhIadqAtiteBY_NMHoSQBLZ3RBIJ/view?usp=sharing)

---

## 👨‍💻 Tim Pengembang

Proyek ini dikembangkan oleh tiga mahasiswa sebagai bagian dari eksplorasi dalam bidang *Computer Vision* dan *Keselamatan Berkendara*:

* **Reza Irwansyah Aryanto**
* **Nadya Adisti Cendana**
* **Namira Adzanya Yandhini**



