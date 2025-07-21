from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.stencilview import StencilView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.core.image import Image as CoreImage
import datetime
import os
import json

from temp import (
    SoftButton,
    MinButton,
    SoftTextInput,
    fonts,
    SoftPopUp,
    SoftSpinner,
    SoftSpinnerOption,
    ImageButton,
)
from db import get_all_produk, insert_transaksi, get_cafe_profile

# import insert_transaksi
default_imports = [get_all_produk]
try:
    from db import insert_transaksi
except ImportError:
    pass

# File untuk menyimpan meja aktif
MEJA_AKTIF_FILE = "meja_aktif.json"


def reset_meja_aktif():
    try:
        with open(MEJA_AKTIF_FILE, "w") as f:
            json.dump([], f)
    except Exception as e:
        print(f"Gagal reset meja_aktif: {e}")


def save_meja_aktif(meja_aktif):
    try:
        with open(MEJA_AKTIF_FILE, "w") as f:
            json.dump(list(meja_aktif), f)
    except Exception as e:
        print(f"Gagal menyimpan meja_aktif: {e}")


def load_meja_aktif():
    try:
        with open(MEJA_AKTIF_FILE, "r") as f:
            return set(json.load(f))
    except Exception:
        return set()


class CategoryLabel(ButtonBehavior, Label):
    pass


