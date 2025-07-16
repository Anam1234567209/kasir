import sqlite3

# Membuat (atau membuka) database baru bernama kasir.db
conn = sqlite3.connect("kasir.db")
c = conn.cursor()

# Membuat tabel produk jika belum ada
c.execute(
    """
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    harga REAL NOT NULL,
    gambar TEXT,
    kategori TEXT DEFAULT 'Makanan'
)
"""
)

# Membuat tabel profil cafe jika belum ada
c.execute(
    """
CREATE TABLE IF NOT EXISTS cafe_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_cafe TEXT NOT NULL DEFAULT 'WAROENG CAFE',
    slogan TEXT DEFAULT 'Nikmati Kelezatan dalam Setiap Gigitan',
    logo_cafe TEXT DEFAULT 'gambar/logo_icon/waroeng_cafe.png',
    alamat_cafe TEXT DEFAULT 'Jl. Contoh No. 123, Kota, Provinsi',
    email_cafe TEXT DEFAULT 'info@waroengcafe.com',
    no_hp_cafe TEXT DEFAULT '+62 812-3456-7890',
    website TEXT DEFAULT 'www.waroengcafe.com',
    jam_operasional TEXT DEFAULT '08:00 - 22:00 WIB',
    instagram TEXT DEFAULT '@waroengcafe'
)
"""
)

# c.execute("""INSERT INTO transaksi ADD COLUMN no_meja INTEGER;""")
# Membuat tabel transaksi jika belum ada
c.execute(
    """
CREATE TABLE IF NOT EXISTS transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    waktu TEXT NOT NULL,
    no_meja INTEGER,
    total INTEGER NOT NULL,
    pembayaran INTEGER NOT NULL,
    kembalian INTEGER NOT NULL
)
"""
)

c.execute(
    """
CREATE TABLE IF NOT EXISTS transaksi_detail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaksi_id INTEGER NOT NULL,
    nama_produk TEXT NOT NULL,
    harga INTEGER NOT NULL,
    qty INTEGER NOT NULL,
    FOREIGN KEY(transaksi_id) REFERENCES transaksi(id)
)
"""
)

