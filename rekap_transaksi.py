from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.spinner import Spinner
from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from temp import SoftButton, SoftPopUp, fonts, MinButton, ImageBtn, SoftSpinner, SoftSpinnerOption
from db import get_all_transaksi
from collections import defaultdict
import datetime


class RekapTransaksiScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 24
        self.spacing = 24
        with self.canvas.before:
            Color(0.96, 0.97, 1, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[32])
        self.bind(pos=self.update_rect, size=self.update_rect)

        # Baris atas: tombol kembali + label Rekap Transaksi + tombol eksport
        top_bar = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=48, spacing=5
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
        
        rekap_label = Label(
            text="[b]Rekap Transaksi[/b]",
            markup=True,
            size_hint=(1, 1),
            font_size=24,
            font_name=fonts.Bold,
            color=(0.2, 0.3, 0.4, 1),
            halign="center",
            valign="middle",
        )
        
        eksport_btn = SoftButton(
            text="Eksport",
            size_hint_x=None,
            size_hint_y=None,
            height=40,
            width=100,
            font_size=15,
            background_color=(0.4, 0.85, 0.87, 1),
            font_name=fonts.Bold
        )
        eksport_btn.bind(on_press=self.eksport_data)

        rekap_label.bind(size=rekap_label.setter("text_size"))
        top_bar.add_widget(back_btn)
        top_bar.add_widget(Widget(size_hint_x=0.32))  # Spacer
        top_bar.add_widget(rekap_label)
        top_bar.add_widget(Widget(size_hint_x=0.11))  # Spacer
        top_bar.add_widget(eksport_btn)
        self.add_widget(top_bar)

        # ScrollView untuk konten utama
        self.scroll = ScrollView()
        self.main_layout = BoxLayout(
            orientation="vertical", spacing=20, size_hint_y=None
        )
        self.main_layout.bind(minimum_height=self.main_layout.setter("height"))
        self.scroll.add_widget(self.main_layout)
        self.add_widget(self.scroll)

        # Inisialisasi data
        self.rentan_tanggal = "Hari Ini"
        self.rentan_options = ["Hari Ini", "Minggu Ini", "Bulan Ini", "Semua"]
        
        self.tampilkan_rekap()

    def update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def kembali(self, instance):
        app = App.get_running_app()
        app.riwayat_transaksi()

    def eksport_data(self, instance):
        # TODO: Implementasi eksport data
        popup = SoftPopUp("Fitur eksport akan segera hadir!")
        popup.open()

    def get_transaksi_by_rentan(self, rentan):
        # Mendapatkan transaksi berdasarkan rentan tanggal
        all_transaksi = get_all_transaksi()
        today = datetime.datetime.now().date()
        
        if rentan == "Hari Ini":
            return [t for t in all_transaksi if self.parse_date(t["waktu"]).date() == today]
        elif rentan == "Minggu Ini":
            week_start = today - datetime.timedelta(days=today.weekday())
            return [t for t in all_transaksi if week_start <= self.parse_date(t["waktu"]).date() <= today]
        elif rentan == "Bulan Ini":
            return [t for t in all_transaksi if self.parse_date(t["waktu"]).month == today.month and self.parse_date(t["waktu"]).year == today.year]
        else:  # Semua
            return all_transaksi

    def parse_date(self, date_str):
        # Parse string tanggal ke datetime object
        try:
            return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except:
            return datetime.datetime.now()

    def hitung_total_pendapatan(self, transaksi_list):
        #Menghitung total pendapatan dari list transaksi#
        return sum(t["total"] for t in transaksi_list)

    def hitung_jumlah_cash(self, transaksi_list):
        #Menghitung jumlah transaksi cash (semua transaksi dianggap cash untuk sementara)#
        return len(transaksi_list)

    def get_produk_laris(self, transaksi_list):
        #Mendapatkan produk paling laris berdasarkan jumlah terjual#
        produk_count = defaultdict(int)
        produk_info = {}  # Untuk menyimpan info tambahan produk
        
        for transaksi in transaksi_list:
            for item in transaksi["items"]:
                produk_count[item["name"]] += item["qty"]
                # Simpan harga dari transaksi (gunakan harga terakhir)
                produk_info[item["name"]] = {
                    "harga": item["price"],
                    "kategori": "Makanan"  # Default, bisa diambil dari database nanti
                }
        
        # Sort berdasarkan jumlah terjual (descending)
        sorted_produk = sorted(produk_count.items(), key=lambda x: x[1], reverse=True)
        
        # Return dengan info tambahan
        result = []
        for nama_produk, jumlah in sorted_produk[:5]:  # Ambil 5 produk teratas
            info = produk_info.get(nama_produk, {"harga": 0, "kategori": "Makanan"})
            result.append({
                "nama": nama_produk,
                "jumlah": jumlah,
                "harga": info["harga"],
                "kategori": info["kategori"]
            })
        return result

    def tampilkan_rekap(self):
        self.main_layout.clear_widgets()
        
        # Spacer awal
        top_spacer = Widget(size_hint_y=None, height=40)
        self.main_layout.add_widget(top_spacer)
        
        # Dapatkan transaksi berdasarkan rentan tanggal
        transaksi_list = self.get_transaksi_by_rentan(self.rentan_tanggal)
        
        # KOLOM 1: Rentan Tanggal, Total Pendapatan, Jumlah Cash
        kolom1_container = BoxLayout(orientation="vertical", size_hint_y=None, height=140, spacing=10)
        # kolom1_container.padding = [10, 10, 10, 10]
        
        # Background untuk kolom1
        with kolom1_container.canvas.before:
            Color(1, 1, 1, 0.9)
            kolom1_container.bg_rect = RoundedRectangle(pos=kolom1_container.pos, size=kolom1_container.size, radius=[15])
        kolom1_container.bind(pos=lambda inst, val: setattr(kolom1_container.bg_rect, "pos", val),
                             size=lambda inst, val: setattr(kolom1_container.bg_rect, "size", val))
        
        kolom1 = BoxLayout(orientation="horizontal", size_hint_y=None, height=120, spacing=20)
        
        # Sub-kolom 1: Rentan Tanggal
        sub_kolom1 = BoxLayout(orientation="vertical", size_hint_x=0.33, spacing=10)
        rentan_label = Label(
            text="[b]Rentan Tanggal[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=16,
            color=(0.2, 0.3, 0.4, 1),
            size_hint_y=None,
            height=30,
            halign="center",
            valign="middle",
        )
        rentan_label.bind(size=rentan_label.setter("text_size"))
        sub_kolom1.add_widget(rentan_label)
        
        # Container untuk spinner dengan FloatLayout
        spinner_container = FloatLayout(size_hint_y=None, height=50)
        
        self.rentan_spinner = Spinner(
            text=self.rentan_tanggal,
            values=self.rentan_options,
            size_hint=(None, None),
            size=(120, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_name=fonts.Medium,
            font_size=14,
            background_color=(0.9, 0.9, 0.9, 1),
            color=(0.2, 0.3, 0.4, 1),
            option_cls=SoftSpinnerOption,

        )
        self.rentan_spinner.bind(text=self.on_rentan_changed)
        spinner_container.add_widget(self.rentan_spinner)
        sub_kolom1.add_widget(spinner_container)
        
        # Sub-kolom 2: Total Pendapatan
        sub_kolom2 = BoxLayout(orientation="vertical", size_hint_x=0.33, spacing=10)
        pendapatan_label = Label(
            text="[b]Total Pendapatan[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=16,
            color=(0.2, 0.3, 0.4, 1),
            size_hint_y=None,
            height=30,
            halign="center",
            valign="middle",
        )
        pendapatan_label.bind(size=pendapatan_label.setter("text_size"))
        sub_kolom2.add_widget(pendapatan_label)
        
        # Container untuk total pendapatan dengan FloatLayout
        pendapatan_container = FloatLayout(size_hint_y=None, height=50)
        
        self.total_pendapatan_label = Label(
            text=f"Rp {self.hitung_total_pendapatan(transaksi_list):,}",
            font_name=fonts.Bold,
            font_size=18,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_y=None,
            height=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign="center",
            valign="middle",
        )
        self.total_pendapatan_label.bind(size=self.total_pendapatan_label.setter("text_size"))
        pendapatan_container.add_widget(self.total_pendapatan_label)
        sub_kolom2.add_widget(pendapatan_container)
        
        # Sub-kolom 3: Jumlah Cash
        sub_kolom3 = BoxLayout(orientation="vertical", size_hint_x=0.33, spacing=10)
        cash_label = Label(
            text="[b]Jumlah Pembayaran Cash[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=16,
            color=(0.2, 0.3, 0.4, 1),
            size_hint_y=None,
            height=30,
            halign="center",
            valign="middle",
        )
        cash_label.bind(size=cash_label.setter("text_size"))
        sub_kolom3.add_widget(cash_label)
        
        # Container untuk jumlah cash dengan FloatLayout
        cash_container = FloatLayout(size_hint_y=None, height=50)
        
        self.jumlah_cash_label = Label(
            text=str(self.hitung_jumlah_cash(transaksi_list)),
            font_name=fonts.Bold,
            font_size=18,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_y=None,
            height=40,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign="center",
            valign="middle",
        )
        self.jumlah_cash_label.bind(size=self.jumlah_cash_label.setter("text_size"))
        cash_container.add_widget(self.jumlah_cash_label)
        sub_kolom3.add_widget(cash_container)
        
        kolom1.add_widget(sub_kolom1)
        kolom1.add_widget(sub_kolom2)
        kolom1.add_widget(sub_kolom3)
        kolom1_container.add_widget(kolom1)
        self.main_layout.add_widget(kolom1_container)
        
        # Spacer antara kolom 1 dan 2
        spacer1 = Widget(size_hint_y=None, height=20)
        self.main_layout.add_widget(spacer1)
        
        # KOLOM 2: Produk Paling Laris
        kolom2_container = BoxLayout(orientation="vertical", size_hint_y=None, height=320, spacing=10)
        kolom2_container.padding = [10, 10, 10, 10]
        
        # Background untuk kolom2
        with kolom2_container.canvas.before:
            Color(1, 1, 1, 0.9)
            kolom2_container.bg_rect = RoundedRectangle(pos=kolom2_container.pos, size=kolom2_container.size, radius=[15])
        kolom2_container.bind(pos=lambda inst, val: setattr(kolom2_container.bg_rect, "pos", val),
                             size=lambda inst, val: setattr(kolom2_container.bg_rect, "size", val))
        
        kolom2 = BoxLayout(orientation="vertical", size_hint_y=None, height=300, spacing=20)
        
        # Container untuk judul dengan FloatLayout
        judul_container = FloatLayout(size_hint_y=None, height=50)
        
        laris_label = Label(
            text="[b]PRODUK PALING LARIS[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=18,
            color=(0.2, 0.3, 0.4, 1),
            size_hint_y=None,
            height=30,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign="center",
            valign="middle",
        )
        laris_label.bind(size=laris_label.setter("text_size"))
        judul_container.add_widget(laris_label)
        kolom2.add_widget(judul_container)
        
        # Header tabel produk laris
        header_laris = BoxLayout(orientation="horizontal", size_hint_y=None, height=35, spacing=10)
        header_laris.add_widget(Label(
            text="[b]Kategori[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=14,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_x=0.25,
            halign="center",
            valign="middle",
        ))
        header_laris.add_widget(Label(
            text="[b]Nama[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=14,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_x=0.2,
            halign="center",
            valign="middle",
        ))
        header_laris.add_widget(Label(
            text="[b]Harga[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=14,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_x=0.35,
            halign="center",
            valign="middle",
        ))
        header_laris.add_widget(Label(
            text="[b]Jumlah Terjual[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=14,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_x=0.2,
            halign="center",
            valign="middle",
        ))
        kolom2.add_widget(header_laris)
        
        # Data produk laris
        produk_laris = self.get_produk_laris(transaksi_list)
        for produk in produk_laris:
            # Container untuk setiap baris dengan FloatLayout
            row_container = FloatLayout(size_hint_y=None, height=40)
            
            row_laris = BoxLayout(orientation="horizontal", size_hint_y=None, height=30, spacing=10, pos_hint={'center_x': 0.5, 'center_y': 0.5})
            row_laris.add_widget(Label(
                text=produk["kategori"],
                font_name=fonts.Regular,
                font_size=12,
                color=(0.2, 0.3, 0.4, 1),
                size_hint_x=0.25,
                halign="center",
                valign="middle",
            ))
            row_laris.add_widget(Label(
                text=produk["nama"],
                font_name=fonts.Regular,
                font_size=12,
                color=(0.2, 0.3, 0.4, 1),
                size_hint_x=0.2,
                halign="center",
                valign="middle",
            ))
            row_laris.add_widget(Label(
                text=f"{produk['harga']:,}",
                font_name=fonts.Regular,
                font_size=12,
                color=(0.2, 0.3, 0.4, 1),
                size_hint_x=0.35,
                halign="center",
                valign="middle",
            ))
            row_laris.add_widget(Label(
                text=str(produk["jumlah"]),
                font_name=fonts.Bold,
                font_size=12,
                color=(0.18, 0.38, 0.54, 1),
                size_hint_x=0.2,
                halign="center",
                valign="middle",
            ))
            row_container.add_widget(row_laris)
            kolom2.add_widget(row_container)
        
        if not produk_laris:
            empty_label = Label(
                text="Belum ada transaksi pada rentang ini.",
                font_name=fonts.Italic,
                font_size=13,
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=40,
                halign="center",
                valign="middle",
            )
            empty_label.bind(size=empty_label.setter("text_size"))
            kolom2.add_widget(empty_label)

        kolom2_container.add_widget(kolom2)
        self.main_layout.add_widget(kolom2_container)
        
        # Spacer untuk memisahkan kolom
        spacer = Widget(size_hint_y=None, height=30)
        self.main_layout.add_widget(spacer)
        
        # KOLOM 3: Riwayat Transaksi
        kolom3_container = BoxLayout(orientation="vertical", size_hint_y=None, height=450, spacing=10)
        kolom3_container.padding = [10, 10, 10, 10]
        
        # Background untuk kolom3
        with kolom3_container.canvas.before:
            Color(1, 1, 1, 0.9)
            kolom3_container.bg_rect = RoundedRectangle(pos=kolom3_container.pos, size=kolom3_container.size, radius=[15])
        kolom3_container.bind(pos=lambda inst, val: setattr(kolom3_container.bg_rect, "pos", val),
                             size=lambda inst, val: setattr(kolom3_container.bg_rect, "size", val))
        
        kolom3 = BoxLayout(orientation="vertical", size_hint_y=None, height=430, spacing=20)
        
        # Container untuk judul dengan FloatLayout
        riwayat_judul_container = FloatLayout(size_hint_y=None, height=50)
        
        riwayat_label = Label(
            text="[b]RIWAYAT TRANSAKSI[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=18,
            color=(0.2, 0.3, 0.4, 1),
            size_hint_y=None,
            height=30,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign="center",
            valign="middle",
        )
        riwayat_label.bind(size=riwayat_label.setter("text_size"))
        riwayat_judul_container.add_widget(riwayat_label)
        kolom3.add_widget(riwayat_judul_container)
        
        # Header tabel riwayat
        header_riwayat = BoxLayout(orientation="horizontal", size_hint_y=None, height=35, spacing=10)
        header_riwayat.add_widget(Label(
            text="[b]Waktu[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=14,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_x=0.25,
            halign="center",
            valign="middle",
        ))
        header_riwayat.add_widget(Label(
            text="[b]No Meja[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=14,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_x=0.2,
            halign="center",
            valign="middle",
        ))
        header_riwayat.add_widget(Label(
            text="[b]Pesanan[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=14,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_x=0.35,
            halign="center",
            valign="middle",
        ))
        header_riwayat.add_widget(Label(
            text="[b]Total[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=14,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_x=0.2,
            halign="center",
            valign="middle",
        ))
        kolom3.add_widget(header_riwayat)
        
        # ScrollView untuk data riwayat transaksi
        scroll_container = BoxLayout(orientation="vertical", size_hint_y=None, height=300)
        scroll_container.bind(minimum_height=scroll_container.setter("height"))
        
        # Data riwayat transaksi
        for trx in transaksi_list:
            pesanan_str = ", ".join([f"{item['name']} x{item['qty']}" for item in trx["items"]])
            # Hitung tinggi baris berdasarkan panjang pesanan
            pesanan_lines = len(pesanan_str) // 30 + 1
            row_height = max(35, 25 + pesanan_lines * 15)
            
            # Container untuk setiap baris dengan FloatLayout
            row_container = FloatLayout(size_hint_y=None, height=row_height + 15)
            
            row_riwayat = BoxLayout(orientation="horizontal", size_hint_y=None, height=row_height, spacing=10, pos_hint={'center_x': 0.5, 'center_y': 0.5})
            
            # Kolom waktu
            waktu = Label(
                text=trx["waktu"][:16],  # Ambil hanya tanggal dan jam
                font_name=fonts.Regular,
                font_size=12,
                color=(0.2, 0.3, 0.4, 1),
                size_hint_x=0.25,
                halign="center",
                valign="middle",
            )
            waktu.bind(size=waktu.setter("text_size"))
            row_riwayat.add_widget(waktu)
            
            # Kolom no meja
            no_meja_val = trx["no_meja"]
            from_riwayat = trx.get("from_riwayat", False)
            if from_riwayat:
                no_meja_text = f"{no_meja_val}+" if no_meja_val is not None else "TA+"
            else:
                no_meja_text = f"{no_meja_val:,}" if no_meja_val is not None else "TA"
            no_meja = Label(
                text=no_meja_text,
                font_name=fonts.Bold,
                font_size=12,
                color=(0.18, 0.38, 0.54, 1),
                size_hint_x=0.2,
                halign="center",
                valign="middle",
            )
            row_riwayat.add_widget(no_meja)
            
            # Kolom pesanan
            pesanan = Label(
                text=pesanan_str,
                font_name=fonts.Regular,
                font_size=11,
                color=(0.2, 0.3, 0.4, 1),
                size_hint_x=0.35,
                halign="center",
                valign="middle",
            )
            pesanan.bind(size=pesanan.setter("text_size"))
            row_riwayat.add_widget(pesanan)
            
            # Kolom total
            total = Label(
                text=f"Rp {trx['total']:,}",
                font_name=fonts.Bold,
                font_size=12,
                color=(0.18, 0.38, 0.54, 1),
                size_hint_x=0.2,
                halign="center",
                valign="middle",
            )
            total.bind(size=total.setter("text_size"))
            row_riwayat.add_widget(total)
            
            row_container.add_widget(row_riwayat)
            scroll_container.add_widget(row_container)
        
        # ScrollView untuk data transaksi
        scroll_view = ScrollView(size_hint_y=None, height=300)
        scroll_view.add_widget(scroll_container)
        kolom3.add_widget(scroll_view)
        
        kolom3_container.add_widget(kolom3)
        self.main_layout.add_widget(kolom3_container)
        
        # Spacer akhir untuk memastikan ada ruang yang cukup
        end_spacer = Widget(size_hint_y=None, height=120)
        self.main_layout.add_widget(end_spacer)

    def on_rentan_changed(self, instance, value):
        #Callback ketika rentan tanggal berubah#
        self.rentan_tanggal = value
        # Update label total pendapatan dan jumlah cash
        transaksi_list = self.get_transaksi_by_rentan(self.rentan_tanggal)
        self.total_pendapatan_label.text = f"Rp {self.hitung_total_pendapatan(transaksi_list):,}"
        self.jumlah_cash_label.text = str(self.hitung_jumlah_cash(transaksi_list))
        
        # Update kolom 2 dan 3
        self.update_kolom2_dan_3(transaksi_list)
    
    def update_kolom2_dan_3(self, transaksi_list):
        #Update kolom 2 dan 3 dengan data baru#
        # Hapus kolom 2 dan 3 yang lama
        if len(self.main_layout.children) > 3:  # Lebih dari spacer, kolom1, dan spacer
            # Hapus kolom 3, spacer, dan kolom 2
            self.main_layout.remove_widget(self.main_layout.children[0])  # end_spacer
            self.main_layout.remove_widget(self.main_layout.children[0])  # kolom3_container
            self.main_layout.remove_widget(self.main_layout.children[0])  # spacer
            self.main_layout.remove_widget(self.main_layout.children[0])  # kolom2_container
        
        # Tambahkan spacer antara kolom 1 dan 2
        spacer1 = Widget(size_hint_y=None, height=20)
        self.main_layout.add_widget(spacer1)
        
        # KOLOM 2: Produk Paling Laris
        kolom2_container = BoxLayout(orientation="vertical", size_hint_y=None, height=320, spacing=10)
        kolom2_container.padding = [10, 10, 10, 10]
        
        # Background untuk kolom2
        with kolom2_container.canvas.before:
            Color(1, 1, 1, 0.9)
            kolom2_container.bg_rect = RoundedRectangle(pos=kolom2_container.pos, size=kolom2_container.size, radius=[15])
        kolom2_container.bind(pos=lambda inst, val: setattr(kolom2_container.bg_rect, "pos", val),
                             size=lambda inst, val: setattr(kolom2_container.bg_rect, "size", val))
        
        kolom2 = BoxLayout(orientation="vertical", size_hint_y=None, height=300, spacing=20)
        
        # Container untuk judul dengan FloatLayout
        judul_container = FloatLayout(size_hint_y=None, height=50)
        
        laris_label = Label(
            text="[b]PRODUK PALING LARIS[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=18,
            color=(0.2, 0.3, 0.4, 1),
            size_hint_y=None,
            height=30,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign="center",
            valign="middle",
        )
        laris_label.bind(size=laris_label.setter("text_size"))
        judul_container.add_widget(laris_label)
        kolom2.add_widget(judul_container)
        
        # Header tabel produk laris
        header_laris = BoxLayout(orientation="horizontal", size_hint_y=None, height=35, spacing=10)
        header_laris.add_widget(Label(
            text="[b]Kategori[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=14,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_x=0.25,
            halign="center",
            valign="middle",
        ))
        header_laris.add_widget(Label(
            text="[b]Nama[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=14,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_x=0.4,
            halign="center",
            valign="middle",
        ))
        header_laris.add_widget(Label(
            text="[b]Harga[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=14,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_x=0.2,
            halign="center",
            valign="middle",
        ))
        header_laris.add_widget(Label(
            text="[b]Jumlah Terjual[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=14,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_x=0.15,
            halign="center",
            valign="middle",
        ))
        kolom2.add_widget(header_laris)
        
        # Data produk laris
        produk_laris = self.get_produk_laris(transaksi_list)
        for produk in produk_laris:
            # Container untuk setiap baris dengan FloatLayout
            row_container = FloatLayout(size_hint_y=None, height=40)
            
            row_laris = BoxLayout(orientation="horizontal", size_hint_y=None, height=30, spacing=10, pos_hint={'center_x': 0.5, 'center_y': 0.5})
            row_laris.add_widget(Label(
                text=produk["kategori"],
                font_name=fonts.Regular,
                font_size=12,
                color=(0.2, 0.3, 0.4, 1),
                size_hint_x=0.25,
                halign="center",
                valign="middle",
            ))
            row_laris.add_widget(Label(
                text=produk["nama"],
                font_name=fonts.Regular,
                font_size=12,
                color=(0.2, 0.3, 0.4, 1),
                size_hint_x=0.4,
                halign="center",
                valign="middle",
            ))
            row_laris.add_widget(Label(
                text=f"{produk['harga']:,}",
                font_name=fonts.Regular,
                font_size=12,
                color=(0.2, 0.3, 0.4, 1),
                size_hint_x=0.2,
                halign="center",
                valign="middle",
            ))
            row_laris.add_widget(Label(
                text=str(produk["jumlah"]),
                font_name=fonts.Bold,
                font_size=12,
                color=(0.18, 0.38, 0.54, 1),
                size_hint_x=0.15,
                halign="center",
                valign="middle",
            ))
            row_container.add_widget(row_laris)
            kolom2.add_widget(row_container)
        
        if not produk_laris:
            empty_label = Label(
                text="Belum ada transaksi pada rentang ini.",
                font_name=fonts.Italic,
                font_size=13,
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=40,
                halign="center",
                valign="middle",
            )
            empty_label.bind(size=empty_label.setter("text_size"))
            kolom2.add_widget(empty_label)

        kolom2_container.add_widget(kolom2)
        self.main_layout.add_widget(kolom2_container)
        
        # Spacer untuk memisahkan kolom
        spacer = Widget(size_hint_y=None, height=60)
        self.main_layout.add_widget(spacer)
        
        # KOLOM 3: Riwayat Transaksi
        kolom3_container = BoxLayout(orientation="vertical", size_hint_y=None, height=450, spacing=10)
        kolom3_container.padding = [10, 10, 10, 10]
        
        # Background untuk kolom3
        with kolom3_container.canvas.before:
            Color(1, 1, 1, 0.9)
            kolom3_container.bg_rect = RoundedRectangle(pos=kolom3_container.pos, size=kolom3_container.size, radius=[15])
        kolom3_container.bind(pos=lambda inst, val: setattr(kolom3_container.bg_rect, "pos", val),
                             size=lambda inst, val: setattr(kolom3_container.bg_rect, "size", val))
        
        kolom3 = BoxLayout(orientation="vertical", size_hint_y=None, height=430, spacing=20)
        
        # Container untuk judul dengan FloatLayout
        riwayat_judul_container = FloatLayout(size_hint_y=None, height=50)
        
        riwayat_label = Label(
            text="[b]RIWAYAT TRANSAKSI[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=18,
            color=(0.2, 0.3, 0.4, 1),
            size_hint_y=None,
            height=30,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            halign="center",
            valign="middle",
        )
        riwayat_label.bind(size=riwayat_label.setter("text_size"))
        riwayat_judul_container.add_widget(riwayat_label)
        kolom3.add_widget(riwayat_judul_container)
        
        # Header tabel riwayat
        header_riwayat = BoxLayout(orientation="horizontal", size_hint_y=None, height=35, spacing=10)
        header_riwayat.add_widget(Label(
            text="[b]Waktu[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=14,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_x=0.25,
            halign="center",
            valign="middle",
        ))
        header_riwayat.add_widget(Label(
            text="[b]No Meja[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=14,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_x=0.2,
            halign="center",
            valign="middle",
        ))
        header_riwayat.add_widget(Label(
            text="[b]Pesanan[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=14,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_x=0.35,
            halign="center",
            valign="middle",
        ))
        header_riwayat.add_widget(Label(
            text="[b]Total[/b]",
            markup=True,
            font_name=fonts.Bold,
            font_size=14,
            color=(0.18, 0.38, 0.54, 1),
            size_hint_x=0.2,
            halign="center",
            valign="middle",
        ))
        kolom3.add_widget(header_riwayat)
        
        # ScrollView untuk data riwayat transaksi
        scroll_container = BoxLayout(orientation="vertical", size_hint_y=None, height=300)
        scroll_container.bind(minimum_height=scroll_container.setter("height"))
        
        # Data riwayat transaksi
        for trx in transaksi_list:
            pesanan_str = ", ".join([f"{item['name']} x{item['qty']}" for item in trx["items"]])
            # Hitung tinggi baris berdasarkan panjang pesanan
            pesanan_lines = len(pesanan_str) // 30 + 1
            row_height = max(35, 25 + pesanan_lines * 15)
            
            # Container untuk setiap baris dengan FloatLayout
            row_container = FloatLayout(size_hint_y=None, height=row_height + 15)
            
            row_riwayat = BoxLayout(orientation="horizontal", size_hint_y=None, height=row_height, spacing=10, pos_hint={'center_x': 0.5, 'center_y': 0.5})
            
            # Kolom waktu
            waktu = Label(
                text=trx["waktu"][:16],  # Ambil hanya tanggal dan jam
                font_name=fonts.Regular,
                font_size=12,
                color=(0.2, 0.3, 0.4, 1),
                size_hint_x=0.25,
                halign="center",
                valign="middle",
            )
            waktu.bind(size=waktu.setter("text_size"))
            row_riwayat.add_widget(waktu)
            
            # Kolom no meja
            no_meja_val = trx["no_meja"]
            from_riwayat = trx.get("from_riwayat", False)
            if from_riwayat:
                no_meja_text = f"{no_meja_val}+" if no_meja_val is not None else "TA+"
            else:
                no_meja_text = f"{no_meja_val:,}" if no_meja_val is not None else "TA"
            no_meja = Label(
                text=no_meja_text,
                font_name=fonts.Bold,
                font_size=12,
                color=(0.18, 0.38, 0.54, 1),
                size_hint_x=0.2,
                halign="center",
                valign="middle",
            )
            row_riwayat.add_widget(no_meja)
            
            # Kolom pesanan
            pesanan = Label(
                text=pesanan_str,
                font_name=fonts.Regular,
                font_size=11,
                color=(0.2, 0.3, 0.4, 1),
                size_hint_x=0.35,
                halign="center",
                valign="middle",
            )
            pesanan.bind(size=pesanan.setter("text_size"))
            row_riwayat.add_widget(pesanan)
            
            # Kolom total
            total = Label(
                text=f"Rp {trx['total']:,}",
                font_name=fonts.Bold,
                font_size=12,
                color=(0.18, 0.38, 0.54, 1),
                size_hint_x=0.2,
                halign="center",
                valign="middle",
            )
            total.bind(size=total.setter("text_size"))
            row_riwayat.add_widget(total)
            
            row_container.add_widget(row_riwayat)
            scroll_container.add_widget(row_container)
        
        # ScrollView untuk data transaksi
        scroll_view = ScrollView(size_hint_y=None, height=300)
        scroll_view.add_widget(scroll_container)
        kolom3.add_widget(scroll_view)
        
        kolom3_container.add_widget(kolom3)
        self.main_layout.add_widget(kolom3_container)
        
        # Spacer akhir untuk memastikan ada ruang yang cukup
        end_spacer = Widget(size_hint_y=None, height=120)
        self.main_layout.add_widget(end_spacer) 