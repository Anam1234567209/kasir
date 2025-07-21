from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.properties import BooleanProperty
from kivy.core.window import Window
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior


# Daftarkan semua varian font Poppins
LabelBase.register(name="Poppins", fn_regular="font/Poppins-Regular.ttf")
LabelBase.register(name="Poppins_Bold", fn_regular="font/Poppins-Bold.ttf")
LabelBase.register(name="Poppins_Italic", fn_regular="font/Poppins-Italic.ttf")
LabelBase.register(name="Poppins_BoldItalic", fn_regular="font/Poppins-BoldItalic.ttf")
LabelBase.register(name="Poppins_Light", fn_regular="font/Poppins-Light.ttf")
LabelBase.register(
    name="Poppins_LightItalic", fn_regular="font/Poppins-LightItalic.ttf"
)
LabelBase.register(name="Poppins_Medium", fn_regular="font/Poppins-Medium.ttf")
LabelBase.register(
    name="Poppins_MediumItalic", fn_regular="font/Poppins-MediumItalic.ttf"
)
LabelBase.register(name="Poppins_SemiBold", fn_regular="font/Poppins-SemiBold.ttf")
LabelBase.register(
    name="Poppins_SemiBoldItalic", fn_regular="font/Poppins-SemiBoldItalic.ttf"
)
LabelBase.register(name="Poppins_ExtraBold", fn_regular="font/Poppins-ExtraBold.ttf")
LabelBase.register(
    name="Poppins_ExtraBoldItalic", fn_regular="font/Poppins-ExtraBoldItalic.ttf"
)
LabelBase.register(name="Poppins_Black", fn_regular="font/Poppins-Black.ttf")
LabelBase.register(
    name="Poppins_BlackItalic", fn_regular="font/Poppins-BlackItalic.ttf"
)
LabelBase.register(name="Poppins_Thin", fn_regular="font/Poppins-Thin.ttf")
LabelBase.register(name="Poppins_ThinItalic", fn_regular="font/Poppins-ThinItalic.ttf")


class fonts:
    Regular = "Poppins"
    Bold = "Poppins_Bold"
    Italic = "Poppins_Italic"
    BoldItalic = "Poppins_BoldItalic"
    Light = "Poppins_Light"
    LightItalic = "Poppins_LightItalic"
    Medium = "Poppins_Medium"
    MediumItalic = "Poppins_MediumItalic"
    SemiBold = "Poppins_SemiBold"
    SemiBoldItalic = "Poppins_SemiBoldItalic"
    ExtraBold = "Poppins_ExtraBold"
    ExtraBoldItalic = "Poppins_ExtraBoldItalic"
    Black = "Poppins_Black"
    BlackItalic = "Poppins_BlackItalic"
    Thin = "Poppins_Thin"
    ThinItalic = "Poppins_ThinItalic"


