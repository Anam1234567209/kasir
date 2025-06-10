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

from home import home_kv as HOME_KV
from menu_transaksi import transaksi_kv as TRANSAKSI_KV

# Atur ukuran default window agar terlihat rapi
Window.size = (800, 560)
Window.clearcolor = (0.96, 0.97, 1, 1)  # Soft light blue background

POPPINS_FONT = "font/Poppins-Regular.ttf"


class SoftTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = POPPINS_FONT
        self.padding = [15, 12, 15, 12]
        self.background_color = (1, 1, 1, 0.7)  # Lebih soft dan transparan
        self.foreground_color = (0.3, 0.4, 0.5, 1)  # Teks lebih soft
        self.hint_text_color = (0.5, 0.6, 0.7, 0.5)  # Hint lebih soft dan transparan
        self.cursor_color = (0.6, 0.7, 0.9, 0.7)  # Cursor lebih soft
        self.font_size = 16
        self.hint_font_size = 12
        self.background_active = ""
        self.background_normal = ""

    def update_rect(self, *args):
        pass  # Tidak perlu update rect jika tidak menggunakan canvas


class SoftButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = POPPINS_FONT
        with self.canvas.before:
            Color(0.40, 0.85, 0.87, 1)  # Soft blue
            self.rect = RoundedRectangle(radius=[20], pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.background_color = (0, 0, 0, 0)  # Transparent to show custom bg
        self.color = (0.2, 0.3, 0.4, 1)  # Soft dark text

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(
            orientation="vertical", padding=20, spacing=20, **kwargs
        )
        with self.canvas.before:
            Color(0.96, 0.97, 1, 1)  # Soft light blue
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[0])
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.size_hint = (None, None)
        self.size = (300, 400)

        # Logo di tengah (center x dan y) menggunakan AnchorLayout
        logo_anchor = AnchorLayout(
            anchor_x="center", anchor_y="center", size_hint=(1, None), height=100
        )
        logo_box = BoxLayout(
            orientation="vertical", size_hint=(None, None), size=(100, 100)
        )
        logo_box.add_widget(Widget())  # Spacer atas (opsional)
        logo_box.add_widget(
            Image(
                source="gambar/pos.png",
                size_hint=(None, None),
                size=(70, 70),
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
                font_size=24,
                font_name=POPPINS_FONT,
                bold=False,
                color=(0.2, 0.3, 0.4, 1),
                size_hint=(1, None),
                height=40,
                halign="center",
            )
        )

        # Username field dengan ikon
        username_layout = BoxLayout(
            orientation="horizontal", spacing=10, size_hint_y=None, height=50
        )
        username_layout.add_widget(
            Image(
                source="gambar/user.png",
                size_hint=(None, None),
                size=(50, 50),
                pos_hint={"center_y": 0.5},
            )
        )
        self.username_input = SoftTextInput(
            hint_text="Username",
            multiline=False,
        )
        username_layout.add_widget(self.username_input)
        self.add_widget(username_layout)

        # Password field dengan ikon
        password_layout = BoxLayout(
            orientation="horizontal", spacing=10, size_hint_y=None, height=50
        )
        password_layout.add_widget(
            Image(
                source="gambar/gembok.png",
                size_hint=(None, None),
                size=(50, 50),
                pos_hint={"center_y": 0.5},
            )
        )
        self.password_input = SoftTextInput(
            hint_text="Password",
            password=True,
            multiline=False,
        )
        password_layout.add_widget(self.password_input)
        self.add_widget(password_layout)

        # Tombol Login
        self.login_button = SoftButton(
            text="LOGIN",
            size_hint=(1, None),
            height=40,
            font_size=16,
            bold=True,
        )
        self.login_button.font_name = POPPINS_FONT
        self.login_button.bind(on_press=self.validate_login)
        self.add_widget(self.login_button)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def validate_login(self, instance):
        uname = self.username_input.text
        pwd = self.password_input.text

        if uname == "anam" and pwd == "1122":
            MDApp.get_running_app().home()
        else:
            self.show_popup("Login Gagal", "Username atau password salah.")

    def show_popup(self, title, message):
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(
            Label(text=message, color=(1, 1, 1, 1), font_name=POPPINS_FONT)
        )
        close_btn = SoftButton(text="Tutup", size_hint=(1, 0.6))
        close_btn.font_name = POPPINS_FONT
        content.add_widget(close_btn)

        popup = Popup(
            title=title, content=content, size_hint=(None, None), size=(300, 200)
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


class KasirApp(MDApp):
    def back_to_login(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(self.login_screen)

    def build(self):
        self.root_layout = AnchorLayout(anchor_x="center", anchor_y="center")
        self.login_screen = LoginScreen(size_hint=(None, None), size=(210, 400))
        self.root_layout.add_widget(self.login_screen)
        return self.root_layout

    def home(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(Builder.load_string(HOME_KV))

    def transaksi(self):
        self.root_layout.clear_widgets()
        self.root_layout.add_widget(Builder.load_string(TRANSAKSI_KV))


if __name__ == "__main__":
    KasirApp().run()
