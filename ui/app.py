
import streamlit as st
import requests
from datetime import date

# --------------------------------
# AYARLAR
# --------------------------------

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Akıllı Buzdolabım",
    page_icon="🥑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------
# TASARIM
# --------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ANA ARKA PLAN */

.stApp {
    background-color: #E9EDE5;
}

/* YAN MENÜ */

[data-testid="stSidebar"] {
    background-color: #1F3A32;
}

[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: #FFFFFF !important;
}

/* ANA BAŞLIKLAR */

.main-title {
    font-size: 36px;
    font-weight: 800;
    color: #203A31;
    margin-bottom: 5px;
}

.subtitle {
    color: #68796E;
    font-size: 15px;
    margin-bottom: 28px;
}

/* İSTATİSTİK KARTLARI */

.metric-card {
    background: #D6E1D3;
    padding: 23px;
    border-radius: 17px;
    border: 1px solid #C2D1BF;
    min-height: 125px;
    box-shadow: 0 3px 10px rgba(31, 58, 50, 0.04);
    margin-bottom: 15px;
}

.metric-label {
    color: #52695A;
    font-size: 14px;
    font-weight: 600;
}

.metric-value {
    color: #203A31;
    font-size: 30px;
    font-weight: 800;
    margin-top: 8px;
}

/* BÖLÜM BAŞLIKLARI */

.section-title {
    color: #203A31;
    font-size: 24px;
    font-weight: 800;
    margin-top: 25px;
    margin-bottom: 15px;
}

/* ÜRÜN KARTLARI */

[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #F0F1E9;
    border: 1px solid #CFD9CB;
    border-radius: 16px;
    padding: 5px;
    box-shadow: 0 3px 10px rgba(31, 58, 50, 0.04);
}

.product-name {
    color: #203A31;
    font-size: 20px;
    font-weight: 800;
}

.product-detail {
    color: #68796E;
    font-size: 13px;
}

/* BUTONLAR */

div.stButton > button {
    background-color: #496B56;
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    transition: 0.2s;
}

div.stButton > button:hover {
    background-color: #203A31;
    color: white;
    border: none;
}

/* FORM ALANI */

div[data-testid="stForm"] {
    background-color: #DDE5D8;
    padding: 22px;
    border-radius: 17px;
    border: 1px solid #C2D1BF;
}

/* GİRİŞ ALANLARI */

.stTextInput input,
.stNumberInput input {
    background-color: #F5F6F0;
    border-radius: 9px;
    border-color: #C5D2C2;
}

.stSelectbox div[data-baseweb="select"] > div {
    background-color: #F5F6F0;
    border-radius: 9px;
}

/* FORM KAYDET BUTONU */

.stFormSubmitButton button {
    background-color: #315B45;
    color: white;
    border-radius: 11px;
    font-weight: 700;
    min-height: 45px;
}

.stFormSubmitButton button:hover {
    background-color: #203A31;
    color: white;
}

/* BİLGİ MESAJLARI */

div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* AYIRICILAR */

