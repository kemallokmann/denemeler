import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import threading
import time

class MakyajOyunu:
    def __init__(self, root):
        self.root = root
        self.root.title("💄 Makyaj Oyunu")
        self.root.geometry("600x500")
        self.root.configure(bg="light pink")

        self.label = tk.Label(root, text="Fotoğraf yükleyin ve makyaja başlayın!", bg="light pink", font=("Arial", 14))
        self.label.pack(pady=10)

        self.load_button = tk.Button(root, text="📷 Fotoğraf Yükle", command=self.fotograf_yukle)
        self.load_button.pack()

        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.pack(pady=10)

        # Makyaj seçenekleri
        self.ruj_button = tk.Button(root, text="💋 Ruj Sür", command=lambda: self.makyaj_uygula("Ruj"))
        self.eyeliner_button = tk.Button(root, text="👁️ Eyeliner Sür", command=lambda: self.makyaj_uygula("Eyeliner"))
        self.allik_button = tk.Button(root, text="🌸 Allık Sür", command=lambda: self.makyaj_uygula("Allık"))
        self.palet_button = tk.Button(root, text="🎨 Palet Uygula", command=lambda: self.makyaj_uygula("Palet"))

        for btn in [self.ruj_button, self.eyeliner_button, self.allik_button, self.palet_button]:
            btn.pack(pady=3)

        self.finish_label = tk.Label(root, text="", font=("Arial", 16), fg="dark red", bg="light pink")
        self.finish_label.pack(pady=10)

    def fotograf_yukle(self):
        file_path = filedialog.askopenfilename(filetypes=[("Görseller", "*.png *.jpg *.jpeg")])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((300, 300))
            self.photo = ImageTk.PhotoImage(image)
            self.canvas.create_image(150, 150, image=self.photo)
            self.label.config(text="Fotoğraf yüklendi. Makyaj yapmaya başlayın!")
            # Başlatma zamanlayıcısı
            threading.Thread(target=self.otomatik_kapat, daemon=True).start()

    def makyaj_uygula(self, tur):
        self.finish_label.config(text=f"{tur} uygulandı!")

    def otomatik_kapat(self):
        for i in range(20, 0, -1):
            self.label.config(text=f"Makyaj bitiyor: {i} saniye kaldı...")
            time.sleep(1)
        self.label.config(text="💄 Makyaj Bitti! 💋")
        time.sleep(3)
        self.root.quit()

# Uygulama başlat
if __name__ == "__main__":
    root = tk.Tk()
    app = MakyajOyunu(root)
    root.mainloop()