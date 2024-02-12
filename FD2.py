import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import os

class FonDunyasi(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FonDünyası v2.0")
        self.geometry("400x300")
        self.output_format_var = tk.StringVar(value='png')
        self.image_resize_var = tk.StringVar(value='1792x1024')

        self.filigran_yolu = "filigran.png"
        self.ek_filigran_yolu = "logo.png"
        self.filigran_kullan = tk.BooleanVar(value=True)
        self.ek_filigran_kullan = tk.BooleanVar(value=False)
        self.image_resize = tk.BooleanVar(value=False)

        # Initialize the progress bar before setting up the UI
        self.progress = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=250, mode='determinate')
        
        self.arayuzu_ayarla()

    def arayuzu_ayarla(self):
        ttk.Label(self, text="Seçenekler:").pack(pady=10)

        ttk.Checkbutton(self, text="Varsayılan filigranı kullan", variable=self.filigran_kullan, onvalue=True, offvalue=False).pack(anchor=tk.W, padx=10)
        ttk.Checkbutton(self, text="Logo kullan", variable=self.ek_filigran_kullan, onvalue=True, offvalue=False).pack(anchor=tk.W, padx=10)
        ttk.Checkbutton(self, text="Görseli yeniden boyutlandır", variable=self.image_resize, onvalue=True, offvalue=False).pack(anchor=tk.W, padx=10)
        etiketler_ve_comboboxlar = [
            ("Çıkış Formatı:", self.output_format_var, ['png', 'psd', 'gif', 'jpg', 'jpeg', 'pdf', 'bmp', 'tiff', 'mkv', 'ico', 'mpeg']),
            ("Resim Boyutları:", self.image_resize_var, ['720x480', '800x600', '1024x768', '1024x1024', '1280x720', '1360x768', '1366x768', '1600x1200', '1792x1024', '1920x1080', '2048x1080', '2048x1536', '2560x1440', '3840x2160', '7680x4320'])
        ]
        for metin, var, degerler in etiketler_ve_comboboxlar:
            etiket = ttk.Label(self, text=metin)
            etiket.pack(pady=5)
            combobox = ttk.Combobox(self, textvariable=var, values=degerler, state="readonly")
            combobox.pack(pady=5)

        ttk.Button(self, text="Görseli Seç ve Dönüştür", command=self.resim_sec_ve_filigran_ekle).pack(pady=10)
        self.progress.pack(pady=20)  # This will now work as self.progress is already defined


    def resim_sec_ve_filigran_ekle(self):
        dosya_yolları = filedialog.askopenfilenames(title='Resim(ler) Seçin')

        if not dosya_yolları:
            messagebox.showinfo("Bilgi", "Görsel seçilmedi.")
            return

        self.progress['maximum'] = len(dosya_yolları)
        basarili_islem_sayisi = 0

        for index, dosya_yolu in enumerate(dosya_yolları):
            try:
                if self.filigran_kullan.get():
                    self.filigran_ekle(dosya_yolu, self.filigran_yolu)
                elif self.ek_filigran_kullan.get():
                    self.filigran_ekle(dosya_yolu, self.ek_filigran_yolu, "_logo")
                else:
                    self.filigran_ekle(dosya_yolu, None, "_")
                    self
                basarili_islem_sayisi += 1
            except Exception as e:
                messagebox.showerror("Hata", f"{dosya_yolu} işlenirken bir hata oluştu: {e}")
            finally:
                self.progress['value'] = index + 1
                self.update_idletasks()  # Update the progress bar

        messagebox.showinfo("Başarılı", f"İşlem başarıyla tamamlandı. {basarili_islem_sayisi} adet resim işlendi.")
        self.progress['value'] = 0  # Reset the progress bar for the next operation

        if dosya_yolları:
            son_dosya_yolu = os.path.dirname(dosya_yolları[-1])
            os.startfile(son_dosya_yolu)

    def ayarla_filigran_rengi(self, filigran):
        """Filigran rengini ve opaklığını ayarla."""
        sonuc = filigran.copy()  # Orijinalini korumak için bir kopya oluştur
        veriler = sonuc.getdata()

        yeni_veriler = []
        for item in veriler:
            if item[3] != 0:  # Alfa değeri 0 olmayan pikseller için
                yeni_veriler.append((180, 180, 180, int(item[3] * 0.4)))  # Opaklığı %40'a ayarla
            else:
                yeni_veriler.append(item)  # Tamamen şeffaf pikselleri koru

        sonuc.putdata(yeni_veriler)
        return sonuc

    def filigran_ekle(self, resim_yolu, filigran_yolu, eki="_fil"):
        resim = Image.open(resim_yolu).convert("RGBA")
        if self.image_resize.get():
            size = tuple(map(int, self.image_resize_var.get().split("x")))
            resim = resim.resize(size, Image.Resampling.LANCZOS)
        cikti_dosya_yolu = f"{os.path.splitext(resim_yolu)[0]}{eki}.{self.output_format_var.get()}"
        if filigran_yolu:
            filigran = Image.open(filigran_yolu).convert("RGBA")
            filigran = self.ayarla_filigran_rengi(filigran)  # Filigran rengini ve opaklığını ayarla
        
            filigran_boyutlandirilmis = filigran.resize(resim.size, Image.Resampling.LANCZOS)
            filigranli_resim = Image.alpha_composite(resim, filigran_boyutlandirilmis)
            filigranli_resim.save(cikti_dosya_yolu, format=self.output_format_var.get())
        else:
            resim.save(cikti_dosya_yolu, format=self.output_format_var.get())
        
if __name__ == "__main__":
    uygulama = FonDunyasi()
    uygulama.mainloop()