class SoftTextInput(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = fonts.Regular
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
    hovered = BooleanProperty(False)
    pressed = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.font_name = fonts.Bold
        with self.canvas.before:
            self.bg_color = Color(0.40, 0.85, 0.87, 1)  # Soft blue
            self.rect = RoundedRectangle(radius=[20], pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.background_color = (0, 0, 0, 0)
        self.color = (0.2, 0.3, 0.4, 1)

        # Hover event
        self.bind(hovered=self.on_hover)
        self.bind(pressed=self.on_press_state)
        self.register_event_type("on_enter")
        self.register_event_type("on_leave")

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_enter(self, *args):
        self.hovered = True

    def on_leave(self, *args):
        self.hovered = False

    def on_hover(self, instance, value):
        if self.pressed:
            self.bg_color.rgba = (0.25, 0.65, 0.75, 1)  # Lebih gelap saat klik
        elif value:
            self.bg_color.rgba = (0.55, 0.92, 0.95, 1)  # Biru muda saat hover
        else:
            self.bg_color.rgba = (0.40, 0.85, 0.87, 1)  # Normal

    def on_press_state(self, instance, value):
        if value:
            self.bg_color.rgba = (0.25, 0.65, 0.75, 1)
        else:
            self.on_hover(self, self.hovered)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.pressed:
            self.pressed = False
        return super().on_touch_up(touch)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if inside and not self.hovered:
            self.dispatch("on_enter")
        elif not inside and self.hovered:
            self.dispatch("on_leave")

    def on_parent(self, instance, parent):
        if parent:
            Window.bind(mouse_pos=self.on_mouse_pos)
        else:
            Window.unbind(mouse_pos=self.on_mouse_pos)


# soft button with red color for delete action
class MinButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = fonts.Bold
        # with self.canvas.before:
        #     self.bg_color = Color(rgba=(204/255, 85/255, 0/255, 1))  # Soft blue
        #     self.rect = RoundedRectangle(radius=[20], pos=self.pos, size=self.size)
        # self.bind(pos=self.update_rect, size=self.update_rect)
        self.background_color = (0, 0, 0, 0)
        self.color = (0.2, 0.3, 0.4, 1)  # Warna teks
        with self.canvas.before:
            Color(0.87, 0.57, 0.40)
            self.inline = Line(
                width=1.3,
                rounded_rectangle=[self.x, self.y, self.width, self.height, 18],
            )
        self.bind(pos=self.update_inline, size=self.update_inline)

    def update_inline(self, *args):
        self.inline.rounded_rectangle = [self.x, self.y, self.width, self.height, 18]

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_hover(self, instance, value):
        if self.pressed:
            self.bg_color.rgba = (0.85, 0.18, 0.18, 1)  # Merah gelap saat klik
        elif value:
            self.bg_color.rgba = (1, 0.35, 0.35, 1)  # Merah muda saat hover
        else:
            self.bg_color.rgba = (1, 0.55, 0.55, 1)  # Normal

class ImageButton(ButtonBehavior, Image):
    pass

class ImageBtn(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = fonts.Bold
        # with self.canvas.before:
        #     self.bg_color = Color(rgba=(204/255, 85/255, 0/255, 1))  # Soft blue
        #     self.rect = RoundedRectangle(radius=[20], pos=self.pos, size=self.size)
        # self.bind(pos=self.update_rect, size=self.update_rect)
        self.background_color = (0, 0, 0, 0)
        # self.color = (0.2, 0.3, 0.4, 1)  # Warna teks
        with self.canvas.before:
            Color(0.87, 0.57, 0.40)
            self.inline = Line(
                width=1.3,
                rounded_rectangle=[self.x, self.y, self.width, self.height, 18],
            )
        self.bind(pos=self.update_inline, size=self.update_inline)

    def update_inline(self, *args):
        self.inline.rounded_rectangle = [self.x, self.y, self.width, self.height, 18]

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_hover(self, instance, value):
        if self.pressed:
            self.bg_color.rgba = (0.85, 0.18, 0.18, 1)  # Merah gelap saat klik
        elif value:
            self.bg_color.rgba = (1, 0.35, 0.35, 1)  # Merah muda saat hover
        else:
            self.bg_color.rgba = (1, 0.55, 0.55, 1)  # Normal

class HomeHoverBtn(Button):
    hovered = BooleanProperty(False)
    pressed = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_name = fonts.Bold
        with self.canvas.before:
            self.bg_color = Color(0, 0, 0, 0)  # Soft blue
            self.rect = RoundedRectangle(radius=[20], pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)
        self.background_color = (0, 0, 0, 0)
        self.color = (0, 0, 0, 0)

        # Hover event
        self.bind(hovered=self.on_hover)
        self.bind(pressed=self.on_press_state)
        self.register_event_type("on_enter")
        self.register_event_type("on_leave")

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_enter(self, *args):
        self.hovered = True

    def on_leave(self, *args):
        self.hovered = False

    def on_hover(self, instance, value):
        if self.pressed:
            self.bg_color.rgba = (0, 0, 0, 0)  # Lebih gelap saat klik
        elif value:
            self.bg_color.rgba = (0.55, 0.92, 0.95, 0.1)  # Biru muda saat hover
        else:
            self.bg_color.rgba = (0.40, 0.85, 0.87, 0)  # Normal

    def on_press_state(self, instance, value):
        if value:
            self.bg_color.rgba = (0.25, 0.65, 0.75, 1)
        else:
            self.on_hover(self, self.hovered)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.pressed:
            self.pressed = False
        return super().on_touch_up(touch)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if inside and not self.hovered:
            self.dispatch("on_enter")
        elif not inside and self.hovered:
            self.dispatch("on_leave")

    def on_parent(self, instance, parent):
        if parent:
            Window.bind(mouse_pos=self.on_mouse_pos)
        else:
            Window.unbind(mouse_pos=self.on_mouse_pos)


class SoftPopUp(ModalView):
    def __init__(self, message="Pesan berhasil disimpan!", **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.6, 0.28)
        self.background_color = (0, 0, 0, 0.25)  # Lebih transparan
        self.auto_dismiss = True

        # Konten popup
        layout = FloatLayout()
        box = BoxLayout(
            orientation="vertical",
            size_hint=(1, 1),
            padding=[24, 28, 24, 24],
            spacing=18,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        with box.canvas.before:
            Color(0.97, 0.99, 1, 1)  # Biru pastel sangat soft
            box.bg_rect = RoundedRectangle(pos=box.pos, size=box.size, radius=[20])
        box.bind(
            pos=lambda inst, val: setattr(box.bg_rect, "pos", val),
            size=lambda inst, val: setattr(box.bg_rect, "size", val),
        )

        label = Label(
            text=message,
            font_size=23,
            font_name="Poppins",
            color=(0.18, 0.38, 0.54, 1),
            halign="center",
            valign="middle",
        )
        label.bind(size=label.setter("text_size"))
        box.add_widget(label)

        close_button = SoftButton(
            text="Tutup",
            size_hint=(None, None),
            width=120,
            height=44,
            pos_hint={"center_x": 0.5},
            background_normal="",
            background_color=(0.4, 0.85, 0.87, 1),  # Soft biru
            color=(1, 1, 1, 1),
            font_size=16,
            font_name="Poppins_Bold",
        )
        close_button.bind(on_release=self.dismiss)
        box.add_widget(close_button)

        layout.add_widget(box)
        self.add_widget(layout)

        # Animasi masuk
        self.opacity = 0
        anim = Animation(opacity=1, duration=0.15)
        anim.start(self)


class ConfirmDeletePopup(ModalView):
    def __init__(self, on_confirm=None, message="Apakah Anda yakin ingin menghapus transaksi ini?", **kwargs):
        super().__init__(**kwargs)
        self.on_confirm = on_confirm
        self.size_hint = (0.7, 0.35)
        self.background_color = (0, 0, 0, 0.25)
        self.auto_dismiss = True

        # Konten popup
        layout = FloatLayout()
        box = BoxLayout(
            orientation="vertical",
            size_hint=(1, 1),
            padding=[24, 28, 24, 24],
            spacing=18,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )
        with box.canvas.before:
            Color(0.97, 0.99, 1, 1)  # Biru pastel sangat soft
            box.bg_rect = RoundedRectangle(pos=box.pos, size=box.size, radius=[20])
        box.bind(
            pos=lambda inst, val: setattr(box.bg_rect, "pos", val),
            size=lambda inst, val: setattr(box.bg_rect, "size", val),
        )

        label = Label(
            text=message,
            font_size=23,
            font_name="Poppins",
            color=(0.18, 0.38, 0.54, 1),
            halign="center",
            valign="middle",
        )
        label.bind(size=label.setter("text_size"))
        box.add_widget(label)
        

        # Box untuk tombol dengan FloatLayout untuk posisi yang lebih presisi
        button_container = FloatLayout(
            size_hint_y=None,
            height=50,
        )

        # Tombol Ya (sebelah kiri)
        btn_ya = SoftButton(
            text="Ya",
            size_hint=(None, None),
            width=120,
            height=44,
            pos_hint={"center_x": 0.35, "center_y": 0.5},
            background_color=(1, 0.4, 0.4, 1),  # Merah
            color=(1, 1, 1, 1),
            font_size=16,
            font_name="Poppins_Bold",
        )
        btn_ya.bind(on_release=self.confirm_delete)
        button_container.add_widget(btn_ya)
        
        # Tombol Tidak (sebelah kanan)
        btn_tidak = SoftButton(
            text="Tidak",
            size_hint=(None, None),
            width=120,
            height=44,
            pos_hint={"center_x": 0.65, "center_y": 0.5},
            background_color=(0.6, 0.6, 0.6, 1),  # Abu-abu
            color=(1, 1, 1, 1),
            font_size=16,
            font_name="Poppins_Bold",
        )
        btn_tidak.bind(on_release=self.dismiss)
        button_container.add_widget(btn_tidak)

        box.add_widget(button_container)
        layout.add_widget(box)
        self.add_widget(layout)

        # Animasi masuk
        self.opacity = 0
        anim = Animation(opacity=1, duration=0.15)
        anim.start(self)

    def confirm_delete(self, instance):
        if self.on_confirm:
            self.on_confirm()
        self.dismiss()


class SoftSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)
        self.color = (0.2, 0.3, 0.4, 1)
        self.font_name = fonts.Bold
        self.font_size = 14
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Soft white background
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[5])
        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


class SoftSpinner(Spinner):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.width = 60
        self.padding = [8, 4, 8, 4]
        self.orientation = "vertical"
        self.color = (0.2, 0.3, 0.4, 1)
        with self.canvas.before:
            Color(1, 1, 1, 0.8)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size


if __name__ == "__main__":
    from db import import_produk_csv
    import_produk_csv("produk2.csv")
    print("Produk dari produk2.csv berhasil diimpor ke database.")


