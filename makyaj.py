import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import threading
import time

class MakyajOyunu:
    def __init__(self, root):
        self.root = root
        self.root.title("Makyaj Yapma Oyunu")

        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        self.button = tk.Button(root, text="Fotoğraf Yükle", command=self.fotograf_yukle)
        self.button.pack()

        self.status_label = tk.Label(root, text="")
        self.status_label.pack()

        self.image = None
        self.tk_image = None

    def fotograf_yukle(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.image = Image.open(file_path).resize((400, 400))
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)
        self.status_label.config(text="Makyaj Başlıyor...")

        # Makyaj süreci başlat
        threading.Thread(target=self.makyaj_yap).start()

    def makyaj_yap(self):
        time.sleep(1)
        self.status_label.config(text="Pudra sürülüyor...")
        pudrali = self.image.filter(ImageFilter.SMOOTH_MORE)
        self.tk_image = ImageTk.PhotoImage(pudrali)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        time.sleep(5)
        self.status_label.config(text="Kapatıcı uygulanıyor...")
        kapaticili = pudrali.filter(ImageFilter.GaussianBlur(1.5))
        enhancer = ImageEnhance.Brightness(kapaticili)
        kapaticili = enhancer.enhance(1.1)  # biraz parlat

        self.tk_image = ImageTk.PhotoImage(kapaticili)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        time.sleep(14)
        self.status_label.config(text="Makyaj tamamlandı!")

        # 20 saniye sonra pencereyi kapat
        time.sleep(2)
        self.root.quit()

# Uygulamayı başlat
if __name__ == "__main__":
    root = tk.Tk()
    app = MakyajOyunu(root)
    root.mainloop()