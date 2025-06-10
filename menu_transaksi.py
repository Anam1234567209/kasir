from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.core.text import LabelBase

LabelBase.register(name="Poppins", fn_regular="font/Poppins-Regular.ttf")

transaksi_kv = """

BoxLayout:
    orientation: 'vertical'
    spacing: 20  
    padding: 30
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
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
            text: "HALAMAN TRANSAKSI"
            font_name: "Poppins"
            font_size: 20
            color: 1, 1, 1, 1

    BoxLayout:
        orientation: 'horizontal'

        GridLayout:
            cols: 4
            spacing: 15
            size_hint_x: 0.7
                
            # Produk Contoh
            Button:
                on_release: root.add_to_cart('Produk A', '10000')
                orientation: 'vertical'
                background_normal: ''
                background_color: 0.88, 0.94, 1, 1
                GridLayout:
                    cols: 1
                    size_hint_y: None
                    # orientation: 'vertical'
                    padding: 10
                    spacing: 5
                    Image:
                        source: 'gambar/produk1.png'
                        size_hint: None, None
                        size: 100, 100
                        pos_hint: {'center_x': 0.5}
                    Label:
                        text: 'Produk A'
                        font_name: 'Poppins'
                        font_size: 16
                        color: 0, 0, 0, 1
                    Label:
                        text: 'Rp10.000'
                        font_name: 'Poppins'
                        font_size: 14
                        color: 0.1, 0.1, 0.1, 1
    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.3
        spacing: 10
        padding: 10
        canvas.before:
            Color:
                rgba: 0.95, 0.95, 0.95, 1
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: "Keranjang"
            font_name: "Poppins"
            font_size: 18
            color: 0, 0, 0, 1
            size_hint_y: None
            height: 40
        ScrollView:
            GridLayout:
                id: cart_box
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                        
    Button:
        text: "Kembali ke Home"
        font_name: "Poppins"
        font_size: 18
        size_hint_y: None
        height: 50
        on_release: app.home()
"""

Builder.load_string(transaksi_kv)


class TransaksiScreen(Screen):
    def add_to_cart(self, nama, harga):
        from kivy.uix.label import Label

        cart = self.ids.cart_box
        cart.add_widget(
            Label(
                text=f"{nama} - Rp{harga}",
                font_name="Poppins",
                size_hint_y=None,
                height=30,
            )
        )
