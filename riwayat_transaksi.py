from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from temp import SoftButton, fonts
from db import get_all_transaksi
from db import delete_transaksi

class RiwayatTransaksiScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 24
        self.spacing = 24
        with self.canvas.before:
            Color(0.96, 0.97, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[32])
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Baris atas: tombol kembali + label Riwayat
        top_bar = BoxLayout(orientation="horizontal", size_hint_y=None, height=48, spacing=0)
        back_btn = SoftButton(
            text="<",
            size_hint=(None, None),
            size=(48, 48),
            font_size=24,
            font_name=fonts.Bold,
            background_color=(0.8, 0.9, 1, 1),
        )
        back_btn.bind(on_press=self.kembali)
        riwayat_label = Label(
            text="[b]Riwayat Transaksi[/b]",
            markup=True,
            size_hint=(1, 1),
            font_size=24,
            font_name=fonts.Bold,
            color=(0.2, 0.3, 0.4, 1),
            halign="center",
            valign="middle",
        )
        riwayat_label.bind(size=riwayat_label.setter("text_size"))
        top_bar.add_widget(back_btn)
        top_bar.add_widget(Widget())
        top_bar.add_widget(riwayat_label)
        top_bar.add_widget(Widget())
        self.add_widget(top_bar)

        # ScrollView untuk daftar transaksi
        self.scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=16, padding=[8, 8, 8, 8], size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.scroll.add_widget(self.grid)
        self.add_widget(self.scroll)

        self.tampilkan_riwayat()

    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def kembali(self, instance):
        app = App.get_running_app()
        app.home()

    def tampilkan_riwayat(self):
        self.grid.clear_widgets()
        riwayat = get_all_transaksi()
        if not riwayat:
            self.grid.add_widget(Label(text="Belum ada transaksi.", font_name=fonts.Regular, font_size=18, color=(0.3,0.3,0.3,1), size_hint_y=None, height=40))
            return

        # Header tabel
        header = BoxLayout(orientation="horizontal", size_hint_y=None, height=40, padding=[0,0,0,0], spacing=8)
        header.add_widget(Label(text="[b]Waktu Pemesanan[/b]", markup=True, font_name=fonts.Bold, font_size=16, color=(0.18,0.38,0.54,1), size_hint_x=0.22, halign="center", valign="middle"))
        header.add_widget(Label(text="[b]Pesanan[/b]", markup=True, font_name=fonts.Bold, font_size=16, color=(0.18,0.38,0.54,1), size_hint_x=0.38, halign="center", valign="middle"))
        header.add_widget(Label(text="[b]Harga[/b]", markup=True, font_name=fonts.Bold, font_size=16, color=(0.18,0.38,0.54,1), size_hint_x=0.18, halign="center", valign="middle"))
        header.add_widget(Label(text="[b]Tindakan[/b]", markup=True, font_name=fonts.Bold, font_size=16, color=(0.18,0.38,0.54,1), size_hint_x=0.18, halign="center", valign="middle"))
        self.grid.add_widget(header)

        for trx in riwayat:
            pesanan_str = "\n".join([f"{item['name']} x{item['qty']}" for item in trx['items']])
            # Hitung tinggi baris berdasarkan jumlah pesanan (min 60, per baris +20)
            pesanan_lines = pesanan_str.count("\n") + 1
            row_height = max(60, 24 + pesanan_lines * 22)
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=row_height, padding=[0,0,0,0], spacing=8)
            # Kolom waktu
            waktu = Label(text=trx['waktu'], font_name=fonts.Medium, font_size=14, color=(0.2,0.3,0.4,1), size_hint_x=0.22, halign="center", valign="middle")
            waktu.bind(size=waktu.setter("text_size"))
            row.add_widget(waktu)
            # Kolom pesanan (daftar item, multiline, wrap)
            pesanan = Label(text=pesanan_str, font_name=fonts.Regular, font_size=13, color=(0.2,0.3,0.4,1), size_hint_x=0.38, halign="center", valign="middle")
            pesanan.bind(size=lambda inst, val: setattr(inst, "text_size", (inst.width, None)))
            row.add_widget(pesanan)
            # Kolom harga (total)
            harga = Label(text=f"Rp {trx['total']:,}", font_name=fonts.Bold, font_size=14, color=(0.18,0.38,0.54,1), size_hint_x=0.18, halign="center", valign="middle")
            harga.bind(size=harga.setter("text_size"))
            row.add_widget(harga)
            # Kolom tindakan (hapus)
            tindakan_box = BoxLayout(orientation="vertical", size_hint_x=0.18, size_hint_y=1)
            btn_hapus = SoftButton(text="Hapus", size_hint_x=1, size_hint_y=None, height=60, font_size=13, background_color=(1,0.4,0.4,1))
            btn_hapus.bind(on_press=lambda inst, id=trx['id']: self.hapus_transaksi(id))
            tindakan_box.add_widget(Widget())  # Spacer atas
            tindakan_box.add_widget(btn_hapus)
            tindakan_box.add_widget(Widget())  # Spacer bawah
            row.add_widget(tindakan_box)
            self.grid.add_widget(row)

    def hapus_transaksi(self, transaksi_id):
        delete_transaksi(transaksi_id)
        self.tampilkan_riwayat() 