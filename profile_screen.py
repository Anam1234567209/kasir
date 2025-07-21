from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.boxlayout import BoxLayout
from temp import SoftButton, SoftTextInput, fonts, MinButton, ImageButton
import os
import db


class ProfileScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = [48, 32, 48, 32]
        self.spacing = 32
        self.size_hint = (1, 1)
        self.edit_mode = False

        # Ambil data profil dari database
        profile = db.get_cafe_profile() or {}
        self.profile_keys = [
            ("Nama Cafe", "nama_cafe"),
            ("Alamat", "alamat_cafe"),
            ("Slogan", "slogan"),
            ("Email", "email_cafe"),
            ("No HP", "no_hp_cafe"),
            # ("Website", "website"),
            ("Jam Operasional", "jam_operasional"),
            ("Instagram", "instagram"),
        ]

        # Baris atas: tombol kembali + label Profile
        top_bar = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=32, spacing=0
        )
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
            text="[b]Profile[/b]",
            markup=True,
            size_hint=(1, 1),
            font_size=24,
            font_name=fonts.Bold,
            color=(0.2, 0.3, 0.4, 1),
            halign="center",
            valign="middle",
        )
        header_label.bind(size=header_label.setter("text_size"))
        top_bar.add_widget(back_btn)
        top_bar.add_widget(header_label)
        top_bar.add_widget(
            Widget(size_hint_x=None, width=48)
        )  # Spacer kanan agar label tetap di tengah
        self.add_widget(top_bar)

        # Konten utama dibungkus agar header tidak terdorong keluar
        main_content = BoxLayout(orientation="vertical", size_hint_y=1, spacing=0)

        # Bagian Atas: Logo + label nama_cafe & alamat_cafe (hanya saat non-edit)
        self.atas = BoxLayout(
            orientation="vertical", size_hint=(1, None), height=280, spacing=8
        )
        logo_path = "gambar/logo_icon/waroeng_cafe.png"
        self.logo = Image(
            source=logo_path,
            size_hint=(None, None),
            size=(200, 200),
            allow_stretch=True,
        )
        logo_row = BoxLayout(
            orientation="horizontal", size_hint=(1, None), height=220, spacing=16
        )
        logo_row.add_widget(Widget(size_hint_x=0.1))  # Spacer kiri, opsional
        logo_row.add_widget(self.logo)
        edit_logo_btn = ImageButton(
            source="gambar/logo_icon/edit.png", size_hint=(None, None), size=(20, 20)
        )
        edit_logo_btn.bind(on_press=self.edit_logo)
        logo_row.add_widget(edit_logo_btn)
        logo_row.add_widget(Widget(size_hint_x=0.09))  # Spacer kanan, opsional
        self.atas.add_widget(logo_row)
        self.nama_label = Label(
            text=f"[b]{profile.get('nama_cafe','')}[/b]",
            markup=True,
            font_size=25,
            font_name=fonts.Bold,
            color=(0.2, 0.3, 0.4, 1),
            size_hint=(1, None),
            height=32,
            halign="center",
            valign="middle",
        )
        self.nama_label.bind(size=self.nama_label.setter("text_size"))
        self.atas.add_widget(self.nama_label)
        self.alamat_label = Label(
            text=profile.get("alamat_cafe", ""),
            font_size=17,
            font_name=fonts.Regular,
            color=(0.3, 0.4, 0.5, 1),
            size_hint=(1, None),
            height=26,
            halign="center",
            valign="middle",
        )
        self.alamat_label.bind(size=self.alamat_label.setter("text_size"))
        self.atas.add_widget(self.alamat_label)
        main_content.add_widget(self.atas)

        # Bagian Tengah: Grid 2 kolom (1:3)
        self.tengah = BoxLayout(
            orientation="horizontal", size_hint=(1, None), height=420, spacing=0
        )
        self.grid = GridLayout(
            cols=2,
            spacing=[0, 18],
            size_hint=(1, 1),
            row_default_height=48,
            row_force_default=True,
        )
        label_style = {
            "font_size": 17,
            "font_name": fonts.Bold,
            "color": (0.2, 0.3, 0.4, 1),
            "halign": "right",
            "valign": "middle",
            "size_hint_x": 0.25,
            "text_size": (None, 48),
        }
        field_style = {
            "font_size": 17,
            "font_name": fonts.Regular,
            "size_hint_x": 0.75,
            "height": 44,
            "background_color": (0.97, 0.98, 1, 1),
            "foreground_color": (0.2, 0.3, 0.4, 1),
            "padding": [12, 10, 12, 10],
        }
        self.fields = {}
        self._refresh_grid(profile)
        self.tengah.add_widget(self.grid)
        main_content.add_widget(self.tengah)

        # Spacer
        main_content.add_widget(Widget(size_hint_y=None, height=12))

        # Bagian Bawah: Tombol Ubah/Simpan
        self.bawah = AnchorLayout(
            anchor_x="center", anchor_y="center", size_hint=(1, None), height=60
        )
        self.btn_ubah = (
            SoftButton(
                text="UBAH",
                size_hint=(None, None),
                size=(180, 48),
                font_size=18,
                font_name=fonts.Bold,
                background_color=(0.4, 0.9, 0.95, 1),
            )
            if "SoftButton" in globals()
            else Button(
                text="UBAH", size_hint=(None, None), size=(180, 48), font_size=18
            )
        )
        self.btn_ubah.bind(on_press=self.ubah_profile)
        self.bawah.add_widget(self.btn_ubah)
        # main_content.add_widget(self.bawah)

        # Bungkus main_content dengan ScrollView
        scroll = ScrollView(size_hint=(1, 1))
        main_content.size_hint_y = None
        main_content.bind(minimum_height=main_content.setter("height"))
        scroll.add_widget(main_content)

        self.add_widget(scroll)
        self.add_widget(self.bawah)  # tombol UBAH selalu di bawah

    def kembali(self, instance):
        app = App.get_running_app()
        app.home()

    def _refresh_grid(self, profile):
        self.grid.clear_widgets()
        # Saat non-edit, sembunyikan nama_cafe dan alamat_cafe dari grid
        # Saat edit, tampilkan semua
        if not self.edit_mode:
            keys = [
                k for k in self.profile_keys if k[1] not in ("nama_cafe", "alamat_cafe")
            ]
        else:
            keys = self.profile_keys
        for label, key in keys:
            value = profile.get(key, "")
            self.grid.add_widget(
                Label(
                    text=label + ":",
                    font_size=17,
                    font_name=fonts.Bold,
                    color=(0.2, 0.3, 0.4, 1),
                    halign="right",
                    valign="middle",
                    size_hint_x=0.25,
                    text_size=(None, 48),
                )
            )
            ti = (
                SoftTextInput(
                    text=value,
                    multiline=False,
                    font_size=17,
                    font_name=fonts.Regular,
                    size_hint_x=0.75,
                    height=44,
                    background_color=(0.97, 0.98, 1, 1),
                    foreground_color=(0.2, 0.3, 0.4, 1),
                    padding=[12, 10, 12, 10],
                )
                if "SoftTextInput" in globals()
                else TextInput(
                    text=value,
                    multiline=False,
                    font_size=17,
                    font_name=fonts.Regular,
                    size_hint_x=0.75,
                    height=44,
                    background_color=(0.97, 0.98, 1, 1),
                    foreground_color=(0.2, 0.3, 0.4, 1),
                    padding=[12, 10, 12, 10],
                )
            )
            ti.disabled = not self.edit_mode
            self.fields[key] = ti
            self.grid.add_widget(ti)

    def edit_logo(self, instance):
        content = BoxLayout(orientation="vertical")
        filechooser = FileChooserIconView(
            filters=["*.png", "*.jpg", "*.jpeg"], path="gambar/logo_icon/"
        )
        content.add_widget(filechooser)
        btn_box = BoxLayout(size_hint_y=None, height=40)
        select_btn = Button(text="Pilih")
        cancel_btn = Button(text="Batal")
        btn_box.add_widget(select_btn)
        btn_box.add_widget(cancel_btn)
        content.add_widget(btn_box)
        popup = Popup(title="Pilih Logo Cafe", content=content, size_hint=(0.8, 0.8))

        def pilih_logo(instance):
            if filechooser.selection:
                selected_path = filechooser.selection[0]
                # Update logo di UI
                self.logo.source = selected_path
                # Simpan ke database
                profile = db.get_cafe_profile() or {}
                db.update_cafe_profile(
                    profile.get("nama_cafe", ""),
                    profile.get("slogan", ""),
                    selected_path,  # logo baru
                    profile.get("alamat_cafe", ""),
                    profile.get("email_cafe", ""),
                    profile.get("no_hp_cafe", ""),
                    profile.get("jam_operasional", ""),
                    profile.get("instagram", ""),
                )
                popup.dismiss()

        select_btn.bind(on_press=pilih_logo)
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        popup.open()

    def ubah_profile(self, instance):
        if not self.edit_mode:
            # Masuk ke mode edit
            self.edit_mode = True
            self.nama_label.opacity = 0
            self.alamat_label.opacity = 0
            profile = db.get_cafe_profile() or {}
            self._refresh_grid(profile)
            for ti in self.fields.values():
                ti.disabled = False
            self.btn_ubah.text = "SIMPAN"
        else:
            # Simpan ke database
            data = {key: self.fields[key].text for _, key in self.profile_keys}
            profile = db.get_cafe_profile() or {}
            db.update_cafe_profile(
                data.get("nama_cafe", profile.get("nama_cafe", "")),
                data.get("slogan", profile.get("slogan", "")),
                profile.get("logo_cafe", "gambar/logo_icon/waroeng_cafe.png"),
                data.get("alamat_cafe", profile.get("alamat_cafe", "")),
                data.get("email_cafe", profile.get("email_cafe", "")),
                data.get("no_hp_cafe", profile.get("no_hp_cafe", "")),
                # data.get("website", profile.get("website", "")),
                data.get("jam_operasional", profile.get("jam_operasional", "")),
                data.get("instagram", profile.get("instagram", "")),
            )
            self.edit_mode = False
            # Tampilkan label nama dan alamat lagi
            profile = db.get_cafe_profile() or {}
            self.nama_label.text = f"[b]{profile.get('nama_cafe','')}[/b]"
            self.alamat_label.text = profile.get("alamat_cafe", "")
            self.nama_label.opacity = 1
            self.alamat_label.opacity = 1
            self._refresh_grid(profile)
            for ti in self.fields.values():
                ti.disabled = True
            self.btn_ubah.text = "UBAH"
