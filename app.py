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
        "Sinh Tố Trái Cây Trí Tuệ Sumeru": {"price": 55000, "elem": "dendro", "desc": "Tăng cường độ tập trung tối đa cho lữ khách."},
        "Cacao Nóng Vực Thẳm (Abyss Cocoa)": {"price": 48000, "elem": "pyro", "desc": "Đậm đà socola nguyên chất từ cõi tối."},
    },
}

DESSERTS_MENU = {
    "Bánh ngọt tráng miệng": {
        "Bánh Mousse Trà Xanh Inazuma": {"price": 45000, "elem": "dendro", "desc": "Mềm mịn vị matcha nguyên bản từ đảo Narukami."},
        "Bánh Tiramisu Hạt Dẻ Fontaine": {"price": 50000, "elem": "hydro", "desc": "Hương vị lãng mạn kinh điển xứ sở nghệ thuật."},
        "Bánh Su Kem Ngọt Ngào Mondstadt": {"price": 35000, "elem": "cryo", "desc": "Tan chảy ngay từ miếng cắn đầu tiên."},
        "Bánh Tart Trứng Liyue Thơm Phức": {"price": 32000, "elem": "pyro", "desc": "Vỏ ngàn lớp giòn rụm, nhân trứng béo ngậy."},
        "Bánh Brownie Socola Vực Thẳm": {"price": 45000, "elem": "electro", "desc": "Ngọt sâu lắng kích thích mọi giác quan."},
    }
}

TOPPINGS = {
    "Trân châu đen hoàng gia (+8k)": 8000,
    "Trân châu trắng sương mù (+8k)": 8000,
    "Thạch dừa nha đam nguyên tố (+10k)": 10000,
    "Kem Cheese béo ngậy thượng hạng (+12k)": 12000,
    "Pudding trứng béo tan chảy (+10k)": 10000,
}

# ==========================================
# HEADER GIAO DIỆN CHÍNH
# ==========================================
st.markdown('<div class="genshin-title">☕ LIMDIM COFFEE • TEYVAT STATION</div>', unsafe_allow_html=True)
st.markdown('<div class="genshin-subtitle">"Nơi hội tụ lữ khách khắp các đại lục • Quán trà & cà phê phong cách Genshin Impact độc quyền"</div>', unsafe_allow_html=True)

# ==========================================
# THANH ĐIỀU HƯỚNG SIDEBAR
# ==========================================
with st.sidebar:
    st.markdown("### 🌟 TRUNG TÂM LỮ KHÁCH TEYVAT")
    st.info(f"💎 Nguyên Thạch (Primogems): **{st.session_state.user_primogems} ✨**")
    
    nav_option = st.radio(
        "Chọn không gian:",
        [
            "🛒 Gọi Món & Thanh Toán",
            "✨ Cổng Gacha Wish (5 Sao)",
            "🎲 Xúc Xắc Định Mệnh",
            "🪑 Sơ Đồ Bàn Trống Quán",
        ],
    )

    st.markdown("---")
    st.markdown("### 📊 Giỏ Hàng Lữ Khách")
    total_items = sum([item["qty"] for item in st.session_state.cart])
    st.metric(label="Tổng sản phẩm đã chọn", value=f"{total_items} món")
    if st.button("🗑️ Làm sạch giỏ hàng"):
        st.session_state.cart = []
        st.session_state.discount_code = None
        st.session_state.discount_percent = 0
        st.success("Đã xóa sạch giỏ hàng!")
        st.rerun()

