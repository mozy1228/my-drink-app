import streamlit as st
import random
import time

# 1. 設定網頁標題與初始外觀
st.set_page_config(page_title="🔮 今日心情飲料占卜器", page_icon="🧋", layout="centered")

# 2. 注入自訂的 CSS 樣式，讓介面變得超級明亮、有活力！
st.markdown("""
    <style>
    /* 調整網頁背景與字體 */
    .stApp {
        background: linear-gradient(135deg, #FFF9E6 0%, #FFF0F5 100%);
    }

    /* 大標題樣式：暖橘色系，看起來超好喝 */
    .main-title {
        font-size: 42px !important;
        font-weight: 800;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 5px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    /* 副標題樣式 */
    .sub-title {
        font-size: 18px;
        color: #666666;
        text-align: center;
        margin-bottom: 30px;
    }

    /* 調整下拉選單的標題字體 */
    div[data-testid="stMarkdownContainer"] p strong {
        color: #4A4A4A;
        font-size: 16px;
    }

    /* 占卜結果字體放大與顏色調整 */
    .result-shop {
        font-size: 24px !important;
        color: #004E64;
        font-weight: bold;
    }

    .result-drink {
        font-size: 32px !important;
        color: #FF4B4B;
        font-weight: 900;
        background: linear-gradient(transparent 60%, #FFF0F5 0%);
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# 完整 20 個心情與對應的飲料店、經典品項
mood_beverage_map = {
    "累到快升天 (需要咖啡因)": {"shop": "可不可熟成紅茶", "drinks": ["熟成紅茶", "胭脂紅茶", "熟成冷露", "春芽綠茶"]},
    "今天心情超好 (想熱鬧一下)": {"shop": "五十嵐",
                                  "drinks": ["四季春珍波椰", "冰淇淋紅茶", "燕麥烏龍拿鐵", "黃金烏龍"]},
    "壓力大想咬東西 (嚼勁十足)": {"shop": "麻古茶坊",
                                  "drinks": ["芝芝芒果果粒", "柳橙果粒茶", "波霸紅茶拿鐵", "金萱雙Q"]},
    "憂鬱想吃甜的 (療癒系奶類)": {"shop": "迷客夏",
                                  "drinks": ["大甲芋頭鮮奶", "伯爵紅茶拿鐵", "焙香大麥鮮奶", "青檸香茶"]},
    "心靈乾枯想修仙 (極簡極清爽)": {"shop": "得正", "drinks": ["輕烏龍", "春烏龍", "焙烏龍", "檸檬春烏龍"]},
    "純粹嘴饞想喝茶 (茶感重信徒)": {"shop": "烏弄 UNOCHA",
                                    "drinks": ["名間鄉冬片", "金萱烏龍", "十八領紅玉", "冬片仔鮮奶茶"]},
    "今天走優雅路線 (法式浪漫風)": {"shop": "五桐號",
                                    "drinks": ["五桐茶後鮮奶華爾茲", "最完美手沖泰奶", "杏仁凍五桐茶", "老實人紅茶"]},
    "天氣太熱要融化 (消暑透心涼)": {"shop": "大苑子", "drinks": ["愛文芒果冰沙", "芭樂檸檬", "新鮮水果茶", "翡翠檸檬"]},
    "減脂中罪惡感重 (無糖微卡首選)": {"shop": "龜記茗品", "drinks": ["紅柚翡翠", "三韻紅萱", "蘋果紅萱", "柳丁翡翠"]},
    "星期一症候群 (需要超強重擊)": {"shop": "清心福全", "drinks": ["優多綠茶", "珍珠奶茶", "烏龍綠茶", "蜂蜜綠茶"]},
    "台味靈魂覺醒 (粉粿愛好者)": {"shop": "一沐日",
                                  "drinks": ["逮丸奶茶 (草仔粿)", "粉粿黑糖奶茶", "荔枝烏龍", "油切蕎麥茶"]},
    "日系文青上身 (極致和風茶)": {"shop": "八曜和茶",
                                  "drinks": ["八曜和茶", "柚香覺醒 307", "炙燒濃乳 307", "浪人茶王"]},
    "懷舊復古風情 (港式與紅茶控)": {"shop": "鶴茶樓", "drinks": ["鶴頂紅茶", "綺夢那堤", "金萱青茶", "藝妓紅茶"]},
    "今天想當貴婦 (精緻果茶系列)": {"shop": "Mr.Wish", "drinks": ["大荔芝冬瓜", "光果茶", "芒果厚奶", "草莓芝芝"]},
    "低調不想踩雷 (老牌穩健選擇)": {"shop": "CoCo都可", "drinks": ["百香雙響炮", "奶茶三兄弟", "珍珠奶茶", "美式咖啡"]},
    "文青魂大爆發 (茶香韻味十足)": {"shop": "茶湯會", "drinks": ["鐵觀音拿鐵", "翡翠檸檬", "碳燒烏龍", "珍珠紅豆拿鐵"]},
}

# 使用 HTML 語法渲染精美的亮色系標題
st.markdown('<p class="main-title">🍹 今日心情飲料店占卜 🔮</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">把選擇障礙交給宇宙！選個心情，一鍵抽出今天的專屬快樂！</p>', unsafe_allow_html=True)

# 建立網頁下拉選單
mood_options = list(mood_beverage_map.keys())
selected_mood = st.selectbox("👉 **你現在的心情狀態是？**", mood_options)

st.write("")  # 稍微留白

# 建立占卜按鈕
if st.button("✨ 叮咚！解鎖今日小確幸 ✨", type="primary", use_container_width=True):
    # 搭配可愛的文字與進度條，製造滿滿的期待感
    with st.spinner("🥤 正在瘋狂搖晃雪克杯... 冰塊甜度黃金比例調配中..."):
        time.sleep(1.5)

    shop_info = mood_beverage_map[selected_mood]

    # 隨機抽取飲料與甜度冰量
    recommended_drink = random.choice(shop_info["drinks"])
    ice_levels = ["去冰微糖 🍃", "微冰微糖 ✨", "少冰半糖 🍯", "完全去冰無糖 🥛", "微冰少糖 ⚡"]
    recommended_sugar_ice = random.choice(ice_levels)

    # 炫彩成功的提示框
    st.success("🎉 登登！今日專屬手搖飲出爐囉！")

    # 使用帶有自訂樣式的卡片呈現結果
    st.markdown(f"""
    <div style="background-color: #FFFFFF; padding: 25px; border-radius: 15px; border-left: 8px solid #FF6B35; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
        <p style="margin-bottom:10px; color:#666666; font-size:16px;">🛸 宇宙為你指引的目標：</p>
        <p class="result-shop">🏪 推薦店家：👉 <span style="color:#00A896;">{shop_info['shop']}</span> 👈</p>
        <p class="result-drink">🍹 命定品項：{recommended_drink}</p>
        <p style="font-size: 20px; color: #4A4A4A; margin-top:10px; font-weight:bold;">🍬 推薦黃金比例：{recommended_sugar_ice}</p>
    </div>
    """, unsafe_allow_html=True)

    # 灑花特效（噴出滿滿氣球與彩帶）
    st.balloons()