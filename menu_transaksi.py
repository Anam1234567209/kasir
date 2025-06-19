from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
import datetime
import os

from temp import SoftButton
from temp import SoftTextInput
from temp import fonts
from temp import SoftPopUp


class CategoryLabel(ButtonBehavior, Label):
    pass


class MinButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)  # Background transparan
        self.color = (0.2, 0.3, 0.4, 1)  # Warna teks
        self.font_name = "Poppins_Bold"
        with self.canvas.before:
            Color(0.4, 0.85, 0.87, 1)  # Warna stroke (biru soft)
            self.outline = Line(
                width=1.3,
                rounded_rectangle=[self.x, self.y, self.width, self.height, 18],
            )
        self.bind(pos=self.update_outline, size=self.update_outline)

    def update_outline(self, *args):
        self.outline.rounded_rectangle = [self.x, self.y, self.width, self.height, 18]


class RoundedImage(Widget):
    def __init__(self, source, size=(80, 80), radius=18, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = size
        with self.canvas:
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[radius])
        self.img = Image(
            source=source,
            size_hint=(None, None),
            size=self.size,
            allow_stretch=True,
            keep_ratio=True,
        )
        self.add_widget(self.img)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.img.pos = self.pos
        self.img.size = self.size


class MenuTransaksiScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.padding = 24
        self.spacing = 24
        with self.canvas.before:
            Color(0.96, 0.97, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[32])
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.menu_items = [
            {
                "name": "Ammericano Coffee",
                "price": 25000,
                "image": "gambar/menu_minuman/americano.jpg",
                "kategori": "Minuman",
            },
            {
                "name": "Cappucino Coffee",
                "price": 20000,
                "image": "gambar/menu_minuman/cappucino.jpg",
                "kategori": "Minuman",
            },
            {
                "name": "Matcha",
                "price": 10000,
                "image": "gambar/menu_minuman/matcha.jpg",
                "kategori": "Minuman",
            },
            {
                "name": "Roti Panggang",
                "price": 5000,
                "image": "gambar/menu_makanan/ropang.jpg",
                "kategori": "Makanan",
            },
            {
                "name": "Pizza Mini",
                "price": 5000,
                "image": "gambar/menu_makanan/mini_pizza.jpg",
                "kategori": "Makanan",
            },
        ]
        self.transaksi = []

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
            size_hint_x=0.5,  # Atur lebar sesuai kebutuhan, atau gunakan size_hint_x jika ingin lebih fleksibel
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
        top_bar.add_widget(menu_label)
        top_bar.add_widget(Widget())  # Spacer kanan

        self.menu_layout.add_widget(top_bar)

        self.kategori_list = ["Makanan", "Minuman"]
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
            len(self.kategori_list) * 120 + (len(self.kategori_list) - 1) * 24
        )  # 120=lebar label, 24=spacing

        for i, kategori in enumerate(self.kategori_list):
            lbl = CategoryLabel(
                text=f"[u]{kategori}[/u]" if i == self.kategori_aktif else kategori,
                markup=True,
                font_size=18,
                color=(0.2, 0.3, 0.4, 1)
                if i == self.kategori_aktif
                else (0.5, 0.5, 0.5, 1),
                size_hint=(None, 1),
                width=120,
                halign="center",
                valign="middle",
            )
            lbl.bind(on_press=lambda inst, idx=i: self.pilih_kategori(idx))
            kategori_bar.add_widget(lbl)

        kategori_bar_container.add_widget(Widget(size_hint_x=1))  # Spacer kiri
        kategori_bar_container.add_widget(kategori_bar)
        kategori_bar_container.add_widget(Widget(size_hint_x=1))  # Spacer kanan

        self.menu_layout.add_widget(kategori_bar_container)
        self.kategori_bar = kategori_bar

        self.scroll = ScrollView()
        self.grid = GridLayout(
            cols=1, spacing=16, size_hint_y=None, padding=[0, 8, 0, 8]
        )
        self.grid.bind(minimum_height=self.grid.setter("height"))
        self.scroll.add_widget(self.grid)
        self.menu_layout.add_widget(self.scroll)
        self.tampilkan_menu()

        # RIGHT: Transaksi info
        self.transaksi_layout = BoxLayout(
            orientation="vertical", size_hint=(0.6, 1), spacing=16
        )
        self.transaksi_layout.add_widget(
            Label(
                text="[b]Transaksi[/b]",
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
            height=36,
            font_size=18,
            font_name="Poppins_Bold",
            color=(0.2, 0.3, 0.4, 1),
        )
        self.kembalian_label = Label(
            text="Kembalian: Rp 0",
            size_hint_y=None,
            height=36,
            font_size=18,
            font_name="Poppins_Bold",
            color=(0.2, 0.3, 0.4, 1),
        )
        self.transaksi_layout.add_widget(self.total_label)
        self.transaksi_layout.add_widget(self.kembalian_label)

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
        bayar_btn = SoftButton(text="BAYAR", size_hint_y=None, height=54, font_size=20)
        bayar_btn.bind(on_press=self.bayar)
        self.transaksi_layout.add_widget(bayar_btn)

        print_btn = SoftButton(text="PRINT", size_hint_y=None, height=54, font_size=20)
        print_btn.bind(on_press=self.print)
        self.transaksi_layout.add_widget(print_btn)

        # Add both sections to main layout
        self.add_widget(self.menu_layout)
        self.add_widget(self.transaksi_layout)

        self.menu_layout.size_hint_x = 2
        self.transaksi_layout.size_hint_x = 1

        self.bind(on_touch_move=self.on_swipe_kategori)

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

    def kembali(self, instance):
        app = App.get_running_app()
        app.home()  # Pastikan fungsi open_home() ada di App Anda

    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def tampilkan_menu(self):
        self.grid.clear_widgets()
        kategori = self.kategori_list[self.kategori_aktif]
        for item in self.menu_items:
            if item["kategori"] != kategori:
                continue
            row = BoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=110,
                padding=8,
                spacing=12,
            )
            with row.canvas.before:
                Color(0.92, 0.96, 1, 1)
                row.bg_rect = RoundedRectangle(pos=row.pos, size=row.size, radius=[18])
            row.bind(
                pos=lambda i, v: setattr(i.bg_rect, "pos", v),
                size=lambda i, v: setattr(i.bg_rect, "size", v),
            )
            # Gambar menu
            img_box = BoxLayout(size_hint=(None, None), size=(80, 80))
            img = RoundedImage(
                source=item["image"],
                size_hint=(1, 1),  # Mengisi penuh img_box
            )
            img_box.add_widget(img)
            row.add_widget(img_box)
            # Info
            info = BoxLayout(orientation="vertical", size_hint_x=0.5, spacing=2)
            info.add_widget(
                Label(
                    text=item["name"],
                    font_name="Poppins",
                    font_size=18,
                    color=(0.2, 0.3, 0.4, 1),
                )
            )
            info.add_widget(
                Label(
                    text=f'Rp {item["price"]:,}',
                    font_name="Poppins",
                    font_size=15,
                    color=(0.3, 0.4, 0.5, 1),
                )
            )
            row.add_widget(info)
            # Tombol Tambah & Kurangi dalam satu BoxLayout vertikal
            btn_box = BoxLayout(orientation="vertical", size_hint_x=0.28, spacing=6)
            btn_tambah = SoftButton(text="Tambah", font_size=16, height=44)
            btn_tambah.bind(on_press=lambda instance, i=item: self.tambah_transaksi(i))
            btn_kurang = MinButton(text="Kurangi", font_size=16, height=36)
            btn_kurang.bind(on_press=lambda instance, i=item: self.kurang_transaksi(i))
            btn_box.add_widget(btn_tambah)
            btn_box.add_widget(btn_kurang)
            row.add_widget(btn_box)
            self.grid.add_widget(row)

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
            label = Label(
                text=f'{item["name"]} - Rp {item["price"]:,} x{item["qty"]}'
                if item["qty"] > 1
                else f'{item["name"]} - Rp {item["price"]:,}',
                size_hint_y=None,
                height=32,
                font_name="Poppins",
                font_size=16,
                color=(0.2, 0.3, 0.4, 1),
            )
            self.daftar_pesanan.add_widget(label)
            total += item["price"] * item["qty"]
        self.total_label.text = f"Total: Rp {total:,}"

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
            popup = SoftPopUp("Pembayaran berhasil!")
            popup.open()

    def print(self, instance):
        pesanan = self.transaksi
        total = sum(item["price"] * item["qty"] for item in pesanan)
        pembayaran = int(self.pembayaran_input.text or 0)
        kembalian = pembayaran - total if pembayaran >= total else 0

        waktu = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transaksi_{waktu}.pdf"
        folder = "D:/Kasir/print_transaksi"
        if not os.path.exists(folder):
            os.makedirs(folder)
        filepath = os.path.join(folder, filename)

        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas

        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4
        y = height - 50

        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, y, "Ringkasan Transaksi")
        y -= 40

        c.setFont("Helvetica", 12)
        c.drawString(
            50, y, f"Tanggal: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}"
        )
        y -= 30

        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "Daftar Pesanan:")
        y -= 25

        c.setFont("Helvetica", 12)
        for item in pesanan:
            c.drawString(
                60, y, f"- {item['name']}   Rp {item['price']:,} {item['qty']}x"
            )
            y -= 20

        y -= 10
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Total      : Rp {total:,}")
        y -= 20
        c.drawString(50, y, f"Pembayaran : Rp {pembayaran:,}")
        y -= 20
        c.drawString(50, y, f"Kembalian  : Rp {kembalian:,}")

        c.save()

        popup = SoftPopUp(message=f"PDF berhasil dibuat:\n{filename}")
        popup.open()
