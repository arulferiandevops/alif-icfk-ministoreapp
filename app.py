import streamlit as st
import streamlit.components.v1 as components


# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="Toko Buku dan Alat Tulis Alif",
    layout="centered"
)


# =========================================================
# DESAIN KHUSUS (SIMPLE & RAMAH ANAK - WARNA SOLID)
# =========================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700;800&display=swap');

    /* Font ramah anak dan mudah dibaca */
    html, body, [class*="css"], .stApp {
        font-family: 'Quicksand', sans-serif;
    }

    /* Heading dengan warna hijau solid dan ramah */
    h1, h2, h3, h4 {
        font-family: 'Quicksand', sans-serif !important;
        font-weight: 700 !important;
        color: #166534;
    }

    /* Header Banner Sederhana (Warna Hijau Solid Pastel, Tanpa Gradient) */
    .kids-header {
        background-color: #DCFCE7;
        border: 2px solid #86EFAC;
        border-radius: 20px;
        padding: 24px 16px;
        text-align: center;
        margin-bottom: 24px;
    }

    .kids-header h1 {
        color: #15803D !important;
        font-size: 2rem !important;
        margin: 0;
    }

    .kids-header h3 {
        color: #166534 !important;
        font-size: 1.2rem !important;
        margin: 8px 0 4px 0;
    }

    .kids-header p {
        color: #374151;
        font-size: 0.9rem;
        margin: 0;
    }

    /* Tombol melengkung dengan warna hijau solid */
    .stButton > button {
        font-family: 'Quicksand', sans-serif;
        font-weight: 700;
        font-size: 1rem;
        border-radius: 14px;
        padding: 0.55rem 1.2rem;
        background-color: #16A34A !important;
        color: #FFFFFF !important;
        border: none;
        transition: all 0.2s ease-in-out;
    }

    .stButton > button:hover {
        background-color: #15803D !important;
        color: #FFFFFF !important;
        transform: translateY(-2px);
    }

    /* Input & Selectbox dengan sudut melengkung dan border hijau lembut */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        border-radius: 14px !important;
        border: 1.5px solid #86EFAC !important;
    }

    /* Notifikasi melengkung */
    .stAlert {
        border-radius: 14px !important;
        font-family: 'Quicksand', sans-serif;
        font-weight: 600;
    }

    /* Garis pemisah */
    hr {
        margin: 1.5rem 0 !important;
        border-color: #BBF7D0 !important;
    }

    /* Pengaturan Cetak / Print Struk */
    @media print {
        [data-testid="stSidebar"],
        [data-testid="stHeader"],
        footer,
        .kids-header,
        .stButton,
        iframe,
        div[data-testid="stSelectbox"],
        div[data-testid="stNumberInput"],
        div[data-testid="stCheckbox"],
        div[data-testid="stAlert"] {
            display: none !important;
        }

        .stApp {
            background-color: #FFFFFF !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# DATA PRODUK
# =========================================================

produk = {
    "Buku Matematika": {
        "harga": 25000,
        "stok": 10,
        "kategori": "Buku"
    },

    "Buku Fisika": {
        "harga": 20000,
        "stok": 15,
        "kategori": "Buku"
    },

    "Buku Tulis": {
        "harga": 6000,
        "stok": 25,
        "kategori": "Buku"
    },

    "Pensil": {
        "harga": 3000,
        "stok": 50,
        "kategori": "Alat Tulis"
    },

    "Pulpen": {
        "harga": 5000,
        "stok": 40,
        "kategori": "Alat Tulis"
    },

    "Penghapus": {
        "harga": 2000,
        "stok": 30,
        "kategori": "Alat Tulis"
    },

    "Penggaris": {
        "harga": 4000,
        "stok": 20,
        "kategori": "Alat Tulis"
    }
}


# =========================================================
# SESSION STATE
# =========================================================

if "keranjang" not in st.session_state:
    st.session_state.keranjang = []

if "transaksi" not in st.session_state:
    st.session_state.transaksi = 0

if "pembayaran_berhasil" not in st.session_state:
    st.session_state.pembayaran_berhasil = False


# =========================================================
# FUNCTION
# =========================================================

def rupiah(angka):
    """
    Mengubah angka menjadi format Rupiah.
    Contoh:
    25000 -> Rp25.000
    """

    return f"Rp{angka:,.0f}".replace(",", ".")


def hitung_subtotal(harga, jumlah):
    """
    Menghitung harga x jumlah barang.
    """

    return harga * jumlah


def hitung_total(keranjang):
    """
    Menghitung total semua barang
    yang ada di keranjang.
    """

    total = 0

    for item in keranjang:
        total += item["subtotal"]

    return total


def hitung_diskon(total, member):
    """
    Menghitung diskon.

    Aturan:
    - Member mendapatkan diskon 5%
    - Belanja >= Rp100.000 mendapatkan diskon 10%
    """

    diskon = 0

    # Diskon berdasarkan total belanja
    if total >= 100000:
        diskon += total * 0.10

    # Diskon member
    if member:
        diskon += total * 0.05

    return diskon


def hitung_kembalian(bayar, total):
    """
    Menghitung uang kembalian.
    """

    return bayar - total


def tambah_ke_keranjang(nama_produk, jumlah):
    """
    Menambahkan produk ke keranjang.
    """

    data_produk = produk[nama_produk]

    harga = data_produk["harga"]

    subtotal = hitung_subtotal(
        harga,
        jumlah
    )

    item = {
        "produk": nama_produk,
        "harga": harga,
        "jumlah": jumlah,
        "subtotal": subtotal
    }

    st.session_state.keranjang.append(item)


def hapus_item(index):
    """
    Menghapus item berdasarkan index.
    """

    st.session_state.keranjang.pop(index)


def reset_transaksi():
    """
    Menghapus semua data transaksi.
    """

    st.session_state.keranjang = []

    st.session_state.pembayaran_berhasil = False


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="kids-header">
    <h1>Toko Buku dan Alat Tulis Alif</h1>
    <h3>Aplikasi Kasir</h3>
    <p>Project Akhir Islamic Coding for Kids</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("Toko Buku dan Alat Tulis Alif")

    st.write("Menu")

    st.write("Produk")
    st.write("Keranjang")
    st.write("Pembayaran")
    st.write("Struk")


# =========================================================
# PILIH PRODUK
# =========================================================

st.header("Pilih Produk")

with st.container(border=True):

    nama_produk = st.selectbox(
        "Pilih Produk",
        list(produk.keys())
    )

    # Ambil data produk
    data = produk[nama_produk]

    harga_produk = data["harga"]
    stok_produk = data["stok"]
    kategori_produk = data["kategori"]

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Kategori**")
        st.write(kategori_produk)

    with col2:
        st.write("**Harga**")
        st.write(rupiah(harga_produk))

    st.write(f"Stok tersedia: **{stok_produk}**")

    jumlah = st.number_input(
        "Jumlah",
        min_value=1,
        max_value=stok_produk,
        value=1,
        step=1
    )

    subtotal = hitung_subtotal(
        harga_produk,
        jumlah
    )

    st.info(f"Subtotal: **{rupiah(subtotal)}**")

    if st.button(
        "Tambah ke Keranjang",
        use_container_width=True
    ):
        tambah_ke_keranjang(
            nama_produk,
            jumlah
        )
        st.success(f"{nama_produk} berhasil ditambahkan!")


st.divider()


# =========================================================
# KERANJANG
# =========================================================

st.header("Keranjang")

with st.container(border=True):

    if len(st.session_state.keranjang) == 0:
        st.info("Keranjang masih kosong.")
    else:
        # Menampilkan setiap item
        for index, item in enumerate(st.session_state.keranjang):
            col1, col2, col3 = st.columns([4, 2, 1])

            with col1:
                st.write(f"**{item['produk']}**")
                st.caption(f"{item['jumlah']} x {rupiah(item['harga'])}")

            with col2:
                st.write(rupiah(item["subtotal"]))

            with col3:
                if st.button("Hapus", key=f"hapus_{index}"):
                    hapus_item(index)
                    st.rerun()


# =========================================================
# PERHITUNGAN TOTAL
# =========================================================

total_sebelum_diskon = hitung_total(
    st.session_state.keranjang
)

st.divider()

with st.container(border=True):

    st.subheader("Ringkasan Belanja")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Total Belanja")

    with col2:
        st.write(f"**{rupiah(total_sebelum_diskon)}**")

    member = st.checkbox("Pelanggan Member (diskon 5%)")

    diskon = hitung_diskon(
        total_sebelum_diskon,
        member
    )

    if diskon > 0:
        st.write(f"Diskon: **{rupiah(diskon)}**")
    else:
        st.write("Diskon: **Rp0**")

    total_akhir = total_sebelum_diskon - diskon

    st.success(f"### Total Bayar: {rupiah(total_akhir)}")


# =========================================================
# PEMBAYARAN
# =========================================================

st.divider()

st.header("Pembayaran")

with st.container(border=True):

    bayar = st.number_input(
        "Uang Pembayaran",
        min_value=0,
        step=1000,
        value=0
    )

    if st.button(
        "BAYAR",
        use_container_width=True
    ):
        # Cek keranjang
        if len(st.session_state.keranjang) == 0:
            st.warning("Keranjang masih kosong!")

        # Cek pembayaran
        elif bayar < total_akhir:
            kekurangan = total_akhir - bayar
            st.error(f"Uang kurang {rupiah(kekurangan)}")

        else:
            # Hitung kembalian
            kembalian = hitung_kembalian(
                bayar,
                total_akhir
            )

            # Tambah nomor transaksi
            st.session_state.transaksi += 1

            # Tandai berhasil
            st.session_state.pembayaran_berhasil = True

            st.success("Pembayaran berhasil!")


# =========================================================
# STRUK
# =========================================================

if st.session_state.pembayaran_berhasil:

    kembalian = hitung_kembalian(
        bayar,
        total_akhir
    )

    st.divider()

    with st.container(border=True):

        st.header("Struk Belanja")

        nomor_transaksi = f"TRX-{st.session_state.transaksi:04d}"

        st.write(f"**Nomor Transaksi:** {nomor_transaksi}")
        st.write("Terima kasih sudah berbelanja!")

        st.divider()

        # Daftar barang
        for item in st.session_state.keranjang:
            st.write(f"**{item['produk']}**")
            st.write(f"{item['jumlah']} x {rupiah(item['harga'])} = **{rupiah(item['subtotal'])}**")

        st.divider()

        # Ringkasan
        st.write(f"Total Belanja: **{rupiah(total_sebelum_diskon)}**")
        st.write(f"Diskon: **{rupiah(diskon)}**")
        st.write(f"Total Bayar: **{rupiah(total_akhir)}**")
        st.write(f"Uang Dibayar: **{rupiah(bayar)}**")
        st.write(f"Kembalian: **{rupiah(kembalian)}**")

        st.success("Terima kasih! Sudah Berbelanja di Toko Kami!")

        # Teks struk terformat untuk cetak / simpan
        struk_teks = (
            "========================================\n"
            "   TOKO BUKU DAN ALAT TULIS ALIF\n"
            "          APLIKASI KASIR\n"
            "========================================\n"
            f"Nomor Transaksi : {nomor_transaksi}\n"
            "----------------------------------------\n"
        )
        for item in st.session_state.keranjang:
            struk_teks += f"{item['produk']:<20} {item['jumlah']}x {rupiah(item['harga']):>10}\n"
            struk_teks += f"Subtotal: {rupiah(item['subtotal']):>30}\n"

        struk_teks += (
            "----------------------------------------\n"
            f"Total Belanja   : {rupiah(total_sebelum_diskon):>20}\n"
            f"Diskon          : {rupiah(diskon):>20}\n"
            f"Total Bayar     : {rupiah(total_akhir):>20}\n"
            f"Uang Dibayar    : {rupiah(bayar):>20}\n"
            f"Kembalian       : {rupiah(kembalian):>20}\n"
            "========================================\n"
            " Terima kasih! Sudah Berbelanja di Toko Kami!\n"
            "========================================\n"
        )

        col_print1, col_print2 = st.columns(2)

        with col_print1:
            # Tombol cetak langsung lewat browser print dialog
            components.html(
                """
                <button onclick="window.parent.print()" style="
                    width: 100%;
                    background-color: #16A34A;
                    color: #FFFFFF;
                    border: none;
                    padding: 10px 16px;
                    font-family: 'Quicksand', sans-serif;
                    font-size: 15px;
                    font-weight: 700;
                    border-radius: 12px;
                    cursor: pointer;
                ">
                    Cetak Struk
                </button>
                """,
                height=55
            )

        with col_print2:
            # Tombol simpan teks struk
            st.download_button(
                label="Simpan Struk",
                data=struk_teks,
                file_name=f"struk_{nomor_transaksi}.txt",
                mime="text/plain",
                use_container_width=True
            )

        if st.button(
            "Transaksi Baru",
            use_container_width=True
        ):
            reset_transaksi()
            st.rerun()