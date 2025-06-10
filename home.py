from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.core.text import LabelBase

LabelBase.register(
    name="Poppins",
    fn_regular="font/Poppins-Regular.ttf"
)

home_kv = '''
BoxLayout:
    orientation: 'vertical'
    spacing: 20
    padding: [40, 40, 40, 40]
    canvas.before:
        Color:
            rgba: 0.96, 0.97, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: 50
        canvas.before:
            Color:
                rgba: 0.4, 0.6, 0.95, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: "HOME"
            bold: True
            font_size: 20
            font_name: "Poppins"
            color: 1, 1, 1, 1

    Label:
        text: "Selamat Datang, Kasir"
        font_size: 24
        font_name: "Poppins"
        color: 0.1, 0.1, 0.1, 1
        size_hint_y: None
        height: 40

    GridLayout:
        cols: 2
        radius: [50, 50, 50, 50]
        spacing: 20
        size_hint_y: None
        height: self.minimum_height

        Button:
            text: "Transaksi Baru"
            font_size: 25
            font_name: "Poppins"
            bold: True
            size_hint_y: None
            height: 300
            background_normal: ''
            background_color: 0.88, 0.94, 1, 1
            color: 0.1, 0.2, 0.3, 1
            on_release: app.transaksi()
            Image:
                source: "gambar/cart.png"
                center_x: self.parent.center_x
                center_y: self.parent.center_y + 50
                size_hint: None, None
                size: 100, 100

        Button:
            text: "Riwayat Transaksi"
            font_size: 25
            font_name: "Poppins"
            bold: True
            size_hint_y: None
            height: 300
            background_normal: ''
            background_color: 0.88, 0.94, 1, 1
            color: 0.1, 0.2, 0.3, 1
            Image:
                source: "gambar/history.png"
                center_x: self.parent.center_x
                center_y: self.parent.center_y + 50
                size_hint: None, None
                size: 100, 100

        Button:
            text: "Kelola Produk"
            font_size: 25
            font_name: "Poppins"
            bold: True
            size_hint_y: None
            height: 300
            background_normal: ''
            background_color: 0.88, 0.94, 1, 1
            color: 0.1, 0.2, 0.3, 1
            Image:
                source: "gambar/produk.png"
                center_x: self.parent.center_x
                center_y: self.parent.center_y + 50
                size_hint: None, None
                size: 100, 100

        Button:
            text: "Logout"
            font_size: 25
            font_name: "Poppins"
            bold: True
            size_hint_y: None
            height: 300
            background_normal: ''
            background_color: 0.88, 0.94, 1, 1
            color: 0.1, 0.2, 0.3, 1
            on_release: app.back_to_login()
            Image:
                source: "gambar/logout.png"
                center_x: self.parent.center_x
                center_y: self.parent.center_y + 50
                size_hint: None, None
                size: 110, 110
'''
Builder.load_string(home_kv)

class HomeScreen(Screen):
    pass