import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pendeteksi import DrowsinessDetector
import cv2
import os
import sys

class App:
    def __init__(self, root):
        self.root = root
        self.detector = None
        self.detection_active = False

        # UI setup
        self.root.title("Aplikasi Pendeteksi Kantuk")
        self.root.geometry("800x400") 
        self.root.resizable(False, False)

        # Warna latar belakang gelap
        self.bg_color = "#2C2F33"
        self.text_color = "#FFFFFF"

        # Frame kiri untuk gambar (video frame)
        self.frame_left = tk.Frame(root, width=600, height=400, bg=self.bg_color)  # Frame for video output
        self.frame_left.pack(side="left", fill="both", expand=True)

        # Menambahkan gambar di frame kiri
        try:
            image_path = self.resource_path("ngantuk.jpg")
            image = Image.open(image_path)
            image = image.resize((500, 400), Image.Resampling.LANCZOS)
            self.img = ImageTk.PhotoImage(image)
            label_image = tk.Label(self.frame_left, image=self.img, bg=self.bg_color)
            label_image.pack()
        except Exception as e:
            print(f"Error: {e}")
            label_image = tk.Label(self.frame_left, text="Gambar tidak tersedia", bg=self.bg_color, fg=self.text_color)
            label_image.pack(expand=True)

        # Frame kanan untuk teks dan tombol
        self.frame_right = tk.Frame(root, width=400, height=500, bg=self.bg_color)  # Right frame for text and buttons
        self.frame_right.pack(side="right", fill="both", expand=True)

        # Menambahkan teks di frame kanan
        self.label_welcome = tk.Label(self.frame_right, text="Selamat Datang di\nAplikasi Pendeteksi Kantuk", 
                                      font=("Helvetica Neue", 16, "bold"), bg=self.bg_color, fg=self.text_color)
        self.label_welcome.pack(pady=50)

        # Menambahkan tombol Start Detection
        self.btn_start = tk.Button(self.frame_right, text="Start Detection", font=("Helvetica Neue", 12), 
                                   command=self.initialize_detector, bg="green", fg="white")
        self.btn_start.pack(pady=10)

        # Menambahkan tombol Exit
        self.btn_exit = tk.Button(self.frame_right, text="Exit", font=("Helvetica Neue", 12), 
                                  command=self.stop_program, bg="red", fg="white")
        self.btn_exit.pack(pady=10)

        # Frame untuk deteksi
        self.main_frame = tk.Frame(root)
        self.label = tk.Label(self.main_frame)
        self.label.pack()

        # Initialize the instruction label and buttons
        self.instruction_label = tk.Label(self.main_frame, text="Klik 'Start Detection' untuk memulai", 
                                           font=("Helvetica Neue", 14), pady=20)
        self.instruction_label.pack()
        self.start_button = tk.Button(self.main_frame, text="Start Detection", command=self.start_detection, 
                                       font=("Helvetica Neue", 14))
        self.start_button.pack(pady=10)
        self.exit_button = tk.Button(self.main_frame, text="Exit", command=self.stop_program, 
                                      font=("Helvetica Neue", 14))
        self.exit_button.pack(pady=10)

    def resource_path(self, relative_path):
        # Mendapatkan path ke file resource, baik saat di development atau saat di build dengan PyInstaller.
        
        if hasattr(sys, '_MEIPASS'):  # Jika aplikasi dijalankan sebagai executable
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def initialize_detector(self):
        #Initialize the drowsiness detector with the default integrated model.
        try:
            self.detector = DrowsinessDetector()
            messagebox.showinfo("Success", "Model berhasil dimuat! Memulai deteksi.")

            # Menghilangkan Tombol dan Tulisan dihalaman awal
            self.frame_left.pack_forget()
            self.frame_right.pack_forget()
            self.instruction_label.pack_forget()
            self.start_button.pack_forget()
            self.exit_button.pack_forget()

            # Mengubah warna backgroung menjadi lebih gelap
            self.bg_color = "#2C2F33"  
            self.root.configure(bg=self.bg_color)

            # Memperbaharui ukuran Window menjadi lebih besar
            self.root.geometry("1000x600")  

            # Memunculkan Deteksi
            self.main_frame.pack(fill="both", expand=True)

            # Label for displaying video frames
            self.label = tk.Label(self.main_frame)
            self.label.pack()

            # Memunculkan Tombol Exit ketika Pendeteksian Berjalan
            self.exit_button_during_detection = tk.Button(self.main_frame, text="Exit", command=self.stop_program, 
                                                           font=("Helvetica Neue", 16), bg="red", fg="white")
            self.exit_button_during_detection.pack(pady=20)

            # Memulai Deteksi
            self.start_detection() 

        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat model: {e}")

    def start_detection(self):
        # Memulai Deteksi
        if self.detector:
            self.detection_active = True
            self.update_frame()

    def update_frame(self):
        # Update video frames
        if not self.detection_active:
            return
        frame, warning_message = self.detector.process_frame()
        
        if frame is not None:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            tk_image = ImageTk.PhotoImage(pil_image)
            self.label.config(image=tk_image)
            self.label.image = tk_image
        self.root.after(10, self.update_frame)

    def stop_program(self):
        # Menutup Aplikasi
        if self.detector:
            self.detector.release()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
