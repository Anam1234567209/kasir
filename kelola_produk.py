from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.spinner import Spinner
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.image import Image
import db
import os
import shutil

from temp import (
    SoftButton,
    SoftTextInput,
    fonts,
    SoftPopUp,
)


class KelolaProdukScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 24
        self.spacing = 18
        with self.canvas.before:
            Color(0.96, 0.97, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[32])
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Header
        header = BoxLayout(size_hint=(1, None), height=56, padding=[0, 0, 0, 0])
        back_btn = SoftButton(
            text="<",
            size_hint=(None, None),
            size=(48, 48),
            font_size=24,
            font_name=fonts.Bold,
            background_color=(0.8, 0.9, 1, 1),
        )
        back_btn.bind(on_press=self.kembali)
        header.add_widget(back_btn)
        header.add_widget(
            Label(
                text="[b]Kelola Produk[/b]",
                markup=True,
                font_size=24,
                font_name=fonts.Bold,
                color=(0.2, 0.3, 0.4, 1),
            )
        )
        header.add_widget(Widget())
        self.add_widget(header)

        # Form tambah/ubah produk
        form = BoxLayout(
            orientation="horizontal", size_hint=(1, None), height=60, spacing=12
        )
        self.nama_input = SoftTextInput(
            hint_text="Nama Produk", size_hint=(None, 1), width=180
        )
        self.harga_input = SoftTextInput(
            hint_text="Harga", input_filter="float", size_hint=(None, 1), width=100
        )
        self.gambar_input = SoftTextInput(
            hint_text="Path Gambar", size_hint=(None, 1), width=220
        )

        class RoundedSoftSpinner(BoxLayout):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.size_hint = (None, 1)
                self.width = 140
                self.padding = [8, 4, 8, 4]
                self.orientation = "vertical"
                with self.canvas.before:
                    Color(0.4, 0.85, 0.87, 1)  # soft cyan
                    self.bg = RoundedRectangle(
                        pos=self.pos, size=self.size, radius=[18]
                    )
                self.bind(pos=self.update_bg, size=self.update_bg)

                self.spinner = Spinner(
                    text="Makanan",
                    values=["Makanan", "Minuman"],
                    font_name=fonts.Bold,
                    background_color=(0, 0, 0, 0),
                    color=(0.18, 0.38, 0.54, 1),
                    font_size=18,
                    size_hint=(1, 1),
                    sync_height=True,
                )
                self.add_widget(self.spinner)

            def update_bg(self, *args):
                self.bg.pos = self.pos
                self.bg.size = self.size

            @property
            def text(self):
                return self.spinner.text

            @text.setter
            def text(self, value):
                self.spinner.text = value

        self.rounded_kategori = RoundedSoftSpinner()
        self.simpan_btn = SoftButton(text="Simpan", size_hint=(None, 1), width=100)
        self.simpan_btn.bind(on_press=self.simpan_produk)
        self.pilih_gambar_btn = SoftButton(
            text="Pilih",
            size_hint=(None, 1),
            width=110,
        )
        self.pilih_gambar_btn.bind(on_press=self.buka_file_chooser)
        form.add_widget(self.nama_input)
        form.add_widget(self.harga_input)
        form.add_widget(self.gambar_input)
        form.add_widget(self.pilih_gambar_btn)
        form.add_widget(self.rounded_kategori)
        form.add_widget(self.simpan_btn)
        self.add_widget(form)

        # Daftar produk
        self.scroll = ScrollView(size_hint=(1, 1))
        self.grid = GridLayout(
            cols=1, spacing=8, size_hint_y=None, padding=[0, 8, 0, 8]
        )
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.scroll.add_widget(self.grid)
        self.add_widget(self.scroll)

        self.selected_id = None
        self.load_produk()

    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def kembali(self, instance):
        App.get_running_app().home()

    def load_produk(self):
        self.grid.clear_widgets()
        produk_list = db.get_all_produk()
        for pid, nama, harga, gambar, kategori in produk_list:
            row = BoxLayout(
                orientation="horizontal", size_hint_y=None, height=64, spacing=8
            )
            row.add_widget(
                Label(
                    text=nama,
                    size_hint_x=0.22,
                    font_name=fonts.Regular,
                    font_size=16,
                    color=(0.2, 0.3, 0.4, 1),
                )
            )
            row.add_widget(
                Label(
                    text=kategori,
                    size_hint_x=0.13,
                    font_name=fonts.Regular,
                    font_size=14,
                    color=(0.25, 0.4, 0.6, 1),
                )
            )
            row.add_widget(
                Label(
                    text=f"Rp {harga:,.0f}",
                    size_hint_x=0.18,
                    font_name=fonts.Regular,
                    font_size=16,
                    color=(0.2, 0.3, 0.4, 1),
                )
            )
            # Tampilkan gambar sebagai preview
            if gambar and os.path.exists(gambar):
                img_widget = Image(
                    source=gambar,
                    size_hint_x=0.18,
                    size_hint_y=None,
                    height=48,
                    allow_stretch=True,
                    keep_ratio=True,
                )
            else:
                img_widget = Label(
                    text="-",
                    size_hint_x=0.18,
                    font_name=fonts.Regular,
                    font_size=13,
                    color=(0.4, 0.4, 0.4, 1),
                )
            row.add_widget(img_widget)
            edit_btn = SoftButton(
                text="Edit", size_hint_x=0.13, height=36, font_size=14
            )
            edit_btn.bind(
                on_press=lambda inst,
                pid=pid,
                nama=nama,
                harga=harga,
                gambar=gambar,
                kategori=kategori: self.edit_produk(pid, nama, harga, gambar, kategori)
            )
            hapus_btn = SoftButton(
                text="Hapus",
                size_hint_x=0.13,
                height=36,
                font_size=14,
                background_color=(1, 0.4, 0.4, 1),
            )
            hapus_btn.bind(on_press=lambda inst, pid=pid: self.hapus_produk(pid))
            row.add_widget(edit_btn)
            row.add_widget(hapus_btn)
            self.grid.add_widget(row)

    def simpan_produk(self, instance):
        nama = self.nama_input.text.strip()
        harga = self.harga_input.text.strip()
        gambar = self.gambar_input.text.strip()
        kategori = self.rounded_kategori.text
        if not nama or not harga or not kategori:
            SoftPopUp("Semua field harus diisi!").open()
            return
        try:
            harga = float(harga)
        except ValueError:
            SoftPopUp("Harga tidak valid!").open()
            return
        if self.selected_id:
            db.update_produk(
                self.selected_id,
                nama,
                harga,
                gambar if gambar else None,
                kategori,
            )
            SoftPopUp("Produk berhasil diubah!").open()
            self.selected_id = None
            self.simpan_btn.text = "Simpan"
        else:
            db.insert_produk(nama, harga, gambar if gambar else None, kategori)
            SoftPopUp("Produk berhasil ditambah!").open()
        self.nama_input.text = ""
        self.harga_input.text = ""
        self.gambar_input.text = ""
        self.rounded_kategori.text = "Makanan"
        self.load_produk()

    def edit_produk(self, pid, nama, harga, gambar, kategori):
        self.selected_id = pid
        self.nama_input.text = nama
        self.harga_input.text = str(harga)
        self.gambar_input.text = gambar or ""
        self.rounded_kategori.text = kategori
        self.simpan_btn.text = "Ubah"

    def hapus_produk(self, pid):
        db.delete_produk(pid)
        SoftPopUp("Produk berhasil dihapus!").open()
        self.load_produk()

    def buka_file_chooser(self, instance):
        layout = BoxLayout(orientation="vertical", spacing=8)
        start_dir = os.path.expanduser("~/Downloads")
        filechooser = FileChooserIconView(
            filters=["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif"], path=start_dir
        )
        layout.add_widget(filechooser)
        btn_pilih = SoftButton(text="Pilih", size_hint=(1, None), height=40)
        layout.add_widget(btn_pilih)
        popup = Popup(title="Pilih Gambar", content=layout, size_hint=(0.9, 0.9))

        def pilih_file(inst):
            if filechooser.selection:
                src_path = filechooser.selection[0]
                kategori = self.rounded_kategori.text  # "Makanan" atau "Minuman"
                # Pastikan folder tujuan ada
                dest_folder = os.path.join("kasir", "gambar", kategori)
                os.makedirs(dest_folder, exist_ok=True)
                # Nama file baru (bisa pakai nama asli atau diganti)
                filename = os.path.basename(src_path)
                dest_path = os.path.join(dest_folder, filename)
                # Jika file belum ada di tujuan, copy
                if not os.path.exists(dest_path):
                    shutil.copy(src_path, dest_path)
                # Simpan path relatif ke input gambar
                self.gambar_input.text = dest_path
                popup.dismiss()

        btn_pilih.bind(on_press=pilih_file)
        popup.open()
