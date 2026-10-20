import random
import time
import pandas as pd
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Limdim Coffee • Teyvat Genshin Edition",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# GIAO DIỆN & HIỆU ỨNG CSS NÂNG CAO (GENSHIN STYLE)
# ==========================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;900&family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');

    /* Nền không gian Teyvat huyền ảo */
    .stApp {
        background: radial-gradient(circle at 50% 20%, #111827 0%, #07090e 70%, #030406 100%);
        background-attachment: fixed;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #f1f5f9;
    }

    /* Hiệu ứng viền phát sáng nguyên tố quanh card */
    @keyframes elementGlow {
        0% { border-color: rgba(245, 158, 11, 0.3); box-shadow: 0 0 15px rgba(245, 158, 11, 0.1); }
        50% { border-color: rgba(245, 158, 11, 0.8); box-shadow: 0 0 25px rgba(245, 158, 11, 0.4); }
        100% { border-color: rgba(245, 158, 11, 0.3); box-shadow: 0 0 15px rgba(245, 158, 11, 0.1); }
    }

    /* Tiêu đề hoàng gia Genshin */
    .genshin-title {
        font-family: 'Cinzel', serif;
        font-weight: 900;
        background: linear-gradient(180deg, #ffffff 0%, #fde047 50%, #ca8a04 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 4px 25px rgba(234, 179, 8, 0.5);
        text-align: center;
        font-size: 3rem;
        letter-spacing: 2px;
        margin-bottom: 0px;
    }

    .genshin-subtitle {
        text-align: center;
        color: #cbd5e1;
        font-style: italic;
        font-size: 1.15rem;
        margin-bottom: 25px;
        font-family: 'Cinzel', serif;
    }

    /* Khung thẻ phong cách Gacha/Menu Teyvat */
    .genshin-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 2px solid rgba(245, 158, 11, 0.4);
        border-radius: 20px;
        padding: 24px;
        backdrop-filter: blur(16px);
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.6);
        margin-bottom: 20px;
        animation: elementGlow 4s infinite ease-in-out;
    }

    /* Nút bấm phong cách Vision */
    .stButton>button {
        background: linear-gradient(135deg, #d97706 0%, #b45309 50%, #78350f 100%);
        color: #fffdf0;
        border: 1px solid #fde047;
        border-radius: 14px;
        font-family: 'Cinzel', serif;
        font-weight: 700;
        letter-spacing: 1px;
        padding: 0.7rem 1.5rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 20px rgba(217, 119, 6, 0.4);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 50%, #b45309 100%);
        border-color: #ffffff;
        box-shadow: 0 0 30px rgba(253, 224, 71, 0.8);
        transform: translateY(-3px);
    }

    /* Thẻ thông tin nguyên tố */
    .element-tag {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-right: 6px;
        text-transform: uppercase;
    }
    .pyro { background: rgba(239, 68, 68, 0.25); color: #f87171; border: 1px solid #ef4444; }
    .hydro { background: rgba(59, 130, 246, 0.25); color: #60a5fa; border: 1px solid #3b82f6; }
    .cryo { background: rgba(56, 189, 248, 0.25); color: #38bdf8; border: 1px solid #0284c7; }
    .electro { background: rgba(168, 85, 247, 0.25); color: #c084fc; border: 1px solid #a855f7; }
    .dendro { background: rgba(34, 197, 94, 0.25); color: #4ade80; border: 1px solid #22c55e; }

    /* Sidebar Teyvat */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #090d16 0%, #0f172a 100%);
        border-right: 2px solid rgba(245, 158, 11, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# KHỞI TẠO SESSION STATE
# ==========================================
if "cart" not in st.session_state:
    st.session_state.cart = []
if "discount_code" not in st.session_state:
    st.session_state.discount_code = None
if "discount_percent" not in st.session_state:
    st.session_state.discount_percent = 0
if "user_primogems" not in st.session_state:
    st.session_state.user_primogems = 1600  # Tặng sẵn Nguyên Thạch cho khách gacha
if "table_status" not in st.session_state:
    st.session_state.table_status = {
        "Bàn 01 (Quán rượu Angel's Share - Mondstadt)": True,
        "Bàn 02 (Cảng Liyue - Nguy Hải Gian)": False,
        "Bàn 03 (Đền Narukami - Inazuma)": True,
        "Bàn 04 (Học viện Sumeru - Akademiya)": True,
        "Bàn 05 (Nhà hát Opera Fontaine)": False,
        "Bàn VIP Hoàng Gia Natlan": True,
    }

# ==========================================
# DỮ LIỆU MENU KẾT HỢP NGUYÊN TỐ
# ==========================================
DRINKS_MENU = {
    "Cà phê đậm vị Teyvat": {
        "Năng Lượng Cà Phê Muối (Sứ giả Fontaine)": {"price": 45000, "elem": "hydro", "desc": "Hương vị mặn mòi dòng nước nguyên thủy."},
        "Bạc Xỉu Tinh Thể Nguyệt Quang": {"price": 42000, "elem": "cryo", "desc": "Ngọt ngào và mát lạnh như sương sớm Mondstadt."},
        "Espresso Phong Ấn Địa Mạch": {"price": 35000, "elem": "pyro", "desc": "Đánh thức sức mạnh hỏa diệm nguyên tố."},
        "Cold Brew Trái Cây Phong Thần": {"price": 50000, "elem": "dendro", "desc": "Thanh mát hương cỏ cây từ rừng sâu Sumeru."},
    },
    "Trà trái cây Nguyên Tố": {
        "Trà Đào Hỏa Nguyên Tố": {"price": 48000, "elem": "pyro", "desc": "Bùng nổ vị giác với đào tươi và thạch lửa."},
        "Trà Sữa Trân Châu Lôi Nguyên Tố": {"price": 52000, "elem": "electro", "desc": "Tia chớp tím béo ngậy từ đảo Inazuma."},
        "Trà Thanh Long Băng Giá": {"price": 55000, "elem": "cryo", "desc": "Thanh long đỏ rực kết hợp đá tuyết Long Tích."},
        "Hồng Trà Kem Cheese Fontaine": {"price": 50000, "elem": "hydro", "desc": "Lớp kem mặn bồng bềnh như sóng biển Court of Fontaine."},
    },
    "Đồ uống độc quyền (Signature)": {
        "Nước Ép Hoa Tinh Linh (Oceanid Elixir)": {"price": 58000, "elem": "hydro", "desc": "Thức uống thần bí ban phước từ suối nguồn."},
        "Sinh Tố Trái Cây Trí Tuệ Sumeru": {"price": 55000, "elem": "
