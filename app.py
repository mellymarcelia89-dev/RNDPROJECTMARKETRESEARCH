import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
import base64
import io
from pathlib import Path

# --- CONFIG ---
st.set_page_config(page_title="E-Bike Market Intelligence", page_icon="⚡", layout="wide", initial_sidebar_state="expanded")

# --- DATABASE USER (MULTI-USER) ---
# Kamu bisa tambah user di sini sesuai kebutuhan
USER_DB = {
    "admin": {"pw": "ebike2026", "role": "Full Access"},
    "research": {"pw": "ebike_data", "role": "Data Analyst"},
    "marketing": {"pw": "ebike_smart", "role": "Marketing"}
}

# --- FUNGSI UNTUK MERENDER GAMBAR LOKAL KE BACKGROUND ---
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# --- LOAD ASSETS (BACKGROUND & LOGO) ---
path_foto = os.path.join("assets", "Foto Sepeda Listrik.webp") 
bin_str = get_base64_of_bin_file(path_foto)

path_logo = os.path.join("assets", "logo.png") 
logo_str = get_base64_of_bin_file(path_logo)

# --- SISTEM LOGIN REVISI (AESTHETIC & RAPIH) ---
def login_page():
    # CSS KHUSUS LOGIN (Glassmorphism Effect)
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.8)), 
                        url("data:image/webp;base64,{bin_str if bin_str else ""}");
            background-size: cover !important;
            background-position: center !important;
        }}
        /* Container utama login biar gak melayang gak jelas */
        .login-box {{
            background: transparent;            /* Jadi transparan total */
            backdrop-filter: none;              /* Efek buram hilang */
            padding: 40px;
            border: none;                       /* Garis pinggir hilang */
            box-shadow: none;                   /* Bayangan hilang */
        }}
        .login-title {{
            font-family: 'Inter', sans-serif;
            font-weight: 900;
            font-size: 52px;
            text-align: center;
            margin-bottom: 5px; /* Kurangi margin bawah agar dekat dengan tulisan R&D */
            
            /* EFEK GRADASI TEKS */
            background: linear-gradient(to bottom, #ffffff 40%, #60a5fa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            
            /* EFEK CAHAYA (GLOW) */
            filter: drop-shadow(0px 0px 10px rgba(96, 165, 250, 0.5));
            text-transform: uppercase;
            letter-spacing: -1px;
        }}
        /* Menghilangkan border default streamlit di tabs */
        .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
        .stTabs [data-baseweb="tab"] {{
            background-color: rgba(255,255,255,0.05);
            border-radius: 10px;
            padding: 10px 20px;
            color: white !important;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # PENGGUNAAN TABS UNTUK HOME, LOGIN, ABOUT
        tab_login, tab_home, tab_about = st.tabs(["ACCESS SYSTEM", "HOME", "ABOUT"])
        
        with tab_login:
            st.markdown("<div class='login-box'>", unsafe_allow_html=True)
            st.markdown("<div class='login-title'>E-BIKE MARKET RESEARCH</div>", unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; color:#ffffff; font-family:\"Poppins\", sans-serif; font-style:normal; font-size:15px; margin-top:-10px; margin-bottom:35px; font-weight:500; letter-spacing:4px; text-shadow: 0px 0px 15px rgba(255,255,255,0.6), 2px 2px 10px rgba(0,0,0,1); text-transform:uppercase;'>by Research & Development</p>", unsafe_allow_html=True)
            user = st.text_input("Username", placeholder="Masukkan ID Anda...")
            pw = st.text_input("Password", type="password", placeholder="••••••••")
            
            # FITUR LUPA PASSWORD (Sederhana via Pop-up)
            with st.expander("Forgot Password?"):
                st.info("Silakan hubungi R&D Departement Hub atau Admin IT untuk reset password Anda.")
            
            if st.button("AUTHENTICATE", width="stretch", type="primary"):
                if user in USER_DB and USER_DB[user]["pw"] == pw:
                    st.session_state["logged_in"] = True
                    st.session_state["user_now"] = user
                    st.session_state["role_now"] = USER_DB[user]["role"]
                    st.success(f"Selamat Datang {user.capitalize()}! Mengalihkan...")
                    st.rerun()
                else:
                    st.error("Credential tidak valid. Coba lagi!")
            st.markdown("</div>", unsafe_allow_html=True)

        with tab_home:
            st.markdown("""
                <div class='login-box'>
                    <h3 style='color:white;'>Selamat Datang di Website Ar En Dy</h3>
                    <p style='color:#ccc;'>Sistem ini dirancang untuk memantau pergerakan pasar e-bike secara real-time. 
                    Gunakan akun resmi Anda untuk mengakses visualisasi data dan laporan penjualan.</p>
                    <ul style='color:#60a5fa;'>
                        <li>Monitoring Revenue 30 Hari</li>
                        <li>Analisis Segmen Produk</li>
                        <li>Pemantauan Kompetitor</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

        with tab_about:
            st.markdown("""
                <div class='login-box'>
                    <h3 style='color:white;'>R&D Departement Mantuls</h3>
                    <p style='color:#ccc;'>Versi Dashboard: v2.4.0 (Update 2026)<br>
                    Sistem ini mengintegrasikan data dari berbagai marketplace untuk memberikan gambaran pasar yang akurat.</p>
                </div>
            """, unsafe_allow_html=True)

# Inisialisasi status login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Cek apakah sudah login atau belum
if not st.session_state["logged_in"]:
    login_page()
    st.stop()

# --- CSS REVISI UNTUK DASHBOARD UTAMA ---
bg_style = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');

    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.9)), 
                    url("data:image/webp;base64,{bin_str if bin_str else ""}");
        background-size: cover !important;
        background-position: center !important;
        background-attachment: fixed !important;
    }}
    /* --- FITUR BARU: LOGOUT DI KANAN ATAS --- */
    .stButton > button[key="logout_top"] {{
        position: fixed;
        top: 15px;
        right: 80px;
        z-index: 999999;
        background-color: #ff4b4b !important;
        color: white !important;
        border: none !important;
        padding: 5px 20px !important;
        font-weight: 900 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
        transition: 0.3s;
    }}

    /* --- FITUR BARU: LOGOUT BUTTON DI KIRI BAWAH --- */
    .logout-fixed {{
        position: fixed;
        bottom: 20px;
        left: 20px;
        z-index: 999999;
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(255, 75, 75, 0.9);
        padding: 10px 15px;
        border-radius: 8px;
        cursor: pointer;
        color: white;
        font-weight: 900;
        transition: 0.3s;
        border: 1px solid #ff4b4b;
    }}
    
    .logout-fixed:hover {{
        background: rgba(255, 75, 75, 1);
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.5);
    }}

    /* --- RESPONSIVE DESIGN --- */
    @media (max-width: 768px) {{
        .main-title {{
            font-size: 45px !important;
            margin: 25px 0px 40px 0px !important;
        }}
        .section-header {{
            font-size: 18px;
            padding: 8px 15px;
        }}
        div[data-testid="stMetric"] {{
            padding: 10px !important;
        }}
        .sidebar-title {{
            font-size: 28px !important;
        }}
    }}

    @media (max-width: 480px) {{
        .main-title {{
            font-size: 32px !important;
            margin: 15px 0px 25px 0px !important;
            white-space: normal !important;
        }}
        .sidebar-title {{
            font-size: 24px !important;
        }}
        .section-header {{
            font-size: 16px;
            padding: 8px 12px;
        }}
    }}
    
    /* --- LOGO STYLING (TRANSPARENT BACKGROUND) --- */
    .sidebar-logo {{
        background-color: transparent !important;
        background: transparent !important;
    }}

    /* --- FITUR BARU: USER STATUS DI KIRI BAWAH --- */
    .user-status-fixed {{
        position: fixed;
        bottom: 20px;
        left: 20px;
        z-index: 999999;
        background: rgba(15, 23, 42, 0.7);
        padding: 12px 18px;
        border-radius: 12px;
        border: 1px solid rgba(96, 165, 250, 0.3);
        color: white;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        line-height: 1.5;
    }}
    .main-title {{
        font-family: 'Inter', sans-serif !important;
        font-size: 75px !important; 
        font-weight: 900 !important;
        text-align: center !important;
        margin: 40px 0px 60px 0px !important;
        background: linear-gradient(to bottom, #ffffff 40%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        white-space: nowrap !important;
        letter-spacing: -1px !important; 
        text-transform: uppercase;
        line-height: 1.1 !important;
        filter: drop-shadow(0px 15px 25px rgba(0,0,0,0.6));
    }}

    .sidebar-header-container {{
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 30px !important;
    }}

    .sidebar-logo {{
        width: 100px;
        height: auto;
        filter: drop-shadow(0px 0px 10px rgba(96, 165, 250, 0.5));
    }}

    .sidebar-title {{
        font-family: 'Inter', sans-serif !important;
        font-size: 38px !important; 
        font-weight: 900 !important;
        line-height: 0.95 !important;
        letter-spacing: -1.5px !important;
        background: linear-gradient(to bottom, #ffffff 30%, #60a5fa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0px 5px 15px rgba(96, 165, 250, 0.3));
        text-transform: uppercase;
        margin-left: 20px !important;
        margin-top: 0 !important;
    }}

    div[data-testid="stMetric"] {{
        background: rgba(15, 23, 42, 0.92) !important;
        padding: 15px !important;
        border-radius: 14px !important;
        border: 1px solid rgba(96, 165, 250, 0.25) !important;
        transition: all 0.3s ease;
    }}
    
    div[data-testid="stMetric"]:hover {{
        border: 1px solid rgba(96, 165, 250, 0.5) !important;
        box-shadow: 0 4px 16px rgba(96, 165, 250, 0.1);
        transform: translateY(-2px);
    }}
    
    .section-header {{ 
        font-size: 24px; color: #ffffff; font-weight: 700; 
        margin-top: 35px; margin-bottom: 20px;
        background: rgba(96, 165, 250, 0.2);
        border-left: 6px solid #60a5fa; padding: 10px 20px;
        border-radius: 0 10px 10px 0;
        text-transform: uppercase;
        transition: all 0.3s ease;
    }}
    
    .section-header:hover {{
        background: rgba(96, 165, 250, 0.3);
        border-left-width: 8px;
    }}

    .podium-base {{
        width: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 8px 0px;
        border-radius: 8px;
        position: relative;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .rank-1-base {{ background: linear-gradient(180deg, rgba(255, 215, 0, 0.2) 0%, rgba(255, 215, 0, 0.05) 100%); border: 1.5px solid rgba(255, 215, 0, 0.4); }}
    .rank-2-base {{ background: rgba(192, 192, 192, 0.1); border: 1.5px solid rgba(192, 192, 192, 0.3); }}
    .rank-3-base {{ background: rgba(205, 127, 50, 0.1); border: 1.5px solid rgba(205, 127, 50, 0.3); }}
    .rank-4-base {{ background: rgba(96, 165, 250, 0.05); border: 1px solid rgba(96, 165, 250, 0.2); }}
    .rank-5-base {{ background: rgba(96, 165, 250, 0.05); border: 1px solid rgba(96, 165, 250, 0.2); }}

    .badge-label {{
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
        font-size: 15px;
        margin: 0px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.6);
        transition: all 0.3s ease;
    }}
    
    .badge-label:hover {{
        transform: scale(1.1);
        box-shadow: 0 6px 16px rgba(0,0,0,0.7);
    }}

    .gallery-card {{
        background: rgba(255, 255, 255, 0.03);
        padding: 10px 8px;
        border-radius: 8px;
        border: 1px solid rgba(96, 165, 250, 0.15);
        margin-top: 8px;
        width: 100%;
        transition: all 0.3s ease;
    }}
    
    .gallery-card:hover {{
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(96, 165, 250, 0.3);
    }}
    
    /* --- BUTTON STYLING FOR ELEGANCE --- */
    .stButton > button {{
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        border: none !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
    }}
    
    .stButton > button[type="primary"] {{
        background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 100%) !important;
    }}
    
    .stButton > button[type="secondary"] {{
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
    }}
    
    /* --- ELEGANT INPUT STYLING --- */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {{
        border-radius: 8px !important;
        border: 1px solid rgba(96, 165, 250, 0.2) !important;
        background: rgba(15, 23, 42, 0.6) !important;
        color: white !important;
        padding: 10px 12px !important;
        transition: all 0.3s ease !important;
        font-family: 'Inter', sans-serif !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {{
        border: 1px solid rgba(96, 165, 250, 0.6) !important;
        box-shadow: 0 0 12px rgba(96, 165, 250, 0.2) !important;
        background: rgba(15, 23, 42, 0.8) !important;
    }}
    
    /* --- SLIDER STYLING --- */
    .stSlider > div > div > div > div {{
        background: linear-gradient(to right, #60a5fa, #3b82f6) !important;
    }}
    
    /* --- EXPANDER STYLING --- */
    .streamlit-expanderHeader {{
        background: rgba(96, 165, 250, 0.1) !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        transition: all 0.3s ease !important;
    }}
    
    .streamlit-expanderHeader:hover {{
        background: rgba(96, 165, 250, 0.2) !important;
    }}
    
    .streamlit-expanderHeader p {{
        font-weight: 600 !important;
        letter-spacing: 0.3px !important;
    }}
    
    /* --- DOWNLOAD BUTTON STYLING (COMPACT) --- */
    .stDownloadButton > button {{
        padding: 8px 12px !important;
        font-size: 12px !important;
        font-weight: 600 !important;
        height: 36px !important;
        min-height: 36px !important;
        background: linear-gradient(135deg, #ec4899 0%, #db2777 100%) !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(236, 72, 153, 0.2) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.3px !important;
    }}
    
    .stDownloadButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 16px rgba(236, 72, 153, 0.4) !important;
        background: linear-gradient(135deg, #f472b6 0%, #ec4899 100%) !important;
    }}
    
    .stDownloadButton > button:active {{
        transform: translateY(0px) !important;
        box-shadow: 0 2px 4px rgba(236, 72, 153, 0.3) !important;
    }}
    .stDataFrame {{
        border-radius: 8px;
        overflow: hidden;
    }}
    
    .stDataFrame > div {{
        border-radius: 8px;
    }}
    
    /* --- DIVIDER STYLING --- */
    .stDivider {{
        margin: 1.5rem 0;
        opacity: 0.3;
    }}
</style>
"""
st.markdown(bg_style, unsafe_allow_html=True)

# --- FUNGSI HELPER ---
@st.cache_data(show_spinner=False)
def load_image_url(url):
    try:
        if not isinstance(url, str) or not url.startswith("http"): return None
        response = requests.get(url.strip(), headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        return response.content if response.status_code == 200 else None
    except: return None

@st.cache_data
def load_pdf(pdf_path):
    """Load PDF file untuk ditampilkan"""
    try:
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                return f.read()
    except:
        pass
    return None

def clean_num(val):
    if pd.isna(val) or val == 0: return 0.0
    if isinstance(val, str):
        clean = val.replace('Rp', '').replace('.', '').replace(',', '').strip()
        try: return float(clean)
        except: return 0.0
    return float(val)

def get_market_demand(total_sold):
    """Fungsi untuk menentukan market demand berdasarkan total sold"""
    if total_sold > 5000:
        return "🔥 VERY HIGH"
    elif total_sold > 2000:
        return "📈 HIGH"
    elif total_sold > 500:
        return "✅ MEDIUM"
    else:
        return "📉 LOW"

def get_market_demand(total_sold):
    """Fungsi untuk menentukan market demand berdasarkan total sold"""
    if total_sold > 5000:
        return "🔥 VERY HIGH"
    elif total_sold > 2000:
        return "📈 HIGH"
    elif total_sold > 500:
        return "✅ MEDIUM"
    else:
        return "📉 LOW"

@st.cache_data
def load_data(category):
    if category == "Sepeda Listrik":
        filenames = ["sepeda listrik.csv", "Sepeda Listrik.csv", os.path.join("data", "sepeda listrik.csv")]
    elif category == "Sepeda Lipat":
        filenames = ["sepeda lipat.csv", "Sepeda Lipat.csv", os.path.join("data", "sepeda lipat.csv")]
    elif category == "Sepeda Listrik Lipat":
        filenames = ["Sepeda listrik lipat.csv", os.path.join("data", "Sepeda listrik lipat.csv")]
    elif category == "China Market":
        filenames = ["china market.csv", os.path.join("data", "china market.csv")]
    else: return pd.DataFrame()
    
    df = pd.DataFrame()
    for f in filenames:
        if os.path.exists(f):
            df = pd.read_csv(f)
            break
    
    if df.empty: return df
    df.columns = [c.strip() for c in df.columns]
    
    # --- SPECIAL HANDLING UNTUK CHINA MARKET ---
    if category == "China Market":
        # Konversi USD ke Rupiah (1 USD = 16.822,35 Rp)
        USD_TO_IDR = 16822.35
        
        # Extract harga dari kolom "Unit Price (USD)" atau "Price in Rupiah"
        if "Unit Price (USD)" in df.columns:
            df['Harga_Clean'] = df["Unit Price (USD)"].str.replace('$', '').str.replace(',', '').astype(float) * USD_TO_IDR
        elif "Price in Rupiah" in df.columns:
            df['Harga_Clean'] = df["Price in Rupiah"].str.replace('Rp', '').str.replace('.', '').astype(float)
        else:
            df['Harga_Clean'] = 0.0
        
        # Untuk China Market, set nilai dummy untuk kolom lain
        df['Omset_Clean'] = df['Harga_Clean'] * 5  # Asumsi penjualan rata-rata 5 unit
        df['Sold_Clean'] = 5  # Default sold
        df['Rating_Clean'] = 4.8  # Rating tinggi untuk produk import
        df['Nama Toko'] = df.get('Manufacturer', 'Hebei Fanghao Bicycle Co., Ltd.')
        df['Nama Produk'] = df.get('Product Name', 'E-Bike Model')
    else:
        col_map = {
            'Harga': ['Harga', 'price', 'Price'], 
            'Omset': ['Omset 30 Hari', 'Revenue', 'Omset'], 
            'Sold': ['Penjualan 30 Hari', 'Terjual', 'Sold', 'Penjualan Total'], 
            'Rating': ['Rating', 'Stars']
        }
        
        for key, variants in col_map.items():
            found = next((v for v in variants if v in df.columns), None)
            df[f'{key}_Clean'] = df[found].apply(clean_num) if found else 0.0
    
    df['Category_Label'] = category
    df['Segment'] = pd.cut(df['Harga_Clean'], 3, labels=['Entry', 'Mid', 'Premium'])
    return df

# --- SIDEBAR & CONTENT ---
with st.sidebar:
    logo_html = f'<img src="data:image/png;base64,{logo_str}" class="sidebar-logo">' if logo_str else ""
    st.markdown(f"""
        <div class="sidebar-header-container">
            {logo_html}
            <div class="sidebar-title">MARKET<br>FILTER</div>
        </div>
    """, unsafe_allow_html=True)

    # Info User Login di Sidebar
    st.info(f"👤 User: {st.session_state['user_now']}\n\n🛡️ Role: {st.session_state['role_now']}")

    category_choice = st.selectbox("Pilih Kategori", ["Best Product All", "Sepeda Listrik", "Sepeda Lipat", "Sepeda Listrik Lipat", "China Market"], index=0)
    
    if category_choice == "Best Product All":
        df1 = load_data("Sepeda Listrik")
        df2 = load_data("Sepeda Lipat")
        df3 = load_data("Sepeda Listrik Lipat")
        df = pd.concat([df1, df2, df3], ignore_index=True)
    else:
        df = load_data(category_choice)

    if not df.empty:
        all_segments = df['Segment'].unique().tolist()
        selected_segments = st.multiselect("Pilih Segmen Harga", all_segments, default=all_segments)
        toko_col = 'Nama Toko' if 'Nama Toko' in df.columns else df.columns[1]
        selected_shops = st.multiselect("Pilih Toko", sorted(df[toko_col].unique().astype(str)))
        min_p, max_p = int(df['Harga_Clean'].min()), int(df['Harga_Clean'].max())
        price_range = st.slider("Rentang Harga (Rp)", min_p, max_p, (min_p, max_p))
        min_rating = st.slider("Minimal Rating ⭐", 0.0, 5.0, 4.0, 0.5)

    # --- LOGOUT BUTTON DI SIDEBAR (BOTTOM) ---
    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    logout_col = st.columns([1, 1.5])
    with logout_col[0]:
        if st.button("🚪 Log Out", width="stretch", type="secondary", key="sidebar_logout"):
            st.session_state["logged_in"] = False
            st.rerun()

# --- LANJUTAN MAIN PAGE ---
if df.empty:
    st.error(f"❌ Data tidak ditemukan!")
else:
    mask = (df['Harga_Clean'].between(price_range[0], price_range[1])) & \
            (df['Rating_Clean'] >= min_rating) & \
            (df['Segment'].isin(selected_segments))
    if selected_shops: mask = mask & (df[toko_col].isin(selected_shops))
    df_filtered = df[mask].copy()

    if category_choice == "Best Product All":
        st.markdown("<div class='main-title'>🏆 BEST PRODUCT ALL CATEGORIES</div>", unsafe_allow_html=True)
        top_5 = df_filtered.nlargest(5, 'Sold_Clean')
        col_img = next((c for c in ['Gambar Produk', 'Gambar', 'Image'] if c in top_5.columns), None)
        
        order_indices = [0, 1, 2, 3, 4]  # Sequential order: 1st, 2nd, 3rd, 4th, 5th
        podium_cols = st.columns([1, 1, 1, 1, 1])  # Equal width columns
        
        ranks_config = {
            0: {"color": "#FFD700", "class": "rank-1-base", "label": "1st"},
            1: {"color": "#C0C0C0", "class": "rank-2-base", "label": "2nd"},
            2: {"color": "#CD7F32", "class": "rank-3-base", "label": "3rd"},
            3: {"color": "#60a5fa", "class": "rank-4-base", "label": "4th"},
            4: {"color": "#60a5fa", "class": "rank-5-base", "label": "5th"}
        }

        for i, idx in enumerate(order_indices):
            if idx < len(top_5):
                item = top_5.iloc[idx]
                cfg = ranks_config[idx]
                with podium_cols[i]:
                    # Trophy/Badge di atas
                    st.markdown(f"""
                        <div class="podium-base {cfg['class']}" style="margin-bottom: 8px;">
                            <div class="badge-label" style="border: 3px solid {cfg['color']}; color:{cfg['color']};">{cfg['label']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Gambar produk
                    if col_img:
                        img_data = load_image_url(item[col_img])
                        if img_data: st.image(img_data, width="stretch")
                    
                    # Info produk dan harga
                    st.markdown(f"""
                        <div class="gallery-card">
                            <p style='font-size:11px; font-weight:bold; color:white; margin:0;'>{str(item.iloc[0])[:35]}...</p>
                            <p style='font-size:9px; color:#60a5fa; margin:0;'>{item['Category_Label']}</p>
                            <h3 style='color:white; margin:5px 0 0 0; font-size:16px;'>Rp {item['Harga_Clean']:,.0f}</h3>
                            <p style='font-size:11px; color:#ccc; margin:2px 0 0 0;'>Sold: {int(item['Sold_Clean'])}</p>
                        </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("<div class='section-header'>📈 Comparison Data Top 5</div>", unsafe_allow_html=True)
        st.dataframe(top_5[['Nama Produk', 'Category_Label', 'Harga_Clean', 'Sold_Clean', 'Rating_Clean']], width="stretch")

    else:
        # Fix duplicate MARKET text for China Market category
        display_title = category_choice.upper() if category_choice == "China Market" else f"{category_choice.upper()} MARKET"
        st.markdown(f"<div class='main-title'>⚡ {display_title} INTELLIGENCE</div>", unsafe_allow_html=True)

        # --- SHOW KPI ONLY FOR NON-CHINA MARKET ---
        if category_choice != "China Market":
            m1, m2, m3, m4 = st.columns(4)
            avg_revenue = df_filtered['Omset_Clean'].sum() / max(len(df_filtered), 1)
            avg_sold = df_filtered['Sold_Clean'].sum() / max(len(df_filtered), 1)
            market_demand = get_market_demand(df_filtered['Sold_Clean'].sum())
            
            m1.metric("Avg. Total Revenue", f"Rp {avg_revenue:,.0f}")
            m2.metric("Avg. Sold / Product", f"{int(avg_sold)} Pcs")
            m3.metric("Avg. Price", f"Rp {df_filtered['Harga_Clean'].mean():,.0f}")
            m4.metric("Market Demand\n(R&D Insight)", market_demand)

        # --- SPECIAL SECTION FOR CHINA MARKET (LANGSUNG TOP 5) ---
        if category_choice == "China Market":
            # PDF button di ujung kiri dengan spacing
            col_pdf, col_space = st.columns([0.4, 4.6], gap="small")
            with col_pdf:
                pdf_path = os.path.join("data", "China Market.pdf")
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="📄 PDF",
                            data=pdf_file,
                            file_name="China Market.pdf",
                            mime="application/pdf",
                            width="stretch",
                            key="china_pdf_btn"
                        )
            
            # Header untuk TOP 5
            st.markdown("<div class='section-header'>🏆 TOP 5 PRODUK TERBAIK (CHINA MARKET)</div>", unsafe_allow_html=True)
            
            top_5_china = df_filtered.nlargest(5, 'Harga_Clean')
            
            # Buat dataframe untuk ditampilkan
            top_5_display = pd.DataFrame({
                'No.': range(1, len(top_5_china) + 1),
                'Nama Produk': top_5_china['Nama Produk'].values,
                'Harga (Rupiah)': [f"Rp {int(x):,}" for x in top_5_china['Harga_Clean'].values],
                'Rating': [f"{'⭐' * int(x)}" for x in top_5_china['Rating_Clean'].values],
                'Status': ['Top Grade'] * len(top_5_china)
            })
            
            st.dataframe(top_5_display, width="stretch", hide_index=True)
            
            # Chart untuk Top 5 dengan harga dalam Rupiah
            st.markdown("<div class='section-header'>💰 ANALISIS HARGA TOP 5 PRODUK</div>", unsafe_allow_html=True)
            
            chart_col1, chart_col2 = st.columns([1.5, 1])
            
            with chart_col1:
                fig_top5 = px.bar(
                    x=top_5_china['Nama Produk'].values,
                    y=top_5_china['Harga_Clean'].values,
                    color=top_5_china['Harga_Clean'].values,
                    title="Top 5 Produk Berdasarkan Harga (dalam Rupiah)",
                    labels={'y': 'Harga (Rp)', 'x': 'Nama Produk'},
                    template="plotly_dark",
                    color_continuous_scale="Viridis"
                )
                fig_top5.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                fig_top5.update_yaxes(tickformat=",")
                st.plotly_chart(fig_top5, width="stretch")
            
            with chart_col2:
                # Statistik harga
                price_stats = pd.DataFrame({
                    'Metrik': ['Tertinggi', 'Terendah', 'Rata-rata', 'Median'],
                    'Harga (Rp)': [
                        f"Rp {df_filtered['Harga_Clean'].max():,.0f}",
                        f"Rp {df_filtered['Harga_Clean'].min():,.0f}",
                        f"Rp {df_filtered['Harga_Clean'].mean():,.0f}",
                        f"Rp {df_filtered['Harga_Clean'].median():,.0f}"
                    ]
                })
                st.dataframe(price_stats, width="stretch", hide_index=True)
            
            st.markdown("<div class='section-header'>📊 ANALISIS SEGMEN HARGA CHINA MARKET</div>", unsafe_allow_html=True)
            
            seg_col1, seg_col2 = st.columns([1, 1])
            
            with seg_col1:
                # Pie chart untuk distribusi segmen
                segment_dist = df_filtered['Segment'].value_counts()
                fig_seg_pie = px.pie(
                    names=segment_dist.index,
                    values=segment_dist.values,
                    title="Distribusi Produk per Segmen",
                    template="plotly_dark",
                    color_discrete_map={"Entry": "#60a5fa", "Mid": "#fbbf24", "Premium": "#f87171"}
                )
                fig_seg_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_seg_pie, width="stretch")
            
            with seg_col2:
                # Tabel segmen dengan detail
                segment_analysis = df_filtered.groupby('Segment', observed=True).agg({
                    'Harga_Clean': ['min', 'max', 'mean', 'count']
                }).round(0)
                
                segment_analysis.columns = ['Harga Min (Rp)', 'Harga Max (Rp)', 'Harga Rata-rata (Rp)', 'Jumlah Produk']
                segment_analysis = segment_analysis.astype(int)
                
                st.write("**Analisis Segmen Harga:**")
                for segment in ['Entry', 'Mid', 'Premium']:
                    if segment in segment_analysis.index:
                        row = segment_analysis.loc[segment]
                        with st.expander(f"📌 {segment.upper()} SEGMENT"):
                            col_s1, col_s2 = st.columns(2)
                            with col_s1:
                                st.metric("Harga Minimum", f"Rp {int(row['Harga Min (Rp)']):,}")
                                st.metric("Harga Rata-rata", f"Rp {int(row['Harga Rata-rata (Rp)']):,}")
                            with col_s2:
                                st.metric("Harga Maksimum", f"Rp {int(row['Harga Max (Rp)']):,}")
                                st.metric("Jumlah Produk", f"{int(row['Jumlah Produk'])} pcs")

        st.markdown("<div class='section-header'>📊 Market Overview</div>", unsafe_allow_html=True)
        c1, c2 = st.columns([2, 1])
        with c1:
            if not df_filtered.empty:
                df_filtered['Price_Range'] = pd.cut(df_filtered['Harga_Clean'], bins=5)
                df_filtered['Price_Range_Label'] = df_filtered['Price_Range'].apply(lambda x: f"Rp {x.left/1e6:.1f}jt - {x.right/1e6:.1f}jt")
                range_analysis = df_filtered.groupby(['Price_Range', 'Price_Range_Label'], observed=True)['Sold_Clean'].sum().reset_index().sort_values('Price_Range')
                fig_range = px.bar(range_analysis, x='Price_Range_Label', y='Sold_Clean', color='Sold_Clean', template="plotly_dark", color_continuous_scale="Blues", title="Unit Terjual Berdasarkan Rentang Harga")
                fig_range.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
                st.plotly_chart(fig_range, width="stretch")

        with c2:
            fig_pie = px.pie(df_filtered, names='Segment', hole=0.5, template="plotly_dark", title="Distribusi Segmen")
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, width="stretch")

        st.markdown("<div class='section-header'>💰 Revenue Analysis</div>", unsafe_allow_html=True)
        rev_c1, rev_c2 = st.columns([1, 1.5])
        
        with rev_c1:
            seg_rev = df_filtered.groupby('Segment', observed=True)['Omset_Clean'].sum().reset_index()
            fig_seg_rev = px.bar(
                seg_rev, x='Segment', y='Omset_Clean', 
                color='Segment', title="Revenue per Segmen (Vertical)",
                labels={'Omset_Clean': 'Total Revenue (Rp)'},
                template="plotly_dark",
                color_discrete_map={"Entry": "#60a5fa", "Mid": "#fbbf24", "Premium": "#f87171"}
            )
            fig_seg_rev.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_seg_rev, width="stretch")

        with rev_c2:
            store_rev = df_filtered.groupby(toko_col)['Omset_Clean'].sum().nlargest(10).reset_index()
            fig_store_rev = px.bar(
                store_rev, x='Omset_Clean', y=toko_col, 
                orientation='h', title="Top 10 Stores by Revenue (Horizontal)",
                labels={'Omset_Clean': 'Total Revenue (Rp)', toko_col: 'Nama Toko'},
                template="plotly_dark", color='Omset_Clean', color_continuous_scale="Viridis"
            )
            fig_store_rev.update_layout(yaxis={'categoryorder':'total ascending'}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_store_rev, width="stretch")

        # Hanya tampilkan Top Sellers Gallery untuk kategori yang bukan China Market
        if category_choice != "China Market":
            st.markdown("<div class='section-header'>🏆 Top Sellers Gallery</div>", unsafe_allow_html=True)
            top_10 = df_filtered.nlargest(10, 'Sold_Clean')
            rows = st.columns(5)
            col_img = next((c for c in ['Gambar Produk', 'Gambar', 'Image'] if c in top_10.columns), None)
            col_link = next((c for c in ['Link Produk', 'Url', 'Link'] if c in top_10.columns), None)
            
            for i, (_, item) in enumerate(top_10.iterrows()):
                with rows[i % 5]:
                    if col_img:
                        img_data = load_image_url(item[col_img])
                        if img_data: st.image(img_data, use_container_width=True)
                    st.markdown(f'<div class="gallery-card"><p style="font-size:12px; font-weight:bold; color:#ddd; height:40px; overflow:hidden;">{str(item.iloc[0])[:50]}...</p><h4 style="color:#60a5fa; margin:0;">Rp {item["Harga_Clean"]:,.0f}</h4><p style="font-size:11px; color:#999;">Terjual: {int(item["Sold_Clean"])}</p></div>', unsafe_allow_html=True)
                    if col_link and pd.notna(item[col_link]):
                        st.link_button("🛒 Open Product", item[col_link], width="stretch")
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>⚙️ SYSTEM CONTROL</div>", unsafe_allow_html=True)
    
    ctrl_col1, ctrl_col2 = st.columns([2, 1])
    
    with ctrl_col1:
        # Convert to Excel format
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_filtered.to_excel(writer, sheet_name='Report', index=False)
        excel_data = output.getvalue()
        
        st.download_button(
            label="📥 DOWNLOAD CURRENT REPORT (EXCEL)",
            data=excel_data,
            file_name=f"report_{category_choice.lower()}.xlsx",
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            width="stretch"
        )

    with ctrl_col2:
        if st.button("🚪 LOG OUT", width="stretch", type="secondary"):
            st.session_state["logged_in"] = False
            st.rerun()

    st.markdown("<br><hr><center style='color:white; opacity:0.5;'>Dashboard by R&D Departement Hub © 2026</center>", unsafe_allow_html=True)