# Insert default cafe profile if not exists
c.execute("SELECT COUNT(*) FROM cafe_profile")
if c.fetchone()[0] == 0:
    c.execute(
        """
    INSERT INTO cafe_profile (nama_cafe, slogan, logo_cafe, alamat_cafe, email_cafe, no_hp_cafe, website, jam_operasional, instagram) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            "WAROENG CAFE",
            "Nikmati Kelezatan dalam Setiap Gigitan",
            "gambar/logo_icon/waroeng_cafe.png",
            "Jl. Contoh No. 123, Kota, Provinsi",
            "info@waroengcafe.com",
            "+62 812-3456-7890",
            "www.waroengcafe.com",
            "08:00 - 22:00 WIB",
            "@waroengcafe",
        ),
    )

# Add instagram column if it doesn't exist
try:
    c.execute(
        "ALTER TABLE cafe_profile ADD COLUMN instagram TEXT DEFAULT '@waroengcafe'"
    )
    conn.commit()
except:
    pass  # Column already exists

conn.commit()
conn.close()


def get_all_produk():
    import sqlite3

    conn = sqlite3.connect("kasir.db")
    c = conn.cursor()
    c.execute("SELECT id, nama, harga, gambar, kategori FROM produk")
    result = c.fetchall()
    conn.close()
    return result


def insert_produk(nama, harga, gambar, kategori):
    import sqlite3

    conn = sqlite3.connect("kasir.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO produk (nama, harga, gambar, kategori) VALUES (?, ?, ?, ?)",
        (nama, harga, gambar, kategori),
    )
    conn.commit()
    conn.close()


def delete_produk(pid):
    import sqlite3

    conn = sqlite3.connect("kasir.db")
    c = conn.cursor()
    c.execute("DELETE FROM produk WHERE id=?", (pid,))
    conn.commit()
    conn.close()


def update_produk(pid, nama, harga, gambar, kategori):
    import sqlite3

    conn = sqlite3.connect("kasir.db")
    c = conn.cursor()
    c.execute(
        "UPDATE produk SET nama=?, harga=?, gambar=?, kategori=? WHERE id=?",
        (nama, harga, gambar, kategori, pid),
    )
    conn.commit()
    conn.close()


def insert_transaksi(waktu, no_meja, total, pembayaran, kembalian, items):
    import sqlite3

    conn = sqlite3.connect("kasir.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO transaksi (waktu, no_meja, total, pembayaran, kembalian) VALUES (?, ?, ?, ?, ?)",
        (waktu, no_meja, total, pembayaran, kembalian),
    )
    transaksi_id = c.lastrowid
    for item in items:
        c.execute(
            "INSERT INTO transaksi_detail (transaksi_id, nama_produk, harga, qty) VALUES (?, ?, ?, ?)",
            (transaksi_id, item["name"], item["price"], item["qty"]),
        )
    conn.commit()
    conn.close()


def get_all_transaksi():
    import sqlite3

    conn = sqlite3.connect("kasir.db")
    c = conn.cursor()
    c.execute(
        "SELECT id, waktu, no_meja, total, pembayaran, kembalian FROM transaksi ORDER BY id DESC"
    )
    transaksi = c.fetchall()
    result = []
    for t in transaksi:
        c.execute(
            "SELECT nama_produk, harga, qty FROM transaksi_detail WHERE transaksi_id=?",
            (t[0],),
        )
        items = c.fetchall()
        result.append(
            {
                "id": t[0],
                "waktu": t[1],
                "no_meja": t[2],
                "total": t[3],
                "pembayaran": t[4],
                "kembalian": t[5],
                "items": [{"name": i[0], "price": i[1], "qty": i[2]} for i in items],
            }
        )
    conn.close()
    return result


def delete_transaksi(transaksi_id):
    import sqlite3

    conn = sqlite3.connect("kasir.db")
    c = conn.cursor()
    c.execute("DELETE FROM transaksi_detail WHERE transaksi_id=?", (transaksi_id,))
    c.execute("DELETE FROM transaksi WHERE id=?", (transaksi_id,))
    conn.commit()
    conn.close()


def delete_all_transaksi():
    import sqlite3

    conn = sqlite3.connect("kasir.db")
    c = conn.cursor()
    c.execute("DELETE FROM transaksi_detail")
    c.execute("DELETE FROM transaksi")
    conn.commit()
    conn.close()


def get_cafe_profile():
    import sqlite3

    conn = sqlite3.connect("kasir.db")
    c = conn.cursor()
    c.execute(
        "SELECT nama_cafe, slogan, logo_cafe, alamat_cafe, email_cafe, no_hp_cafe, website, jam_operasional, instagram FROM cafe_profile LIMIT 1"
    )
    result = c.fetchone()
    conn.close()
    if result:
        return {
            "nama_cafe": result[0],
            "slogan": result[1],
            "logo_cafe": result[2],
            "alamat_cafe": result[3],
            "email_cafe": result[4],
            "no_hp_cafe": result[5],
            "website": result[6],
            "jam_operasional": result[7],
            "instagram": result[8],
        }
    return None


def update_cafe_profile(
    nama_cafe,
    slogan,
    logo_cafe,
    alamat_cafe,
    email_cafe,
    no_hp_cafe,
    website,
    jam_operasional,
    instagram,
):
    import sqlite3

    conn = sqlite3.connect("kasir.db")
    c = conn.cursor()
    c.execute(
        """
    UPDATE cafe_profile SET 
    nama_cafe=?, slogan=?, logo_cafe=?, alamat_cafe=?, email_cafe=?, no_hp_cafe=?, website=?, jam_operasional=?, instagram=?
    WHERE id=1
    """,
        (
            nama_cafe,
            slogan,
            logo_cafe,
            alamat_cafe,
            email_cafe,
            no_hp_cafe,
            website,
            jam_operasional,
            instagram,
        ),
    )
    conn.commit()
    conn.close()