class MenuImageBox(StencilView):
    def __init__(self, source, size=80, radius=18, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (size, size)
        with self.canvas:
            Color(1, 1, 1, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[36])
        self.img = Image(
            source=source,
            size_hint=(None, None),
            size=self.size,
            allow_stretch=True,
            keep_ratio=False,
        )
        self.add_widget(self.img)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.img.pos = self.pos
        self.img.size = self.size


class MenuTransaksiScreen(BoxLayout):
    def __init__(self, from_riwayat=False, selected_meja=None, **kwargs):
        super().__init__(**kwargs)
        self.from_riwayat = from_riwayat
        self.selected_meja = selected_meja
        self.orientation = "horizontal"
        self.padding = 24
        self.spacing = 24
        with self.canvas.before:
            Color(0.96, 0.97, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[32])
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Ambil produk dari database
        self.menu_items = []
        for pid, nama, harga, gambar, kategori in get_all_produk():
            self.menu_items.append(
                {
                    "name": nama,
                    "price": harga,
                    "image": (
                        gambar if gambar else "gambar/menu_makanan/ropang.jpg"
                    ),  # default jika kosong
                    "kategori": kategori,
                }
            )
        self.transaksi = []
        self.meja_aktif = load_meja_aktif()  # Set untuk menyimpan no meja aktif

        # LEFT: Menu list
        self.menu_layout = BoxLayout(
            orientation="vertical", size_hint=(0.6, 1), spacing=16
        )
        # Baris atas: tombol kembali + label Menu
        top_bar = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=48, spacing=0
        )
        back_btn = SoftButton(
            text="<",
            size_hint=(None, None),
            size=(48, 48),
            font_size=24,
            font_name="Poppins_Bold",
            background_color=(0.8, 0.9, 1, 1),
        )
        back_btn.bind(on_press=self.kembali)

        menu_label = Label(
            text="[b]Menu[/b]",
            markup=True,
            size_hint=(None, 1),
            # width=200,
            size_hint_x=None,  # Atur lebar sesuai kebutuhan, atau gunakan size_hint_x jika ingin lebih fleksibel
            font_size=24,
            font_name="Poppins_Bold",
            color=(0.2, 0.3, 0.4, 1),
            halign="center",
            valign="middle",
        )
        menu_label.bind(size=menu_label.setter("text_size"))

        # Spacer kanan agar label tetap di tengah
        spacer = Widget()

        top_bar.add_widget(back_btn)
        top_bar.add_widget(spacer)
        # top_bar.add_widget(Widget(size_hint_x=1))  # Spacer kiri
        top_bar.add_widget(menu_label)
        top_bar.add_widget(Widget(size_hint_x=1.2))  # Spacer kanan

        self.menu_layout.add_widget(top_bar)

        self.kategori_list = ["Makanan", "Sate-satean", "Minuman"]
        self.kategori_aktif = 0  # index kategori aktif

        # Kategori bar di tengah
        kategori_bar_container = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=40,
            padding=[0, 0, 0, 0],
            spacing=0,
        )
        kategori_bar = BoxLayout(
            orientation="horizontal",
            size_hint=(None, 1),
            height=40,
            spacing=82,
            pos_hint={"center_x": 0.5},
        )
        kategori_bar.width = (
            len(self.kategori_list) * 120 + (len(self.kategori_list) - 1) * 60
        )  # 120=lebar label, 24=spacing

        for i, kategori in enumerate(self.kategori_list):
            lbl = CategoryLabel(
                text=f"[u]{kategori}[/u]" if i == self.kategori_aktif else kategori,
                markup=True,
                font_size=18,
                font_name="Poppins_Medium",
                color=(
                    (0.2, 0.3, 0.4, 1)
                    if i == self.kategori_aktif
                    else (0.5, 0.5, 0.5, 1)
                ),
                size_hint=(None, 1),
                width=120,
                halign="center",
                valign="middle",
            )
            lbl.bind(on_press=lambda inst, idx=i: self.pilih_kategori(idx))
            kategori_bar.add_widget(lbl)

        kategori_bar_container.add_widget(Widget(size_hint_x=1))  # Spacer kiri
        kategori_bar_container.add_widget(kategori_bar)
        kategori_bar_container.add_widget(Widget(size_hint_x=1.5))  # Spacer kanan

        self.menu_layout.add_widget(kategori_bar_container)
        self.kategori_bar = kategori_bar

        self.scroll = ScrollView()
        self.grid = GridLayout(
            cols=4,
            spacing=24,
            padding=[8, 8, 8, 8],
            size_hint_y=None,
            size_hint_x=1,
        )
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.grid.bind(minimum_width=self.grid.setter("width"))
        self.scroll.add_widget(self.grid)
        self.menu_layout.add_widget(self.scroll)
        self.tampilkan_menu()

        # RIGHT: Transaksi info
        self.transaksi_layout = BoxLayout(
            orientation="vertical", size_hint=(0.6, 1), spacing=16
        )
        # Label transaksi yang dinamis berdasarkan sumber
        transaksi_label_text = "[b]Tambah Transaksi[/b]" if self.from_riwayat else "[b]Transaksi[/b]"
        self.transaksi_layout.add_widget(
            Label(
                text=transaksi_label_text,
                markup=True,
                size_hint_y=None,
                height=48,
                font_size=24,
                font_name="Poppins_Bold",
                color=(0.2, 0.3, 0.4, 1),
            )
        )

        self.daftar_pesanan = GridLayout(
            cols=1, spacing=8, size_hint_y=None, padding=[0, 8, 0, 8]
        )
        self.daftar_pesanan.bind(minimum_height=self.daftar_pesanan.setter("height"))
        self.scroll_transaksi = ScrollView(size_hint=(1, 0.5))
        self.scroll_transaksi.add_widget(self.daftar_pesanan)
        self.transaksi_layout.add_widget(self.scroll_transaksi)

        self.total_label = Label(
            text="Total: Rp 0",
            size_hint_y=None,
            height=20,
            font_size=15,
            font_name="Poppins_Bold",
            color=(0.2, 0.3, 0.4, 1),
        )
        self.kembalian_label = Label(
            text="Kembalian: Rp 0",
            size_hint_y=None,
            height=20,
            font_size=15,
            font_name="Poppins_Bold",
            color=(0.2, 0.3, 0.4, 1),
        )
        self.noMeja_label = Label(
            text="No Meja:",
            size_hint_y=None,
            height=32,
            font_size=15,
            font_name="Poppins_Bold",
            color=(0.2, 0.3, 0.4, 1),
            size_hint_x=None,
            width=70,
        )

        # Set no meja berdasarkan sumber
        initial_meja = str(self.selected_meja) if self.selected_meja else self.get_next_meja()
        self.noMeja_input = SoftSpinner(
            text=initial_meja,
            values=self.get_meja_options(),
            size_hint_y=None,
            height=32,
            size_hint_x=None,
            width=80,
            font_size=18,
            font_name="Poppins_Bold",
            background_color=(0.92, 0.96, 1, 0),
            color=(0.2, 0.3, 0.4, 1),
            option_cls=SoftSpinnerOption,
        )
        self.noMeja_input.bind(text=self.on_meja_selected)

        self.reset_btn = ImageButton(
            source="gambar/logo_icon/reset.png",
            size_hint=(None, 1),  # tambahkan ini
            size=(16, 16),
            allow_stretch=True,
            keep_ratio=True,
            on_press=lambda inst: self.reset_no_meja_manual(),
        )
        # reset_btn.bind()
        # self.transaksi_layout.add_widget(reset_btn)
        # bayar_btn.bind(on_press=self.bayar)

        no_meja_box = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=32, spacing=0, padding=0
        )
        no_meja_box.add_widget(Widget(size_hint_x=1))  # Spacer kiri
        no_meja_box.add_widget(self.noMeja_label)
        no_meja_box.add_widget(self.noMeja_input)
        no_meja_box.add_widget(self.reset_btn)
        no_meja_box.add_widget(Widget(size_hint_x=1))  # Spacer kanan

        self.transaksi_layout.add_widget(self.total_label)
        self.transaksi_layout.add_widget(self.kembalian_label)
        self.transaksi_layout.add_widget(no_meja_box)

        self.pembayaran_input = SoftTextInput(
            hint_text="Pembayaran",
            multiline=False,
            input_filter="int",
            size_hint_y=None,
            height=50,
            font_size=20,
            padding=[16, 12, 16, 12],
            background_color=(1, 1, 1, 0.8),
            foreground_color=(0.2, 0.3, 0.4, 1),
            font_name="Poppins",
        )
        self.transaksi_layout.add_widget(self.pembayaran_input)

        # Tombol BAYAR membulat
        bayar_btn = SoftButton(text="BAYAR", size_hint_y=None, height=54, font_size=20, font_name=fonts.Bold,)
        bayar_btn.bind(on_press=self.bayar)
        self.transaksi_layout.add_widget(bayar_btn)

        print_btn = SoftButton(text="PRINT", size_hint_y=None, height=54, font_size=20, font_name=fonts.Bold,)
        print_btn.bind(on_press=self.print)
        self.transaksi_layout.add_widget(print_btn)

        # Add both sections to main layout
        self.add_widget(self.menu_layout)
        self.add_widget(self.transaksi_layout)

        self.menu_layout.size_hint_x = 2.3
        self.transaksi_layout.size_hint_x = 1

        self.bind(on_touch_move=self.on_swipe_kategori)

    def kembali(self, instance):
        app = App.get_running_app()
        app.home()  # Pastikan fungsi open_home() ada di App Anda

    def pilih_kategori(self, idx):
        self.kategori_aktif = idx
        self.update_kategori_bar()
        self.tampilkan_menu()

    def update_kategori_bar(self):
        for i, lbl in enumerate(self.kategori_bar.children[::-1]):
            lbl.text = (
                f"[u]{self.kategori_list[i]}[/u]"
                if i == self.kategori_aktif
                else self.kategori_list[i]
            )
            lbl.color = (
                (0.2, 0.3, 0.4, 1) if i == self.kategori_aktif else (0.5, 0.5, 0.5, 1)
            )

    def on_swipe_kategori(self, instance, touch):
        if self.collide_point(*touch.pos):
            if abs(touch.dx) > 40:  # threshold swipe
                if touch.dx < 0 and self.kategori_aktif < len(self.kategori_list) - 1:
                    self.kategori_aktif += 1
                    self.update_kategori_bar()
                    self.tampilkan_menu()
                elif touch.dx > 0 and self.kategori_aktif > 0:
                    self.kategori_aktif -= 1
                    self.update_kategori_bar()
                    self.tampilkan_menu()

    def ganti_kategori(self, kategori):
        self.kategori_aktif = kategori
        self.tampilkan_menu()

    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def tampilkan_menu(self):
        self.grid.clear_widgets()
        kategori = self.kategori_list[self.kategori_aktif]
        self.grid.cols = 4
        self.grid.size_hint_x = 1
        self.grid.size_hint_y = None
        self.grid.padding = [10, 10, 10, 10]
        self.grid.spacing = 25
        from kivy.uix.floatlayout import FloatLayout
        from kivy.graphics import Color, RoundedRectangle

        class CardButton(ButtonBehavior, FloatLayout):
            def __init__(self, source, name, price, **kwargs):
                super().__init__(**kwargs)
                self.size_hint = (None, None)
                self.size = (160, 190)
                from kivy.uix.label import Label
                from kivy.graphics import Color, RoundedRectangle
                from kivy.core.image import Image as CoreImage

                # Gambar dan background dalam satu RoundedRectangle
                with self.canvas:
                    try:
                        tex = CoreImage(source).texture
                        Color(1, 1, 1, 1)
                        self.bg = RoundedRectangle(
                            pos=(self.x, self.y + self.height - 110),
                            size=(160, 140),
                            radius=[24],
                            texture=tex,
                        )
                    except Exception:
                        Color(0.95, 0.95, 0.95, 1)
                        self.bg = RoundedRectangle(
                            pos=(self.x, self.y + self.height - 110),
                            size=(160, 140),
                            radius=[24],
                        )
                self.bind(pos=self.update_bg, size=self.update_bg)
                # Overlay info di atas gambar (benar-benar overlay, satu info_box per kartu)
                info_box = FloatLayout(
                    size_hint=(1, None), height=44, pos_hint={"x": 0, "y": 0}
                )
                with info_box.canvas.before:
                    Color(1, 1, 1, 0)
                    info_box.bg = RoundedRectangle(
                        pos=info_box.pos, size=(160, 44), radius=[0, 0, 20, 20]
                    )

                def update_info_bg(inst, *args):
                    info_box.bg.pos = info_box.pos
                    info_box.bg.size = info_box.size

                info_box.bind(pos=update_info_bg, size=update_info_bg)
                # Nama
                name_label = Label(
                    text=f"[b]{name}[/b]",
                    markup=True,
                    font_size=15,
                    font_name="Poppins_Bold",
                    color=(0.18, 0.18, 0.18, 1),
                    size_hint=(1, None),
                    height=24,
                    pos_hint={"x": 0, "y": 0.45},
                    halign="center",
                    valign="middle",
                )
                name_label.bind(size=name_label.setter("text_size"))
                # Harga
                price_label = Label(
                    text=f"Rp {int(price):,}",
                    font_size=13,
                    font_name="Poppins",
                    color=(0.18, 0.18, 0.18, 1),
                    size_hint=(1, None),
                    height=18,
                    pos_hint={"x": 0, "y": 0},
                    halign="center",
                    valign="middle",
                )
                price_label.bind(size=price_label.setter("text_size"))
                info_box.add_widget(name_label)
                info_box.add_widget(price_label)
                self.add_widget(info_box)

            def update_bg(self, *args):
                self.bg.pos = (self.x, self.y + self.height - 140)
                self.bg.size = (160, 140)

        class RoundedImage(FloatLayout):
            def __init__(self, source, name, price, **kwargs):
                super().__init__(**kwargs)
                self.size_hint = (None, None)
                self.size = (160, 140)
                from kivy.uix.label import Label
                from kivy.uix.boxlayout import BoxLayout
                from kivy.graphics import Color, RoundedRectangle
                from kivy.uix.widget import Widget
                from kivy.metrics import dp

                try:
                    tex = CoreImage(source).texture
                    with self.canvas:
                        Color(1, 1, 1, 1)
                        self.img_rect = RoundedRectangle(
                            pos=self.pos, size=self.size, radius=[24], texture=tex
                        )
                except Exception:
                    with self.canvas:
                        Color(0.95, 0.95, 0.95, 1)
                        self.img_rect = RoundedRectangle(
                            pos=self.pos, size=self.size, radius=[24]
                        )
                self.bind(pos=self.update_img, size=self.update_img)
                # Overlay info di atas gambar (menumpuk di bawah)
                info_box = BoxLayout(
                    orientation="vertical",
                    size_hint=(1, None),
                    height=44,
                    pos_hint={"x": 0, "y": 0},
                    padding=[0, 0, 0, 0],
                    spacing=0,
                )
                with info_box.canvas.before:
                    Color(1, 1, 1, 0.85)
                    info_box.bg = RoundedRectangle(
                        pos=info_box.pos, size=(130, 44), radius=[0, 0, 20, 20]
                    )

                def update_info_bg(inst, *args):
                    info_box.bg.pos = info_box.pos
                    info_box.bg.size = info_box.size

                info_box.bind(pos=update_info_bg, size=update_info_bg)
                info_box.add_widget(
                    Label(
                        text=f"[b]{name}[/b]",
                        markup=True,
                        font_size=15,
                        font_name="Poppins_Bold",
                        color=(0.18, 0.18, 0.18, 1),
                        size_hint_y=None,
                        height=24,
                        halign="center",
                        valign="middle",
                    )
                )
                info_box.add_widget(
                    Label(
                        text=f"Rp {int(price):,}",
                        font_size=13,
                        font_name="Poppins",
                        color=(0.18, 0.18, 0.18, 1),
                        size_hint_y=None,
                        height=18,
                        halign="center",
                        valign="middle",
                    )
                )
                self.add_widget(info_box)

            def update_img(self, *args):
                self.img_rect.pos = self.pos
                self.img_rect.size = self.size

        # Hitung tinggi grid agar responsif
        count = 0
        for item in self.menu_items:
            if item["kategori"] != kategori:
                continue
            card = CardButton(item["image"], item["name"], item["price"])
            card.bind(on_press=lambda inst, i=item: self.tambah_transaksi(i))
            self.grid.add_widget(card)
            count += 1
        # Atur tinggi grid agar cukup untuk semua baris
        baris = (count + self.grid.cols - 1) // self.grid.cols
        self.grid.height = (
            baris * 170 + (baris - 1) * self.grid.spacing[1] if count else 0
        )

    def tambah_transaksi(self, item):
        for t in self.transaksi:
            if t["name"] == item["name"]:
                t["qty"] += 1
                break
        else:
            self.transaksi.append(
                {"name": item["name"], "price": item["price"], "qty": 1}
            )
        self.update_transaksi()

    def kurang_transaksi(self, item):
        for t in self.transaksi:
            if t["name"] == item["name"]:
                t["qty"] -= 1
                if t["qty"] <= 0:
                    self.transaksi.remove(t)
                break
        self.update_transaksi()

    def update_transaksi(self):
        self.daftar_pesanan.clear_widgets()
        total = 0
        for item in self.transaksi:
            row = BoxLayout(
                orientation="horizontal", size_hint_y=None, height=32, spacing=8
            )
            label = Label(
                text=(
                    f'{item["name"]} - Rp {item["price"]:,} x{item["qty"]}'
                    if item["qty"] > 1
                    else f'{item["name"]} - Rp {item["price"]:,}'
                ),
                size_hint_x=0.8,
                font_name="Poppins",
                font_size=16,
                color=(0.2, 0.3, 0.4, 1),
                halign="left",
                valign="middle",
            )
            label.bind(size=label.setter("text_size"))
            btn_kurang = MinButton(
                text="-",
                size_hint_x=0.1,
                height=10,
                font_size=18,
                background_color=(1, 0.6, 0.6, 1),
            )
            btn_kurang.bind(on_press=lambda inst, i=item: self.kurang_transaksi(i))
            row.add_widget(label)
            row.add_widget(btn_kurang)
            self.daftar_pesanan.add_widget(row)
            total += item["price"] * item["qty"]
        self.total_label.text = f"Total: Rp {total:,}"

    def get_next_meja(self):
        terpakai = self.meja_aktif
        if len(terpakai) >= 50:
            # Jika sudah penuh, reset meja aktif
            self.meja_aktif.clear()
            save_meja_aktif(self.meja_aktif)
            reset_meja_aktif()
            return "1"
        for i in range(1, 51):
            if i not in terpakai:
                return f"{i}"
        return "1"

    def get_meja_options(self):
        terpakai = self.meja_aktif
        current = self.noMeja_input.text if hasattr(self, "noMeja_input") else None
        # options = [str(i) for i in range(1, 51) if i not in terpakai or str(i) == current]
        if len(terpakai) >= 50:
            # Jika sudah penuh, reset
            self.meja_aktif.clear()
            save_meja_aktif(self.meja_aktif)
            reset_meja_aktif()
            return [str(i) for i in range(1, 51)]
        return [str(i) for i in range(1, 51) if i not in terpakai or str(i) == current]

    def on_meja_selected(self, instance, value):
        # Tidak perlu validasi int, Spinner hanya berisi angka valid
        pass

    def get_meja_aktif(self):
        # Implementasi: return list nomor meja yang sedang aktif/transaksi berjalan
        # Contoh dummy:
        return list(self.meja_aktif)

    def reset_no_meja_manual(self):
        self.meja_aktif.clear()
        save_meja_aktif(self.meja_aktif)
        reset_meja_aktif()
        self.noMeja_input.values = self.get_meja_options()
        self.noMeja_input.text = self.get_next_meja()

    def bayar(self, instance):
        pembayaran = int(self.pembayaran_input.text or 0)
        total = sum(item["price"] * item["qty"] for item in self.transaksi)
        kembalian = pembayaran - total if pembayaran >= total else 0
        self.kembalian_label.text = f"Kembalian: Rp {kembalian:,}"

        content = BoxLayout(orientation="vertical", padding=18, spacing=12)

        if pembayaran < total:
            popup = SoftPopUp("Pembayaran gagal, uang tidak cukup.")
            popup.open()
        else:
            # Simpan transaksi ke database
            waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                no_meja = int(self.noMeja_input.text)
                # Tandai transaksi jika berasal dari riwayat
                if self.from_riwayat:
                    # Tambahkan tanda khusus untuk transaksi dari riwayat
                    insert_transaksi(
                        waktu, no_meja, total, pembayaran, kembalian, self.transaksi, from_riwayat=True
                    )
                else:
                    insert_transaksi(
                        waktu, no_meja, total, pembayaran, kembalian, self.transaksi
                    )
                self.meja_aktif.add(no_meja)
                save_meja_aktif(self.meja_aktif)
                # Update pilihan Spinner setelah pembayaran
                self.noMeja_input.values = self.get_meja_options()
                self.noMeja_input.text = self.get_next_meja()
            except Exception as e:
                popup = SoftPopUp(f"Gagal menyimpan transaksi: {e}")
                popup.open()
                return
            popup = SoftPopUp("Pembayaran berhasil!")
            popup.open()

    def print(self, instance):
        pesanan = self.transaksi
        total = sum(item["price"] * item["qty"] for item in pesanan)
        pembayaran = int(self.pembayaran_input.text or 0)
        kembalian = pembayaran - total if pembayaran >= total else 0

        waktu = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transaksi_{waktu}.pdf"
        folder = "print_transaksi"
        if not os.path.exists(folder):
            os.makedirs(folder)
        filepath = os.path.join(folder, filename)

        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4
        y = height - 50

        # Get cafe profile data
        cafe_profile = get_cafe_profile()

        # Header section with cafe profile
        c.setFont("Helvetica-Bold", 24)
        cafe_name = cafe_profile["nama_cafe"] if cafe_profile else "WAROENG CAFE"
        c.drawString(40, y, cafe_name)
        y -= 30

        # c.setFont("Helvetica", 14)
        # slogan = (
        #     cafe_profile["slogan"]
        #     if cafe_profile
        #     else "Nikmati Kelezatan dalam Setiap Gigitan"
        # )
        # c.drawString(50, y, slogan)
        # y -= 25

        c.setFont("Helvetica", 10)
        alamat = (
            cafe_profile["alamat_cafe"]
            if cafe_profile
            else "Jl. Contoh No. 123, Kota, Provinsi"
        )
        c.drawString(50, y, alamat)
        y -= 15

        email = cafe_profile["email_cafe"] if cafe_profile else "info@waroengcafe.com"
        c.drawString(50, y, email)
        y -= 15

        phone = cafe_profile["no_hp_cafe"] if cafe_profile else "+62 812-3456-7890"
        c.drawString(50, y, phone)
        y -= 25

        # Divider line
        c.line(50, y, width - 50, y)
        y -= 25

        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, y, "Transaksi")
        y -= 40

        # Tampilkan no meja
        c.setFont("Helvetica", 12)
        no_meja_text = self.noMeja_input.text
        if self.from_riwayat:
            c.drawString(50, y, f"No Meja: {no_meja_text}+ (Tambah Transaksi)")
        else:
            c.drawString(50, y, f"No Meja: {no_meja_text}")
        y -= 20

        c.setFont("Helvetica", 12)
        c.drawString(
            50, y, f"Waktu: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        )
        y -= 30

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Daftar Pesanan:")
        y -= 25

        c.setFont("Helvetica", 12)
        total_items = sum(item['qty'] for item in pesanan)
        c.drawString(60, y, f"Total Item: {total_items}")
        y -= 20

        for item in pesanan:
            c.drawString(
                60, y, f"- {item['name']}   Rp {item['price']:,} x{item['qty']}"
            )
            y -= 20

        y -= 10
        # Garis pemisah
        c.line(50, y, width - 50, y)
        y -= 20
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Total      : Rp {total:,}")
        y -= 20
        c.drawString(50, y, f"Pembayaran : Rp {pembayaran:,}")
        y -= 20
        c.drawString(50, y, f"Kembalian  : Rp {kembalian:,}")

        y -= 30
        # Footer
        c.setFont("Helvetica", 10)
        c.drawString(50, y, "Terima kasih telah berkunjung!")
        y -= 15
        c.drawString(50, y, "Silakan datang kembali")

        c.save()

        popup = SoftPopUp(message=f"PDF berhasil dibuat:\n{filename}")
        popup.open()

        # Reset transaksi setelah print
        self.transaksi = []
        self.pembayaran_input.text = ""
        self.kembalian_label.text = "Kembalian: Rp 0"
        self.total_label.text = "Total: Rp 0"
        try:
            no_meja = int(self.noMeja_input.text)
            # self.meja_aktif.discard(no_meja)
            # save_meja_aktif(self.meja_aktif)
            # Jangan reset values spinner di sini!
            # self.noMeja_input.values = self.get_meja_options()
            # self.noMeja_input.text = self.get_next_meja()
        except Exception:
            pass
        self.update_transaksi()