hr {
    border-color: #C8D3C6;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------
# API FONKSİYONLARI
# --------------------------------

def api_istek_yap(method, endpoint, **kwargs):
    try:
        cevap = requests.request(
            method,
            f"{API_URL}{endpoint}",
            timeout=15,
            **kwargs
        )
        cevap.raise_for_status()
        return cevap

    except requests.RequestException as hata:
        st.error(f"İşlem başarısız: {hata}")
        return None


def urunleri_getir():
    cevap = api_istek_yap("GET", "/items/")

    if cevap:
        return cevap.json()

    return []


# --------------------------------
# YAN MENÜ
# --------------------------------

with st.sidebar:

    st.markdown("# 🥑 Akıllı Mutfak")

    st.caption("Buzdolabı ve stok yönetimi")

    st.divider()

    sayfa = st.radio(
        "MENÜ",
        ["Ana Sayfa", "Ürün Ekle"]
    )

    st.divider()

    st.markdown("### 🌱 Akıllı Yaşam")

    st.caption(
        "Daha az israf, daha fazla tasarruf."
    )

    st.divider()

    st.caption("Akıllı Tarif ve Buzdolabı Takibi")


# --------------------------------
# VERİLER
# --------------------------------

urunler = urunleri_getir()

toplam = len(urunler)

tuketilen = sum(
    1 for u in urunler if u["is_consumed"]
)

israf = sum(
    1 for u in urunler if u["is_wasted"]
)

stokta = sum(
    1 for u in urunler
    if not u["is_consumed"] and not u["is_wasted"]
)

stok_degeri = sum(
    float(u["price_tl"]) * float(u["quantity"])
    for u in urunler
    if not u["is_consumed"] and not u["is_wasted"]
)


# --------------------------------
# ANA SAYFA
# --------------------------------

if sayfa == "Ana Sayfa":

    st.markdown(
        '<div class="main-title">Merhaba! 👋</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Mutfağındaki ürünleri takip et, israfı azalt ve tasarruf et.'
        '</div>',
        unsafe_allow_html=True
    )

    # İSTATİSTİK KARTLARI

    c1, c2, c3, c4 = st.columns(4)

    kartlar = [
        (c1, "📦 Toplam Ürün", toplam),
        (c2, "🧊 Aktif Stok", stokta),
        (c3, "🥗 Tüketilen", tuketilen),
        (c4, "⚠️ İsraf Edilen", israf)
    ]

    for kolon, baslik, deger in kartlar:

        with kolon:

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{baslik}</div>
                <div class="metric-value">{deger}</div>
            </div>
            """, unsafe_allow_html=True)

    # AKTİF STOK DEĞERİ

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">💰 Aktif Stok Değeri</div>
        <div class="metric-value">{stok_degeri:,.2f} TL</div>
    </div>
    """, unsafe_allow_html=True)

    # ÜRÜN LİSTESİ BAŞLIĞI

    st.markdown(
        '<div class="section-title">🧊 Buzdolabındaki Ürünler</div>',
        unsafe_allow_html=True
    )

    if urunler:

        arama = st.text_input(
            "🔍 Ürün ara",
            placeholder="Örneğin süt, peynir, tavuk..."
        )

        filtre = st.selectbox(
            "Ürün durumuna göre filtrele",
            ["Tümü", "Stokta", "Tüketildi", "İsraf Edildi"]
        )

        for urun in urunler:

            if arama.lower() not in urun["name"].lower():
                continue

            if filtre == "Stokta" and (
                urun["is_consumed"] or urun["is_wasted"]
            ):
                continue

            if filtre == "Tüketildi" and not urun["is_consumed"]:
                continue

            if filtre == "İsraf Edildi" and not urun["is_wasted"]:
                continue

            # ÜRÜN DURUMU

            if urun["is_consumed"]:
                durum = "🥗 Tüketildi"

            elif urun["is_wasted"]:
                durum = "⚠️ İsraf Edildi"

            else:
                durum = "🟢 Stokta"

            # SON KULLANMA TARİHİ KONTROLÜ

            try:

                skt = date.fromisoformat(
                    urun["expiration_date"]
                )

                kalan_gun = (skt - date.today()).days

                if not urun["is_consumed"] and not urun["is_wasted"]:

                    if kalan_gun < 0:
                        uyari = "🔴 Son kullanma tarihi geçmiş"

                    elif kalan_gun <= 3:
                        uyari = "🟠 Son kullanma tarihi yaklaşıyor"

                    else:
                        uyari = "🟢 Son kullanma tarihi uygun"

                else:
                    uyari = ""

            except (ValueError, TypeError):
                uyari = ""

            # ÜRÜN KARTI

            with st.container(border=True):

                sol, orta, sag = st.columns([3, 2, 2])

                with sol:

                    st.markdown(
                        f'<div class="product-name">{urun["name"]}</div>',
                        unsafe_allow_html=True
                    )

                    st.caption(urun["category"])

                    st.write(
                        f"Miktar: {urun['quantity']} {urun['unit']}"
                    )

                with orta:

                    st.write(f"💰 {urun['price_tl']} TL")

                    st.write(
                        f"📅 SKT: {urun['expiration_date']}"
                    )

                    if uyari:
                        st.caption(uyari)

                with sag:

                    st.write(durum)

                    if not urun["is_consumed"] and not urun["is_wasted"]:

                        if st.button(
                            "Tüketildi",
                            key=f"tuket_{urun['id']}",
                            use_container_width=True
                        ):

                            sonuc = api_istek_yap(
                                "PATCH",
                                f"/items/{urun['id']}/consume"
                            )

                            if sonuc:
                                st.rerun()

                        if st.button(
                            "İsraf Edildi",
                            key=f"israf_{urun['id']}",
                            use_container_width=True
                        ):

                            sonuc = api_istek_yap(
                                "PATCH",
                                f"/items/{urun['id']}/waste"
                            )

                            if sonuc:
                                st.rerun()

                    if st.button(
                        "🗑️ Sil",
                        key=f"sil_{urun['id']}",
                        use_container_width=True
                    ):

                        sonuc = api_istek_yap(
                            "DELETE",
                            f"/items/{urun['id']}"
                        )

                        if sonuc:
                            st.rerun()

    else:

        st.info(
            "Henüz kayıtlı ürün bulunmuyor. Ürün ekleyerek başlayabilirsin."
        )


# --------------------------------
# ÜRÜN EKLEME SAYFASI
# --------------------------------

elif sayfa == "Ürün Ekle":

    st.markdown(
        '<div class="main-title">➕ Yeni Ürün Ekle</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Buzdolabına yeni bir ürün kaydet.'
        '</div>',
        unsafe_allow_html=True
    )

    with st.form("urun_formu"):

        ad = st.text_input(
            "Ürün Adı",
            placeholder="Örn: Süt"
        )

        kategori = st.selectbox(
            "Kategori",
            [
                "Süt Ürünleri",
                "Et Ürünleri",
                "Sebze",
                "Meyve",
                "İçecek",
                "Bakliyat",
                "Diğer"
            ]
        )

        col1, col2 = st.columns(2)

        with col1:

            miktar = st.number_input(
                "Miktar",
                min_value=0.1,
                value=1.0
            )

            fiyat = st.number_input(
                "Birim Fiyatı (TL)",
                min_value=0.0,
                value=0.0
            )

        with col2:

            birim = st.selectbox(
                "Birim",
                ["adet", "kg", "gram", "litre", "paket"]
            )

            skt = st.date_input(
                "Son Kullanma Tarihi",
                min_value=date.today()
            )

        kaydet = st.form_submit_button(
            "💾 Ürünü Kaydet",
            use_container_width=True
        )

        if kaydet:

            if not ad.strip():

                st.warning("Lütfen ürün adını gir.")

            else:

                sonuc = api_istek_yap(
                    "POST",
                    "/items/",
                    params={
                        "name": ad,
                        "category": kategori,
                        "quantity": miktar,
                        "unit": birim,
                        "price_tl": fiyat,
                        "expiration_date": str(skt)
                    }
                )

                if sonuc:

                    st.success(
                        "Ürün başarıyla kaydedildi!"
                    )

                    st.rerun()
