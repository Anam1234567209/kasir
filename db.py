import sqlite3

# Membuat (atau membuka) database baru bernama kasir.db
conn = sqlite3.connect("kasir.db")
c = conn.cursor()

# Membuat tabel produk jika belum ada
c.execute("""
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    harga REAL NOT NULL,
    gambar TEXT,
    kategori TEXT DEFAULT 'Makanan'
)
""")

# Membuat tabel transaksi jika belum ada
c.execute("""
CREATE TABLE IF NOT EXISTS transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    waktu TEXT NOT NULL,
    total INTEGER NOT NULL,
    pembayaran INTEGER NOT NULL,
    kembalian INTEGER NOT NULL
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS transaksi_detail (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaksi_id INTEGER NOT NULL,
    nama_produk TEXT NOT NULL,
    harga INTEGER NOT NULL,
    qty INTEGER NOT NULL,
    FOREIGN KEY(transaksi_id) REFERENCES transaksi(id)
)
""")

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


def insert_transaksi(waktu, total, pembayaran, kembalian, items):
    import sqlite3
    conn = sqlite3.connect("kasir.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO transaksi (waktu, total, pembayaran, kembalian) VALUES (?, ?, ?, ?)",
        (waktu, total, pembayaran, kembalian)
    )
    transaksi_id = c.lastrowid
    for item in items:
        c.execute(
            "INSERT INTO transaksi_detail (transaksi_id, nama_produk, harga, qty) VALUES (?, ?, ?, ?)",
            (transaksi_id, item["name"], item["price"], item["qty"])
        )
    conn.commit()
    conn.close()


def get_all_transaksi():
    import sqlite3
    conn = sqlite3.connect("kasir.db")
    c = conn.cursor()
    c.execute("SELECT id, waktu, total, pembayaran, kembalian FROM transaksi ORDER BY id DESC")
    transaksi = c.fetchall()
    result = []
    for t in transaksi:
        c.execute("SELECT nama_produk, harga, qty FROM transaksi_detail WHERE transaksi_id=?", (t[0],))
        items = c.fetchall()
        result.append({
            "id": t[0],
            "waktu": t[1],
            "total": t[2],
            "pembayaran": t[3],
            "kembalian": t[4],
            "items": [{"name": i[0], "price": i[1], "qty": i[2]} for i in items]
        })
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
