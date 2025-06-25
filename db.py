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
