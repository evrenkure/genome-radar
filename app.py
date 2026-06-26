import streamlit as st

# Sayfa Yapısı: Geniş ekran modu ve temiz bir görünüm
st.set_page_config(layout="wide", page_title="Genome Radar")

# --- CSS İLE GÖRSEL GÜZELLEŞTİRME (MOBİL ODAKLI & KOMPAKT) ---
st.markdown("""
    <style>
    /* Sayfanın genel üst ve alt boşluklarını daraltır */
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    
    /* Streamlit'in kendi container (border=True) kutularını özelleştirir */
    div[data-testid="stContainer"] {
        padding: 10px 15px !important;  /* İç boşlukları ciddi oranda azaltır, kutuyu küçültür */
        margin-bottom: -10px !important; /* Kutuların alt alta çok açık durmasını engeller */
        border-radius: 6px !important;   /* Köşeleri hafifçe yumuşatır */
        background-color: #1e1e1e !important; /* Kutunun arkasını hafif koyu/gri yapar (isteğe bağlı) */
        border: 1px solid #333333 !important; /* İnce ve gözü yormayan net bir çerçeve */
    }
    
    /* Detayları gösteren expander kutusunun çizgisini ve gölgesini siler */
    div[data-testid="stExpander"] { 
        border: none !important; 
        box-shadow: none !important;
        margin-top: 5px !important;
    }
    
    /* Küçük etiketlerin (Gen, Mutasyon) yazı boyutunu telefona göre ayarlar */
    .stMarkdown p {
        font-size: 14px !important;
        margin-bottom: 2px !important;
    }
    </style>
""", unsafe_allow_html=True)

#makaleleri excel'den okumak
import streamlit as st
import pandas as pd
try:
    df = pd.read_excel("makaleler.xlsx") #bilgisayardan açar
    df = df.fillna("") # Excel boş hücreleri temizler
    MAKALELER = df.to_dict(orient="records") #tabloyu kodun beklediği formata dönüştürür
except FileNotFoundError:
    MAKALELER = [] # Eğer henüz 2. adımdaki Excel'i oluşturmadıysan kod patlamasın diye yedek plan:

# --- 2. ÜST PANEL & BAŞLIK ---
st.title("🧬 Genome Radar")
st.markdown("A curated personal knowledge base for genomic research.")
st.markdown(
    """
    <p style="color: #FFD700; font-weight: bold;">
    I do not claim any rights over the original papers; all credits belong to their respective authors.<br></p>
    <p>If you want your paper to be removed, e-mail: evrenkure@gmail.com
    </p>
    """, 
    unsafe_allow_html=True
)
st.markdown("---")


# --- 3. SOL PANEL (GEN VE METOT FİLTRELERİ - LİSTE DESTEKLİ) ---
#birden fazla gen olması durumunda, mevcut_genler parametresine geçmeden önce ayıklıyoruz
gen_havuzu = []
for m in MAKALELER:
    if isinstance(m["gen"], list):
        gen_havuzu.extend(m["gen"])  # Eğer listedeyse içindeki tüm genleri ekle
    else:
        gen_havuzu.append(m["gen"])   # Tek bir metinse direkt ekle

# --- FİLTRELEME İÇİN ÖN HAZIRLIK ---
# (Bu kısmı kodunun en başına, veri yükledikten hemen sonra koy)
mevcut_genler = sorted(list(set(gen_havuzu)))
mevcut_metotlar = sorted(list(set([m["metot"] for m in MAKALELER])))
mevcut_kanserler = [k for k in df['kanser_turu'].unique().tolist() if k != ""]
mevcut_tipler = [k for k in df['tipler'].unique().tolist() if k != ""]


