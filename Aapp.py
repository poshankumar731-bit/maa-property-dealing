import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import random
import requests

# ==========================================
# 🎨 अल्ट्रा-लग्जरी डार्क गोल्ड थीम & कॉन्फिगरेशन
# ==========================================
st.set_page_config(
    page_title="मां प्रॉपर्टी प्रीमियम डिजिटल",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>  
    [data-testid="stAppViewContainer"] {  
        background: linear-gradient(135deg, #0b0f19, #111827);  
        color: #F3F4F6 !important;  
    }  
    /* लग्जरी ग्लास कार्ड्स विद गोल्ड बॉर्डर */  
    .luxury-card, div[data-testid="stForm"] {  
        background: rgba(255, 255, 255, 0.03) !important;  
        backdrop-filter: blur(25px);  
        padding: 25px;  
        border-radius: 20px;  
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.6);  
        margin-bottom: 20px;  
        border: 1px solid rgba(212, 175, 55, 0.2) !important;  
    }  
    /* प्रीमियम बटन्स विद नियॉन इफ़ेक्ट */  
    div.stButton > button {  
        width: 100%;  
        border-radius: 12px;  
        height: 50px;  
        font-size: 16px;  
        font-weight: 700;  
        background: linear-gradient(90deg, #D4AF37, #AA7C11) !important;  
        color: #000000 !important;  
        border: none;  
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);  
        transition: 0.3s;  
    }  
    div.stButton > button:hover {  
        transform: translateY(-2px);  
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);  
    }  
    /* इनपुट बॉक्स स्टाइलिंग */  
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {  
        border-radius: 12px !important;  
        background-color: #1f2937 !important;  
        color: #FFFFFF !important;  
        border: 1px solid rgba(255, 255, 255, 0.15) !important;  
    }  
    label, p, span { color: #E5E7EB !important; }  
    .stMetric {  
        background: rgba(212, 175, 55, 0.05);   
        border: 1px solid rgba(212, 175, 55, 0.15);  
        border-radius: 15px;  
        padding: 15px;  
    }  
    button[data-baseweb="tab"][aria-selected="true"] { color: #D4AF37 !important; font-weight: bold; border-bottom-color: #D4AF37 !important; }  
</style>  
""", unsafe_allow_html=True)

# 🔱 मुख्य लग्जरी ब्रांड हेडर
st.markdown("<h1 style='text-align: center; color: #D4AF37; margin-top: -10px;'>🔱 मां प्रॉपर्टीज़ डिजिटल एम्पायर</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #9CA3AF; font-size:16px;'>🚀 स्टॉक इन्वेंटरी, स्मार्ट सेल्स, बयाना ट्रैकर एवं लाइव ओटीपी बहीखाता</p>", unsafe_allow_html=True)
st.write("---")

# डेटाबेस कॉलम्स परिभाषा
INV_COLS = ['prop_id', 'seller_name', 'district', 'tehsil', 'village', 'ph_no', 'total_area', 'available_area', 'buy_rate', 'total_cost', 'date_added']
SALES_COLS = ['sale_id', 'prop_id', 'buyer_name', 'buyer_phone', 'deal_area', 'deal_rate', 'total_deal_amount', 'amount_paid', 'balance_amount', 'payment_mode', 'tx_date']

# ==========================================
# ☁️ क्लाउड डेटाबेस सिंक (गूगल शीट्स)
# ==========================================
@st.cache_data(ttl=0)
def load_new_app_data():
    inv_blank = pd.DataFrame(columns=INV_COLS)
    sales_blank = pd.DataFrame(columns=SALES_COLS)
    sets_blank = pd.DataFrame([
        {"key": "username", "value": "admin"},
        {"key": "password", "value": "Radhe@2026"},
        {"key": "app_phone", "value": "9876543210"},
        {"key": "sms_api_key", "value": "YOUR_API_KEY"}
    ])
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        try:
            inv = pd.DataFrame(conn.read(worksheet="Inventory"))
            for col in INV_COLS:
                if col not in inv.columns: inv[col] = None
        except: inv = inv_blank
        
        try:
            sales = pd.DataFrame(conn.read(worksheet="SalesBook"))
            for col in SALES_COLS:
                if col not in sales.columns: sales[col] = None
        except: sales = sales_blank
        
        try:
            sets = pd.DataFrame(conn.read(worksheet="Settings"))
        except: sets = sets_blank
        
        return conn, inv, sales, sets
    except:
        return None, inv_blank, sales_blank, sets_blank

conn, inv_df, sales_df, settings_df = load_new_app_data()

# सेटिंग्स रीवरिफ़िकेशन
def get_config(key_name, default):
    if not settings_df.empty and 'key' in settings_df.columns:
        try: return str(settings_df[settings_df['key'] == key_name]['value'].values[0])
        except: return default
    return default

current_user = get_config('username', 'admin')
current_pass = get_config('password', 'Radhe@2026')
current_phone = get_config('app_phone', '9876543210')
sms_key = get_config('sms_api_key', '')

# छत्तीसगढ़ के मुख्य जिले
CG_DISTRICTS = ["रायपुर (Raipur)", "दुर्ग (Durg)", "बिलासपुर (Bilaspur)", "राजनांदगांव", "रायगढ़ (Raigarh)", "कोरबा (Korba)", "बलौदा बाज़ार", "महासमुंद", "धमतरी", "कांकेर", "बस्तर"]

# OTP सिस्टम
def send_otp(mobile, code):
    if not sms_key or sms_key == "YOUR_API_KEY": return True, "DEMO"
    try:
        url = "https://www.fast2sms.com/dev/bulkV2"
        p = {"authorization": sms_key, "variables_values": str(code), "route": "otp", "numbers": str(mobile)}
        res = requests.get(url, params=p, timeout=5)
        return True, res.json()
    except: return False, "Error"

# ==========================================
# 🔒 सिक्योर लॉगिन गेट
# ==========================================
if 'auth_done' not in st.session_state: st.session_state.auth_done = False
if 'otp_sent' not in st.session_state: st.session_state.otp_sent = False
if 'otp_code' not in st.session_state: st.session_state.otp_code = None

if not st.session_state.auth_done:
    st.markdown("<div class='luxury-card'>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #D4AF37;'>🔐 सिक्योर एडमिन लॉगिन ऑथेंटिकेशन</h4>", unsafe_allow_html=True)
    
    if not st.session_state.otp_sent:
        with st.form("login_f1"):
            u = st.text_input("👤 एडमिन यूज़रनेम")
            p = st.text_input("🔑 एडमिन पासवर्ड", type="password")
            if st.form_submit_button("📲 OTP जनरेट करें"):
                if u == current_user and p == current_pass:
                    st.session_state.otp_code = str(random.randint(112233, 998899))
                    _, status = send_otp(current_phone, st.session_state.otp_code)
                    st.session_state.otp_sent = True
                    if status == "DEMO": st.info(f"💡 [टेस्ट मोड] आपका OTP है: {st.session_state.otp_code}")
                    st.rerun()
                else: st.error("❌ यूज़रनेम या पासवर्ड गलत है!")
    else:
        with st.form("login_f2"):
            entered_otp = st.text_input("🔢 6-अंकों का मोबाइल OTP दर्ज करें", type="password")
            c_b1, c_b2 = st.columns(2)
            if c_b1.form_submit_button("🔓 ऐप अनलॉक करें"):
                if entered_otp == st.session_state.generated_otp or entered_otp == st.session_state.otp_code:
                    st.session_state.auth_done = True
                    st.rerun()
                else: st.error("❌ गलत OTP!")
            if c_b2.form_submit_button("🔄 वापस जाएँ"):
                st.session_state.otp_sent = False
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 🏢 मुख्य ऐप इंटरफ़ेस (लॉगिन के बाद)
# ==========================================
else:
    tabs = st.tabs(["📊 लाइव डैशबोर्ड", "🌾 ज़मीन खरीदी एंट्री", "🤝 बिक्री & बयाना बुकिंग", "🔍 स्मार्ट सर्च इंजन", "📂 लाइव स्टॉक रजिस्टर"])

    # ------------------------------------------
    # 1. लाइव डैशबोर्ड
    # ------------------------------------------
    with tabs[0]:
        st.markdown("### 📊 बिजनेस परफॉरमेंस समरी")
        total_purchased = len(inv_df)
        total_sales = len(sales_df)
        
        inflow = pd.to_numeric(sales_df['amount_paid'], errors='coerce').sum() if not sales_df.empty else 0.0
        receivable = pd.to_numeric(sales_df['balance_amount'], errors='coerce').sum() if not sales_df.empty else 0.0
        
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.metric("🌾 कुल खरीदी सौदे", f"{total_purchased} रजिस्ट्री")
        with m2: st.metric("🤝 कुल बिक्री सौदे", f"{total_sales} ग्राहक")
        with m3: st.metric("💵 कुल नगद आवक (Inflow)", f"₹{inflow:,.2f}")
        with m4: st.metric("🔴 मार्केट से कुल लेना (बकाया)", f"₹{receivable:,.2f}")
        
        st.write("---")
        st.info(f"🟢 सिस्टम सुरक्षित रूप से एक्टिव है | मास्टर मोबाइल: +91 {current_phone}")

    # ------------------------------------------
    # 2. ज़मीन खरीदी एंट्री (Stock In)
    # ------------------------------------------
    with tabs[1]:
        st.markdown("#### 🌾 नया स्टॉक / ज़मीन खरीदी एंट्री")
        with st.form("purchase_form", clear_on_submit=True):
            cl1, cl2 = st.columns(2)
            with cl1:
                s_name = st.text_input("👤 विक्रेता / किसान का नाम *")
                dist = st.selectbox("📍 जिला", CG_DISTRICTS)
                teh = st.text_input("📍 तहसील *")
                vil = st.text_input("📍 ग्राम/नगर *")
                ph = st.text_input("🔢 पटवारी हल्का नंबर (PH No.)")
            with cl2:
                area = st.number_input("📐 कुल रकबा (एकड़ / डिसमिल)", min_value=0.0, step=0.01, format="%.2f")
                rate = st.number_input("💵 खरीद रेट (प्रति एकड़ / डिसमिल)", min_value=0.0, step=1.0)
                st.caption("ℹ️ कुल लागत मूल्य रकबा और रेट के आधार पर ऑटो-कैलकुलेट हो जाएगा।")
            
            if st.form_submit_button("💾 स्टॉक डेटाबेस में जमा करें"):
                if not s_name or not teh or not vil or area <= 0 or rate <= 0:
                    st.error("❌ कृपया सभी अनिवार्य (*) जानकारियां सही-सही भरें!")
                else:
                    try:
                        p_id = f"PROP-{random.randint(1000, 9999)}"
                        t_cost = area * rate
                        new_inv_row = pd.DataFrame([{
                            'prop_id': p_id, 'seller_name': s_name, 'district': dist, 'tehsil': teh,
                            'village': vil, 'ph_no': ph, 'total_area': area, 'available_area': area,
                            'buy_rate': rate, 'total_cost': t_cost, 'date_added': datetime.now().strftime("%Y-%m-%d %H:%M")
                        }])
                        if conn:
                            updated_inv = pd.concat([inv_df, new_inv_row], ignore_index=True)
                            conn.update(worksheet="Inventory", data=updated_inv)
                            st.success(f"🎉 नया स्टॉक सुरक्षित! प्रॉपर्टी कोड: {p_id}")
                            st.cache_data.clear()
                            st.rerun()
                    except Exception as e: st.error(f"त्रुटि: {e}")

    # ------------------------------------------
    # 3. बिक्री & बयाना बुकिंग (Sales & Token)
    # ------------------------------------------
    with tabs[2]:
        st.markdown("#### 🤝 नई बिक्री / टोकन मनी बुकिंग फॉर्म")
        if inv_df.empty:
            st.warning("⚠️ बिक्री करने के लिए पहले स्टॉक रजिस्टर में ज़मीन एंट्री करें!")
        else:
            # केवल वही प्रॉपर्टी दिखाएं जिनका स्टॉक बचा हो
            active_inv = inv_df[pd.to_numeric(inv_df['available_area'], errors='coerce') > 0]
            
            if active_inv.empty:
                st.info("ℹ️ बेचने के लिए कोई लाइव स्टॉक उपलब्ध नहीं है।")
            else:
                prop_options = {f"{row['prop_id']} - {row['village']} (उपलब्ध: {row['available_area']})": row['prop_id'] for _, row in active_inv.iterrows()}
                selected_prop_label = st.selectbox("🎯 किस प्रॉपर्टी/प्लॉट में से बेचना है? चुनें", list(prop_options.keys()))
                p_id_selected = prop_options[selected_prop_label]
                
                # चुनी गई प्रॉपर्टी का डेटा निकालें
                prop_data = inv_df[inv_df['prop_id'] == p_id_selected].iloc[0]
                max_avail = float(prop_data['available_area'])
                
                with st.form("sales_form", clear_on_submit=True):
                    sc1, sc2 = st.columns(2)
                    with sc1:
                        b_name = st.text_input("👤 क्रेता / ग्राहक का नाम *")
                        b_phone = st.text_input("📱 ग्राहक का मोबाइल नंबर *")
                        s_area = st.number_input("📐 बेचा जाने वाला रकबा (मात्रा) *", min_value=0.0, max_value=max_avail, step=0.01, format="%.2f")
                    with sc2:
                        s_rate = st.number_input("💵 बिक्री रेट (प्रति एकड़ / यूनिट) *", min_value=0.0, step=1.0)
                        p_amount = st.number_input("💰 बयाना / नगद भुगतान राशि (Paid)", min_value=0.0, step=1.0)
                        mode = st.selectbox("💳 भुगतान का प्रकार", ["नगद (Cash)", "बैंक ट्रांसफर (Online)", "चेक (Cheque)"])
                    
                    if st.form_submit_button("📝 बिक्री और टोकन पक्का करें"):
                        if not b_name or not b_phone or s_area <= 0 or s_rate <= 0:
                            st.error("❌ कृपया ग्राहक का नाम, रकबा और रेट सही भरें!")
                        else:
                            try:
                                s_id = f"SALE-{random.randint(1000, 9999)}"
                                total_deal = s_area * s_rate
                                bal_amount = total_deal - p_amount
                                
                                new_sale_row = pd.DataFrame([{
                                    'sale_id': s_id, 'prop_id': p_id_selected, 'buyer_name': b_name,
                                    'buyer_phone': b_phone, 'deal_area': s_area, 'deal_rate': s_rate,
                                    'total_deal_amount': total_deal, 'amount_paid': p_amount,
                                    'balance_amount': bal_amount, 'payment_mode': mode,
                                    'tx_date': datetime.now().strftime("%Y-%m-%d %H:%M")
                                }])
                                
                                # 💡 स्मार्ट ऑटो-माइनस इन्वेंटरी कैलकुलेशन
                                inv_df.loc[inv_df['prop_id'] == p_id_selected, 'available_area'] = max_avail - s_area
                                
                                if conn:
                                    updated_sales = pd.concat([sales_df, new_sale_row], ignore_index=True)
                                    conn.update(worksheet="SalesBook", data=updated_sales)
                                    conn.update(worksheet="Inventory", data=inv_df)
                                    st.success(f"🎉 सौदा पक्का हुआ! सेल्स आईडी: {s_id} | बकाया राशि: ₹{bal_amount:,.2f}")
                                    st.cache_data.clear()
                                    st.rerun()
                            except Exception as e: st.error(f"सेल्स एंट्री में त्रुटि: {e}")

    # ------------------------------------------
    # 4. स्मार्ट सर्च इंजन
    # ------------------------------------------
    with tabs[3]:
        st.markdown("#### 🔍 लाइव डिजिटल खोज इंजन")
        q = st.text_input("🔎 किसान का नाम, ग्राहक का नाम, गांव या प्रॉपर्टी ID से कुछ भी खोजें...")
        
        if q:
            st.markdown("##### 🌾 इन्वेंटरी (खरीद) परिणाम:")
            if not inv_df.empty:
                f_inv = inv_df[inv_df.astype(str).apply(lambda x: x.str.contains(q, case=False, na=False)).any(axis=1)]
                st.dataframe(f_inv, use_container_width=True)
                
            st.markdown("##### 🤝 सेल्स और बयाना बहीखाता परिणाम:")
            if not sales_df.empty:
                f_sales = sales_df[sales_df.astype(str).apply(lambda x: x.str.contains(q, case=False, na=False)).any(axis=1)]
                st.dataframe(f_sales, use_container_width=True)
        else:
            st.info("💡 सर्च करने के लिए ऊपर बॉक्स में टाइप करें।")

    # ------------------------------------------
    # 5. लाइव स्टॉक रजिस्टर
    # ------------------------------------------
    with tabs[4]:
        st.markdown("#### 📂 वर्तमान लाइव स्टॉक स्थिति")
        if not inv_df.empty:
            st.dataframe(inv_df, use_container_width=True)
        else: st.info("ℹ️ स्टॉक रजिस्टर पूरी तरह से खाली है।")
        
        st.write("---")
        if st.button("🚪 ऐप को सुरक्षित रूप से लॉगआउट करें"):
            st.session_state.auth_done = False
            st.session_state.otp_sent = False
            st.rerun()
