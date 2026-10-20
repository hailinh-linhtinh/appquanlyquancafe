import base64
import random
import time
import pandas as pd
import streamlit as st

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Limdim Coffee • Teyvat Edition",
    page_icon="⭐",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Hàm mã hóa video nền động
def set_background_video(video_file):
    try:
        with open(video_file, "rb") as f:
            encoded_video = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
        <style>
        .stApp {{ background: transparent !important; font-family: 'Plus Jakarta Sans', sans-serif; color: #f1f5f9; }}
        #bg-video {{ position: fixed; right: 0; bottom: 0; min-width: 100%; min-height: 100%; z-index: -999; object-fit: cover; filter: brightness(0.5) contrast(1.1); }}
        @keyframes cardGlow {{
            0% {{ border-color: rgba(245, 158, 11, 0.3); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6); }}
            50% {{ border-color: rgba(245, 158, 11, 0.8); box-shadow: 0 12px 40px rgba(245, 158, 11, 0.3); }}
            100% {{ border-color: rgba(245, 158, 11, 0.3); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6); }}
        }}
        .genshin-title {{
            font-family: 'Cinzel', serif; font-weight: 900;
            background: linear-gradient(180deg, #ffffff 0%, #fde047 50%, #ca8a04 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            text-shadow: 0px 4px 25px rgba(234, 179, 8, 0.8); text-align: center; font-size: 2.8rem; letter-spacing: 2px; margin-bottom: 0px;
        }}
        .genshin-subtitle {{ text-align: center; color: #cbd5e1; font-style: italic; font-size: 1.1rem; margin-bottom: 25px; font-family: 'Cinzel', serif; }}
        .genshin-card {{ background: rgba(11, 15, 25, 0.85); border: 2px solid rgba(245, 158, 11, 0.4); border-radius: 20px; padding: 20px; backdrop-filter: blur(14px); margin-bottom: 20px; animation: cardGlow 5s infinite ease-in-out; }}
        .stButton>button {{
            background: linear-gradient(135deg, #d97706 0%, #b45309 50%, #78350f 100%); color: #fffdf0; border: 1px solid #fde047; border-radius: 12px;
            font-family: 'Cinzel', serif; font-weight: 700; letter-spacing: 1px; padding: 0.6rem 1.2rem; transition: all 0.35s ease; box-shadow: 0 4px 20px rgba(217, 119, 6, 0.4);
        }}
        .stButton>button:hover {{ background: linear-gradient(135deg, #f59e0b 0%, #d97706 50%, #b45309 100%); border-color: #ffffff; box-shadow: 0 0 30px rgba(253, 224, 71, 0.9); transform: translateY(-3px); }}
        .element-tag {{ display: inline-block; padding: 3px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; margin-right: 4px; text-transform: uppercase; }}
        .pyro {{ background: rgba(239, 68, 68, 0.25); color: #f87171; border: 1px solid #ef4444; }}
        .hydro {{ background: rgba(59, 130, 246, 0.25); color: #60a5fa; border: 1px solid #3b82f6; }}
        .cryo {{ background: rgba(56, 189, 248, 0.25); color: #38bdf8; border: 1px solid #0284c7; }}
        .electro {{ background: rgba(168, 85, 247, 0.25); color: #c084fc; border: 1px solid #a855f7; }}
        .dendro {{ background: rgba(34, 197, 94, 0.25); color: #4ade80; border: 1px solid #22c55e; }}
        .anemo {{ background: rgba(45, 212, 191, 0.25); color: #2dd4bf; border: 1px solid #14b8a6; }}
        .geo {{ background: rgba(234, 179, 8, 0.25); color: #facc15; border: 1px solid #eab308; }}
        [data-testid="stSidebar"] {{ background: rgba(7, 9, 19, 0.92); border-right: 2px solid rgba(245, 158, 11, 0.25); }}
        </style>
        <video autoplay muted loop id="bg-video"><source src="data:video/mp4;base64,{encoded_video}" type="video/mp4"></video>
        """,
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        pass


set_background_video("teyvat.mp4")

# ==========================================
# KHỞI TẠO SESSION STATE
# ==========================================
if "cart" not in st.session_state:
    st.session_state.cart = []
if "discount_code" not in st.session_state:
    st.session_state.discount_code = None
if "discount_percent" not in st.session_state:
    st.session_state.discount_percent = 0
if "customer_name" not in st.session_state:
    st.session_state.customer_name = "Lữ Khách Vô Danh"

# Lưu trữ Nguyên Thạch riêng cho từng khách hàng
if "primogems_db" not in st.session_state:
    st.session_state.primogems_db = {}

# 12 Bàn chuẩn theo hình ảnh bản đồ game
if "table_status" not in st.session_state:
    st.session_state.table_status = {
        "Bàn 01: Mondstadt": True,
        "Bàn 02: Liyue": False,
        "Bàn 03: Inazuma": True,
        "Bàn 04: Sumeru": True,
        "Bàn 05: Fontaine": False,
        "Bàn 06: Natlan": True,
        "Bàn 07: Nod-Krai": True,
        "Bàn 08: Snezhnaya": False,
        "Bàn 09: Enkanomiya": True,
        "Bàn 10: Vực Đá Sâu - Khu Mỏ Ngầm": True,
        "Bàn 11: Biển Kỷ Nguyên Cũ": False,
        "Bàn 12: Thần Điện Không Gian": True,
    }

if "boardgames" not in st.session_state:
    st.session_state.boardgames = {
        "Bài Ma Sói": True,
        "Cờ Cá Ngựa": True,
        "Cờ Vua": True,
        "Cờ Tướng": True,
        "Khối Rubik": False,
        "True or Dare": True,
        "Bài Uno": True,
        "Mèo Nổ": False,
    }

# ==========================================
# DỮ LIỆU MENU ĐỦ 15 MÓN NƯỚC & 5 MÓN BÁNH
# ==========================================
DRINKS_MENU = {
    "Cà Phê Muối Fontaine": {
        "price": 45000,
        "elem": "hydro",
        "desc": "Hương vị mặn mòi dòng nước nguyên thủy.",
        "img": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=600&q=80",
    },
    "Bạc Xỉu Nguyệt Quang": {
        "price": 42000,
        "elem": "cryo",
        "desc": "Ngọt ngào và mát lạnh như sương sớm Mondstadt.",
        "img": "https://images.unsplash.com/photo-1572442388796-11668a67e53d?auto=format&fit=crop&w=600&q=80",
    },
    "Espresso Địa Mạch": {
        "price": 35000,
        "elem": "pyro",
        "desc": "Đánh thức sức mạnh hỏa diệm nguyên tố.",
        "img": "https://images.unsplash.com/photo-1510591509098-f4fdc6d0ff04?auto=format&fit=crop&w=600&q=80",
    },
    "Trà Đào Hỏa Nguyên": {
        "price": 48000,
        "elem": "pyro",
        "desc": "Bùng nổ vị giác với đào tươi và thạch lửa.",
        "img": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=600&q=80",
    },
    "Soda Băng Giá Cryo": {
        "price": 46000,
        "elem": "cryo",
        "desc": "Soda chanh thanh mát sảng khoái băng giá.",
        "img": "https://images.unsplash.com/photo-1551024709-8f23befc6f87?auto=format&fit=crop&w=600&q=80",
    },
    "Matcha Latte Sumeru": {
        "price": 50000,
        "elem": "dendro",
        "desc": "Hương trà xanh nguyên bản đậm đà học viện.",
        "img": "https://images.unsplash.com/photo-1536256263959-770b48d82b08?auto=format&fit=crop&w=600&q=80",
    },
    "Sinh Tố Xoài Natlan": {
        "price": 54000,
        "elem": "pyro",
        "desc": "Xoài chín ngọt ngào dưới ánh nắng rực lửa.",
        "img": "https://images.unsplash.com/photo-1553530666-ba11a7da3888?auto=format&fit=crop&w=600&q=80",
    },
    "Trà Sữa Khoai Môn Inazuma": {
        "price": 52000,
        "elem": "electro",
        "desc": "Khoai môn bùi béo kết hợp trà sữa truyền thống.",
        "img": "https://images.unsplash.com/photo-1541658016709-82535e94bc69?auto=format&fit=crop&w=600&q=80",
    },
    "Nước Ép Việt Quất": {
        "price": 49000,
        "elem": "hydro",
        "desc": "Việt quất tươi mọng nước giàu vitamin.",
        "img": "https://images.unsplash.com/photo-1527661591475-527312dd65f5?auto=format&fit=crop&w=600&q=80",
    },
    "Hồng Trà Kem Cheese": {
        "price": 53000,
        "elem": "cryo",
        "desc": "Lớp kem mặn bồng bềnh phủ trên hồng trà.",
        "img": "https://images.unsplash.com/photo-1556742049-0a67d553c2a5?auto=format&fit=crop&w=600&q=80",
    },
    "Cacao Nóng Vực Thẳm": {
        "price": 48000,
        "elem": "pyro",
        "desc": "Socola đắng nhẹ nguyên chất từ cõi tối.",
        "img": "https://images.unsplash.com/photo-1542990253-0d0f5be5f0ed?auto=format&fit=crop&w=600&q=80",
    },
    "Cold Brew Trái Cây": {
        "price": 55000,
        "elem": "dendro",
        "desc": "Cà phê ủ lạnh kết hợp trái cây nhiệt đới.",
        "img": "https://images.unsplash.com/photo-1517701550927-30cf4ba1dba5?auto=format&fit=crop&w=600&q=80",
    },
    "Trà Xanh Hoa Nhài": {
        "price": 40000,
        "elem": "anemo",
        "desc": "Thanh tao hương nhài bay bổng gió trời.",
        "img": "https://images.unsplash.com/photo-1576092768241-dec231879fc3?auto=format&fit=crop&w=600&q=80",
    },
    "Sữa Tươi Trân Châu": {
        "price": 50000,
        "elem": "geo",
        "desc": "Sữa tươi thanh paster kèm trân châu đường đen.",
        "img": "https://images.unsplash.com/photo-1505576399279-565b52d4ac71?auto=format&fit=crop&w=600&q=80",
    },
    "Nước Chanh Mật Tông": {
        "price": 38000,
        "elem": "anemo",
        "desc": "Giải khát thanh lọc cơ thể tức thì.",
        "img": "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?auto=format&fit=crop&w=600&q=80",
    },
}

DESSERTS_MENU = {
    "Mousse Trà Xanh": {
        "price": 45000,
        "desc": "Mềm mịn vị matcha nguyên bản từ đảo Narukami.",
        "img": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=600&q=80",
    },
    "Tiramisu Hạt Dẻ": {
        "price": 50000,
        "desc": "Hương vị lãng mạn kinh điển xứ sở nghệ thuật.",
        "img": "https://images.unsplash.com/photo-1571115177098-24ec42ed204d?auto=format&fit=crop&w=600&q=80",
    },
    "Su Kem Mondstadt": {
        "price": 35000,
        "desc": "Tan chảy ngay từ miếng cắn đầu tiên.",
        "img": "https://images.unsplash.com/photo-1509440159596-0249088772ff?auto=format&fit=crop&w=600&q=80",
    },
    "Tart Trứng Liyue": {
        "price": 32000,
        "desc": "Vỏ ngàn lớp giòn rụm, nhân trứng béo ngậy.",
        "img": "https://images.unsplash.com/photo-1519869325930-281384150729?auto=format&fit=crop&w=600&q=80",
    },
    "Brownie Socola": {
        "price": 48000,
        "desc": "Socola nguyên chất đậm sâu kích thích vị giác.",
        "img": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=600&q=80",
    },
}

BOARDGAMES_DATA = {
    "Bài Ma Sói": {
        "desc": "Trò chơi suy luận tâm lý kinh điển cho hội bạn.",
        "img": "https://images.unsplash.com/photo-1511193311914-0346f16efe90?auto=format&fit=crop&w=600&q=80",
    },
    "Cờ Cá Ngựa": {
        "desc": "Trò chơi bàn cờ quen thuộc gắn liền tuổi thơ.",
        "img": "https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?auto=format&fit=crop&w=600&q=80",
    },
    "Cờ Vua": {
        "desc": "Đấu trí đỉnh cao trên bàn cờ vua chiến thuật.",
        "img": "https://images.unsplash.com/photo-1529699211952-734e80c4d42b?auto=format&fit=crop&w=600&q=80",
    },
    "Cờ Tướng": {
        "desc": "Trận chiến tướng sĩ tượng xe pháo mã truyền thống.",
        "img": "https://images.unsplash.com/photo-1586165368502-1bad197a6461?auto=format&fit=crop&w=600&q=80",
    },
    "Khối Rubik": {
        "desc": "Thử thách tư duy logic và tốc độ xoay khối.",
        "img": "https://images.unsplash.com/photo-1591991564624-370c242e8bbd?auto=format&fit=crop&w=600&q=80",
    },
    "True or Dare": {
        "desc": "Bộ bài thử thách Thật hay Thách vui nhộn.",
        "img": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=600&q=80",
    },
    "Bài Uno": {
        "desc": "Bài Uno lật ngược tình thế bất ngờ cùng chiến hữu.",
        "img": "https://images.unsplash.com/photo-1563227812-0ea4c22e6cc8?auto=format&fit=crop&w=600&q=80",
    },
    "Mèo Nổ": {
        "desc": "Game thẻ bài mèo nổ hài hước đầy may rủi.",
        "img": "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&w=600&q=80",
    },
}

TOPPINGS = {
    "Trân châu đen (+5k)": 5000,
    "Trân châu trắng (+5k)": 5000,
    "Phô mai viên (+7k)": 7000,
    "Kem Cheese (+10k)": 10000,
}

# ==========================================
# HEADER
# ==========================================
st.markdown(
    '<div class="genshin-title">✨ LIMDIM COFFEE • TEYVAT STATION</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="genshin-subtitle">"Hành trình phiêu lưu vị giác giữa các vị thần và đại lục nguyên tố"</div>',
    unsafe_allow_html=True,
)

# ==========================================
# SIDEBAR - QUẢN LÝ KHÁCH HÀNG & NGUYÊN THẠCH RIÊNG
# ==========================================
with st.sidebar:
    st.markdown("### 🌟 ĐĂNG NHẬP LỮ KHÁCH")
    input_name = st.text_input(
        "Nhập tên Lữ Khách của bạn:", value=st.session_state.customer_name
    )
    if input_name:
        st.session_state.customer_name = input_name

    # Lấy số nguyên thạch của riêng khách hàng hiện tại
    current_user_gems = st.session_state.primogems_db.get(
        st.session_state.customer_name, 0
    )

    st.info(
        f"👤 Lữ khách: **{st.session_state.customer_name}**\n\n💎 Nguyên Thạch: **{current_user_gems} / 160 ✨**"
    )

    if current_user_gems >= 160:
        st.success("🎉 Đủ 160 Nguyên Thạch! Đổi lượt Gacha ngay!")
    else:
        needed = 160 - current_user_gems
        st.caption(
            f"💡 Cần thêm `{needed} 💎` nữa để đổi lượt Gacha (25k bill = 16 💎)."
        )

    nav_option = st.radio(
        "Chọn không gian:",
        [
            "🛒 Khám Phá Menu & Gọi Món",
            "✨ Cổng Gacha Wish",
            "🎲 Kho Trò Chơi Boardgame & Cờ",
            "🪑 Sơ Đồ Bàn Trống",
        ],
    )

    st.markdown("---")
    st.markdown("### 📊 Giỏ Hàng")
    total_items = sum([item["qty"] for item in st.session_state.cart])
    st.metric(label="Tổng sản phẩm", value=f"{total_items} món")
    if st.button("🗑️ Xóa giỏ hàng"):
        st.session_state.cart = []
        st.session_state.discount_code = None
        st.session_state.discount_percent = 0
        st.success("Đã làm sạch giỏ hàng!")
        st.rerun()

# ==========================================
# 1. MENU & GỌI MÓN (ĐỦ 15 MÓN NƯỚC & 5 BÁNH)
# ==========================================
if nav_option == "🛒 Khám Phá Menu & Gọi Món":
    col_menu_left, col_order_right = st.columns([1.3, 1])

    with col_menu_left:
        st.markdown(
            '<div class="genshin-card"><h3>🍹 Thức Uống Teyvat (15 Món)</h3>',
            unsafe_allow_html=True,
        )
        drink_keys = list(DRINKS_MENU.keys())
        for i in range(0, len(drink_keys), 2):
            c1, c2 = st.columns(2)
            for c_idx, col_slot in enumerate([c1, c2]):
                if i + c_idx < len(drink_keys):
                    d_name = drink_keys[i + c_idx]
                    d_info = DRINKS_MENU[d_name]
                    with col_slot:
                        st.image(d_info["img"], use_column_width=True)
                        st.markdown(f"**{d_name}**")
                        st.markdown(
                            f"<span class='element-tag {d_info['elem']}'>{d_info['elem'].upper()}</span> <b style='color: #fde047;'>{d_info['price']:,.0f}đ</b>",
                            unsafe_allow_html=True,
                        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="genshin-card"><h3>🍰 Bánh Ngọt Tráng Miệng (5 Món)</h3>',
            unsafe_allow_html=True,
        )
        cake_keys = list(DESSERTS_MENU.keys())
        for i in range(0, len(cake_keys), 2):
            c1, c2 = st.columns(2)
            for c_idx, col_slot in enumerate([c1, c2]):
                if i + c_idx < len(cake_keys):
                    c_name = cake_keys[i + c_idx]
                    c_info = DESSERTS_MENU[c_name]
                    with col_slot:
                        st.image(c_info["img"], use_column_width=True)
                        st.markdown(f"**{c_name}**")
                        st.markdown(
                            f"<b style='color: #4ade80;'>{c_info['price']:,.0f}đ</b>",
                            unsafe_allow_html=True,
                        )
        st.markdown("</div>", unsafe_allow_html=True)

    with col_order_right:
        st.markdown(
            f'<div class="genshin-card"><h3>🧋 Gọi Món Cho: <span style="color: #fde047;">{st.session_state.customer_name}</span></h3>',
            unsafe_allow_html=True,
        )
        selected_drink = st.selectbox("Chọn món nước:", drink_keys)
        drink_info = DRINKS_MENU[selected_drink]

        sugar = st.selectbox("Độ ngọt", ["100%", "75%", "50%", "25%", "0%"])
        ice = st.selectbox(
            "Lượng đá", ["Bình thường", "Ít đá", "Đá riêng", "Không đá"]
        )
        size = st.selectbox(
            "Size ly", ["M (Tiêu chuẩn)", "L (+5,000đ)", "XL (+10,000đ)"]
        )

        selected_cake = st.selectbox(
            "Chọn bánh ngọt ăn kèm:", ["-- Không dùng bánh ngọt --"] + cake_keys
        )

        cake_data = None
        if selected_cake != "-- Không dùng bánh ngọt --":
            c_info = DESSERTS_MENU[selected_cake]
            cake_data = {
                "name": selected_cake,
                "price": c_info["price"],
                "desc": c_info["desc"],
            }

        selected_toppings = []
        st.markdown("✨ **Topping:**")
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
        note = st.text_input("Ghi chú", placeholder="VD: ít đá...")

        if st.button("➕ THÊM VÀO GIỎ HÀNG", use_container_width=True):
            actual_price = drink_info["price"]
            if "L (+5,000đ)" in size:
                actual_price += 5000
            elif "XL (+10,000đ)" in size:
                actual_price += 10000

            topping_total = sum([t["price"] for t in selected_toppings])
            total_item_price = (actual_price + topping_total) * qty

            item_order = {
                "customer": st.session_state.customer_name,
                "name": selected_drink,
                "price_unit": actual_price,
                "size": size,
                "sugar": sugar,
                "ice": ice,
                "toppings": selected_toppings,
                "qty": qty,
                "note": note,
                "total_price": total_item_price,
                "paired_cake": cake_data,
            }
            st.session_state.cart.append(item_order)
            st.success(f"Đã thêm món vào giỏ hàng của {st.session_state.customer_name}!")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="genshin-card"><h3>🧾 Hóa Đơn & Xuất Bill</h3>',
            unsafe_allow_html=True,
        )
        if not st.session_state.cart:
            st.warning("Giỏ hàng trống!")
        else:
            subtotal = 0
            st.markdown(f"**Khách hàng:** {st.session_state.customer_name}")
            for i, cart_item in enumerate(st.session_state.cart):
                st.markdown(
                    f"**{i+1}. {cart_item['name']}** x{cart_item['qty']} ({cart_item['size']})"
                )
                if cart_item["paired_cake"]:
                    st.caption(
                        f"🍰 Kèm: {cart_item['paired_cake']['name']} ({cart_item['paired_cake']['price']:,.0f}đ)"
                    )
                    subtotal += cart_item["paired_cake"]["price"]
                subtotal += cart_item["total_price"]
                st.markdown(
                    "<hr style='margin: 4px 0; opacity: 0.1;'>",
                    unsafe_allow_html=True,
                )

            if st.session_state.discount_percent > 0:
                discount_amount = subtotal * (
                    st.session_state.discount_percent / 100
                )
                st.success(f"Voucher giảm: -{st.session_state.discount_percent}%")
            else:
                discount_amount = 0

            final_total = subtotal - discount_amount

            st.markdown(
                f"<h3 style='color: #4ade80; text-align: right;'>Tổng Bill: {final_total:,.0f} VNĐ</h3>",
                unsafe_allow_html=True,
            )

            pay_method = st.radio(
                "Thanh toán:", ["Tiền mặt", "VietQR Ngân hàng"]
            )
            if pay_method == "VietQR Ngân hàng":
                st.markdown(
                    """
                    <div style="text-align: center; background: white; padding: 10px; border-radius: 10px; color: black;">
                        <img src="https://api.vietqr.io/image/970422-0391234567-xxxx.jpg?accountName=LIMDIM&amount="""
                    + str(int(final_total))
                    + """" width="140px">
                        <p style="font-size: 0.8rem; margin: 4px 0; font-weight: bold;">Quét mã VietQR</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            if st.button("🚀 XUẤT HÓA ĐƠN & TÍCH NGUYÊN THẠCH", use_container_width=True):
                earned_primogems = int(final_total // 25000) * 16
                
                # Cập nhật Nguyên Thạch riêng cho khách hàng này
                current_db_gems = st.session_state.primogems_db.get(st.session_state.customer_name, 0)
                st.session_state.primogems_db[st.session_state.customer_name] = current_db_gems + earned_primogems
                st.session_state.user_primogems = st.session_state.primogems_db[st.session_state.customer_name]

                st.balloons()
                st.success(
                    f"🎉 Xuất hóa đơn thành công cho **{st.session_state.customer_name}**! +{earned_primogems} 💎 Nguyên Thạch đã cộng vào ví cá nhân!"
                )
                st.session_state.cart = []
                st.session_state.discount_code = None
                st.session_state.discount_percent = 0
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 2. CỔNG GACHA WISH (5 SAO)
# ==========================================
elif nav_option == "✨ Cổng Gacha Wish":
    st.markdown('<div class="genshin-card">', unsafe_allow_html=True)
    st.markdown(f"## ✨ Cổng Cầu Nguyện của: {st.session_state.customer_name}")
    
    current_user_gems = st.session_state.primogems_db.get(st.session_state.customer_name, 0)
    st.write(
        "Sử dụng Nguyên Thạch tích lũy riêng của bạn (160 💎 / lần quay) để nhận mã giảm giá!"
    )

    col_w1, col_w2 = st.columns([1, 1])
    with col_w1:
        st.markdown(
            """
            * **⭐⭐⭐ Tinh Tú Thường:** Giảm **10%** (Tỷ lệ 60%)
            * **⭐⭐⭐⭐ Sự Kiện:** Giảm **20%** (Tỷ lệ 30%)
            * **⭐⭐⭐⭐⭐ Huyền Thoại:** Giảm **50%** (Tỷ lệ 10%)
            """
        )
        st.info(f"Số Nguyên Thạch của bạn: **{current_user_gems} 💎**")

    with col_w2:
        st.markdown(
            "<div style='text-align: center; padding-top: 15px;'>",
            unsafe_allow_html=True,
        )
        if st.button("🌠 CẦU NGUYỆN 1 LẦN (160 💎)"):
            if current_user_gems < 160:
                st.error("❌ Bạn không đủ 160 Nguyên Thạch! Hãy xuất thêm hóa đơn để tích lũy.")
            else:
                st.session_state.primogems_db[st.session_state.customer_name] -= 160
                st.session_state.user_primogems = st.session_state.primogems_db[st.session_state.customer_name]
                
                with st.spinner("🌌 Mở cổng không gian Teyvat..."):
                    time.sleep(1.2)

                roll = random.randint(1, 100)
                if roll <= 10:
                    discount, tier, code = 50, "⭐⭐⭐⭐⭐ (HUYỀN THOẠI 5 SAO - Giảm 50%)", "TEYVAT50"
                    st.balloons()
                elif roll <= 40:
                    discount, tier, code = 20, "⭐⭐⭐⭐ (SỰ KIỆN 4 SAO - Giảm 20%)", "TEYVAT20"
                else:
                    discount, tier, code = 10, "⭐⭐⭐ (TIÊU CHUẨN 3 SAO - Giảm 10%)", "TEYVAT10"

                st.session_state.discount_percent = discount
                st.session_state.discount_code = code
                st.success(f"🌟 Chúc mừng {st.session_state.customer_name} nhận được {tier}! Mã: {code}")
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 3. KHO TRÒ CHƠI BOARDGAME & CỜ
# ==========================================
elif nav_option == "🎲 Kho Trò Chơi Boardgame & Cờ":
    st.markdown('<div class="genshin-card">', unsafe_allow_html=True)
    st.markdown("## 🎲 Kho Trò Chơi Boardgame & Cờ Giải Trí")
    st.write(
        "Kiểm tra hình ảnh và trạng thái các tựa game bài, cờ vua, cờ tướng, rubik tại quán để mượn chơi!"
    )

    game_keys = list(BOARDGAMES_DATA.keys())
    for i in range(0, len(game_keys), 3):
        cols = st.columns(3)
        for c_idx, col_slot in enumerate(cols):
            if i + c_idx < len(game_keys):
                g_name = game_keys[i + c_idx]
                g_info = BOARDGAMES_DATA[g_name]
                is_available = st.session_state.boardgames[g_name]

                with col_slot:
                    st.markdown(
                        f"<div style='background: rgba(15, 23, 42, 0.7); padding: 14px; border-radius: 14px; margin-bottom: 15px; border: 1px solid rgba(245, 158, 11, 0.3); text-align: center;'>",
                        unsafe_allow_html=True,
                    )
                    st.image(g_info["img"], use_column_width=True)
                    st.markdown(f"**{g_name}**")
                    st.caption(g_info["desc"])

                    if is_available:
                        st.markdown(
                            "<p style='color: #4ade80; font-weight: bold; margin: 6px 0;'>🟢 CÓ SẴN ĐỂ MƯỢN</p>",
                            unsafe_allow_html=True,
                        )
                        if st.button(f"Mượn chơi", key=f"borrow_{g_name}"):
                            st.session_state.boardgames[g_name] = False
