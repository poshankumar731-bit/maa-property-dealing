import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import random
import requests

# ==========================================
# 🎨 अल्ट्रा-लग्जरी डार्क गोल्ड थीम & स्क्रीन सेटिंग्स
# ==========================================
st.set_page_config(
    page_title="Maa Property Premium",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# प्रीमियम कस्टम CSS स्टाइल्स
st.markdown("""
<style>  
    [data-testid="stAppViewContainer"] {  
        background: linear-gradient(135deg, #070a13, #0f172a);  
        color: #F8FAFC !important;  
    }  
    /* प्रीमियम ग्लास कार्ड्स विद गोल्ड नियॉन बॉर्डर */  
    .luxury-card, div[data-testid="stForm"] {  
        background: rgba(30, 41, 59, 0.4) !important;  
        backdrop-filter: blur(25px);  
        padding: 26px;  
        border-radius: 20px;  
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7);  
        margin-bottom: 22px;  
        border: 1px solid rgba(234, 179, 8, 0.25) !important;  
    }  
    /* सॉलिड गोल्ड बटन्स */  
    div.stButton > button {  
        width: 100%;  
        border-radius: 14px;  
        height: 52px;  
        font-size: 17px;  
        font-weight: 700;  
        background: linear-gradient(90deg, #EAB308, #CA8A04) !important;  
        color: #000000 !important;  
        border: none;  
        box-shadow: 0 4px 20px rgba(234, 179, 8, 0.35);  
        transition: 0.3s all ease;  
    }  
    div.stButton > button:hover {  
        transform: translateY(-2px);  
        box-shadow: 0 6px 25px rgba(234, 179, 8, 0.6);  
    }  
    /* इनपुट बॉक्सेस */  
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {  
        border-radius: 12px !important;  
        background-color: #1e293b !important;  
        color: #FFFFFF !important;  
        border: 1px solid rgba(255, 255, 255, 0.15) !important;  
        font-size: 16px !important;  
    }  
    label, p, span { color: #F1F5F9 !important; font-weight: 500; }  
    .stMetric {  
        background: rgba(234, 179, 8, 0.04);   
        border: 1px solid rgba(234, 179, 8, 0.2);  
        border-radius: 16px;  
        padding: 16px;  
    }  
    button[data-baseweb="tab"] { font-size: 16px; color: #94A3B8 !important; }  
    button[data-baseweb="tab"][aria-selected="true"] { color: #EAB308 !important; font-weight: bold; border-bottom-color: #EAB308 !important; }  
</style>  
""", unsafe_allow_html=True)

# 🔱 मुख्य डिजिटल हेडर
st.markdown("<h1 style='text-align: center; color: #EAB308; margin-top: -10px;'>🔱 मां प्रॉपर्टीज़ (Maa Properties)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #38BDF8; font-size:16px; font-weight: bold;'>🚀 लाइव स्टॉक इन्वेंटरी, स्मार्ट सेल्स बूक और सिक्योर OTP बहीखाता</p>", unsafe_allow_html=True)
st.write("---")

# कॉलम संरचना
INV_COLS = ['prop_id', 'seller_name', 'district', 'tehsil', 'village', 'ph_no', 'total_area', 'available_area', 'buy_rate', 'total_cost', 'date_added']
SALES_COLS = ['sale_id', 'prop_id', 'buyer_name', 'buyer_phone', 'deal_area', 'deal_rate', 'total_deal_amount', 'amount_paid', 'balance_amount', 'payment_mode', 'tx_date']

# ==========================================
# ☁️ क्लाउड डेटाबेस सिंक (गूगल शीट्स - क्रैश फ्री)
# ==========================================
@st.cache_data(ttl=0)
def load_perfect_data():
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

conn, inv_df, sales_df, settings_df = load_perfect_data()

def get_config(key_name, default):
    if not settings_df.empty and 'key' in settings_df.columns and 'value' in settings_df.columns:
        try: return str(settings_df[settings_df['key'] == key_name]['value'].values[0])
        except: return default
    return default

current_user = get_config('username', 'admin')
current_pass = get_config('password', 'Radhe@2026')
current_phone = get_config('app_phone', '9876543210')
sms_key = get_config('sms_api_key', '')

# छत्तीसगढ़ के 33 जिलों की मुख्य सूची
CG_DISTRICTS = [
    "रायपुर (Raipur)", "दुर्ग (Durg)", "बिलासपुर (Bilaspur)", "राजनांदगांव", "रायगढ़ (Raigarh)", 
    "कोरবা (Korba)", "बलौदा बाज़ार", "महासमुंद", "धमतरी", "कांकेर", "बस्तर (Bastar)",
    "बालोद", "बलरामपुर", "बेмеतरा", "बीजापुर", "दंतेवाड़ा", "गरियाबंद", "जांजगीर-चांपा", 
    "जशपुर", "कबीरधाम", "कोंडागांव", "कोरिया", "मुंगेली", "नारायणपुर", "सुकма", "सूरजपुर", "सरगुजा"
]

def send_real_otp(mobile, code):
    if not sms_key or sms_key == "YOUR_API_KEY": return True, "DEMO"
    try:
        url = "https://www.fast2sms.com/dev/bulkV2"
        p = {"authorization": sms_key, "variables_values": str(code), "route": "otp", "numbers": str(mobile)}
        res = requests.get(url, params=p, timeout=5)
        return True, res.json()
    except: return False, "Error"

# ==========================================
# 🔒 मोबाइल असली OTP सुरक्षा लॉगिन गेट
# ==========================================
if 'auth_active' not in st.session_state: st.session_state.auth_active = False
if 'sms_sent' not in st.session_state: st.session_state.sms_sent = False
if 'secure_pin' not in st.session_state: st.session_state.secure_pin = None

if not st.session_state.auth_active:
    st.markdown("<div class='luxury-card'>", unsafe_allow_html=True)
    st.markdown
