from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.image import Image
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

from temp import fonts


class HomeScreen(BoxLayout):
    def __init__(self, username=" ", **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.username = username
        with self.canvas.before:
            Color(0.90, 0.93, 1, 1)  # Soft blue background
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[0])
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Header
        header = BoxLayout(size_hint=(1, 0.10), padding=[0, 0, 0, 0])
        header_bg = AnchorLayout(anchor_x="center", anchor_y="center")
        with header_bg.canvas.before:
            Color(0.40, 0.85, 0.87, 1)
            self.header_rect = RoundedRectangle(
                pos=header_bg.pos, size=header_bg.size, radius=[0]
            )
        header_bg.bind(pos=self.update_header_rect, size=self.update_header_rect)
        header_label = Label(
            text="HOME",
            font_size=22,
            font_name="Poppins",
            color=(1, 1, 1, 1),
            bold=True,
        )
        header_bg.add_widget(header_label)
        header.add_widget(header_bg)
        self.add_widget(header)

        # Selamat Datang
        # self.add_widget(Widget(size_hint_y=0.01))
        welcome = Label(
            text=f"Selamat Datang, {self.username.upper()}",
            markup=True,
            font_size=26,
            font_name="Poppins",
            color=(0.1, 0.1, 0.1, 1),
            size_hint=(1, 0.10),
        )
        self.add_widget(welcome)
        # self.add_widget(Widget(size_hint_y=0.01))

        # Menu Grid
        grid = GridLayout(
            cols=2, spacing=20, padding=[40, 0, 40, 0], size_hint=(1, 0.6)
        )
        # Tombol Transaksi Baru
        grid.add_widget(
            self.menu_button("Transaksi Baru", "cart.png", self.transaksi_baru)
        )
        # Tombol Riwayat Transaksi
        grid.add_widget(
            self.menu_button("Riwayat Transaksi", "riwayat.png", self.riwayat_transaksi)
        )
        # Tombol Kelola Produk
        grid.add_widget(
            self.menu_button("Kelola Produk", "produk.png", self.kelola_produk)
        )
        # Tombol Logout
        grid.add_widget(self.menu_button("Logout", "logout.png", self.logout))
        self.add_widget(grid)

        self.add_widget(Widget(size_hint_y=0.1))

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update_header_rect(self, *args):
        self.header_rect.pos = self.children[-1].pos
        self.header_rect.size = self.children[-1].size

    def menu_button(self, text, icon, callback):
        btn = AnchorLayout()
        card = FloatLayout(size_hint=(None, None), size=(400, 200))
        with card.canvas.before:
            Color(0.95, 0.98, 1, 1)
            card.bg_rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[16])
        card.bind(
            pos=lambda i, v: setattr(card.bg_rect, "pos", v),
            size=lambda i, v: setattr(card.bg_rect, "size", v),
        )

        # Ikon
        img = Image(
            source=f"gambar/logo_icon/{icon}",
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={"center_x": 0.5, "center_y": 0.60},
        )
        card.add_widget(img)
        # Label
        lbl = Label(
            text=text,
            font_size=18,
            font_name="Poppins",
            color=(0.2, 0.3, 0.5, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.30},
        )
        card.add_widget(lbl)
        # Button transparan di atas (menutupi seluruh card)
        btn_overlay = Button(
            background_color=(0, 0, 0, 0),
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0},
            on_press=callback,
        )
        card.add_widget(btn_overlay)
        btn.add_widget(card)

        return btn

    def transaksi_baru(self, instance):
        App.get_running_app().transaksi()

    def riwayat_transaksi(self, instance):
        App.get_running_app().riwayat_transaksi()

    def kelola_produk(self, instance):
        App.get_running_app().kelola_produk()

    def logout(self, instance):
        App.get_running_app().back_to_login()

    def make_button(self, text, icon_path, screen_name):
        # Soft, rounded button
        btn_layout = Button(
            on_release=lambda x: self.change_screen(screen_name),
            background_normal="",
            background_color=(0.8, 0.9, 1, 1),  # sky blue soft
            color=(0.18, 0.38, 0.54, 1),
            size_hint=(None, None),
            size=(200, 200),
            font_name="Poppins",
        )
        # Membuat isi tombol lebih soft dan rapi
        layout = BoxLayout(
            orientation="vertical",
            padding=[10, 20, 10, 10],
            spacing=18,
        )
        # Gambar center dan proporsional
        icon = Image(
            source=icon_path,
            size_hint=(None, None),
            size=(80, 80),  # Ukuran gambar lebih kecil dari kotak
            allow_stretch=True,
            keep_ratio=True,
        )
        # Center gambar secara horizontal
        icon_box = BoxLayout(size_hint=(1, 0.7), padding=[0, 10, 0, 0])
        icon_box.add_widget(icon)

        label = Label(
            text=text,
            size_hint=(1, 0.3),
            font_size=18,
            font_name="Poppins",
            color=(0.18, 0.38, 0.54, 1),
            halign="center",
            valign="middle",
        )
        label.bind(size=label.setter("text_size"))

        layout.add_widget(icon_box)
        layout.add_widget(label)
        btn_layout.add_widget(layout)

        return btn_layout
