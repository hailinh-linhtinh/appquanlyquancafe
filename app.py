import random
import time
import pandas as pd
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="limdim coffee • Genshin Edition",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================
# GIAO DIỆN & HIỆU ỨNG CSS (GENSHIN STYLE)
# ==========================================
st.markdown(
    """
    <style>
    /* Import font chữ phong cách fantasy */
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');

    /* Nền động không gian bầu trời Teyvat lấp lánh sao */
    .stApp {
        background: linear-gradient(135deg, #0b0f19 0%, #162032 50%, #1f1b2e 100%);
        background-attachment: fixed;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #e2e8f0;
    }

    /* Hiệu ứng hạt sao rơi nhẹ trên nền */
    @keyframes twinkle {
        0% { opacity: 0.3; transform: scale(0.8); }
        50% { opacity: 1; transform: scale(1.2); }
        100% { opacity: 0.3; transform: scale(0.8); }
    }

    /* Tiêu đề mang phong cách Genshin */
    .genshin-title {
        font-family: 'Cinzel', serif;
        font-weight: 700;
        background: linear-gradient(90deg, #f3e7e2 0%, #ffd700 50%, #ff8c00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 20px rgba(255, 215, 0, 0.4);
        text-align: center;
        font-size: 2.8rem;
        margin-bottom: 0px;
    }

    .genshin-subtitle {
        text-align: center;
        color: #94a3b8;
        font-style: italic;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }

    /* Khung thẻ Glassmorphism */
    .genshin-card {
        background: rgba(22, 32, 50, 0.7);
        border: 1px solid rgba(255, 215, 0, 0.2);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 20px;
    }

    /* Nút bấm phong cách Vision Genshin */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: 1px solid rgba(255, 215, 0, 0.4);
        border-radius: 12px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
        border-color: #ffd700;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
        transform: translateY(-2px);
    }

    /* Tùy chỉnh Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(11, 15, 25, 0.95);
        border-right: 1px solid rgba(255, 215, 0, 0.15);
    }

    /* Badge trạng thái bàn */
    .table-badge-empty {
        background-color: rgba(16, 185, 129, 0.2);
        color: #34d399;
        border: 1px solid #10b981;
        padding: 6px 12px;
        border-radius: 8px;
        text-align: center;
        font-weight: 600;
    }
    .table-badge-full {
        background-color: rgba(239, 68, 68, 0.2);
        color: #f87171;
        border: 1px solid #ef4444;
        padding: 6px 12px;
        border-radius: 8px;
        text-align: center;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# KHỞI TẠO SESSION STATE (GIỎ HÀNG, BÀN, VOUCHER)
# ==========================================
if "cart" not in st.session_state:
    st.session_state.cart = []
if "discount_code" not in st.session_state:
    st.session_state.discount_code = None
if "discount_percent" not in st.session_state:
    st.session_state.discount_percent = 0
if "gacha_history" not in st.session_state:
    st.session_state.gacha_history = []
if "table_status" not in st.session_state:
    # Trạng thái 6 bàn trong quán (True: Trống, False: Đã có khách)
    st.session_state.table_status = {
        "Bàn 01 (Góc Mondstadt)": True,
        "Bàn 02 (Cạnh Liyue)": False,
        "Bàn 03 (Sân thượng Inazuma)": True,
        "Bàn 04 (Thảo nguyên Sumeru)": True,
        "Bàn 05 (Vương quốc Fontaine)": False,
        "Bàn VIP Natlan": True,
    }

# ==========================================
# DỮ LIỆU MENU QUÁN CAFE LIMDIM
# ==========================================
DRINKS_MENU = {
    "Cà phê đậm vị Teyvat": {
        "Năng Lượng Cà Phê Muối (Sứ giả Fontaine)": 45000,
        "Bạc Xỉu Tinh Thể Nguyệt Quang": 42000,
        "Espresso Phong Ấn Địa Mạch": 35000,
        "Cold Brew Trái Cây Phong Thần": 50000,
    },
    "Trà trái cây Nguyên Tố": {
        "Trà Đào Hỏa Nguyên Tố": 48000,
        "Trà Sữa Trân Châu Lôi Nguyên Tố": 52000,
        "Trà Thanh Long Băng Giá (Cryo)": 55000,
        "Hồng Trà Kem Cheese Fontaine": 50000,
    },
    "Đồ uống độc quyền (Signature)": {
        "Nước Ép Hoa Tinh Linh (Oceanid Elixir)": 58000,
        "Sinh Tố Trái Cây Sumeru": 55000,
        "Cacao Nóng Vực Thẳm (Abyss Cocoa)": 48000,
    },
}

DESSERTS_MENU = {
    "Bánh ngọt tráng miệng": {
        "Bánh Mousse Trà Xanh Inazuma": 45000,
        "Bánh Tiramisu Hạt Dẻ Fontaine": 50000,
        "Bánh Su Kem Ngọt Ngào Mondstadt": 35000,
        "Bánh Tart Trứng Liyue Thơm Phức": 32000,
        "Bánh Brownie Socola Vực Thẳm": 45000,
    }
}

TOPPINGS = {
    "Trân châu đen hoàng gia (+8k)": 8000,
    "Trân châu trắng sương mù (+8k)": 8000,
    "Thạch dừa nha đam (+10k)": 10000,
    "Kem Cheese béo ngậy (+12k)": 12000,
    "Pudding trứng béo (+10k)": 10000,
}

# ==========================================
# HEADER GIAO DIỆN CHÍNH
# ==========================================
st.markdown(
    '<div class="genshin-title">☕ LIMDIM COFFEE • TEYVAT STATION</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="genshin-subtitle">"Nơi hội tụ lữ khách khắp các đại lục - Thưởng thức hương vị vượt thời gian"</div>',
    unsafe_allow_html=True,
)

# ==========================================
# THANH ĐIỀU HƯỚNG SIDEBAR & TÍNH NĂNG ĐỘC LẠ
# ==========================================
with st.sidebar:
    st.markdown("### 🌌 TRUNG TÂM LỮ KHÁCH")
    nav_option = st.radio(
        "Chọn khu vực:",
        [
            "🛒 Gọi Món & Thanh Toán",
            "✨ Cổng Gacha Ưu Đãi (Wish)",
            "🎲 Xúc Xắc May Mắn",
            "🪑 Sơ Đồ Bàn Trống",
        ],
    )

    st.markdown("---")
    st.markdown("### 📊 Trạng Thái Giỏ Hàng")
    total_items = sum([item["qty"] for item in st.session_state.cart])
    st.metric(
        label="Số lượng sản phẩm",
        value=f"{total_items} món",
        delta="Sẵn sàng phục vụ",
    )
    if st.button("🗑️ Xóa toàn bộ giỏ hàng"):
        st.session_state.cart = []
        st.session_state.discount_code = None
        st.session_state.discount_percent = 0
        st.success("Đã làm sạch giỏ hàng!")
        st.rerun()

# ==========================================
# TÍNH NĂNG 1: GỌI MÓN & THANH TOÁN (BILL)
# ==========================================
if nav_option == "🛒 Gọi Món & Thanh Toán":
    col1, col2 = st.load_tab_placeholder = (
        st.columns([1.3, 1])
        if "col1" not in locals()
        else (None, None)
    )  # Safe split layout
    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.markdown(
            '<div class="genshin-card"><h3>📜 Menu Đại Lục Limdim</h3>',
            unsafe_allow_html=True,
        )

        category_type = st.selectbox(
            "Phân loại thực đơn:", ["Thức uống", "Bánh ngọt tráng miệng"]
        )

        if category_type == "Thức uống":
            selected_cat = st.selectbox(
                "Chọn dòng sản phẩm:", list(DRINKS_MENU.keys())
            )
            current_menu = DRINKS_MENU[selected_cat]
        else:
            selected_cat = "Bánh ngọt tráng miệng"
            current_menu = DESSERTS_MENU[selected_cat]

        selected_item = st.selectbox("Chọn món:", list(current_menu.keys()))
        item_price = current_menu[selected_item]

        st.info(
            f"💰 Giá cơ bản: **{item_price:,.0f} VNĐ** | Loại: *{selected_cat}*"
        )

        # Tùy chỉnh chi tiết nếu là thức uống
        sugar, ice, size, selected_toppings = "100%", "Bình thường", "M (Tiêu chuẩn)", []
        if category_type == "Thức uống":
            c_sug, c_ice, c_size = st.columns(3)
            with c_sug:
                sugar = st.selectbox(
                    "Đường", ["100%", "70%", "50%", "30%", "0%"]
                )
            with c_ice:
                ice = st.selectbox(
                    "Đá", ["Bình thường", "Ít đá", "Đá riêng", "Không đá"]
                )
            with c_size:
                size = st.selectbox(
                    "Size ly", ["M (Tiêu chuẩn)", "L (+7,000đ)", "XL (+15,000đ)"]
                )

            # Chọn topping
            st.markdown("✨ **Thêm Topping thần kỳ:**")
            top_cols = st.columns(2)
            idx = 0
            for top_name, top_price in TOPPINGS.items():
                with top_cols[idx % 2]:
                    if st.checkbox(top_name, key=f"top_{top_name}"):
                        selected_toppings.append(
                            {"name": top_name, "price": top_price}
                        )
                idx += 1

        qty = st.number_input("Số lượng", min_value=1, max_value=20, value=1)
        note = st.text_input(
            "Ghi chú cho Bartender / Đầu bếp (ví dụ: ít ngọt, mang ra sau...)"
        )

        if st.button("➕ Thêm vào Bill"):
            # Tính giá tiền cộng thêm theo size
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
                "price_unit": actual_price,
                "size": size if category_type == "Thức uống" else "Tiêu chuẩn",
                "sugar": sugar if category_type == "Thức uống" else "N/A",
                "ice": ice if category_type == "Thức uống" else "N/A",
                "toppings": selected_toppings,
                "qty": qty,
                "note": note,
                "total_price": total_item_price,
            }
            st.session_state.cart.append(item_data)
            st.success(f"Đã thêm **{selected_item}** vào hóa đơn!")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown(
            '<div class="genshin-card"><h3>🧾 Hóa Đơn Lữ Khách</h3>',
            unsafe_allow_html=True,
        )
        if not st.session_state.cart:
            st.warning("Giỏ hàng của bạn đang trống. Hãy chọn món bên cạnh nhé!")
        else:
            subtotal = 0
            for i, cart_item in enumerate(st.session_state.cart):
                st.markdown(
                    f"**{i+1}. {cart_item['name']}** x{cart_item['qty']}"
                )
                if cart_item["category"] != "Bánh ngọt tráng miệng":
                    st.caption(
                        f"Size: {cart_item['size']} | Đường: {cart_item['sugar']} | Đá: {cart_item['ice']}"
                    )
                if cart_item["toppings"]:
                    top_names = ", ".join([t["name"] for t in cart_item["toppings"]])
                    st.caption(f"Topping: {top_names}")
                if cart_item["note"]:
                    st.caption(f"📝 *{cart_item['note']}*")
                st.markdown(
                    f"<div style='text-align: right; color: #ffd700; font-weight: bold;'>{cart_item['total_price']:,.0f} VNĐ</div>",
                    unsafe_allow_html=True,
                )
                subtotal += cart_item["total_price"]
                st.markdown("<hr style='margin: 5px 0; opacity: 0.2;'>", unsafe_allow_html=True)

            # Áp dụng Voucher giảm giá từ Gacha/Xúc xắc
            if st.session_state.discount_percent > 0:
                st.success(
                    f"🎉 Đã áp dụng Voucher: **{st.session_state.discount_code}** (-{st.session_state.discount_percent}%)"
                )
                discount_amount = subtotal * (st.session_state.discount_percent / 100)
            else:
                discount_amount = 0

            final_total = subtotal - discount_amount

            st.markdown(f"**Tạm tính:** {subtotal:,.0f} VNĐ")
            if discount_amount > 0:
                st.markdown(
                    f"**Giảm giá:** -{discount_amount:,.0f} VNĐ",
                    unsafe_allow_html=True,
                )
            st.markdown(
                f"<h2 style='color: #34d399; text-align: right;'>Tổng Bill: {final_total:,.0f} VNĐ</h2>",
                unsafe_allow_html=True,
            )

            # Chọn phương thức thanh toán
            st.markdown("---")
            st.markdown("### 💳 Phương thức thanh toán")
            pay_method = st.radio(
                "Chọn hình thức:", ["Tiền mặt tại quầy", "Chuyển khoản QR Ngân hàng"]
            )

            if pay_method == "Chuyển khoản QR Ngân hàng":
                st.markdown(
                    """
                    <div style="text-align: center; background: white; padding: 15px; border-radius: 12px; color: black;">
                        <img src="https://api.vietqr.io/image/970422-0391234567-xxxx.jpg?accountName=LIMDIM%20COFFEE&amount="""
                    + str(int(final_total))
                    + """&addInfo=Thanh%20toan%20Bill%20Limdim" width="200px">
                        <p style="margin-top: 8px; font-weight: bold; color: #111;">Quét mã VietQR để thanh toán</p>
                        <p style="font-size: 0.85rem; color: #555;">Ngân hàng: MB Bank | STK: 0391234567<br>Chủ tài khoản: LIMDIM COFFEE</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            if st.button("🚀 Xác nhận Đặt Món & In Bill"):
                if not st.session_state.cart:
                    st.error("Giỏ hàng trống!")
                else:
                    st.balloons()
                    st.success(
                        "🎉 Đặt món thành công! Bartender Limdim đã nhận order và đang pha chế!"
                    )
                    # Reset giỏ hàng sau khi đặt thành công
                    st.session_state.cart = []
                    st.session_state.discount_code = None
                    st.session_state.discount_percent = 0
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TÍNH NĂNG 2: CỔNG GACHA ƯU ĐÃI (WISH SYSTEM)
# ==========================================
elif nav_option == "✨ Cổng Gacha Ưu Đãi (Wish)":
    st.markdown(
        '<div class="genshin-card">', unsafe_allow_html=True
    )
    st.markdown("## ✨ Cổng Gacha Ưu Đãi - Cầu Nguyện Nguyên Tố")
    st.write(
        "Sử dụng vận may của lữ khách để nhận các mức giảm giá độc quyền cực khủng cho hóa đơn tại Limdim Coffee!"
    )

    col_g1, col_g2 = st.columns([1, 1])
    with col_g1:
        st.markdown(
            """
            * **Phần thưởng 3 Sao (Tím/Xanh):** Giảm 10% tổng bill (Tỷ lệ 60%)
            * **Phần thưởng 4 Sao (Vàng nhạt):** Giảm 20% tổng bill (Tỷ lệ 30%)
            * **Phần thưởng 5 Sao (Huyền Thoại):** Giảm 50% tổng bill (Tỷ lệ 10%)
            """
        )
        wish_type = st.radio("Chọn gói cầu nguyện:", ["Cầu nguyện 1 lần", "Cầu nguyện 10 lần liên tiếp"])

    with col_g2:
        st.markdown(
            "<div style='text-align: center; padding-top: 20px;'>",
            unsafe_allow_html=True,
        )
        if st.button("🌟 BẮT ĐẦU CẦU NGUYỆN (WISH)"):
            with st.spinner("🌌 Triệu hồi tinh tú Teyvat..."):
                time.sleep(1.2)

            # Random phần thưởng gacha
            rates = [10] * 10 + [30] * 30 + [60] * 60  # Tổng 100
            roll = random.choice(rates)

            if roll <= 10:
                discount = 50
                tier = "⭐⭐⭐⭐⭐ (HUYỀN THOẠI - Giảm 50%)"
                code = "LIMDIM50"
                st.balloons()
            elif roll <= 40:
                discount = 20
                tier = "⭐⭐⭐⭐ (SỰ KIỆN - Giảm 20%)"
                code = "LIMDIM20"
            else:
                discount = 10
                tier = "⭐⭐⭐ (TIÊU CHUẨN - Giảm 10%)"
                code = "LIMDIM10"

            st.session_state.discount_percent = discount
            st.session_state.discount_code = code

            st.markdown(
                f"""
                <div style="background: rgba(255, 215, 0, 0.15); border: 2px solid #ffd700; padding: 20px; border-radius: 14px; text-align: center;">
                    <h3 style="color: #ffd700; margin: 0;">🎉 CHÚC MỪNG LỮ KHÁCH!</h3>
                    <p style="font-size: 1.2rem; font-weight: bold; margin: 10px 0;">Nhận được: {tier}</p>
                    <p>Mã giảm giá đã tự động lưu: <b style="color: #34d399; font-size: 1.3rem;">{code}</b></p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TÍNH NĂNG 3: XÚC XẮC MAY MẮN
# ==========================================
elif nav_option == "🎲 Xúc Xắc May Mắn":
    st.markdown(
        '<div class="genshin-card">', unsafe_allow_html=True
    )
    st.markdown("## 🎲 Thử Thách Xúc Xắc Định Mệnh")
    st.write(
        "Gieo hai con xúc xắc. Tổng điểm của bạn sẽ quyết định phần quà topping hoặc voucher tương ứng!"
    )

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
            st.session_state.discount_code = "LUCK30"
            st.success(
                "🏆 Cực phẩm! Tổng điểm từ 11 trở lên -> Nhận ngay Voucher giảm **30%** (Mã: LUCK30)!"
            )
            st.balloons()
        elif total_score >= 8:
            st.session_state.discount_percent = 15
            st.session_state.discount_code = "LUCK15"
            st.info("✨ Khá lắm! Tổng điểm từ 8-10 -> Nhận ngay Voucher giảm **15%** (Mã: LUCK15)!")
        else:
            st.warning(
                "🍀 Thần may mắn đang mỉm cười... Hãy thử lại hoặc ghé quầy nhận một viên kẹo ngọt miễn phí từ Limdim!"
            )
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TÍNH NĂNG 4: SƠ ĐỒ BÀN TRỐNG (TABLE MANAGEMENT)
# ==========================================
elif nav_option == "🪑 Sơ Đồ Bàn Trống":
    st.markdown(
        '<div class="genshin-card">', unsafe_allow_html=True
    )
    st.markdown("## 🪑 Sơ Đồ Trạng Thái Bàn Quán Limdim")
    st.write(
        "Kiểm tra nhanh số bàn còn trống trực tiếp tại quán để chọn chỗ ngồi ưng ý hoặc đặt bàn trước."
    )

    cols = st.columns(3)
    idx = 0
    for table_name, is_empty in st.session_state.table_status.items():
        with cols[idx % 3]:
            st.markdown(
                f"<div style='background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; margin-bottom: 15px; border: 1px solid rgba(255,215,0,0.1); text-align: center;'>",
                unsafe_allow_html=True,
            )
            st.markdown(f"#### {table_name}")
            if is_empty:
                st.markdown(
                    '<div class="table-badge-empty">🟢 CÒN TRỐNG</div>',
                    unsafe_allow_html=True,
                )
                if st.button(f"Đặt bàn này", key=f"book_{table_name}"):
                    st.session_state.table_status[table_name] = False
                    st.success(f"Đã đặt thành công {table_name}!")
                    st.rerun()
            else:
                st.markdown(
                    '<div class="table-badge-full">🔴 ĐÃ CÓ KHÁCH</div>',
                    unsafe_allow_html=True,
                )
                if st.button(f"Trống bàn", key=f"free_{table_name}"):
                    st.session_state.table_status[table_name] = True
                    st.success(f"{table_name} đã được làm trống!")
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        idx += 1
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# FOOTER BẢN QUYỀN
# ==========================================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #64748b; font-size: 0.9rem;'>☕ Limdim Coffee • Phong cách Genshin Impact Teyvat Experience • Made with Streamlit</p>",
    unsafe_allow_html=True,
)