# --- 3. SOL PANEL (SIDEBAR) ---
with st.sidebar:
    st.header("🔍 Quick Filters")

    # 1. Gen Seçimi
    secilen_gen = st.selectbox("Gene:", ["All"] + mevcut_genler)
    
    # 2. Metot Seçimi
    secilen_metot = st.selectbox("Method:", ["All"] + mevcut_metotlar) #in vivo in vitro clinic computational ml etc
    
    # 3. Kanser Seçimi
    secilen_kanser = st.selectbox("Cancer Type:", ["All"] + mevcut_kanserler)

    secilen_tip = st.selectbox("Article Type:", ["All"] + mevcut_tipler) #Review, Experimental, Computational, Clinical Trial
    
    st.markdown("---")
    st.caption("Idea & Developer: Evren Keskin")
    st.caption("Personal Open Source Project")
    st.caption("📧 [evrenkure@gmail.com](mailto:eposta@adresin.com) | 🔗 [LinkedIn](https://www.linkedin.com/in/evrenkure/)")

# --- 4. FİLTRELEME MANTIĞI (DÜZELTİLMİŞ) ---
filtreli_liste = MAKALELER

# 1. Gen Filtresi (Çoklu destekli)
if secilen_gen != "All":
    yeni_filtreli = []
    for m in filtreli_liste:
        # İki tarafı da string'e çevirip kontrol et ki hata çıkmasın
        gen_data = m["gen"]
        if isinstance(gen_data, list):
            if secilen_gen in gen_data:
                yeni_filtreli.append(m)
        elif str(gen_data) == str(secilen_gen):
            yeni_filtreli.append(m)
    filtreli_liste = yeni_filtreli

# 2. Metot Filtresi
if secilen_metot != "All":
    filtreli_liste = [m for m in filtreli_liste if str(m["metot"]) == str(secilen_metot)]

if secilen_kanser != "All":
    filtreli_liste = [m for m in filtreli_liste if str(m["kanser_turu"]) == str(secilen_kanser)]

if secilen_tip != "All":
    filtreli_liste = [m for m in filtreli_liste if str(m["tipler"]) == str(secilen_tip)]

# --- 5. ORTA PANEL (Ekrana Basma Alanı) ---
if not filtreli_liste:
    st.info("Bu filtre kombinasyonuna uyan bir makale henüz eklenmemiş.")
else:
    for makale in filtreli_liste:
        with st.container(border=True):
            # Eğer gen kısmı Excel'de liste gibi yazıldıysa veya düz metinse ayıkla
            if isinstance(makale['gen'], list):
                gen_gosterimi = ", ".join(makale['gen'])
            else:
                # Excel'den okurken bazen string formatında gelebilir, tırnakları temizle
                gen_gosterimi = str(makale['gen']).replace("[", "").replace("]", "").replace("'", "")
            
            # Tamamen alt alta (satır satır) duracak tasarım:
            st.markdown(f"**🧬 Gene:** `{gen_gosterimi}`")
            st.markdown(f"**⚡ Mutation:** `{makale['mutasyon']}`")
            st.markdown(f"**🧪 Method:** `{makale['metot']}`")
            st.markdown(f"**⭐ Special Keywords** `{makale['special_keywords']}`")
            
            # Senin kendi ellerinle yazdığın o değerli tıbbi özet:
            st.markdown(f"{makale['mikro_ozet']}")
                
            # Orijinal akademik detayları gizleyen akordeon buton
            with st.expander("🔬 Original Academic Details"):
                st.write(f"**Paper Title:** {makale['orijinal_baslik']}")
                st.page_link(makale["link"], label="Paper Link Pubmed", icon="🔗")

            with st.expander("🔬 Deep Dive"):
                st.markdown(
    """<small style="color: grey; line-height: 1.0; display: block;">
    These are personal notes, may not reflect the full scope of the original work.<br>
    Please refer to the source for definitive information.
    </small><br>""", 
    unsafe_allow_html=True
)
                st.write(f"**Paper Title:** {makale['orijinal_baslik']}")
                st.page_link(makale["link"], label="Paper Link Pubmed", icon="🔗")