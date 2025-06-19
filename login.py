from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager

from home import HomeScreen
from menu_transaksi import MenuTransaksiScreen
from temp import SoftTextInput
from temp import SoftButton
from temp import fonts
from temp import SoftPopUp

# Atur ukuran default window agar terlihat rapi
Window.size = (800, 560)
Window.clearcolor = (0.96, 0.97, 1, 1)  # Soft light blue background


class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(
            orientation="vertical", padding=40, spacing=32, **kwargs
        )
        with self.canvas.before:
            Color(0.96, 0.97, 1, 1)  # Soft light blue
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[32])
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.size_hint = (None, None)
        self.size = (370, 490)

        # Logo di tengah (center x dan y) menggunakan AnchorLayout
        logo_anchor = AnchorLayout(
            anchor_x="center", anchor_y="center", size_hint=(1, None), height=140
        )
        logo_box = BoxLayout(
            orientation="vertical", size_hint=(None, None), size=(140, 140)
        )
        logo_box.add_widget(Widget())  # Spacer atas (opsional)
        logo_box.add_widget(
            Image(
                source="gambar/logo_icon/pos.png",
                size_hint=(None, None),
                size=(110, 110),
                allow_stretch=True,
            )
        )

        logo_box.add_widget(Widget())  # Spacer bawah (opsional)
        logo_anchor.add_widget(logo_box)
        self.add_widget(logo_anchor)

        # Label POS
        self.add_widget(
            Label(
                text="MODUL KIVY",
                font_size=32,
                font_name=fonts.Regular,
                bold=True,
                color=(0.2, 0.3, 0.4, 1),
                size_hint=(1, None),
                height=56,
                halign="center",
            )
        )

        # Username field dengan ikon
        username_layout = BoxLayout(
            orientation="horizontal", spacing=16, size_hint_y=None, height=60
        )
        username_layout.add_widget(
            Image(
                source="gambar/logo_icon/user.png",
                size_hint=(None, None),
                size=(50, 50),
                pos_hint={"center_y": 0.4},
            )
        )
        self.username_input = SoftTextInput(
            hint_text="Username",
            multiline=False,
            font_size=30,
            size_hint_y=None,
            height=50,
            padding=[20, 20, 20, 20],
        )
        username_layout.add_widget(self.username_input)
        self.add_widget(username_layout)

        # Password field dengan ikon
        password_layout = BoxLayout(
            orientation="horizontal", spacing=16, size_hint_y=None, height=60
        )
        password_layout.add_widget(
            Image(
                source="gambar/logo_icon/gembok.png",
                size_hint=(None, None),
                size=(50, 50),
                pos_hint={"center_y": 0.4},
            )
        )
        self.password_input = SoftTextInput(
            hint_text="Password",
            password=True,
            multiline=False,
            font_size=30,
            size_hint_y=None,
            height=50,
            padding=[20, 20, 20, 20],
        )
        password_layout.add_widget(self.password_input)
        self.add_widget(password_layout)

        # Tombol Login
        self.login_button = SoftButton(
            text="LOGIN",
            size_hint=(1, None),
            height=60,
            font_size=24,
            bold=True,
        )
        self.login_button.font_name = fonts.Regular
        self.login_button.bind(on_press=self.validate_login)
        self.add_widget(self.login_button)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def validate_login(self, instance):
        uname = self.username_input.text
        pwd = self.password_input.text

        if uname == "anam" and pwd == "1122":
            MDApp.get_running_app().username = uname
            MDApp.get_running_app().home()
        else:
            # SoftPopUp("Login Gagal", "Username atau password salah.")
            popup = SoftPopUp("Username atau password salah.")
            popup.open()

    def show_popup(self, title, message):
        content = BoxLayout(orientation="vertical", padding=2, spacing=15)
        msg_label = Label(
            text=message,
            color=(1, 1, 1, 1),
            font_name=fonts.Regular,
            font_size=20,
            halign="center",
            valign="middle",
            size_hint=(1, 1),
        )
        msg_label.bind(size=msg_label.setter("text_size"))
        content.add_widget(msg_label)

        close_btn = SoftButton(
            text="Tutup",
            size_hint=(1, None),
            height=48,
            font_size=20,
        )
        close_btn.font_name = fonts.Regular
        close_btn.color = (0, 0, 0, 0.7)
        content.add_widget(close_btn)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(None, None),
            size=(340, 220),
            separator_color=(0.7, 0.85, 1, 1),
            title_color=(1, 1, 1, 1),
            background="atlas://data/images/defaulttheme/button",
            background_color=(1, 1, 1, 1),
        )
        # Membuat sudut popup lebih membulat
        # with popup.canvas.before:
        #     Color(0.96, 0.97, 1, 1)
        #     popup.bg_rect = RoundedRectangle(pos=popup.pos, size=popup.size, radius=[40])
        # popup.bind(pos=lambda i, v: setattr(popup.bg_rect, 'pos', v), size=lambda i, v: setattr(popup.bg_rect, 'size', v))

        close_btn.bind(on_press=popup.dismiss)
        popup.open()


class KasirApp(MDApp):
    username = "Kasir"

    def back_to_login(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.login_screen)

    def kembali(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.home)

    def build(self):
        self.root_layout = AnchorLayout(anchor_x="center", anchor_y="center")
        self.login_screen = LoginScreen(size_hint=(None, None), size=(210, 400))
        self.root_layout.add_widget(self.login_screen)
        return self.root_layout

    def home(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(HomeScreen(username=self.username))

    def transaksi(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(MenuTransaksiScreen())


if __name__ == "__main__":
    KasirApp().run()
