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

from temp import SoftButton, SoftTextInput, fonts, SoftPopUp, MinButton


class ProfileScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 24
        self.spacing = 32  # spacing antar header dan konten
        with self.canvas.before:
            Color(0.96, 0.97, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[32])
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Header dengan label di tengah
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

        header_label = Label(
            text="[b]Profil Cafe[/b]",
            markup=True,
            font_size=24,
            font_name=fonts.Bold,
            color=(0.2, 0.3, 0.4, 1),
            size_hint=(1, 1),
            halign="center",
            valign="middle",
        )
        header_label.bind(size=header_label.setter("text_size"))

        header.add_widget(back_btn)
        header.add_widget(header_label)
        header.add_widget(
            Widget(size_hint_x=None, width=48)
        )  # Spacer kanan agar label tetap di tengah

        self.add_widget(header)

        # Spacer agar header dan konten tidak bertabrakan
        self.add_widget(Widget(size_hint_y=None, height=16))

        # Ambil data profil cafe dari database
        profile = db.get_cafe_profile()
        if not profile:
            profile = {
                "nama_cafe": "WAROENG CAFE",
                "slogan": "Nikmati Kelezatan dalam Setiap Gigitan",
                "logo_cafe": "gambar/logo_icon/waroeng_cafe.png",
                "alamat_cafe": "Jl. Contoh No. 123, Kota, Provinsi",
                "email_cafe": "info@waroengcafe.com",
                "no_hp_cafe": "+62 812-3456-7890",
                "website": "www.waroengcafe.com",
                "jam_operasional": "08:00 - 22:00 WIB",
                "instagram": "@waroengcafe",
            }

        # Layout utama konten profil
        content = BoxLayout(orientation="vertical", spacing=18, padding=[0,0,0,0])
        # Logo Cafe
        logo_path = profile["logo_cafe"] if os.path.exists(profile["logo_cafe"]) else "gambar/logo_icon/waroeng_cafe.png"
        logo = Image(source=logo_path, size_hint=(None, None), size=(120, 120), allow_stretch=True)
        logo_box = AnchorLayout(anchor_x="center", anchor_y="center", size_hint=(1, None), height=130)
        logo_box.add_widget(logo)
        content.add_widget(logo_box)

        # Nama Cafe
        content.add_widget(Label(
            text=f"[b]{profile['nama_cafe']}[/b]",
            markup=True,
            font_size=22,
            font_name=fonts.Bold,
            color=(0.2, 0.3, 0.4, 1),
            size_hint=(1, None),
            height=32,
            halign="center",
            valign="middle",
        ))
        # Slogan
        content.add_widget(Label(
            text=profile["slogan"],
            font_size=16,
            font_name=fonts.Italic,
            color=(0.3, 0.4, 0.5, 1),
            size_hint=(1, None),
            height=26,
            halign="center",
            valign="middle",
        ))
        # Spacer
        content.add_widget(Widget(size_hint_y=None, height=8))

        # Info Grid
        info_grid = GridLayout(cols=2, spacing=8, size_hint=(1, None), padding=[0,0,0,0])
        info_grid.bind(minimum_height=info_grid.setter("height"))
        def add_info(label, value):
            info_grid.add_widget(Label(
                text=f"[b]{label}[/b]",
                markup=True,
                font_size=15,
                font_name=fonts.SemiBold,
                color=(0.2, 0.3, 0.4, 1),
                size_hint_x=0.35,
                halign="right",
                valign="middle",
                height=28,
            ))
            info_grid.add_widget(Label(
                text=value,
                font_size=15,
                font_name=fonts.Regular,
                color=(0.3, 0.4, 0.5, 1),
                size_hint_x=0.65,
                halign="left",
                valign="middle",
                height=28,
            ))
        add_info("Alamat", profile["alamat_cafe"])
        add_info("Email", profile["email_cafe"])
        add_info("No. HP", profile["no_hp_cafe"])
        add_info("Website", profile["website"])
        add_info("Jam Operasional", profile["jam_operasional"])
        add_info("Instagram", profile["instagram"])
        content.add_widget(info_grid)

        # Spacer bawah
        content.add_widget(Widget(size_hint_y=None, height=8))

        # Tambahkan ke layout utama
        self.add_widget(content)


    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        
    def kembali(self, instance):
        App.get_running_app().home()