# ==========================================
# TÍNH NĂNG 1: GỌI MÓN & THANH TOÁN (BILL)
# ==========================================
if nav_option == "🛒 Gọi Món & Thanh Toán":
    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown('<div class="genshin-card"><h3>📜 Thực Đơn Đại Lục Limdim</h3>', unsafe_allow_html=True)
        
        category_type = st.selectbox("Phân loại:", ["Thức uống nguyên tố", "Bánh ngọt tráng miệng"])

        if category_type == "Thức uống nguyên tố":
            selected_cat = st.selectbox("Chọn dòng:", list(DRINKS_MENU.keys()))
            current_menu = DRINKS_MENU[selected_cat]
        else:
            selected_cat = "Bánh ngọt tráng miệng"
            current_menu = DESSERTS_MENU[selected_cat]

        selected_item = st.selectbox("Chọn món:", list(current_menu.keys()))
        item_info = current_menu[selected_item]
        item_price = item_info["price"]
        item_elem = item_info["elem"]
        item_desc = item_info["desc"]

        # Hiển thị huy hiệu nguyên tố
        st.markdown(
            f"""
            <div style="margin: 10px 0;">
                <span class="element-tag {item_elem}">Nguyên tố {item_elem.upper()}</span>
                <span style="color: #94a3b8; font-size: 0.9rem; font-style: italic;">{item_desc}</span>
            </div>
            <div style="font-size: 1.1rem; color: #fde047; font-weight: bold; margin-bottom: 12px;">
                💰 Giá cơ bản: {item_price:,.0f} VNĐ
            </div>
            """,
            unsafe_allow_html=True,
        )

        sugar, ice, size, selected_toppings = "100%", "Bình thường", "M (Tiêu chuẩn)", []
        if category_type == "Thức uống nguyên tố":
            c_sug, c_ice, c_size = st.columns(3)
            with c_sug:
                sugar = st.selectbox("Độ ngọt", ["100%", "70%", "50%", "30%", "0%"])
            with c_ice:
                ice = st.selectbox("Lượng đá", ["Bình thường", "Ít đá", "Đá riêng", "Không đá"])
            with c_size:
                size = st.selectbox("Kích thước ly", ["M (Tiêu chuẩn)", "L (+7,000đ)", "XL (+15,000đ)"])

            st.markdown("✨ **Thêm Topping Thần Kỳ:**")
            top_cols = st.columns(2)
            idx = 0
            for top_name, top_price in TOPPINGS.items():
                with top_cols[idx % 2]:
                    if st.checkbox(top_name, key=f"top_{top_name}"):
                        selected_toppings.append({"name": top_name, "price": top_price})
                idx += 1

        qty = st.number_input("Số lượng", min_value=1, max_value=20, value=1)
        note = st.text_input("Ghi chú cho Bartender (VD: ít đá, mang ra bàn chính...)", placeholder="Nhập ghi chú...")

        if st.button("➕ Thêm vào Hóa Đơn"):
            actual_price = item_price
            if "L (+7,000đ)" in size:
                actual_price += 7000
            elif "XL (+15,000đ)" in size:
                actual_price += 15000

            topping_total = sum([t["price"] for t in selected_toppings])
            total_item_price = (actual_price + topping_total) * qty

            item_data = {
                "name": selected_item,
                "category": selected_cat,
                "element": item_elem,
                "price_unit": actual_price,
                "size": size if category_type == "Thức uống nguyên tố" else "Tiêu chuẩn",
                "sugar": sugar if category_type == "Thức uống nguyên tố" else "N/A",
                "ice": ice if category_type == "Thức uống nguyên tố" else "N/A",
                "toppings": selected_toppings,
                "qty": qty,
                "note": note,
                "total_price": total_item_price,
            }
            st.session_state.cart.append(item_data)
            st.success(f"Đã nạp thành công **{selected_item}** vào order!")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="genshin-card"><h3>🧾 Hóa Đơn Lữ Khách</h3>', unsafe_allow_html=True)
        if not st.session_state.cart:
            st.warning("Giỏ hàng chưa có món nào. Hãy chọn món bên trái nhé!")
        else:
            subtotal = 0
            for i, cart_item in enumerate(st.session_state.cart):
                st.markdown(f"**{i+1}. {cart_item['name']}** x{cart_item['qty']}")
                if cart_item["category"] != "Bánh ngọt tráng miệng":
                    st.caption(f"Size: {cart_item['size']} | Đường: {cart_item['sugar']} | Đá: {cart_item['ice']}")
                if cart_item["toppings"]:
                    top_names = ", ".join([t["name"] for t in cart_item["toppings"]])
                    st.caption(f"Topping: {top_names}")
                if cart_item["note"]:
                    st.caption(f"📝 *{cart_item['note']}*")
                st.markdown(
                    f"<div style='text-align: right; color: #fde047; font-weight: bold;'>{cart_item['total_price']:,.0f} VNĐ</div>",
                    unsafe_allow_html=True,
                )
                subtotal += cart_item["total_price"]
                st.markdown("<hr style='margin: 6px 0; opacity: 0.15;'>", unsafe_allow_html=True)

            if st.session_state.discount_percent > 0:
                st.success(f"🎉 Voucher kích hoạt: **{st.session_state.discount_code}** (-{st.session_state.discount_percent}%)")
                discount_amount = subtotal * (st.session_state.discount_percent / 100)
            else:
                discount_amount = 0

            final_total = subtotal - discount_amount

            st.markdown(f"**Tạm tính:** {subtotal:,.0f} VNĐ")
            if discount_amount > 0:
                st.markdown(f"**Giảm giá:** -{discount_amount:,.0f} VNĐ", unsafe_allow_html=True)
            st.markdown(
                f"<h2 style='color: #4ade80; text-align: right;'>Tổng Bill: {final_total:,.0f} VNĐ</h2>",
                unsafe_allow_html=True,
            )

            st.markdown("---")
            st.markdown("### 💳 Phương thức thanh toán")
            pay_method = st.radio("Chọn hình thức:", ["Tiền mặt tại quầy", "Chuyển khoản VietQR Ngân hàng"])

            if pay_method == "Chuyển khoản VietQR Ngân hàng":
                st.markdown(
                    """
                    <div style="text-align: center; background: #ffffff; padding: 15px; border-radius: 14px; color: #000;">
                        <img src="https://api.vietqr.io/image/970422-0391234567-xxxx.jpg?accountName=LIMDIM%20COFFEE&amount="""
                    + str(int(final_total))
                    + """&addInfo=Thanh%20toan%20Bill%20Limdim" width="190px">
                        <p style="margin-top: 8px; font-weight: bold; color: #111;">Quét mã VietQR thanh toán tự động</p>
                        <p style="font-size: 0.85rem; color: #555;">MB Bank | STK: 0391234567<br>Chủ tài khoản: LIMDIM COFFEE</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            if st.button("🚀 Gửi Order Cho Bartender"):
                if not st.session_state.cart:
                    st.error("Giỏ hàng trống!")
                else:
                    st.balloons()
                    st.success("🎉 Đặt món thành công! Các Master Bartender tại Limdim đang pha chế ngay lập tức!")
                    st.session_state.cart = []
                    st.session_state.discount_code = None
                    st.session_state.discount_percent = 0
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TÍNH NĂNG 2: CỔNG GACHA WISH (5 SAO)
# ==========================================
elif nav_option == "✨ Cổng Gacha Wish (5 Sao)":
    st.markdown('<div class="genshin-card">', unsafe_allow_html=True)
    st.markdown("## ✨ Cổng Cầu Nguyện Tinh Tú (Gacha Wish System)")
    st.write("Sử dụng Nguyên Thạch hoặc lượt cầu nguyện để quay ra các mức giảm giá độc quyền siêu cấp (3 sao, 4 sao, 5 sao huyền thoại)!")

    col_w1, col_w2 = st.columns([1, 1])
    with col_w1:
        st.markdown(
            """
            * **⭐⭐⭐ Tinh Tú Thường:** Giảm **10%** tổng bill (Tỷ lệ 60%)
            * **⭐⭐⭐⭐ Sự Kiện Đặc Biệt:** Giảm **20%** tổng bill (Tỷ lệ 30%)
            * **⭐⭐⭐⭐⭐ Vực Thẳm Huyền Thoại:** Giảm **50%** tổng bill (Tỷ lệ 10%)
            """
        )
        st.info(f"Số Nguyên Thạch hiện có: **{st.session_state.user_primogems} 💎**")

    with col_w2:
        st.markdown("<div style='text-align: center; padding-top: 15px;'>", unsafe_allow_html=True)
        if st.button("🌠 CẦU NGUYỆN 1 LẦN (160 💎)"):
            if st.session_state.user_primogems < 160:
                st.error("Không đủ Nguyên Thạch! Hãy ghé quầy check-in để nhận thêm.")
            else:
                st.session_state.user_primogems -= 160
                with st.spinner("🌌 Mở cổng không gian Teyvat... Sao băng xuất hiện..."):
                    time.sleep(1.5)

                roll = random.randint(1, 100)
                if roll <= 10:
                    discount = 50
                    tier = "⭐⭐⭐⭐⭐ (HUYỀN THOẠI 5 SAO - Giảm 50%)"
                    code = "TEYVAT50"
                    st.balloons()
                elif roll <= 40:
                    discount = 20
                    tier = "⭐⭐⭐⭐ (SỰ KIỆN 4 SAO - Giảm 20%)"
                    code = "TEYVAT20"
                else:
                    discount = 10
                    tier = "⭐⭐⭐ (TIÊU CHUẨN 3 SAO - Giảm 10%)"
                    code = "TEYVAT10"

                st.session_state.discount_percent = discount
                st.session_state.discount_code = code

                st.markdown(
                    f"""
                    <div style="background: rgba(234, 179, 8, 0.15); border: 2px solid #fde047; padding: 20px; border-radius: 14px; text-align: center; margin-top: 15px;">
                        <h3 style="color: #fde047; margin: 0;">🌟 TRIỆU HỒI THÀNH CÔNG!</h3>
                        <p style="font-size: 1.1rem; font-weight: bold; margin: 10px 0;">{tier}</p>
                        <p>Mã giảm giá đã lưu: <b style="color: #4ade80; font-size: 1.2rem;">{code}</b></p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TÍNH NĂNG 3: XÚC XẮC ĐỊNH MỆNH
# ==========================================
elif nav_option == "🎲 Xúc Xắc Định Mệnh":
    st.markdown('<div class="genshin-card">', unsafe_allow_html=True)
    st.markdown("## 🎲 Thử Thách Xúc Xắc Định Mệnh Teyvat")
    st.write("Gieo xúc xắc nguyên tố để thử thách vận may nhận voucher giảm giá trực tiếp cho hóa đơn!")

    if st.button("🎲 Gieo Xúc Xắc Ngay"):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        total_score = dice1 + dice2

        col_d1, col_d2, col_d3 = st.columns(3)
        col_d1.metric("Xúc xắc 1", f"🎲 {dice1}")
        col_d2.metric("Xúc xắc 2", f"🎲 {dice2}")
        col_d3.metric("Tổng điểm", f"⭐ {total_score}")

        if total_score >= 11:
            st.session_state.discount_percent = 30
            st.session_state.discount_code = "DICE30"
            st.success("🏆 Tuyệt đỉnh! Tổng điểm >= 11 -> Nhận ngay Voucher giảm **30%** (Mã: DICE30)!")
            st.balloons()
        elif total_score >= 8:
            st.session_state.discount_percent = 15
            st.session_state.discount_code = "DICE15"
            st.info("✨ Khá lắm! Tổng điểm 8-10 -> Nhận ngay Voucher giảm **15%** (Mã: DICE15)!")
        else:
            st.warning("🍀 Thần may mắn hẹn gặp bạn lần sau! Ghé quầy nhận ngay một viên kẹo ngọt miễn phí nhé.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TÍNH NĂNG 4: SƠ ĐỒ BÀN TRỐNG QUÁN
# ==========================================
elif nav_option == "🪑 Sơ Đồ Bàn Trống Quán":
    st.markdown('<div class="genshin-card">', unsafe_allow_html=True)
    st.markdown("## 🪑 Bản Đồ Ghế Ngồi Tại Quán Limdim")
    st.write("Kiểm tra bàn trống thời gian thực để chọn không gian ngồi phù hợp khi ghé quán.")

    cols = st.columns(3)
    idx = 0
    for table_name, is_empty in st.session_state.table_status.items():
        with cols[idx % 3]:
            st.markdown(
                f"<div style='background: rgba(15, 23, 42, 0.7); padding: 16px; border-radius: 14px; margin-bottom: 15px; border: 1px solid rgba(245, 158, 11, 0.3); text-align: center;'>",
                unsafe_allow_html=True,
            )
            st.markdown(f"**{table_name}**")
            if is_empty:
                st.markdown("<p style='color: #4ade80; font-weight: bold; margin: 8px 0;'>🟢 CÒN TRỐNG</p>", unsafe_allow_html=True)
                if st.button(f"Đặt bàn này", key=f"book_{table_name}"):
                    st.session_state.table_status[table_name] = False
                    st.success(f"Đã giữ chỗ thành công {table_name}!")
                    st.rerun()
            else:
                st.markdown("<p style='color: #f87171; font-weight: bold; margin: 8px 0;'>🔴 ĐÃ CÓ KHÁCH</p>", unsafe_allow_html=True)
                if st.button(f"Giải phóng bàn", key=f"free_{table_name}"):
                    st.session_state.table_status[table_name] = True
                    st.success(f"{table_name} đã sẵn sàng đón khách mới!")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        idx += 1
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# FOOTER BẢN QUYỀN
# ==========================================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #64748b; font-size: 0.9rem;'>☕ Limdim Coffee • Teyvat Exploration Experience • Powered by Streamlit</p>",
    unsafe_allow_html=True,
)
