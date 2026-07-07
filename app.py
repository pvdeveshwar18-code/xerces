import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import datetime
import pytz
# XERCES+ enhancement module (watchlist, alerts, heatmap, compare, AI, journal, export)
import xerces_plus as xp
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import concurrent.futures
import urllib.request
import urllib.parse
import re
import xml.etree.ElementTree as ET
import json
import time
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.holtwinters import ExponentialSmoothing

warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(page_title="XERCES // QUANT ENGINE", page_icon="⚡", layout="wide")
IST = pytz.timezone("Asia/Kolkata")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Space+Mono&family=Inter:wght@300;400;500;600&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
.stApp{background:radial-gradient(circle at 50% 0%,#0a192f 0%,#020813 100%) !important;color:#e2e8f0 !important;}
section[data-testid="stSidebar"]{background-color:rgba(3,11,24,0.97) !important;border-right:1px solid rgba(0,200,255,0.15) !important;}
.xerces-title{font-family:'Orbitron',sans-serif;font-weight:900;font-size:2.2rem;background:linear-gradient(90deg,#00c8ff,#00e87a);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:3px;margin:0;}
.telemetry-tag{font-family:'Space Mono',monospace;color:#4a7090;font-size:11px;letter-spacing:1px;}
.section-header{font-family:'Orbitron',sans-serif;color:#00c8ff;font-size:12px;letter-spacing:1px;margin-top:12px;margin-bottom:8px;}
.glass-card{background:rgba(7,18,32,0.65);border:1px solid rgba(0,200,255,0.15);border-radius:6px;padding:12px 16px;margin-bottom:10px;backdrop-filter:blur(4px);}
.glass-label{font-family:'Space Mono',monospace;color:#6a90aa;font-size:10px;margin:0;text-transform:uppercase;letter-spacing:1px;}
.glass-value{font-family:'Orbitron',sans-serif;font-size:1.3rem;font-weight:700;margin-top:2px;}
div[data-baseweb="tab-list"]{gap:3px;}
button[data-baseweb="tab"]{font-family:'Space Mono',monospace !important;border-radius:4px !important;background:rgba(10,25,40,0.4) !important;color:#5a80a0 !important;border:1px solid rgba(0,200,255,0.05) !important;padding:0.35rem 0.75rem !important;font-size:11px !important;}
button[data-baseweb="tab"][aria-selected="true"]{border-color:#00c8ff !important;color:#00c8ff !important;background:rgba(13,32,53,0.75) !important;}
.signal-buy{color:#00e87a;font-family:'Orbitron',sans-serif;font-weight:700;font-size:1.4rem;}
.signal-sell{color:#ff3355;font-family:'Orbitron',sans-serif;font-weight:700;font-size:1.4rem;}
.signal-hold{color:#ffcc00;font-family:'Orbitron',sans-serif;font-weight:700;font-size:1.4rem;}
.accuracy-good{color:#00e87a;font-weight:700;}
.accuracy-mid{color:#ffcc00;font-weight:700;}
.accuracy-bad{color:#ff3355;font-weight:700;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# COMPLETE NSE/BSE STOCK UNIVERSE — 600+ STOCKS
# ══════════════════════════════════════════════════════════════════════════════
SECTORS = {
    "🏦 Banking & Finance": [
        ("HDFC Bank","HDFCBANK"),("ICICI Bank","ICICIBANK"),("SBI","SBIN"),("Kotak Mahindra Bank","KOTAKBANK"),
        ("Axis Bank","AXISBANK"),("IndusInd Bank","INDUSINDBK"),("Bank of Baroda","BANKBARODA"),
        ("PNB","PNB"),("Canara Bank","CANBK"),("Union Bank","UNIONBANK"),("Bank of India","BANKINDIA"),
        ("Indian Bank","INDIANB"),("UCO Bank","UCOBANK"),("Central Bank","CENTRALBK"),("IOB","IOB"),
        ("Federal Bank","FEDERALBNK"),("RBL Bank","RBLBANK"),("Yes Bank","YESBANK"),
        ("IDFC First Bank","IDFCFIRSTB"),("Bandhan Bank","BANDHANBNK"),("AU Small Finance Bank","AUBANK"),
        ("Equitas Small Finance","EQUITASBNK"),("Ujjivan Small Finance","UJJIVANSFB"),
        ("City Union Bank","CUB"),("Karur Vysya Bank","KARURVYSYA"),("South Indian Bank","SOUTHBANK"),
        ("Dhanlaxmi Bank","DHANBANK"),("Karnataka Bank","KTKBANK"),
        ("Bajaj Finance","BAJFINANCE"),("Bajaj Finserv","BAJAJFINSV"),("Cholamandalam Finance","CHOLAFIN"),
        ("Muthoot Finance","MUTHOOTFIN"),("Manappuram Finance","MANAPPURAM"),("L&T Finance","LTF"),
        ("Shriram Finance","SHRIRAMFIN"),("Piramal Enterprises","PEL"),("HDFC AMC","HDFCAMC"),
        ("Nippon India AMC","NAM-INDIA"),("UTI AMC","UTIAMC"),("Aditya Birla AMC","ABSLAMC"),
        ("SBI Cards","SBICARD"),("SBI Life Insurance","SBILIFE"),("HDFC Life","HDFCLIFE"),
        ("LIC India","LICI"),("Star Health Insurance","STARHEALTH"),("New India Assurance","NIACL"),
        ("General Insurance Corp","GICRE"),("ICICI Prudential Life","ICICIPRULI"),
        ("ICICI Lombard","ICICIGI"),("Max Financial","MFSL"),("Five Star Business","FIVESTAR"),
        ("Aavas Financiers","AAVAS"),("Home First Finance","HOMEFIRST"),("Aptus Value Housing","APTUS"),
        ("Repco Home Finance","REPCOHOME"),("Can Fin Homes","CANFINHOME"),("LIC Housing Finance","LICHSGFIN"),
    ],
    "💻 IT & Technology": [
        ("TCS","TCS"),("Infosys","INFY"),("HCL Technologies","HCLTECH"),("Wipro","WIPRO"),
        ("Tech Mahindra","TECHM"),("LTIMindtree","LTIM"),("Mphasis","MPHASIS"),("Coforge","COFORGE"),
        ("Persistent Systems","PERSISTENT"),("L&T Technology","LTTS"),("Tata Elxsi","TATAELXSI"),
        ("KPIT Technologies","KPITTECH"),("Zensar Technologies","ZENSARTECH"),("Mastek","MASTEK"),
        ("Hexaware","HEXAWARE"),("Birlasoft","BSOFT"),("Intellect Design","INTELLECT"),
        ("Cyient","CYIENT"),("Sonata Software","SONATSOFTW"),("Happiest Minds","HAPPSTMNDS"),
        ("Tanla Platforms","TANLA"),("Firstsource Solutions","FSL"),("Newgen Software","NEWGEN"),
        ("Ramco Systems","RAMCOSYS"),("KFIN Technologies","KFINTECH"),("Angel One","ANGELONE"),
        ("Route Mobile","ROUTE"),("Nazara Technologies","NAZARA"),("Netweb Technologies","NETWEB"),
        ("Tata Communications","TATACOMM"),("Rategain Travel Tech","RATEGAIN"),("Zaggle Prepaid","ZAGGLE"),
        ("Majesco","MAJESCO"),("Saksoft","SAKSOFT"),("Nucleus Software","NUCLEUSSOFT"),
    ],
    "🏭 Industrials & Capital Goods": [
        ("Larsen & Toubro","LT"),("Siemens India","SIEMENS"),("ABB India","ABB"),("Bharat Electronics","BEL"),
        ("HAL","HAL"),("BEML","BEML"),("Thermax","THERMAX"),("Cummins India","CUMMINSIND"),
        ("Bharat Forge","BHARATFORG"),("Ramkrishna Forgings","RKFORGE"),("Escorts Kubota","ESCORTS"),
        ("Carborundum Universal","CARBORUNIV"),("AIA Engineering","AIAENG"),("Timken India","TIMKEN"),
        ("Schaeffler India","SCHAEFFLER"),("SKF India","SKFINDIA"),("Grindwell Norton","GRINDWELL"),
        ("Elgi Equipments","ELGIEQUIP"),("Kirloskar Brothers","KIRLOSBROS"),("KSB","KSB"),
        ("Voltamp Transformers","VOLTAMP"),("Sterling Wilson","SWSOLAR"),("Va Tech Wabag","WABAG"),
        ("NBCC","NBCC"),("NCC","NCC"),("KEC International","KEC"),("Kalpataru Projects","KPIL"),
        ("G R Infraprojects","GRINFRA"),("ITD Cementation","ITDCEM"),("PNC Infratech","PNCINFRA"),
        ("H.G. Infra","HGINFRA"),("Ashoka Buildcon","ASHOKA"),("IRB Infrastructure","IRB"),
        ("Ahluwalia Contracts","AHLUCONT"),("Dilip Buildcon","DBL"),("Rail Vikas Nigam","RVNL"),
        ("Texmaco Rail","TEXRAILWAG"),("Jupiter Wagons","JWL"),("Titagarh Rail","TITAGARH"),
        ("Mazagon Dock","MAZDOCK"),("Garden Reach Shipbuilders","GRSE"),("Cochin Shipyard","COCHINSHIP"),
    ],
    "⚡ Energy & Power": [
        ("Reliance Industries","RELIANCE"),("ONGC","ONGC"),("BPCL","BPCL"),("IOC","IOC"),
        ("HPCL","HPCL"),("GAIL India","GAIL"),("Petronet LNG","PETRONET"),("Castrol India","CASTROLIND"),
        ("NTPC","NTPC"),("Power Grid Corp","POWERGRID"),("Tata Power","TATAPOWER"),
        ("Adani Green","ADANIGREEN"),("Adani Enterprises","ADANIENT"),("JSW Energy","JSWENERGY"),
        ("Torrent Power","TORNTPOWER"),("NHPC","NHPC"),("SJVN","SJVN"),("CESC","CESC"),
        ("Inox Wind","INOXWIND"),("Suzlon Energy","SUZLON"),("IREDA","IREDA"),
        ("PFC","PFC"),("REC","RECLTD"),("IGL","IGL"),("Gujarat Gas","GUJGASLTD"),
        ("Adani Total Gas","ATGL"),("Mahanagar Gas","MGL"),("Reliance Power","RPOWER"),
        ("Jaiprakash Power","JPPOWER"),("CPCL","CPCL"),("Mangalore Refinery","MRPL"),
        ("Chennai Petroleum","CHENNPETRO"),("GIPCL","GIPCL"),("TANGEDCO","TNPL"),
        ("Greenko","GKLENERGY"),("Acme Solar","ACMESOLAR"),("Premier Energies","PREMIERENE"),
    ],
    "🚗 Auto & Auto Ancillaries": [
        ("Maruti Suzuki","MARUTI"),("Tata Motors","TATAMOTORS"),("M&M","M&M"),
        ("Bajaj Auto","BAJAJ-AUTO"),("Hero MotoCorp","HEROMOTOCO"),("Eicher Motors","EICHERMOT"),
        ("TVS Motor","TVSMOTOR"),("Ashok Leyland","ASHOKLEY"),("Force Motors","FORCEMOT"),
        ("Apollo Tyres","APOLLOTYRE"),("MRF","MRF"),("CEAT","CEATLTD"),
        ("Balkrishna Industries","BALKRISIND"),("Bosch India","BOSCHLTD"),("Motherson Sumi","MOTHERSON"),
        ("Minda Industries","MINDAIND"),("Minda Corp","MINDACORP"),("Suprajit Engineering","SUPRAJIT"),
        ("Endurance Technologies","ENDURANCE"),("Gabriel India","GABRIEL"),("Jamna Auto","JAMNAAUTO"),
        ("Sona BLW Precision","SONACOMS"),("Uno Minda","UNOMINDA"),("Fiem Industries","FIEMIND"),
        ("Sandhar Technologies","SANDHAR"),("Craftsman Automation","CRAFTSMAN"),
        ("Bharat Forge","BHARATFORG"),("Schaeffler India","SCHAEFFLER"),("Samvardhana Motherson","MOTHERSON"),
        ("Varroc Engineering","VARROC"),("Pricol","PRICOL"),("Lumax Industries","LUMAXIND"),
        ("Lumax Auto Technologies","LUMAXTECH"),("Spark Minda","MINDAIND"),("Automotive Axles","AUTOAXLES"),
    ],
    "💊 Pharma & Healthcare": [
        ("Sun Pharma","SUNPHARMA"),("Dr. Reddy's","DRREDDY"),("Cipla","CIPLA"),("Lupin","LUPIN"),
        ("Biocon","BIOCON"),("Alkem Labs","ALKEM"),("Torrent Pharma","TORNTPHARM"),
        ("Abbott India","ABBOTINDIA"),("Pfizer India","PFIZER"),("Sanofi India","SANOFI"),
        ("Divi's Laboratories","DIVISLAB"),("Aurobindo Pharma","AUROPHARMA"),("Zydus Lifesciences","ZYDUSLIFE"),
        ("Ipca Laboratories","IPCALAB"),("Natco Pharma","NATCOPHARM"),("Glenmark Pharma","GLENMARK"),
        ("Mankind Pharma","MANKIND"),("Ajanta Pharma","AJANTPHARM"),("JB Chemicals","JBCHEPHARM"),
        ("FDC Limited","FDC"),("Piramal Pharma","PPLPHARMA"),("Laurus Labs","LAURUSLABS"),
        ("Granules India","GRANULES"),("Aarti Drugs","AARTIDRUGS"),("Caplin Point","CAPLIPOINT"),
        ("Apollo Hospitals","APOLLOHOSP"),("Max Healthcare","MAXHEALTH"),("Fortis Healthcare","FORTIS"),
        ("Narayana Hrudayalaya","NH"),("Medanta","MEDANTA"),("HCG Oncology","HCG"),
        ("Vijaya Diagnostic","VIJAYA"),("Metropolis Healthcare","METROPOLIS"),
        ("Dr. Lal Path Labs","LALPATHLAB"),("Thyrocare","THYROCARE"),
        ("Sanofi India","SANOFI"),("Wockhardt","WOCKPHARMA"),("Strides Pharma","STAR"),
        ("Suven Life Sciences","SUVEN"),("Solara Active Pharma","SOLARA"),
    ],
    "🏗️ Metals & Mining": [
        ("Tata Steel","TATASTEEL"),("JSW Steel","JSWSTEEL"),("Hindalco","HINDALCO"),
        ("Vedanta","VEDL"),("Hindustan Zinc","HINDZINC"),("National Aluminium","NATIONALUM"),
        ("SAIL","SAIL"),("Coal India","COALINDIA"),("NMDC","NMDC"),("Jindal Steel","JINDALSTEL"),
        ("APL Apollo Tubes","APLAPOLLO"),("Ratnamani Metals","RATNAMANI"),
        ("Maharashtra Seamless","MAHSEAMLES"),("Welspun Corp","WELCORP"),("Shyam Metalics","SHYAMMETL"),
        ("Godawari Power","GPIL"),("GMDC","GMDC"),("MOIL","MOIL"),
        ("Hindustan Copper","HINDCOPPER"),("Tinplate Company","TINPLATE"),
        ("Jindal Stainless","JSL"),("JSPL","JINDALPOLY"),("Steel Authority","SAIL"),
        ("Tata Metaliks","TATAMETALI"),("Maithan Alloys","MAITHANALL"),
    ],
    "🧱 Cement & Construction": [
        ("UltraTech Cement","ULTRACEMCO"),("Shree Cement","SHREECEM"),("Ambuja Cements","AMBUJACEM"),
        ("ACC","ACC"),("JK Cement","JKCEMENT"),("Dalmia Bharat","DALBHARAT"),
        ("Ramco Cements","RAMCOCEM"),("Heidelberg Cement","HEIDELBERG"),("JK Lakshmi Cement","JKLAKSHMI"),
        ("Birla Corporation","BIRLACORPN"),("Orient Cement","ORIENTCEM"),("India Cements","INDIACEM"),
        ("Sagar Cements","SAGCEM"),("Star Cement","STARCEMENT"),("NCL Industries","NCLIND"),
        ("Prism Johnson","PRSMJOHNSN"),("Kajaria Ceramics","KAJARIACER"),("CERA Sanitary","CERA"),
        ("Astral","ASTRAL"),("Supreme Industries","SUPREMEIND"),("Finolex Industries","FINPIPE"),
        ("Somany Ceramics","SOMANYCERA"),("Cello World","CELLO"),("Polyplex Corp","POLYPLEX"),
    ],
    "🛒 FMCG & Consumer": [
        ("Hindustan Unilever","HINDUNILVR"),("ITC","ITC"),("Nestle India","NESTLEIND"),
        ("Britannia","BRITANNIA"),("Dabur India","DABUR"),("Godrej Consumer","GODREJCP"),
        ("Marico","MARICO"),("Emami","EMAMILTD"),("Bajaj Consumer","BAJAJCON"),
        ("Tata Consumer","TATACONSUM"),("Varun Beverages","VBL"),("Radico Khaitan","RADICO"),
        ("United Spirits","MCDOWELL-N"),("United Breweries","UBL"),("Jubilant FoodWorks","JUBLFOOD"),
        ("Westlife Foodworld","WESTLIFE"),("Burger King India","BURGERKING"),
        ("Devyani International","DEVYANI"),("Sapphire Foods","SAPPHIRE"),
        ("Mrs Bectors Food","BECTORFOOD"),("Heritage Foods","HERITGFOOD"),("Hatsun Agro","HATSUN"),
        ("Bikaji Foods","BIKAJI"),("P&G Hygiene","PGHH"),("Colgate Palmolive","COLPAL"),
        ("Kansai Nerolac","KANSAINER"),("Asian Paints","ASIANPAINT"),("Berger Paints","BERGEPAINT"),
        ("Indigo Paints","INDIGOPNTS"),("Pidilite","PIDILITIND"),("Prataap Snacks","PRATAAP"),
        ("DFM Foods","DFMFOODS"),("CCL Products","CCL"),
    ],
    "🛍️ Retail & E-Commerce": [
        ("Zomato","ZOMATO"),("Eternal (Zomato)","ETERNAL"),("Swiggy","SWIGGY"),("Paytm","PAYTM"),
        ("Nykaa","NYKAA"),("PB Fintech","POLICYBZR"),("Delhivery","DELHIVERY"),
        ("Info Edge (Naukri)","NAUKRI"),("IndiaMart","INDIAMART"),("Just Dial","JUSTDIAL"),
        ("Matrimony.com","MATRIMONY"),("CarTrade Tech","CARTRADE"),
        ("Avenue Supermarts (DMart)","DMART"),("Trent","TRENT"),("V-Mart Retail","VMART"),
        ("Bata India","BATAINDIA"),("Relaxo Footwear","RELAXO"),("Campus Activewear","CAMPUS"),
        ("Metro Brands","METROBRAND"),("Shoppers Stop","SHOPERSTOP"),("Titan Company","TITAN"),
        ("Kalyan Jewellers","KALYANKJIL"),("Senco Gold","SENCO"),("PC Jeweller","PCJEWELLER"),
        ("Thangamayil Jewellery","THANGAMAYL"),
    ],
    "✈️ Infrastructure & Logistics": [
        ("Adani Ports","ADANIPORTS"),("GMR Airports","GMRINFRA"),("IndiGo","INDIGO"),
        ("SpiceJet","SPICEJET"),("Blue Dart","BLUEDART"),("Container Corp","CONCOR"),
        ("Gateway Distriparks","GDL"),("Mahindra Logistics","MAHLOG"),("Delhivery","DELHIVERY"),
        ("IRCTC","IRCTC"),("RITES","RITES"),("IRFC","IRFC"),("Rail Vikas Nigam","RVNL"),
        ("Adani Wilmar","AWL"),("Interglobe Aviation","INDIGO"),("TCI Express","TCIEXP"),
        ("Gati","GATI"),("VRL Logistics","VRLLOG"),("Allcargo Logistics","ALLCARGO"),
        ("Transport Corp","TCI"),("Navkar Corp","NAVKARCORP"),
    ],
    "🔬 Chemicals & Fertilizers": [
        ("UPL","UPL"),("PI Industries","PIIND"),("Coromandel Int.","COROMANDEL"),
        ("Bayer CropScience","BAYERCROP"),("Sumitomo Chemical","SUMICHEM"),("Rallis India","RALLIS"),
        ("Deepak Nitrite","DEEPAKNTR"),("Aarti Industries","AARTIIND"),("Navin Fluorine","NAVINFLUOR"),
        ("SRF Limited","SRF"),("Vinati Organics","VINATIORGA"),("Galaxy Surfactants","GALAXYSURF"),
        ("Fine Organics","FINEORG"),("Balaji Amines","BALAMINES"),("Alkyl Amines","ALKYLAMINE"),
        ("Neogen Chemicals","NEOGEN"),("Clean Science","CLEAN"),("Anupam Rasayan","ANURAS"),
        ("Tata Chemicals","TATACHEM"),("GHCL","GHCL"),("Gujarat Fluorochemicals","FLUOROCHEM"),
        ("Himadri Speciality","HSCL"),("Sudarshan Chemical","SUDARSCHEM"),("NOCIL","NOCIL"),
        ("Chambal Fertilisers","CHAMBLFERT"),("NFL","NFL"),("GSFC","GSFC"),("RCF","RCF"),("FACT","FACT"),
        ("Atul Ltd","ATUL"),("Rossari Biotech","ROSSARI"),("Tatva Chintan","TATVA"),
        ("Ami Organics","AMIORG"),("Archean Chemical","ARCHEAN"),
    ],
    "🏠 Real Estate": [
        ("Godrej Properties","GODREJPROP"),("DLF","DLF"),("Prestige Estates","PRESTIGE"),
        ("Brigade Enterprises","BRIGADE"),("Sobha","SOBHA"),("Oberoi Realty","OBEROIRLTY"),
        ("Macrotech (Lodha)","LODHA"),("Mahindra Lifespace","MAHLIFE"),("Kolte Patil","KOLTEPATIL"),
        ("Puravankara","PURVA"),("DB Realty","DBREALTY"),("Indiabulls Real Estate","IBREALEST"),
        ("Embassy REIT","EMBASSY"),("Mindspace REIT","MINDSPACE"),("Brookfield REIT","BIRET"),
        ("Nexus Select Trust","NEXUSSELCT"),("Sunteck Realty","SUNTECK"),("Phoenix Mills","PHOENIXLTD"),
        ("Shriram Properties","SHRIRAMPPS"),("Signature Global","SIGNATURE"),
    ],
    "📡 Telecom & Media": [
        ("Bharti Airtel","BHARTIARTL"),("Vodafone Idea","IDEA"),("MTNL","MTNL"),
        ("Tata Communications","TATACOMM"),("Route Mobile","ROUTE"),("Tanla Platforms","TANLA"),
        ("Dish TV","DISHTV"),("Zee Entertainment","ZEEL"),("Sun TV Network","SUNTV"),
        ("PVR Inox","PVRINOX"),("Saregama India","SAREGAMA"),("Nazara Technologies","NAZARA"),
        ("Network18 Media","NETWORK18"),("TV18 Broadcast","TV18BRDCST"),
        ("Hathway Cable","HATHWAY"),("Den Networks","DEN"),("Indiacast Media","INDIACAST"),
    ],
    "🧵 Textiles & Apparel": [
        ("Page Industries","PAGEIND"),("Lux Industries","LUXIND"),("Dollar Industries","DOLLAR"),
        ("Trident","TRIDENT"),("Welspun India","WELSPUNIND"),("Raymond","RAYMOND"),
        ("Arvind","ARVIND"),("Vardhman Textiles","VTL"),("KPR Mill","KPRMILL"),
        ("Siyaram Silk Mills","SIYARAM"),("Nitin Spinners","NITINSPIN"),
        ("Indo Count Industries","ICIL"),("Gokaldas Exports","GOKEX"),("TCNS Clothing","TCNSBRANDS"),
        ("Go Fashion","GOCOLORS"),("Monte Carlo","MONTECARLO"),("Kewal Kiran","KKCL"),
    ],
    "🔌 Electronics & Capital Equipment": [
        ("Dixon Technologies","DIXON"),("Amber Enterprises","AMBER"),("Voltas","VOLTAS"),
        ("Blue Star","BLUESTARCO"),("Havells India","HAVELLS"),("Polycab India","POLYCAB"),
        ("KEI Industries","KEI"),("Finolex Cables","FINCABLES"),("V-Guard","VGUARD"),
        ("Crompton Greaves","CROMPTON"),("Orient Electric","ORIENTELEC"),("Bajaj Electricals","BAJAJELEC"),
        ("Whirlpool India","WHIRLPOOL"),("Kaynes Technology","KAYNES"),("Syrma SGS","SYRMA"),
        ("Elin Electronics","ELIN"),("Avalon Technologies","AVALON"),
        ("CDSL","CDSL"),("BSE Ltd","BSE"),("MCX India","MCX"),("Multi Comm Exchange","MCX"),
        ("Genus Power","GENUSPOWER"),("Apar Industries","APARINDS"),("Transformers & Rectifiers","TRIL"),
    ],
    "🌾 Agriculture & Food": [
        ("ITC (Agri)","ITC"),("Kaveri Seed","KSCL"),("Dhanuka Agritech","DHANUKA"),
        ("Venky's India","VENKEYS"),("Avanti Feeds","AVANTIFEED"),("Waterbase","WATERBASE"),
        ("Heritage Foods","HERITGFOOD"),("CCL Products","CCL"),("Agro Tech Foods","AGROTECH"),
        ("Adani Wilmar","AWL"),("Patanjali Foods","PATANJALI"),("Krbl","KRBL"),
        ("LT Foods","LTFOODS"),("Triveni Engineering","TRIVENI"),("Balrampur Chini","BALRAMCHIN"),
        ("Dalmia Bharat Sugar","DALMIASUG"),("EID Parry","EIDPARRY"),("Bajaj Hindusthan","BAJAJHIND"),
        ("Shakti Pumps","SHAKTIPUMP"),("Jain Irrigation","JISLJALEQS"),
    ],
    "🏛️ PSU & Defence": [
        ("HAL","HAL"),("BEL","BEL"),("BEML","BEML"),("Mazagon Dock","MAZDOCK"),
        ("Garden Reach Shipbuilders","GRSE"),("Cochin Shipyard","COCHINSHIP"),("MTNL","MTNL"),
        ("Bharat Dynamics","BDL"),("Data Patterns","DATAPATTNS"),("Paras Defence","PARAS"),
        ("Solar Industries","SOLARINDS"),("Munitions India","MIL"),("GRSE","GRSE"),
        ("RVNL","RVNL"),("IRFC","IRFC"),("IREDA","IREDA"),("NHPC","NHPC"),
        ("SJVN","SJVN"),("NTPC","NTPC"),("PGCIL","POWERGRID"),("NMDC","NMDC"),
        ("SAIL","SAIL"),("Coal India","COALINDIA"),("ONGC","ONGC"),("IOC","IOC"),
        ("BPCL","BPCL"),("HPCL","HPCL"),("GAIL India","GAIL"),
    ],
}

ALL_STOCKS = {}
for sector, stocks in SECTORS.items():
    for name, sym in stocks:
        key = f"{name} ({sym})"
        if key not in ALL_STOCKS:
            ALL_STOCKS[key] = f"{sym}.NS"

# ── TICKER RESOLUTION HELPERS ────────────────────────────────────────────────
def resolve_ticker(ticker_input):
    ticker_input = ticker_input.strip().upper()
    if ticker_input.endswith(".NS") or ticker_input.endswith(".BO") or "^" in ticker_input:
        return ticker_input
    for key, val in ALL_STOCKS.items():
        sym = val.replace(".NS","").replace(".BO","").upper()
        if ticker_input == sym:
            return val
    return f"{ticker_input}.NS"

def get_sector_peers(ticker_symbol, max_peers=2):
    clean = ticker_symbol.replace(".NS","").replace(".BO","").upper()
    for sector, list_of_stocks in SECTORS.items():
        if any(sym == clean for _, sym in list_of_stocks):
            peers = []
            for name, sym in list_of_stocks:
                if sym != clean:
                    peers.append(f"{sym}.NS")
                    if len(peers) >= max_peers:
                        break
            return sector, peers
    return None, []

# ══════════════════════════════════════════════════════════════════════════════
# CORE DATA HELPERS
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=3600, show_spinner=False)
def load_ohlcv(ticker: str, period: str = "5y"):
    try:
        df = yf.download(ticker, period=period, interval="1d", auto_adjust=True,
                          progress=False, timeout=12)
        if df is None or df.empty:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df = df.reset_index()
        df.columns = [str(c).strip() for c in df.columns]
        for col in ["Open","High","Low","Close","Volume"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        df = df.dropna(subset=["Close"])
        return df
    except Exception:
        return None

def _download_raw(ticker: str, period: str = "1y"):
    try:
        df = yf.download(ticker, period=period, interval="1d", auto_adjust=True,
                          progress=False, timeout=8, threads=False)
        if df is None or df.empty:
            return None
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df = df.reset_index()
        df.columns = [str(c).strip() for c in df.columns]
        for col in ["Open","High","Low","Close","Volume"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        df = df.dropna(subset=["Close"])
        return df
    except Exception:
        return None

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if len(out) < 20:
        return out
    c = out["Close"].astype(float)
    out["Return"]        = c.pct_change()
    out["SMA_20"]        = c.rolling(20).mean()
    out["SMA_50"]        = c.rolling(50).mean()
    out["SMA_200"]       = c.rolling(200).mean()
    out["EMA_12"]        = c.ewm(span=12, adjust=False).mean()
    out["EMA_26"]        = c.ewm(span=26, adjust=False).mean()
    out["MACD"]          = out["EMA_12"] - out["EMA_26"]
    out["MACD_Signal"]   = out["MACD"].ewm(span=9, adjust=False).mean()
    out["MACD_Hist"]     = out["MACD"] - out["MACD_Signal"]
    out["BB_Mid"]        = c.rolling(20).mean()
    out["BB_Std"]        = c.rolling(20).std()
    out["BB_Upper"]      = out["BB_Mid"] + 2 * out["BB_Std"]
    out["BB_Lower"]      = out["BB_Mid"] - 2 * out["BB_Std"]
    out["Volatility_20"] = out["Return"].rolling(20).std() * np.sqrt(252)
    delta = c.diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    out["RSI_14"] = 100 - (100 / (1 + gain / (loss + 1e-9)))
    if "High" in out.columns and "Low" in out.columns:
        hi = out["High"].astype(float)
        lo = out["Low"].astype(float)
        hl = hi - lo
        hc = (hi - c.shift()).abs()
        lc = (lo - c.shift()).abs()
        out["ATR_14"] = pd.concat([hl, hc, lc], axis=1).max(axis=1).rolling(14).mean()
    else:
        out["ATR_14"] = c.rolling(14).std()
    low14  = out["Low"].astype(float).rolling(14).min() if "Low" in out.columns else c.rolling(14).min()
    high14 = out["High"].astype(float).rolling(14).max() if "High" in out.columns else c.rolling(14).max()
    out["Stoch_K"] = (c - low14) / (high14 - low14 + 1e-9) * 100
    out["Stoch_D"] = out["Stoch_K"].rolling(3).mean()
    if "Volume" in out.columns:
        vol = out["Volume"].astype(float)
        obv = [0.0]
        for i in range(1, len(out)):
            if out["Close"].iloc[i] > out["Close"].iloc[i-1]:
                obv.append(obv[-1] + vol.iloc[i])
            elif out["Close"].iloc[i] < out["Close"].iloc[i-1]:
                obv.append(obv[-1] - vol.iloc[i])
            else:
                obv.append(obv[-1])
        out["OBV"] = obv
    return out

def get_signal(df: pd.DataFrame) -> str:
    if len(df) < 52:
        return "HOLD"
    last = df.iloc[-1]
    prev = df.iloc[-2]
    needed = ["SMA_20","SMA_50","RSI_14","MACD","MACD_Signal"]
    if any(pd.isna(last.get(x, np.nan)) for x in needed):
        return "HOLD"
    macd_cross_up   = float(last["MACD"]) > float(last["MACD_Signal"]) and float(prev["MACD"]) <= float(prev["MACD_Signal"])
    macd_cross_down = float(last["MACD"]) < float(last["MACD_Signal"]) and float(prev["MACD"]) >= float(prev["MACD_Signal"])
    trend_up   = float(last["SMA_20"]) > float(last["SMA_50"])
    trend_down = float(last["SMA_20"]) < float(last["SMA_50"])
    above_200  = pd.notna(last.get("SMA_200")) and float(last["Close"]) > float(last["SMA_200"])
    rsi = float(last["RSI_14"])
    if trend_up and above_200 and rsi < 70 and (macd_cross_up or rsi < 45):
        return "BUY"
    if trend_down and (rsi > 70 or macd_cross_down):
        return "SELL"
    return "HOLD"

def get_signal_strength(df: pd.DataFrame) -> int:
    if len(df) < 52:
        return 50
    last = df.iloc[-1]
    score = 50
    try:
        rsi = float(last.get("RSI_14", 50) or 50)
        if rsi < 30:   score += 20
        elif rsi < 45: score += 10
        elif rsi > 70: score -= 20
        elif rsi > 60: score -= 10
        sma20 = float(last.get("SMA_20", 0) or 0)
        sma50 = float(last.get("SMA_50", 0) or 0)
        sma200= float(last.get("SMA_200", 0) or 0)
        cl    = float(last.get("Close", 0) or 0)
        if sma20 > sma50:  score += 10
        else:              score -= 10
        if cl > sma200:    score += 10
        else:              score -= 10
        macd  = float(last.get("MACD", 0) or 0)
        macds = float(last.get("MACD_Signal", 0) or 0)
        if macd > macds:   score += 10
        else:              score -= 10
    except Exception:
        pass
    return max(0, min(100, score))

# ── ARIMA + Holt-Winters ─────────────────────────────────────────────────────
def run_arima(series: pd.Series, steps: int = 260):
    log_s = np.log(series.astype(float).dropna())
    d = 0 if adfuller(log_s)[1] < 0.05 else 1
    best_aic, best_model, best_order = np.inf, None, (1, d, 1)
    for p in range(0, 5):
        for q in range(0, 5):
            try:
                m = ARIMA(log_s, order=(p, d, q)).fit()
                if m.aic < best_aic:
                    best_aic, best_model, best_order = m.aic, m, (p, d, q)
            except Exception:
                continue
    if best_model is None:
        best_model = ARIMA(log_s, order=(1, 1, 1)).fit()
        best_order = (1, 1, 1)
    fc  = best_model.get_forecast(steps=steps)
    mu  = fc.predicted_mean
    ci  = fc.conf_int(alpha=0.10)
    return np.exp(mu), np.exp(ci.iloc[:, 0]), np.exp(ci.iloc[:, 1]), best_order, round(best_aic, 1), best_model, log_s

def run_holt_winters(series: pd.Series, steps: int = 260):
    try:
        s = series.astype(float).dropna()
        model = ExponentialSmoothing(s, trend="add", seasonal=None, initialization_method="estimated").fit()
        return model.forecast(steps=steps)
    except Exception:
        s = series.astype(float).dropna()
        drift = (float(s.iloc[-1]) - float(s.iloc[0])) / max(len(s), 1)
        return pd.Series([float(s.iloc[-1]) + drift * i for i in range(1, steps + 1)])

def compute_accuracy(price_series: pd.Series, arima_order: tuple, holdout: int = 60):
    try:
        if len(price_series) < holdout + 100:
            return None, None
        train = price_series.iloc[:-holdout]
        test  = price_series.iloc[-holdout:]
        log_train = np.log(train.astype(float).dropna())
        m = ARIMA(log_train, order=arima_order).fit()
        fc_log = m.forecast(steps=holdout)
        fc_price = np.exp(fc_log.values)
        test_vals = test.values[:len(fc_price)]
        mape = float(np.mean(np.abs((test_vals - fc_price) / (test_vals + 1e-9))) * 100)
        dir_acc = float(np.mean(
            np.sign(np.diff(test_vals)) == np.sign(np.diff(fc_price))
        ) * 100) if len(test_vals) > 1 else 50.0
        return round(mape, 2), round(dir_acc, 1)
    except Exception:
        return None, None

# ── Indices dashboard ─────────────────────────────────────────────────────────
@st.cache_data(ttl=1800, show_spinner=False)
def load_indices():
    tickers = ["^NSEI","^NSEBANK","^BSESN","^CRSMID","^CNXSC","^INDIAVIX"]
    results = {}
    for t in tickers:
        try:
            d = yf.download(t, period="5d", interval="1d", auto_adjust=True, progress=False)
            if d is not None and not d.empty:
                if isinstance(d.columns, pd.MultiIndex):
                    d.columns = d.columns.get_level_values(0)
                d = d.reset_index()
                results[t] = d
        except Exception:
            pass
    return results

# ── News + sentiment ──────────────────────────────────────────────────────────
@st.cache_data(ttl=900, show_spinner=False)
def fetch_news(ticker: str, company_name: str = ""):
    clean = ticker.replace(".NS", "").replace(".BO", "")
    query = company_name.strip() if company_name.strip() else clean
    items = []
    try:
        gquery = urllib.parse.quote(f"{query} stock NSE")
        gurl = f"https://news.google.com/rss/search?q={gquery}&hl=en-IN&gl=IN&ceid=IN:en"
        req = urllib.request.Request(gurl, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            root = ET.fromstring(r.read())
        for item in root.findall(".//item")[:15]:
            title   = (item.find("title").text   or "") if item.find("title")   is not None else ""
            link    = (item.find("link").text    or "") if item.find("link")    is not None else ""
            pubdate = (item.find("pubDate").text or "") if item.find("pubDate") is not None else ""
            if title:
                items.append({"title": title, "link": link, "date": pubdate[:16]})
    except Exception:
        pass

    if items:
        return items

    try:
        url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={clean}&region=IN&lang=en-IN"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=6) as r:
            root = ET.fromstring(r.read())
        for item in root.findall(".//item"):
            title   = (item.find("title").text   or "") if item.find("title")   is not None else ""
            link    = (item.find("link").text    or "") if item.find("link")    is not None else ""
            pubdate = (item.find("pubDate").text or "") if item.find("pubDate") is not None else ""
            items.append({"title": title, "link": link, "date": pubdate[:16]})
        return items
    except Exception:
        return []

BULL_KW = {"surge","rally","grow","growth","jump","rise","gain","profit","record","bullish","beat",
            "positive","expand","outperform","buy","upgrade","strong","boom","breakout","upside"}
BEAR_KW = {"slump","fall","decline","drop","loss","plunge","negative","bearish","miss","sell",
            "downgrade","weak","crash","warn","crisis","debt","cut","lower","pressure","concern"}

def sentiment_score(items):
    if not items:
        return 0.0, "NEUTRAL"
    total = 0
    for it in items:
        tl = it["title"].lower()
        words = set(tl.split())
        bull = len(words & BULL_KW)
        bear = len(words & BEAR_KW)
        for bw in BULL_KW:
            if f"not {bw}" in tl or f"no {bw}" in tl:
                bull -= 2
        total += (bull - bear)
    avg = total / len(items)
    cat = "BULLISH" if avg > 0.2 else "BEARISH" if avg < -0.2 else "NEUTRAL"
    return round(avg, 3), cat

# ── Market status ─────────────────────────────────────────────────────────────
def ist_now():
    return datetime.datetime.now(IST)

def market_status():
    now = ist_now()
    if now.weekday() >= 5:
        return "🔴 NSE CLOSED", "#ff3355"
    ot = now.replace(hour=9, minute=15, second=0, microsecond=0)
    ct = now.replace(hour=15, minute=30, second=0, microsecond=0)
    if ot <= now <= ct:
        return "🟢 NSE OPEN", "#00e87a"
    return "🔴 NSE CLOSED", "#ff3355"

# ── Backtest helper ───────────────────────────────────────────────────────────
def run_backtest(df: pd.DataFrame, strategy: str):
    bt = df.copy().reset_index(drop=True)
    bt["Signal_BT"] = 0
    if strategy == "SMA Crossover":
        valid = bt["SMA_20"].notna() & bt["SMA_50"].notna()
        bt.loc[valid & (bt["SMA_20"] > bt["SMA_50"]), "Signal_BT"] = 1
    elif strategy == "RSI Mean Reversion":
        sig, signals = 0, []
        for r in bt["RSI_14"].fillna(50):
            if r < 30: sig = 1
            elif r > 70: sig = 0
            signals.append(sig)
        bt["Signal_BT"] = signals
    elif strategy == "Bollinger Bands Breakout":
        sig, signals = 0, []
        for c, u, l in zip(bt["Close"].fillna(0), bt["BB_Upper"].fillna(0), bt["BB_Lower"].fillna(0)):
            if pd.isna(u) or pd.isna(l): signals.append(0); continue
            if c > u: sig = 1
            elif c < l: sig = 0
            signals.append(sig)
        bt["Signal_BT"] = signals
    elif strategy == "MACD Crossover":
        sig, signals = 0, []
        macd_vals = bt["MACD"].fillna(0).values
        macds_vals = bt["MACD_Signal"].fillna(0).values
        for i in range(len(bt)):
            if i == 0: signals.append(0); continue
            if macd_vals[i] > macds_vals[i] and macd_vals[i-1] <= macds_vals[i-1]: sig = 1
            elif macd_vals[i] < macds_vals[i] and macd_vals[i-1] >= macds_vals[i-1]: sig = 0
            signals.append(sig)
        bt["Signal_BT"] = signals

    bt["Position"] = bt["Signal_BT"].diff()
    trades, buy_x, buy_y, sell_x, sell_y = [], [], [], [], []
    in_trade, entry_price, entry_date = False, 0.0, None
    for idx in range(len(bt)):
        row = bt.iloc[idx]
        if row["Position"] == 1 and not in_trade and idx + 1 < len(bt):
            nxt = bt.iloc[idx + 1]
            in_trade, entry_price, entry_date = True, float(nxt["Open"]), nxt["Date"]
            buy_x.append(nxt["Date"])
            buy_y.append(float(nxt["Low"]) * 0.985 if pd.notna(nxt.get("Low")) else float(nxt["Open"]))
        elif row["Position"] == -1 and in_trade and idx + 1 < len(bt):
            nxt = bt.iloc[idx + 1]
            in_trade = False
            exit_p   = float(nxt["Open"])
            pnl      = (exit_p - entry_price) / entry_price * 100
            trades.append({"Entry Date": str(entry_date)[:10], "Exit Date": str(nxt["Date"])[:10],
                           "Entry ₹": round(entry_price,2), "Exit ₹": round(exit_p,2),
                           "P&L %": round(pnl,2), "Result": "✅ WIN" if pnl > 0 else "❌ LOSS"})
            sell_x.append(nxt["Date"])
            sell_y.append(float(nxt["High"]) * 1.015 if pd.notna(nxt.get("High")) else float(nxt["Open"]))
    return bt, trades, buy_x, buy_y, sell_x, sell_y


# ══════════════════════════════════════════════════════════════════════════════
# FII / DII FLOW DATA — NSE India
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=1800, show_spinner=False)
def fetch_fii_dii():
    url = "https://www.nseindia.com/api/fiidiiTradeReact"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.nseindia.com/market-data/fii-dii-activity",
    }
    try:
        req = urllib.request.Request(url, headers=headers)
        main_req = urllib.request.Request("https://www.nseindia.com", headers=headers)
        import http.cookiejar
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        opener.open(main_req, timeout=8)
        time.sleep(0.5)
        with opener.open(req, timeout=8) as r:
            data = json.loads(r.read().decode())
        return data
    except Exception:
        return None

def parse_fii_dii(data):
    if not data:
        return None, None
    try:
        rows = data if isinstance(data, list) else data.get("data", [])
        records = []
        for row in rows[:20]:
            try:
                date_str = row.get("date", row.get("Date", ""))
                fii_buy  = float(str(row.get("fiiBuy",  row.get("FII_BUY",  0))).replace(",","") or 0)
                fii_sell = float(str(row.get("fiiSell", row.get("FII_SELL", 0))).replace(",","") or 0)
                dii_buy  = float(str(row.get("diiBuy",  row.get("DII_BUY",  0))).replace(",","") or 0)
                dii_sell = float(str(row.get("diiSell", row.get("DII_SELL", 0))).replace(",","") or 0)
                records.append({
                    "Date": date_str,
                    "FII Net": round(fii_buy - fii_sell, 2),
                    "DII Net": round(dii_buy - dii_sell, 2),
                    "FII Buy": fii_buy, "FII Sell": fii_sell,
                    "DII Buy": dii_buy, "DII Sell": dii_sell,
                })
            except Exception:
                continue
        if not records:
            return None, None
        df = pd.DataFrame(records)
        return df, df.iloc[0] if len(df) > 0 else None
    except Exception:
        return None, None

# ══════════════════════════════════════════════════════════════════════════════
# OPTIONS CHAIN — NSE India
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=900, show_spinner=False)
def fetch_options_chain(symbol: str):
    clean = symbol.replace(".NS","").replace(".BO","").upper()
    url = f"https://www.nseindia.com/api/option-chain-equities?symbol={clean}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": f"https://www.nseindia.com/get-quotes/derivatives?symbol={clean}",
    }
    try:
        import http.cookiejar
        cj   = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        main_req = urllib.request.Request("https://www.nseindia.com", headers=headers)
        opener.open(main_req, timeout=8)
        time.sleep(0.5)
        req = urllib.request.Request(url, headers=headers)
        with opener.open(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception:
        return None

def parse_options_chain(data, spot_price: float):
    if not data:
        return None, None, None, None
    try:
        records = data.get("records", {})
        exp_dates = records.get("expiryDates", [])
        nearest_exp = exp_dates[0] if exp_dates else None
        chain_data  = records.get("data", [])

        rows = []
        for item in chain_data:
            if nearest_exp and item.get("expiryDate") != nearest_exp:
                continue
            strike = item.get("strikePrice", 0)
            ce = item.get("CE", {})
            pe = item.get("PE", {})
            rows.append({
                "Strike":   strike,
                "CE OI":    ce.get("openInterest", 0),
                "CE Chg OI": ce.get("changeinOpenInterest", 0),
                "CE LTP":   ce.get("lastPrice", 0),
                "CE IV":    ce.get("impliedVolatility", 0),
                "PE OI":    pe.get("openInterest", 0),
                "PE Chg OI": pe.get("changeinOpenInterest", 0),
                "PE LTP":   pe.get("lastPrice", 0),
                "PE IV":    pe.get("impliedVolatility", 0),
            })

        if not rows:
            return None, None, None, nearest_exp

        df_chain = pd.DataFrame(rows).sort_values("Strike")

        total_ce_oi = df_chain["CE OI"].sum()
        total_pe_oi = df_chain["PE OI"].sum()
        pcr = round(total_pe_oi / total_ce_oi, 3) if total_ce_oi > 0 else None

        strikes = df_chain["Strike"].values
        ce_ois  = df_chain["CE OI"].values
        pe_ois  = df_chain["PE OI"].values
        pain    = []
        for s in strikes:
            ce_pain = sum(max(0, s - k) * o for k, o in zip(strikes, ce_ois))
            pe_pain = sum(max(0, k - s) * o for k, o in zip(strikes, pe_ois))
            pain.append(ce_pain + pe_pain)
        max_pain_strike = float(strikes[int(np.argmin(pain))])

        return df_chain, pcr, max_pain_strike, nearest_exp
    except Exception as e:
        return None, None, None, None

# ══════════════════════════════════════════════════════════════════════════════
# FUNDAMENTAL DATA — screener.in scraper
# ══════════════════════════════════════════════════════════════════════════════
def _parse_ratio_li(html: str, label: str):
    li_pattern = re.compile(
        r'<li[^>]*>\s*<span class="name">\s*(?:<a[^>]*>)?\s*' + re.escape(label) +
        r'\s*(?:</a>)?\s*</span>(.*?)</li>', re.IGNORECASE | re.DOTALL
    )
    m = li_pattern.search(html)
    if not m:
        return None
    block = m.group(1)
    nums = re.findall(r'-?[\d]+(?:,\d{3})*(?:\.\d+)?', block)
    if not nums:
        return None
    try:
        return float(nums[-1].replace(",", ""))
    except Exception:
        return None

def _sane(value, lo, hi):
    if value is None:
        return None
    return value if lo <= value <= hi else None

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_fundamentals(symbol: str):
    clean = symbol.replace(".NS", "").replace(".BO", "").upper()
    url   = f"https://www.screener.in/company/{clean}/consolidated/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode("utf-8", errors="ignore")
    except Exception:
        try:
            url2 = f"https://www.screener.in/company/{clean}/"
            req2 = urllib.request.Request(url2, headers=headers)
            with urllib.request.urlopen(req2, timeout=10) as r:
                html = r.read().decode("utf-8", errors="ignore")
            url = url2
        except Exception:
            return {}, url

    pe   = _sane(_parse_ratio_li(html, "Stock P/E"),         0, 500)
    pb   = _sane(_parse_ratio_li(html, "Price to Book value"), 0, 100)
    roe  = _sane(_parse_ratio_li(html, "ROE"),                -100, 100)
    roce = _sane(_parse_ratio_li(html, "ROCE"),               -100, 100)
    de   = _sane(_parse_ratio_li(html, "Debt to equity"),      0, 20)
    prom = _sane(_parse_ratio_li(html, "Promoter holding"),    0, 100)
    eps  = _sane(_parse_ratio_li(html, "EPS"),                -1000, 100000)
    dy   = _sane(_parse_ratio_li(html, "Dividend Yield"),       0, 25)

    return {
        "P/E Ratio":      pe,
        "P/B Ratio":      pb,
        "ROE (%)":        roe,
        "ROCE (%)":       roce,
        "Debt/Equity":    de,
        "Promoter Hold%": prom,
        "EPS (TTM)":      eps,
        "Div Yield (%)":  dy,
    }, url

# ══════════════════════════════════════════════════════════════════════════════
# INITIALIZE FORECAST SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "fc_horizon_type" not in st.session_state:
    st.session_state["fc_horizon_type"] = "Swing Trade (Days)"
if "fc_steps" not in st.session_state:
    st.session_state["fc_steps"] = 60
if "fc_years" not in st.session_state:
    st.session_state["fc_years"] = 2
if "fc_history_period" not in st.session_state:
    st.session_state["fc_history_period"] = "2y"

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
col_title, col_clock = st.columns([2,1])
with col_title:
    st.markdown('<h1 class="xerces-title">XERCES // QUANT ENGINE</h1>', unsafe_allow_html=True)
    st.markdown('<p class="telemetry-tag">[ NSE/BSE UNIVERSE: 600+ STOCKS // ARIMA + TECHNICAL + PORTFOLIO ENGINE // GODMODE ]</p>', unsafe_allow_html=True)
with col_clock:
    now_ist = ist_now()
    ms, mc  = market_status()
    st.markdown(f"""
    <div style="text-align:right;font-family:'Space Mono',monospace;font-size:11px;color:#6a90aa;
                background:rgba(7,18,32,0.5);padding:8px;border-radius:4px;border:1px solid rgba(0,200,255,0.08);">
        <div>CLOCK: <span style="color:#ffcc00;font-weight:bold;">{now_ist.strftime('%H:%M:%S')} IST</span></div>
        <div>DATE: <span style="color:#00c8ff;">{now_ist.strftime('%d %b %Y')}</span></div>
        <div style="margin-top:3px;color:{mc};font-weight:bold;">{ms}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<hr style='border-color:rgba(0,200,255,0.12);margin:0.65rem 0;'>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL SEARCH BAR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div style='background:rgba(7,18,32,0.45);border:1px solid rgba(0,200,255,0.12);padding:10px 16px;border-radius:6px;margin-bottom:12px;'>", unsafe_allow_html=True)
sc1, sc2 = st.columns([5,1])
with sc1:
    search_raw = st.text_input("Search", value="", placeholder="Search any NSE/BSE stock — name or symbol (e.g. Reliance, TCS, SBIN, INFY)...", label_visibility="collapsed")
with sc2:
    if search_raw and st.button("✕ Clear", use_container_width=True):
        st.session_state["search_val"] = ""
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# ── Ticker resolution ─────────────────────────────────────────────────────────
search = search_raw.strip()
selected_ticker, selected_name, is_dashboard = "^NSEI", "NIFTY 50", True

if search:
    is_dashboard = False
    match_t, match_n = None, None
    sl = search.lower()
    for label, ticker in ALL_STOCKS.items():
        if sl in label.lower():
            match_t, match_n = ticker, label.split(" (")[0]; break
    if not match_t:
        for label, ticker in ALL_STOCKS.items():
            sym = ticker.replace(".NS","")
            if sl.upper() == sym or sl.upper() == ticker.upper():
                match_t, match_n = ticker, label.split(" (")[0]; break
    if match_t:
        selected_ticker, selected_name = match_t, match_n
    else:
        candidate = search.upper()
        if not candidate.endswith(".NS") and not candidate.endswith(".BO") and "^" not in candidate:
            candidate = candidate + ".NS"
        selected_ticker = candidate
        selected_name   = search.upper().replace(".NS","").replace(".BO","")

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD LANDING PAGE
# ══════════════════════════════════════════════════════════════════════════════
if is_dashboard:
    st.markdown('<h2 class="xerces-title" style="font-size:1.5rem;margin-bottom:12px;">📊 LIVE MARKET OVERVIEW</h2>', unsafe_allow_html=True)
    with st.spinner("Loading market indices..."):
        idx_data = load_indices()
    INDEX_META = [
        ("^NSEI","NIFTY 50","#00e87a"), ("^NSEBANK","BANK NIFTY","#00c8ff"),
        ("^BSESN","SENSEX","#ffcc00"),  ("^CRSMID","NIFTY MIDCAP","#ff6b35"),
        ("^CNXSC","NIFTY SMALLCAP","#7c6ef8"), ("^INDIAVIX","INDIA VIX","#ff3355"),
    ]
    cols = st.columns(6)
    for col, (sym, name, clr) in zip(cols, INDEX_META):
        try:
            idf  = idx_data.get(sym)
            if idf is None or len(idf) < 2:
                col.warning(name); continue
            cv   = float(idf["Close"].iloc[-1])
            pv   = float(idf["Close"].iloc[-2])
            chg  = (cv - pv) / pv * 100
            flip = sym == "^INDIAVIX"
            cclr = ("#ff3355" if chg >= 0 else "#00e87a") if flip else ("#00e87a" if chg >= 0 else "#ff3355")
            arrow= "▲" if chg >= 0 else "▼"
            col.markdown(f"""<div class="glass-card">
                <p class="glass-label" style="color:{clr};">{name}</p>
                <div class="glass-value" style="font-size:1.1rem;">{cv:,.2f}</div>
                <p style="font-size:11px;color:{cclr};margin:2px 0;font-weight:600;">{arrow} {abs(chg):.2f}%</p>
            </div>""", unsafe_allow_html=True)
        except Exception:
            col.warning(name)

    try:
        n50 = idx_data.get("^NSEI")
        if n50 is not None and not n50.empty:
            fig0 = go.Figure()
            fig0.add_trace(go.Scatter(x=n50["Date"], y=n50["Close"], line=dict(color="#00e87a",width=2), name="Nifty 50", fill="tozeroy", fillcolor="rgba(0,232,122,0.04)"))
            fig0.update_layout(height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ddeeff",family="Space Mono",size=10), margin=dict(l=10,r=10,t=10,b=10),
                xaxis=dict(gridcolor="rgba(0,200,255,0.05)"), yaxis=dict(gridcolor="rgba(0,200,255,0.05)",tickprefix="₹"),
                showlegend=False)
            st.plotly_chart(fig0, use_container_width=True)
    except Exception:
        pass

    st.markdown("""<div class="glass-card" style="margin-top:10px;">
        <p class="section-header" style="margin-top:0;">💡 How to use XERCES</p>
        <p style="font-size:12px;color:#a0aec0;line-height:1.7;margin:0;">
        Type any stock name or NSE symbol in the search bar above — e.g. <b style="color:#00c8ff;">Reliance</b>, <b style="color:#00c8ff;">TCS</b>, <b style="color:#00c8ff;">HDFCBANK</b>.
        You'll get live technical charts with MACD/RSI/Bollinger Bands, ARIMA + Holt-Winters price forecast to June 2027 with accuracy metrics,
        multi-strategy backtesting, bulk market scanner, portfolio optimizer (MPT), news sentiment, and full risk calculator.
        </p>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("<p class='telemetry-tag' style='color:#00c8ff;font-weight:700;margin-bottom:5px;'>[ 🛡️ RISK CONTROLS ]</p>", unsafe_allow_html=True)
    allocated_capital = st.number_input("Capital Pool (₹)", min_value=1000, value=100000, step=5000)
    risk_per_trade    = st.slider("Risk per Trade (%)", 0.5, 5.0, 1.5, step=0.1)
    risk_reward       = st.slider("Risk:Reward (1:X)", 1.5, 4.0, 2.0, step=0.5)
    st.markdown("---")
    st.markdown("<p class='telemetry-tag' style='color:#00c8ff;font-weight:700;margin-bottom:5px;'>[ ⚙️ CHART SETTINGS ]</p>", unsafe_allow_html=True)
    show_bb   = st.checkbox("Bollinger Bands", value=True)
    show_sma  = st.checkbox("SMA 20/50/200", value=True)
    show_vol  = st.checkbox("Volume bars", value=True)
    st.markdown("---")
    st.markdown("<p class='telemetry-tag' style='color:#00c8ff;font-weight:700;margin-bottom:5px;'>[ 📈 BACKTEST STRATEGY ]</p>", unsafe_allow_html=True)
    backtest_strategy = st.selectbox("Strategy", ["SMA Crossover","RSI Mean Reversion","Bollinger Bands Breakout","MACD Crossover"])
    st.markdown("---")

    # ── ⭐ WATCHLIST ──
    st.markdown("<p class='telemetry-tag' style='color:#00c8ff;font-weight:700;margin-bottom:5px;'>[ ⭐ WATCHLIST ]</p>", unsafe_allow_html=True)
    _wl = xp.load_watchlist()
    if not selected_ticker.startswith("^"):
        _already = any(w["ticker"] == selected_ticker for w in _wl)
        if _already:
            if st.button(f"➖ Remove {selected_name}", use_container_width=True, key="wl_rm"):
                xp.remove_from_watchlist(selected_ticker); st.rerun()
        else:
            if st.button(f"➕ Add {selected_name}", use_container_width=True, key="wl_add"):
                xp.add_to_watchlist(selected_ticker, selected_name); st.rerun()
    if _wl:
        _pick = st.selectbox("Jump to", ["—"] + [f"{w['name']}" for w in _wl], key="wl_pick")
        if _pick != "—":
            _wt = next((w for w in _wl if w["name"] == _pick), None)
            if _wt:
                st.session_state["search_val"] = _wt["name"]
                st.info(f"Search '{_wt['name']}' above to load.")
    else:
        st.caption("Empty — add stocks from any analysis view.")
    st.markdown("---")

    # ── 🚨 ALERTS ──
    st.markdown("<p class='telemetry-tag' style='color:#ff6b35;font-weight:700;margin-bottom:5px;'>[ 🚨 ALERTS ]</p>", unsafe_allow_html=True)
    _alerts = xp.load_alerts()
    _active = [a for a in _alerts if not a.get("triggered")]
    _fired  = [a for a in _alerts if a.get("triggered")]
    st.caption(f"{len(_active)} active · {len(_fired)} triggered")
    with st.expander("➕ Add alert", expanded=False):
        _akind = st.radio("Type", ["price", "rsi"], horizontal=True, key="al_kind")
        _aop   = st.radio("Condition", [">", "<"], horizontal=True, key="al_op")
        _last_price = float(st.session_state.get("_stock_ctx", {}).get("price", 100.0))
        _aval  = st.number_input("Threshold", value=(_last_price if _akind=="price" else 30.0), key="al_val")
        if st.button("Set Alert", use_container_width=True, key="al_add"):
            xp.add_alert(selected_ticker, selected_name, _akind, _aop, _aval)
            st.success("Alert saved."); st.rerun()
    for _a in _alerts[-6:][::-1]:
        _clr = "#00e87a" if _a.get("triggered") else "#ffcc00"
        _tag = "🔔 FIRED" if _a.get("triggered") else "⏳"
        st.markdown(f"<div style='background:rgba(7,18,32,0.6);padding:6px 8px;border-radius:4px;"
                    f"border-left:3px solid {_clr};margin-bottom:4px;font-size:11px;color:#ddeeff;'>"
                    f"{_tag} <b>{_a['name']}</b> · {_a['kind'].upper()} {_a['op']} {_a['value']}"
                    f"</div>", unsafe_allow_html=True)
    if _fired and st.button("🧹 Clear triggered", use_container_width=True, key="al_clr"):
        xp.save_alerts([a for a in _alerts if not a.get("triggered")]); st.rerun()
    st.markdown("---")
    st.caption("⚠️ Not SEBI registered. Statistical analysis only. Not financial advice. Data: Yahoo Finance.")

# ══════════════════════════════════════════════════════════════════════════════
# LOAD + VALIDATE DATA (WITH DYNAMIC HORIZON PERIOD)
# ══════════════════════════════════════════════════════════════════════════════
history_period = st.session_state.get("fc_history_period", "2y")
with st.spinner(f"Loading {selected_name} ({selected_ticker}) with {history_period} history..."):
    raw_df = load_ohlcv(selected_ticker, period=history_period)

if raw_df is None or len(raw_df) < 40:
    st.error(f"❌ Could not load data for **{selected_ticker}**.")
    if selected_ticker.endswith(".NS"):
        bse = selected_ticker.replace(".NS",".BO")
        st.info(f"Try BSE: type `{bse.replace('.BO','')} .BO` in the search bar, or verify the symbol on NSE India.")
    else:
        st.info("For NSE stocks append `.NS` (e.g. RELIANCE.NS). For BSE append `.BO`.")
    st.stop()

_df_cache_key = f"df__{selected_ticker}__{history_period}"
_bt_cache_key = f"bt__{selected_ticker}__{backtest_strategy}__{history_period}"

if _df_cache_key not in st.session_state:
    st.session_state[_df_cache_key] = add_indicators(raw_df)

df = st.session_state[_df_cache_key]

if _bt_cache_key not in st.session_state:
    st.session_state[_bt_cache_key] = run_backtest(df, backtest_strategy)

bt_df, trades, buy_x, buy_y, sell_x, sell_y = st.session_state[_bt_cache_key]

last     = df.iloc[-1]
prev     = df.iloc[-2]
close    = float(last["Close"])
signal   = get_signal(df)
strength = get_signal_strength(df)
atr_val  = float(last["ATR_14"]) if pd.notna(last.get("ATR_14")) else close * 0.02
sl_price = close - atr_val * 1.5
tp_price = close + atr_val * 1.5 * risk_reward
chg1d    = (close - float(prev["Close"])) / float(prev["Close"]) * 100
hi52     = float(df["Close"].iloc[-252:].max()) if len(df) >= 252 else float(df["Close"].max())
lo52     = float(df["Close"].iloc[-252:].min()) if len(df) >= 252 else float(df["Close"].min())
rsi_val  = float(last["RSI_14"]) if pd.notna(last.get("RSI_14")) else 50.0
macd_v   = float(last.get("MACD") or 0)
macd_sv  = float(last.get("MACD_Signal") or 0)
vol20    = float(last.get("Volatility_20") or 0)

# XERCES+ — build live context for AI / PDF / etc.
_stock_ctx = {
    "ticker": selected_ticker, "name": selected_name,
    "price": close, "change_1d": chg1d,
    "signal": signal, "strength": strength,
    "rsi": rsi_val, "macd": macd_v, "macd_signal": macd_sv,
    "sma20": float(last.get("SMA_20") or 0),
    "sma50": float(last.get("SMA_50") or 0),
    "sma200": float(last.get("SMA_200") or 0),
    "atr": atr_val, "vol": vol20,
    "hi52": hi52, "lo52": lo52,
}
st.session_state["_stock_ctx"] = _stock_ctx

# XERCES+ — evaluate alerts and show banner if any newly triggered
def _alert_lookup(t):
    if t == selected_ticker:
        return {"price": close, "rsi": rsi_val}
    return None
_new_alerts = xp.evaluate_alerts(_alert_lookup)
if _new_alerts:
    for _a in _new_alerts:
        st.warning(f"🔔 ALERT TRIGGERED — {_a['name']}: {_a['kind'].upper()} {_a['op']} {_a['value']} "
                   f"(current: {_a.get('last_val', 0):.2f})")

# ══════════════════════════════════════════════════════════════════════════════
# KPI ROW
# ══════════════════════════════════════════════════════════════════════════════
k1,k2,k3,k4,k5,k6,k7 = st.columns(7)
sig_clr  = {"BUY":"#00e87a","SELL":"#ff3355","HOLD":"#ffcc00"}[signal]
chg_clr  = "#00e87a" if chg1d >= 0 else "#ff3355"
str_clr  = "#00e87a" if strength >= 65 else "#ff3355" if strength <= 35 else "#ffcc00"

for col, lbl, val, clr in zip(
    [k1,k2,k3,k4,k5,k6,k7],
    ["Last Close","1D Change","52W High","52W Low","RSI (14)","Signal","Strength"],
    [f"₹{close:,.2f}",f"{'▲' if chg1d>=0 else '▼'} {abs(chg1d):.2f}%",
     f"₹{hi52:,.2f}",f"₹{lo52:,.2f}",f"{rsi_val:.1f}",signal,f"{strength}/100"],
    ["#ddeeff",chg_clr,"#ddeeff","#ddeeff",
     "#ff3355" if rsi_val>70 else "#00e87a" if rsi_val<30 else "#00c8ff",
     sig_clr, str_clr]
):
    col.markdown(f'<div class="glass-card"><p class="glass-label">{lbl}</p>'
                 f'<div class="glass-value" style="color:{clr};font-size:1.1rem;">{val}</div></div>',
                 unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
(tab_chart, tab_arima, tab_backtest, tab_scan, tab_risk, tab_port, tab_fii,
 tab_options, tab_funds, tab_news,
 tab_heatmap, tab_compare, tab_ai, tab_journal, tab_export,
 tab_help) = st.tabs([
    "📊 CHART", "🔮 FORECAST", "📈 BACKTEST", "📡 SCANNER",
    "🛡️ RISK", "💼 PORTFOLIO", "📊 FII/DII", "🎯 OPTIONS", "📋 FUNDAMENTALS", "📰 NEWS",
    "🔥 HEATMAP", "🔄 COMPARE", "🤖 AI ANALYST", "📓 JOURNAL", "📄 EXPORT",
    "❓ MANUAL"
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: TECHNICAL CHART
# ─────────────────────────────────────────────────────────────────────────────
with tab_chart:
    rows    = 4 if show_vol else 3
    row_h   = ([0.48,0.18,0.18,0.16] if show_vol else [0.56,0.22,0.22])
    titles  = ["Price + Indicators","RSI (14)","MACD"] + (["Volume"] if show_vol else [])
    fig = make_subplots(rows=rows, cols=1, shared_xaxes=True, row_heights=row_h,
                        vertical_spacing=0.025, subplot_titles=titles,
                        specs=[[{"secondary_y":False}]]*rows)

    fig.add_trace(go.Candlestick(
        x=df["Date"], open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"],
        name="OHLC", increasing_line_color="#00e87a", decreasing_line_color="#ff3355",
        increasing_fillcolor="rgba(0,232,122,0.25)", decreasing_fillcolor="rgba(255,51,85,0.25)"
    ), row=1, col=1)

    if show_sma:
        for col_n, clr, dsh in [("SMA_20","#00c8ff","dot"),("SMA_50","#ffcc00","dash"),("SMA_200","#ff6b35","solid")]:
            if col_n in df.columns:
                fig.add_trace(go.Scatter(x=df["Date"], y=df[col_n], name=col_n.replace("_"," "),
                    line=dict(color=clr,width=1.2,dash=dsh), opacity=0.85), row=1, col=1)

    if show_bb and "BB_Upper" in df.columns:
        fig.add_trace(go.Scatter(x=df["Date"], y=df["BB_Upper"], name="BB Upper",
            line=dict(color="rgba(124,78,255,0.5)",width=1,dash="dot")), row=1, col=1)
        fig.add_trace(go.Scatter(x=df["Date"], y=df["BB_Lower"], name="BB Lower",
            line=dict(color="rgba(124,78,255,0.5)",width=1,dash="dot"),
            fill="tonexty", fillcolor="rgba(124,78,255,0.04)"), row=1, col=1)

    fig.add_hline(y=sl_price, line_dash="dash", line_color="rgba(255,51,85,0.6)",
                  annotation_text=f"SL ₹{sl_price:,.0f}", row=1, col=1)
    fig.add_hline(y=tp_price, line_dash="dash", line_color="rgba(0,232,122,0.6)",
                  annotation_text=f"TP ₹{tp_price:,.0f}", row=1, col=1)

    if buy_x:
        fig.add_trace(go.Scatter(x=buy_x, y=buy_y, mode="markers", name="Buy Entry",
            marker=dict(symbol="triangle-up", size=9, color="#00e87a",
                        line=dict(width=1, color="#020813"))), row=1, col=1)
    if sell_x:
        fig.add_trace(go.Scatter(x=sell_x, y=sell_y, mode="markers", name="Sell Exit",
            marker=dict(symbol="triangle-down", size=9, color="#ff3355",
                        line=dict(width=1, color="#020813"))), row=1, col=1)

    fig.add_trace(go.Scatter(x=df["Date"], y=df["RSI_14"], name="RSI 14",
        line=dict(color="#00c8ff",width=1.5)), row=2, col=1)
    for lvl, lc in [(70,"rgba(255,51,85,0.4)"),(30,"rgba(0,232,122,0.4)"),(50,"rgba(255,255,255,0.08)")]:
        fig.add_hline(y=lvl, line_dash="dot", line_color=lc, row=2, col=1)

    mc_colors = ["#00e87a" if v>=0 else "#ff3355" for v in df["MACD_Hist"].fillna(0)]
    fig.add_trace(go.Bar(x=df["Date"], y=df["MACD_Hist"], name="MACD Hist", marker_color=mc_colors, opacity=0.7), row=3, col=1)
    fig.add_trace(go.Scatter(x=df["Date"], y=df["MACD"], name="MACD", line=dict(color="#00c8ff",width=1.2)), row=3, col=1)
    fig.add_trace(go.Scatter(x=df["Date"], y=df["MACD_Signal"], name="Signal", line=dict(color="#ffcc00",width=1.2,dash="dot")), row=3, col=1)
    fig.add_hline(y=0, line_dash="dot", line_color="rgba(255,255,255,0.1)", row=3, col=1)

    if show_vol and "Volume" in df.columns:
        vc = ["rgba(0,232,122,0.4)" if r["Close"] >= r["Open"] else "rgba(255,51,85,0.4)" for _,r in df.iterrows()]
        fig.add_trace(go.Bar(x=df["Date"], y=df["Volume"], name="Volume", marker_color=vc), row=4, col=1)

    fig.update_layout(
        height=780, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ddeeff",family="Space Mono",size=10),
        xaxis_rangeslider_visible=False, showlegend=True,
        legend=dict(bgcolor="rgba(7,18,32,0.5)",bordercolor="rgba(0,200,255,0.15)",borderwidth=1,font=dict(size=9)),
        margin=dict(l=10,r=10,t=30,b=10),
    )
    for i in range(1, rows+1):
        fig.update_xaxes(gridcolor="rgba(0,200,255,0.04)", row=i, col=1)
        fig.update_yaxes(gridcolor="rgba(0,200,255,0.04)", row=i, col=1)
    fig.update_xaxes(rangeselector=dict(
        buttons=[dict(count=1,label="1M",step="month"),dict(count=3,label="3M",step="month"),
                 dict(count=6,label="6M",step="month"),dict(count=1,label="1Y",step="year"),
                 dict(count=2,label="2Y",step="year"),dict(step="all",label="5Y")],
        bgcolor="rgba(7,18,32,0.7)", activecolor="#00c8ff", font=dict(color="#ddeeff",size=9)
    ), row=1, col=1)
    st.plotly_chart(fig, use_container_width=True)

    ls, rs = st.columns([1,2])
    with ls:
        st.markdown(f"""<div class="glass-card" style="text-align:center;">
            <p class="glass-label">Signal</p>
            <div class="signal-{'buy' if signal=='BUY' else 'sell' if signal=='SELL' else 'hold'}">{signal}</div>
            <div style="background:rgba(255,255,255,0.05);border-radius:4px;height:6px;margin:8px 0;">
              <div style="width:{strength}%;height:6px;border-radius:4px;background:{str_clr};"></div>
            </div>
            <p style="font-size:10px;color:#6a90aa;margin:0;">Strength {strength}/100</p>
        </div>""", unsafe_allow_html=True)
    with rs:
        bb_pct = ""
        if pd.notna(last.get("BB_Upper")) and pd.notna(last.get("BB_Lower")):
            bbrng = float(last["BB_Upper"]) - float(last["BB_Lower"])
            bb_pct = f"{(close-float(last['BB_Lower']))/bbrng*100:.0f}%" if bbrng>0 else "—"
        sk = float(last.get("Stoch_K",50) or 50)
        st.markdown(f"""<div class="glass-card">
            <p class="glass-label">Readings</p>
            <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin-top:6px;font-size:11px;font-family:'Space Mono',monospace;">
                <div>RSI: <span style="color:{'#ff3355' if rsi_val>70 else '#00e87a' if rsi_val<30 else '#00c8ff'}">{rsi_val:.1f}</span></div>
                <div>MACD: <span style="color:{'#00e87a' if macd_v>macd_sv else '#ff3355'}">{macd_v:.2f}</span></div>
                <div>ATR(14): <span style="color:#ffcc00;">₹{atr_val:.2f}</span></div>
                <div>Stoch %K: <span style="color:{'#ff3355' if sk>80 else '#00e87a' if sk<20 else '#ddeeff'}">{sk:.0f}</span></div>
                <div>BB Pos: <span style="color:#7c4dff;">{bb_pct}</span></div>
                <div>Volatility: <span style="color:#ddeeff;">{vol20:.1%}</span></div>
                <div>SMA 200: <span style="color:#ff6b35;">₹{float(last.get('SMA_200',0) or 0):,.0f}</span></div>
                <div>SMA 50: <span style="color:#ffcc00;">₹{float(last.get('SMA_50',0) or 0):,.0f}</span></div>
                <div>SMA 20: <span style="color:#00c8ff;">₹{float(last.get('SMA_20',0) or 0):,.0f}</span></div>
            </div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: ARIMA FORECAST (WITH HORIZON TIME ADJUSTER)
# ─────────────────────────────────────────────────────────────────────────────
with tab_arima:
    st.markdown(f'<p class="section-header">[ 🔮 MULTI-HORIZON PRICE FORECAST — {selected_name} ]</p>', unsafe_allow_html=True)
    
    hz_col1, hz_col2 = st.columns(2)
    with hz_col1:
        horizon_type = st.radio(
            "Forecast Horizon Type", 
            ["Swing Trade (Days)", "Long-Term Hold (Years)"], 
            index=0 if st.session_state.get("fc_horizon_type", "Swing Trade (Days)") == "Swing Trade (Days)" else 1,
            key="horizon_type_selector"
        )
    with hz_col2:
        if horizon_type == "Swing Trade (Days)":
            steps_input = st.slider(
                "Forecast Steps (Trading Days)", 
                min_value=1, max_value=252, 
                value=st.session_state.get("fc_steps", 60), step=1,
                key="steps_slider"
            )
            if (st.session_state.get("fc_horizon_type") != "Swing Trade (Days)" or 
                st.session_state.get("fc_steps") != steps_input):
                st.session_state["fc_horizon_type"] = "Swing Trade (Days)"
                st.session_state["fc_steps"] = steps_input
                st.session_state["fc_history_period"] = "2y"
                st.rerun()
            steps = steps_input
        else:
            years_input = st.slider(
                "Forecast Horizon (Years)", 
                min_value=1, max_value=25, 
                value=st.session_state.get("fc_years", 2), step=1,
                key="years_slider"
            )
            if (st.session_state.get("fc_horizon_type") != "Long-Term Hold (Years)" or 
                st.session_state.get("fc_years") != years_input):
                st.session_state["fc_horizon_type"] = "Long-Term Hold (Years)"
                st.session_state["fc_years"] = years_input
                st.session_state["fc_history_period"] = "10y" if years_input <= 5 else "max"
                st.rerun()
            steps = years_input * 252

    price_series = df["Close"].astype(float).dropna()
    last_date    = pd.to_datetime(df["Date"].iloc[-1])
    fc_dates     = pd.bdate_range(start=last_date + pd.Timedelta(days=1), periods=steps)
    target_end   = fc_dates[-1]

    if steps <= 0:
        st.warning("Data already extends past target horizon.")
    else:
        with st.spinner(f"Fitting ARIMA + Holt-Winters model for {steps} steps..."):
            try:
                fc_mean, fc_lo, fc_hi, arima_order, aic_val, arima_model, log_s = run_arima(price_series, steps)
                fc_series = pd.Series(fc_mean.values, index=fc_dates)
                ci_lo     = pd.Series(fc_lo.values,   index=fc_dates)
                ci_hi     = pd.Series(fc_hi.values,   index=fc_dates)
                hw_series = pd.Series(run_holt_winters(price_series, steps).values, index=fc_dates)

                target_arima = float(fc_series.iloc[-1])
                target_hw    = float(hw_series.iloc[-1])
                consensus    = (target_arima + target_hw) / 2
                upside_a     = (target_arima - close) / close * 100
                upside_hw    = (target_hw - close) / close * 100
                upside_c     = (consensus - close) / close * 100

                mape, dir_acc = compute_accuracy(price_series, arima_order, holdout=60)

                fa1,fa2,fa3,fa4,fa5 = st.columns(5)
                for col, lbl, val, clr in zip([fa1,fa2,fa3,fa4,fa5],
                    ["Current Price", "ARIMA Target", "Holt-Winters Target", "Consensus Target", "Model Fitted"],
                    [f"₹{close:,.2f}",
                     f"₹{target_arima:,.0f} ({'▲' if upside_a>=0 else '▼'}{abs(upside_a):.1f}%)",
                     f"₹{target_hw:,.0f} ({'▲' if upside_hw>=0 else '▼'}{abs(upside_hw):.1f}%)",
                     f"₹{consensus:,.0f} ({'▲' if upside_c>=0 else '▼'}{abs(upside_c):.1f}%)",
                     f"ARIMA{arima_order}"],
                    ["#ddeeff","#fbbf24","#00c8ff","#00e87a","#ff6b35"]):
                    col.markdown(f'<div class="glass-card"><p class="glass-label">{lbl}</p>'
                                 f'<div class="glass-value" style="color:{clr};font-size:0.95rem;">{val}</div></div>',
                                 unsafe_allow_html=True)

                if mape is not None:
                    am1, am2, am3 = st.columns(3)
                    mape_clr = "#00e87a" if mape < 5 else "#ffcc00" if mape < 10 else "#ff3355"
                    dacc_clr = "#00e87a" if dir_acc > 60 else "#ffcc00" if dir_acc > 50 else "#ff3355"
                    am1.markdown(f'<div class="glass-card"><p class="glass-label">60-Day Backtest MAPE</p>'
                                 f'<div class="glass-value" style="color:{mape_clr};">{mape:.2f}%</div>'
                                 f'<p style="font-size:10px;color:#6a90aa;margin:3px 0 0;">{"Excellent" if mape<5 else "Good" if mape<10 else "Use with caution"}</p></div>',
                                 unsafe_allow_html=True)
                    am2.markdown(f'<div class="glass-card"><p class="glass-label">Directional Accuracy</p>'
                                 f'<div class="glass-value" style="color:{dacc_clr};">{dir_acc:.0f}%</div>'
                                 f'<p style="font-size:10px;color:#6a90aa;margin:3px 0 0;">Win rate on direction</p></div>',
                                 unsafe_allow_html=True)
                    am3.markdown(f'<div class="glass-card"><p class="glass-label">AIC Score</p>'
                                 f'<div class="glass-value" style="color:#7c4dff;">{aic_val}</div>'
                                 f'<p style="font-size:10px;color:#6a90aa;margin:3px 0 0;">Lower = better fit</p></div>',
                                 unsafe_allow_html=True)

                fig2 = go.Figure()
                hp   = price_series.iloc[-504:]
                hd   = pd.to_datetime(df["Date"].iloc[-504:])
                fig2.add_trace(go.Scatter(x=hd, y=hp.values, name="Historical Data", line=dict(color="#7c6ef8",width=1.8)))
                fig2.add_trace(go.Scatter(x=fc_series.index, y=fc_series.values, name="ARIMA", line=dict(color="#f97316",width=2,dash="dash")))
                fig2.add_trace(go.Scatter(x=hw_series.index, y=hw_series.values, name="Holt-Winters", line=dict(color="#00c8ff",width=1.5,dash="dashdot")))
                fig2.add_trace(go.Scatter(x=fc_series.index, y=(fc_series.values+hw_series.values)/2, name="Consensus",
                    line=dict(color="#00e87a",width=1.5,dash="longdash")))
                fig2.add_trace(go.Scatter(
                    x=list(ci_hi.index)+list(ci_lo.index[::-1]),
                    y=list(ci_hi.values)+list(ci_lo.values[::-1]),
                    fill="toself", fillcolor="rgba(249,115,22,0.08)",
                    line=dict(color="rgba(0,0,0,0)"), name="ARIMA 90% CI"))
                fig2.add_vline(x=str(last_date), line_dash="dot", line_color="rgba(100,100,100,0.4)")
                fig2.add_annotation(x=str(target_end), y=consensus,
                    text=f"Consensus Target<br>{target_end.strftime('%d %b %Y')}<br>₹{consensus:,.0f}",
                    showarrow=True, arrowhead=2, arrowcolor="#00e87a",
                    font=dict(color="#00e87a",size=10), bgcolor="rgba(7,18,32,0.85)",
                    bordercolor="#00e87a", borderwidth=1)
                fig2.update_layout(height=440, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#ddeeff",family="Space Mono",size=10),
                    legend=dict(bgcolor="rgba(7,18,32,0.5)",bordercolor="rgba(0,200,255,0.2)",borderwidth=1),
                    margin=dict(l=10,r=10,t=20,b=10),
                    xaxis=dict(gridcolor="rgba(0,200,255,0.04)"),
                    yaxis=dict(gridcolor="rgba(0,200,255,0.04)",tickprefix="₹"))
                st.plotly_chart(fig2, use_container_width=True)

                fc_df2 = pd.DataFrame({"Forecast":fc_series,"HW":hw_series,"CI_Lo":ci_lo,"CI_Hi":ci_hi})
                
                if horizon_type == "Long-Term Hold (Years)" and years_input > 2:
                    st.markdown('<p class="section-header">[ 📅 YEAR-BY-YEAR ARIMA PRICE TARGETS ]</p>', unsafe_allow_html=True)
                    fc_df2["Year"] = fc_df2.index.to_period("A")
                    yearly = fc_df2.groupby("Year").agg(
                        Forecast=("Forecast","last"), HW=("HW","last"),
                        CI_Lo=("CI_Lo","last"), CI_Hi=("CI_Hi","last")
                    ).reset_index()
                    yearly["Year_str"] = yearly["Year"].dt.strftime("Year %Y")
                    yearly["YoY_pct"]   = yearly["Forecast"].pct_change() * 100
                    yearly.loc[0,"YoY_pct"] = (yearly.loc[0,"Forecast"] - close) / close * 100

                    for i in range(0, len(yearly), 6):
                        chunk = yearly.iloc[i:i+6]
                        cols  = st.columns(len(chunk))
                        for col, (_,row) in zip(cols, chunk.iterrows()):
                            chg   = row["YoY_pct"]
                            arrow = "▲" if chg>=0 else "▼"
                            clr   = "#00e87a" if chg>=0 else "#ff3355"
                            col.markdown(f"""
<div style="background:rgba(7,18,32,0.65);border:1px solid rgba(0,200,255,0.15);border-radius:6px;
     padding:9px 7px;text-align:center;margin-bottom:6px;">
  <div style="font-size:9px;font-family:'Space Mono',monospace;color:#6a90aa;text-transform:uppercase;">{row['Year_str']}</div>
  <div style="font-family:'Orbitron',sans-serif;font-size:.95rem;font-weight:700;color:#fbbf24;margin:3px 0;">₹{row['Forecast']:,.0f}</div>
  <div style="font-size:9px;color:{clr};font-weight:600;">{arrow} {abs(chg):.1f}%</div>
  <div style="font-size:8px;color:rgba(100,120,140,0.8);margin-top:2px;">HW: ₹{row['HW']:,.0f}</div>
  <div style="font-size:8px;color:rgba(100,120,140,0.5);">₹{row['CI_Lo']:,.0f}–₹{row['CI_Hi']:,.0f}</div>
</div>""", unsafe_allow_html=True)
                else:
                    st.markdown('<p class="section-header">[ 📅 MONTH-BY-MONTH ARIMA PRICE TARGETS ]</p>', unsafe_allow_html=True)
                    fc_df2["Month"] = fc_df2.index.to_period("M")
                    monthly = fc_df2.groupby("Month").agg(
                        Forecast=("Forecast","last"), HW=("HW","last"),
                        CI_Lo=("CI_Lo","last"), CI_Hi=("CI_Hi","last")
                    ).reset_index()
                    monthly["Month_str"] = monthly["Month"].dt.strftime("%b %Y")
                    monthly["MoM_pct"]   = monthly["Forecast"].pct_change() * 100
                    monthly.loc[0,"MoM_pct"] = (monthly.loc[0,"Forecast"] - close) / close * 100

                    for i in range(0, len(monthly), 6):
                        chunk = monthly.iloc[i:i+6]
                        cols  = st.columns(len(chunk))
                        for col, (_,row) in zip(cols, chunk.iterrows()):
                            chg   = row["MoM_pct"]
                            arrow = "▲" if chg>=0 else "▼"
                            clr   = "#00e87a" if chg>=0 else "#ff3355"
                            col.markdown(f"""
<div style="background:rgba(7,18,32,0.65);border:1px solid rgba(0,200,255,0.15);border-radius:6px;
     padding:9px 7px;text-align:center;margin-bottom:6px;">
  <div style="font-size:9px;font-family:'Space Mono',monospace;color:#6a90aa;text-transform:uppercase;">{row['Month_str']}</div>
  <div style="font-family:'Orbitron',sans-serif;font-size:.95rem;font-weight:700;color:#fbbf24;margin:3px 0;">₹{row['Forecast']:,.0f}</div>
  <div style="font-size:9px;color:{clr};font-weight:600;">{arrow} {abs(chg):.1f}%</div>
  <div style="font-size:8px;color:rgba(100,120,140,0.8);margin-top:2px;">HW: ₹{row['HW']:,.0f}</div>
  <div style="font-size:8px;color:rgba(100,120,140,0.5);">₹{row['CI_Lo']:,.0f}–₹{row['CI_Hi']:,.0f}</div>
</div>""", unsafe_allow_html=True)

                tbl = fc_df2.round(2)
                st.download_button("⬇️ Download Forecast CSV",
                                   tbl.to_csv().encode(),
                                   f"{selected_name}_forecast.csv","text/csv")

                with st.expander("🔬 Model diagnostics"):
                    pv = adfuller(np.log(price_series.dropna()))[1]
                    st.markdown(f"""
| Parameter | Value |
|---|---|
| Ticker | {selected_ticker} |
| ARIMA order | {arima_order} |
| AIC | {aic_val} |
| MAPE (60-day holdout) | {f"{mape:.2f}%" if mape is not None else "N/A"} |
| Directional accuracy | {f"{dir_acc:.1f}%" if dir_acc is not None else "N/A"} |
| Training observations | {len(price_series):,} |
| Forecast horizon | {steps} trading days |
| Data range | {str(df["Date"].iloc[0])[:10]} to {str(df["Date"].iloc[-1])[:10]} |
""")
            except Exception as e:
                st.error(f"Forecast error: {e}")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: BACKTEST ENGINE
# ─────────────────────────────────────────────────────────────────────────────
with tab_backtest:
    st.markdown(f'<p class="section-header">[ BACKTEST: {backtest_strategy.upper()} — {selected_name} ]</p>', unsafe_allow_html=True)
    st.caption("Next-day open execution — no look-ahead bias.")

    if trades:
        tdf      = pd.DataFrame(trades)
        wins     = (tdf["P&L %"] > 0).sum()
        total    = len(tdf)
        win_rate = wins / total * 100
        gp       = tdf[tdf["P&L %"] > 0]["P&L %"].sum()
        gl       = abs(tdf[tdf["P&L %"] < 0]["P&L %"].sum())
        pf       = gp / gl if gl > 0 else (999.0 if gp > 0 else 0.0)
        pf_str   = f"{pf:.2f}" if gl > 0 else ("inf" if gp > 0 else "0.00")

        bt_df["Strat_Ret"] = bt_df["Signal_BT"].shift(1) * bt_df["Close"].astype(float).pct_change()
        bt_df["Equity"]    = (1 + bt_df["Strat_Ret"].fillna(0)).cumprod()
        bt_df["BH"]        = bt_df["Close"].astype(float) / float(bt_df["Close"].iloc[0])
        bt_df["Peak"]      = bt_df["Equity"].cummax()
        bt_df["DD"]        = (bt_df["Equity"] - bt_df["Peak"]) / bt_df["Peak"]
        max_dd             = abs(float(bt_df["DD"].min()) * 100)
        ret_s              = bt_df["Strat_Ret"].fillna(0)
        sharpe             = float(ret_s.mean() / ret_s.std() * np.sqrt(252)) if ret_s.std() > 0 else 0.0
        ann_ret            = (float(bt_df["Equity"].iloc[-1]) ** (252 / max(len(bt_df), 1)) - 1) * 100
        bh_ret             = (float(bt_df["BH"].iloc[-1]) - 1) * 100

        b1, b2, b3, b4, b5, b6 = st.columns(6)
        for col, lbl, val, clr in zip(
            [b1, b2, b3, b4, b5, b6],
            ["Win Rate", "Profit Factor", "Max Drawdown", "Sharpe Ratio", "Ann. Return", "Alpha vs B&H"],
            [f"{win_rate:.1f}%", pf_str, f"-{max_dd:.1f}%", f"{sharpe:.2f}",
             f"{ann_ret:+.1f}%", f"{ann_ret - bh_ret:+.1f}%"],
            ["#00e87a",
             "#00e87a" if pf >= 1.5 else "#ffcc00" if pf >= 1.0 else "#ff3355",
             "#ff3355", "#00c8ff",
             "#00e87a" if ann_ret > 0 else "#ff3355",
             "#00e87a" if ann_ret > bh_ret else "#ff3355"]
        ):
            col.markdown(
                f'<div class="glass-card"><p class="glass-label">{lbl}</p>'
                f'<div class="glass-value" style="color:{clr};font-size:1rem;">{val}</div></div>',
                unsafe_allow_html=True
            )

        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=bt_df["Date"], y=bt_df["Equity"] * 100, name="Strategy",
                                  line=dict(color="#00e87a", width=2)))
        fig3.add_trace(go.Scatter(x=bt_df["Date"], y=bt_df["BH"] * 100, name="Buy & Hold",
                                  line=dict(color="#7c6ef8", width=1.5, dash="dot")))
        fig3.update_layout(
            height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ddeeff", family="Space Mono", size=10),
            xaxis=dict(gridcolor="rgba(0,200,255,0.04)"),
            yaxis=dict(gridcolor="rgba(0,200,255,0.04)", ticksuffix="%"),
            margin=dict(l=10, r=10, t=15, b=10),
            legend=dict(bgcolor="rgba(7,18,32,0.5)", bordercolor="rgba(0,200,255,0.15)", borderwidth=1)
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('<p class="section-header">[ TRADE LOG — LAST 30 ]</p>', unsafe_allow_html=True)
        st.dataframe(tdf.tail(30), use_container_width=True, hide_index=True)
        st.download_button("Download Trade Log", tdf.to_csv(index=False).encode(),
                           f"{selected_name}_trades.csv", "text/csv")
    else:
        st.info("No signals generated. Try a different stock or strategy.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4: MARKET SCANNER
# ─────────────────────────────────────────────────────────────────────────────
with tab_scan:
    st.markdown('<p class="section-header">[ MULTI-STOCK BULK SCANNER ]</p>', unsafe_allow_html=True)
    default_sector = next((k for k in SECTORS.keys() if "Banking" in k), list(SECTORS.keys())[0])
    scan_sectors = st.multiselect("Sectors", list(SECTORS.keys()), default=[default_sector])
    max_stocks = st.slider("Max stocks", 10, 80, 20, step=5)

    if st.button("RUN SCAN", use_container_width=True):
        pool = []
        for sec in scan_sectors:
            pool += [(n, f"{s}.NS") for n, s in SECTORS.get(sec, [])]
        pool = pool[:max_stocks]

        if not pool:
            st.warning("No stocks in selected sectors.")
        else:
            prog = st.progress(0, text="Downloading batch data from Yahoo Finance...")
            results = []

            try:
                tickers_list = [t for _, t in pool]
                prog.progress(0.1, text=f"Fetching {len(tickers_list)} stocks in one batch...")

                batch_df = yf.download(
                    tickers_list, period="1y", interval="1d",
                    auto_adjust=True, progress=False,
                    timeout=30, group_by="ticker", threads=True
                )
                prog.progress(0.5, text="Computing indicators for each stock...")

                for idx, (name, ticker_s) in enumerate(pool):
                    try:
                        if isinstance(batch_df.columns, pd.MultiIndex):
                            if ticker_s in batch_df.columns.get_level_values(0):
                                sd = batch_df[ticker_s].copy()
                            elif ticker_s in batch_df.columns.get_level_values(1):
                                sd = batch_df.xs(ticker_s, axis=1, level=1).copy()
                            else:
                                continue
                        else:
                            sd = batch_df.copy()

                        if sd is None or sd.empty or len(sd) < 60:
                            continue

                        sd = sd.reset_index()
                        sd.columns = [str(c).strip() for c in sd.columns]
                        for col in ["Open","High","Low","Close","Volume"]:
                            if col in sd.columns:
                                sd[col] = pd.to_numeric(sd[col], errors="coerce")
                        sd = sd.dropna(subset=["Close"])
                        if len(sd) < 60:
                            continue

                        sd  = add_indicators(sd)
                        ls  = sd.iloc[-1]
                        ps  = sd.iloc[-2]
                        sig = get_signal(sd)
                        cp  = float(ls["Close"])
                        chg = (cp - float(ps["Close"])) / float(ps["Close"]) * 100
                        atr = float(ls["ATR_14"]) if pd.notna(ls.get("ATR_14")) else cp * 0.02
                        sl  = cp - atr * 1.5
                        tp  = cp + atr * 1.5 * risk_reward
                        qty = max(1, int(allocated_capital * (risk_per_trade / 100) / (atr * 1.5)))
                        rsi_v = float(ls["RSI_14"]) if pd.notna(ls.get("RSI_14")) else 50.0
                        stre = get_signal_strength(sd)
                        results.append({
                            "Stock": name, "Ticker": ticker_s.replace(".NS",""),
                            "Price": f"₹{cp:,.2f}", "1D%": f"{chg:+.2f}",
                            "RSI": f"{rsi_v:.1f}", "Signal": sig, "Strength": stre,
                            "SL": f"₹{sl:,.2f}", "Target": f"₹{tp:,.2f}", "Qty": qty,
                            "_sig": sig, "_chg": chg, "_str": stre
                        })
                    except Exception:
                        continue
                    prog.progress(0.5 + 0.5 * (idx + 1) / len(pool),
                                  text=f"Processing {idx + 1}/{len(pool)} stocks...")

            except Exception as e:
                st.warning(f"Batch download issue: {e} — try reducing the stock count.")

            prog.empty()
            if results:
                st.session_state["scan_results"] = results
                st.success(f"✅ Scan complete — {len(results)} stocks processed.")

    if st.session_state.get("scan_results"):
        res  = st.session_state["scan_results"]
        filt = st.radio("Filter", ["All", "BUY", "SELL", "HOLD", "High Strength (>=65)"], horizontal=True)
        rdf  = pd.DataFrame(res)
        if filt == "BUY":
            rdf = rdf[rdf["_sig"] == "BUY"]
        elif filt == "SELL":
            rdf = rdf[rdf["_sig"] == "SELL"]
        elif filt == "HOLD":
            rdf = rdf[rdf["_sig"] == "HOLD"]
        elif "High" in filt:
            rdf = rdf[rdf["_str"] >= 65]
        disp = rdf.drop(columns=["_sig", "_chg", "_str"], errors="ignore")
        st.dataframe(disp, use_container_width=True, hide_index=True)
        b = (rdf["_sig"] == "BUY").sum()
        s = (rdf["_sig"] == "SELL").sum()
        h = (rdf["_sig"] == "HOLD").sum()
        total_sc = b + s + h
        breadth = round(b / total_sc * 100, 1) if total_sc > 0 else 0
        st.caption(f"{len(disp)} stocks | BUY {b} | SELL {s} | HOLD {h} | Breadth {breadth}% bullish")
    else:
        st.info("Click RUN SCAN to populate.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 5: RISK CALCULATOR
# ─────────────────────────────────────────────────────────────────────────────
with tab_risk:
    st.markdown(f'<p class="section-header">[ RISK CALCULATOR — {selected_name} ]</p>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1:
        entry_px  = st.number_input("Entry Price", value=round(close, 2), step=1.0)
        stop_px   = st.number_input("Stop Loss",   value=round(sl_price, 2), step=1.0)
        target_px = st.number_input("Take Profit", value=round(tp_price, 2), step=1.0)
    with r2:
        cap2      = st.number_input("Capital", value=float(allocated_capital), step=1000.0)
        risk_pct2 = st.slider("Risk %", 0.5, 10.0, float(risk_per_trade), step=0.5)
        n_trades  = st.number_input("Simultaneous Trades", min_value=1, max_value=20, value=5)

    if entry_px > 0 and entry_px > stop_px > 0:
        rps   = entry_px - stop_px
        rws   = target_px - entry_px
        rr    = rws / rps if rps > 0 else 0
        car   = cap2 * (risk_pct2 / 100)
        qty_c = max(1, int(car / rps))
        tv    = qty_c * entry_px
        ml    = qty_c * rps
        mg    = qty_c * rws

        rc1, rc2, rc3, rc4 = st.columns(4)
        for col, lbl, val, clr in zip(
            [rc1, rc2, rc3, rc4],
            ["Qty to Buy", "Total Value", "Max Loss", "Max Gain"],
            [str(qty_c), f"Rs{tv:,.0f}", f"Rs{ml:,.0f}", f"Rs{mg:,.0f}"],
            ["#00c8ff", "#ddeeff", "#ff3355", "#00e87a"]
        ):
            col.markdown(
                f'<div class="glass-card"><p class="glass-label">{lbl}</p>'
                f'<div class="glass-value" style="color:{clr};font-size:1rem;">{val}</div></div>',
                unsafe_allow_html=True
            )
        rr_clr = "#00e87a" if rr >= 2 else "#ffcc00" if rr >= 1 else "#ff3355"
        st.markdown(
            f'<div class="glass-card" style="text-align:center;"><p class="glass-label">Risk:Reward</p>'
            f'<div class="glass-value" style="color:{rr_clr};">1 : {rr:.2f}</div>'
            f'<p style="font-size:10px;color:#6a90aa;margin:3px 0 0;">Portfolio risk at {n_trades} trades: Rs{ml * n_trades:,.0f}</p></div>',
            unsafe_allow_html=True
        )
    else:
        st.warning("Stop loss must be below entry price.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 6: PORTFOLIO OPTIMIZER & CUSTOM PORTFOLIO ROTATION ADVISOR
# ─────────────────────────────────────────────────────────────────────────────
with tab_port:
    # ── SUBSECTION 1: CUSTOM PORTFOLIO TRACKER & ROTATION ADVISOR ────────────
    st.markdown('<p class="section-header">[ 💼 MY CUSTOM PORTFOLIO TRACKER & ROTATION ADVISOR ]</p>', unsafe_allow_html=True)
    st.caption("Enter your custom portfolio details below to project 1-year returns and receive rotation optimization advice.")

    # Initialize session state for custom portfolio
    if "custom_portfolio" not in st.session_state:
        st.session_state["custom_portfolio"] = pd.DataFrame([
            {"Ticker": "RELIANCE", "Quantity": 10, "Buy Price (₹)": 2400.0},
            {"Ticker": "TCS", "Quantity": 5, "Buy Price (₹)": 3800.0},
            {"Ticker": "HDFCBANK", "Quantity": 15, "Buy Price (₹)": 1500.0}
        ])

    edited_portfolio = st.data_editor(
        st.session_state["custom_portfolio"],
        num_rows="dynamic",
        column_config={
            "Ticker": st.column_config.TextColumn("Stock Symbol", help="e.g. RELIANCE, TCS, SBIN", required=True),
            "Quantity": st.column_config.NumberColumn("Quantity", min_value=1, step=1, required=True),
            "Buy Price (₹)": st.column_config.NumberColumn("Buy Price (₹)", min_value=0.0, step=10.0, required=True)
        },
        use_container_width=True,
        key="portfolio_editor"
    )
    st.session_state["custom_portfolio"] = edited_portfolio

    # Process Portfolio Analysis
    if not edited_portfolio.empty:
        valid_rows = edited_portfolio.dropna(subset=["Ticker", "Quantity", "Buy Price (₹)"])
        if not valid_rows.empty:
            port_tickers_list = []
            peer_tickers_map = {}
            all_tickers_to_fetch = set()

            for _, row in valid_rows.iterrows():
                sym_resolved = resolve_ticker(str(row["Ticker"]))
                port_tickers_list.append((str(row["Ticker"]), sym_resolved, int(row["Quantity"]), float(row["Buy Price (₹)"])))
                all_tickers_to_fetch.add(sym_resolved)

                # Get 2 peers from its sector
                sector, peers = get_sector_peers(sym_resolved, max_peers=2)
                if sector:
                    peer_tickers_map[sym_resolved] = (sector, peers)
                    for p in peers:
                        all_tickers_to_fetch.add(p)

            # Download all in one single batch
            with st.spinner("Downloading portfolio and sector peer market data..."):
                try:
                    batch_port_df = yf.download(
                        list(all_tickers_to_fetch), period="2y", interval="1d",
                        auto_adjust=True, progress=False, timeout=25, group_by="ticker"
                    )

                    def get_ticker_df(ticker_sym):
                        if isinstance(batch_port_df.columns, pd.MultiIndex):
                            if ticker_sym in batch_port_df.columns.get_level_values(0):
                                return batch_port_df[ticker_sym].dropna()
                            elif ticker_sym in batch_port_df.columns.get_level_values(1):
                                return batch_port_df.xs(ticker_sym, axis=1, level=1).dropna()
                        else:
                            return batch_port_df.dropna()
                        return None

                    # Forecast peer tickers to construct peer data database
                    peer_info_db = {}
                    for holding_sym, (sector, peers) in peer_tickers_map.items():
                        if sector not in peer_info_db:
                            peer_info_db[sector] = {}
                        for peer in peers:
                            try:
                                pdf = get_ticker_df(peer)
                                if pdf is not None and len(pdf) >= 50:
                                    current_p = float(pdf["Close"].iloc[-1])
                                    prices_s = pdf["Close"].astype(float)
                                    log_s = np.log(prices_s)
                                    arima_m = ARIMA(log_s, order=(1,1,1)).fit()
                                    fc_arima = np.exp(arima_m.forecast(steps=252).iloc[-1])
                                    fc_hw = run_holt_winters(prices_s, steps=252).iloc[-1]
                                    proj_p = (fc_arima + fc_hw) / 2
                                    proj_ret_pct = (proj_p - current_p) / current_p * 100

                                    pdf_ind = add_indicators(pdf.reset_index())
                                    sig = get_signal(pdf_ind)
                                    stre = get_signal_strength(pdf_ind)

                                    peer_info_db[sector][peer] = {
                                        "_proj_return_pct": proj_ret_pct,
                                        "_tech_sig": sig,
                                        "_strength": stre
                                    }
                            except Exception:
                                continue

                    # Analyze custom portfolio holdings
                    analyzed_rows = []
                    total_cost_basis = 0.0
                    total_current_value = 0.0
                    total_proj_value_1y = 0.0

                    for label_t, sym_resolved, qty, buy_px in port_tickers_list:
                        try:
                            hdf = get_ticker_df(sym_resolved)
                            if hdf is not None and len(hdf) >= 40:
                                current_p = float(hdf["Close"].iloc[-1])
                                cost = qty * buy_px
                                curr_val = qty * current_p

                                # 1Y projections
                                prices_s = hdf["Close"].astype(float)
                                log_s = np.log(prices_s)
                                arima_m = ARIMA(log_s, order=(1,1,1)).fit()
                                fc_arima = np.exp(arima_m.forecast(steps=252).iloc[-1])
                                fc_hw = run_holt_winters(prices_s, steps=252).iloc[-1]
                                proj_p = (fc_arima + fc_hw) / 2
                                proj_val_1y = qty * proj_p

                                pnl_curr = curr_val - cost
                                pnl_proj_1y = proj_val_1y - curr_val
                                proj_ret_pct = (proj_p - current_p) / current_p * 100

                                total_cost_basis += cost
                                total_current_value += curr_val
                                total_proj_value_1y += proj_val_1y

                                hdf_ind = add_indicators(hdf.reset_index())
                                sig = get_signal(hdf_ind)
                                stre = get_signal_strength(hdf_ind)

                                # Determine sector
                                sector = None
                                if sym_resolved in peer_tickers_map:
                                    sector = peer_tickers_map[sym_resolved][0]
                                if not sector:
                                    clean = sym_resolved.replace(".NS","").replace(".BO","").upper()
                                    for sec, list_of_stocks in SECTORS.items():
                                        if any(sym == clean for _, sym in list_of_stocks):
                                            sector = sec
                                            break

                                verdict = "⚪ HOLD"
                                advice = "Hold. Ratios and technical readings are stable."
                                v_clr = "#ffcc00"

                                # Rotation Logic
                                if sig == "SELL" or proj_ret_pct < 5.0 or stre < 40:
                                    verdict = "🔴 ROTATE"
                                    v_clr = "#ff3355"
                                    # Look for sector peer
                                    better_peer = None
                                    best_peer_ret = proj_ret_pct
                                    if sector and sector in peer_info_db:
                                        for peer_sym, p_info in peer_info_db[sector].items():
                                            if peer_sym != sym_resolved and p_info["_proj_return_pct"] > best_peer_ret + 5.0:
                                                better_peer = peer_sym.replace(".NS","").replace(".BO","")
                                                best_peer_ret = p_info["_proj_return_pct"]
                                    
                                    if better_peer:
                                        advice = f"Consider rotating into **{better_peer}** (Sector: {sector}). It has a stronger signal and projected 1Y return of {best_peer_ret:.1f}% (+{best_peer_ret - proj_ret_pct:.1f}% uplift)."
                                    else:
                                        sc_results = st.session_state.get("scan_results")
                                        market_alt = None
                                        if sc_results:
                                            buys = [s for s in sc_results if s["_sig"] == "BUY" and s["_str"] >= 70]
                                            if buys:
                                                buys_sorted = sorted(buys, key=lambda x: x["_str"], reverse=True)
                                                market_alt = buys_sorted[0]["Ticker"]
                                        if market_alt:
                                            advice = f"Projected 1Y return is weak ({proj_ret_pct:.1f}%). Suggest rotating into market leader **{market_alt}** (Strength: {buys_sorted[0]['_str']}/100)."
                                        else:
                                            advice = f"Projected 1Y return is weak ({proj_ret_pct:.1f}%). Reallocate to cash or market leaders."
                                elif sig == "BUY" and stre >= 65:
                                    verdict = "🟢 ACCUMULATE"
                                    v_clr = "#00e87a"
                                    advice = f"Strong buy momentum (Strength: {stre}/100) and projected 1Y return of {proj_ret_pct:.1f}%."
                                else:
                                    verdict = "⚪ HOLD"
                                    v_clr = "#ffcc00"
                                    advice = f"Neutral technicals. Projected 1Y return: {proj_ret_pct:.1f}%."

                                analyzed_rows.append({
                                    "Stock": label_t.upper(),
                                    "Qty": qty,
                                    "Buy Price": f"₹{buy_px:,.2f}",
                                    "Current Price": f"₹{current_p:,.2f}",
                                    "Current Value": f"₹{curr_val:,.2f}",
                                    "P&L": f"₹{pnl_curr:,.2f}",
                                    "Projected 1Y Value": f"₹{proj_val_1y:,.2f}",
                                    "Proj. 1Y %": f"{proj_ret_pct:+.1f}%",
                                    "Advice": verdict,
                                    "_adv_text": advice,
                                    "_color": v_clr,
                                    "_pnl": pnl_curr
                                })
                            else:
                                analyzed_rows.append({
                                    "Stock": label_t.upper(), "Qty": qty, "Buy Price": f"₹{buy_px:,.2f}",
                                    "Current Price": "N/A", "Current Value": "N/A", "P&L": "₹0.00",
                                    "Projected 1Y Value": "N/A", "Proj. 1Y %": "0.0%",
                                    "Advice": "⚪ HOLD", "_adv_text": "Could not retrieve historical data.", "_color": "#ffcc00", "_pnl": 0.0
                                })
                        except Exception as e:
                            st.warning(f"Error analyzing {label_t}: {e}")

                    # Display custom portfolio KPIs
                    total_pnl = total_current_value - total_cost_basis
                    total_proj_pnl = total_proj_value_1y - total_current_value
                    total_proj_return_pct = (total_proj_value_1y - total_current_value) / total_current_value * 100 if total_current_value > 0 else 0.0

                    pk1, pk2, pk3, pk4 = st.columns(4)
                    pk1.markdown(f'<div class="glass-card"><p class="glass-label">Total Cost Basis</p><div class="glass-value">₹{total_cost_basis:,.2f}</div></div>', unsafe_allow_html=True)
                    pk2.markdown(f'<div class="glass-card"><p class="glass-label">Current Value</p><div class="glass-value" style="color:#00c8ff;">₹{total_current_value:,.2f}</div></div>', unsafe_allow_html=True)
                    pk3.markdown(f'<div class="glass-card"><p class="glass-label">Total Current P&L</p><div class="glass-value" style="color:{"#00e87a" if total_pnl>=0 else "#ff3355"};">₹{total_pnl:,.2f} ({"+" if total_pnl>=0 else ""}{total_pnl/total_cost_basis*100:.2f}% if total_cost_basis>0 else 0)</div></div>', unsafe_allow_html=True)
                    pk4.markdown(f'<div class="glass-card"><p class="glass-label">Projected 1Y Value</p><div class="glass-value" style="color:#00e87a;">₹{total_proj_value_1y:,.2f} ({total_proj_return_pct:+.1f}%)</div></div>', unsafe_allow_html=True)

                    # Show details table
                    disp_df = pd.DataFrame(analyzed_rows)
                    st.dataframe(
                        disp_df[["Stock", "Qty", "Buy Price", "Current Price", "Current Value", "P&L", "Projected 1Y Value", "Proj. 1Y %", "Advice"]],
                        use_container_width=True, hide_index=True
                    )

                    # Show advice detail cards
                    st.markdown('<p class="section-header">[ 🛡️ PORTFOLIO ROTATION ADVISORY DETAILS ]</p>', unsafe_allow_html=True)
                    for item in analyzed_rows:
                        st.markdown(f"""
<div class="glass-card" style="border-left: 4px solid {item['_color']}; padding: 10px 14px; margin-bottom: 8px;">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <span style="font-family:'Orbitron',sans-serif; font-weight:700; color:#ddeeff; font-size:13px;">{item['Stock']}</span>
        <span style="font-family:'Space Mono',monospace; font-size:11px; font-weight:bold; color:{item['_color']};">{item['Advice']}</span>
    </div>
    <div style="font-size:12px; color:#a0aec0; margin-top:5px; line-height:1.5;">
        {item['_adv_text']}
    </div>
</div>
""", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"Error during portfolio analysis run: {e}")

    st.markdown("<br><hr style='border-color:rgba(0,200,255,0.08);'><br>", unsafe_allow_html=True)

    # ── SUBSECTION 2: MPT PORTFOLIO OPTIMIZER (MONTE CARLO) ──────────────────
    st.markdown('<p class="section-header">[ 💼 MPT PORTFOLIO OPTIMIZER — MONTE CARLO 3000 ]</p>', unsafe_allow_html=True)
    default_keys = [k for k in ALL_STOCKS if any(x in k for x in ["Reliance (", "TCS (", "HDFC Bank (", "Infosys (", "SBI ("])][:5]
    sel_keys = st.multiselect("Select 2-10 assets for optimization", list(ALL_STOCKS.keys()), default=default_keys)

    if len(sel_keys) < 2:
        st.warning("Select at least 2 assets.")
    else:
        opt_tickers = [ALL_STOCKS[k] for k in sel_keys]
        opt_names   = [k.split(" (")[0] for k in sel_keys]

        with st.spinner("Downloading returns + Monte Carlo simulation..."):
            try:
                dp = yf.download(opt_tickers, period="2y", interval="1d", auto_adjust=True, progress=False)
                if dp is not None and not dp.empty:
                    if isinstance(dp.columns, pd.MultiIndex):
                        lvls = dp.columns.get_level_values(0).unique().tolist()
                        if "Close" in lvls:
                            close_df = dp["Close"]
                        else:
                            close_df = dp.xs("Close", axis=1, level=1)
                    else:
                        close_df = dp[["Close"]] if "Close" in dp.columns else dp

                    ret_df = close_df.pct_change().dropna()
                    na     = len(opt_tickers)
                    mu_r   = ret_df.mean()
                    cov    = ret_df.cov()
                    N      = 3000
                    vols, rets, sharpes, all_w = [], [], [], []

                    for _ in range(N):
                        w  = np.random.dirichlet(np.ones(na))
                        pr = float(np.dot(mu_r, w)) * 252
                        pv = float(np.sqrt(w @ (cov.values * 252) @ w))
                        ps = pr / pv if pv > 0 else 0
                        vols.append(pv); rets.append(pr); sharpes.append(ps); all_w.append(w)

                    max_sh_i = int(np.argmax(sharpes))
                    min_vl_i = int(np.argmin(vols))
                    obj = st.radio("Objective", ["Maximize Sharpe Ratio", "Minimize Volatility"], horizontal=True)
                    idx_sel = max_sh_i if "Sharpe" in obj else min_vl_i
                    opt_w = all_w[idx_sel]
                    sel_v = vols[idx_sel]; sel_r = rets[idx_sel]; sel_s = sharpes[idx_sel]

                    pm1, pm2, pm3 = st.columns(3)
                    pm1.markdown(f'<div class="glass-card"><p class="glass-label">Expected Annual Return</p><div class="glass-value" style="color:#00e87a;">{sel_r:.1%}</div></div>', unsafe_allow_html=True)
                    pm2.markdown(f'<div class="glass-card"><p class="glass-label">Annual Volatility</p><div class="glass-value" style="color:#ff3355;">{sel_v:.1%}</div></div>', unsafe_allow_html=True)
                    pm3.markdown(f'<div class="glass-card"><p class="glass-label">Sharpe Ratio</p><div class="glass-value" style="color:#00c8ff;">{sel_s:.2f}</div></div>', unsafe_allow_html=True)

                    st.markdown('<p class="section-header">[ CAPITAL ALLOCATION ]</p>', unsafe_allow_html=True)
                    colors_list = ["#00c8ff","#00e87a","#ffcc00","#ff6b35","#7c4dff","#ff3355","#fbbf24","#34d399","#a78bfa","#fb923c"]
                    alloc_cols = st.columns(min(len(opt_names), 5))
                    for i, (name, w) in enumerate(zip(opt_names, opt_w)):
                        amt = allocated_capital * w
                        clr = colors_list[i % len(colors_list)]
                        alloc_cols[i % min(len(opt_names), 5)].markdown(
                            f'<div class="glass-card" style="text-align:center;">'
                            f'<p class="glass-label">{name[:14]}</p>'
                            f'<div class="glass-value" style="color:{clr};font-size:.95rem;">Rs{amt:,.0f}</div>'
                            f'<p style="font-size:10px;color:#6a90aa;margin:3px 0 0;">{w:.1%}</p></div>',
                            unsafe_allow_html=True
                        )

                    pc1, pc2 = st.columns(2)
                    with pc1:
                        fig_pie = go.Figure(data=[go.Pie(
                            labels=opt_names, values=opt_w, hole=0.42,
                            marker=dict(colors=colors_list[:len(opt_names)]),
                            textfont=dict(color="#ddeeff")
                        )])
                        fig_pie.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#ddeeff", family="Space Mono", size=10),
                            margin=dict(l=10, r=10, t=10, b=10))
                        st.plotly_chart(fig_pie, use_container_width=True)
                    with pc2:
                        fig_ef = go.Figure()
                        fig_ef.add_trace(go.Scatter(x=vols, y=rets, mode="markers",
                            marker=dict(color=sharpes, colorscale="Viridis", size=3, showscale=True,
                                        colorbar=dict(title="Sharpe", thickness=12,
                                                      titlefont=dict(color="#ddeeff", size=9),
                                                      tickfont=dict(color="#ddeeff", size=8))),
                            name="Portfolios"))
                        fig_ef.add_trace(go.Scatter(x=[sel_v], y=[sel_r], mode="markers",
                            marker=dict(color="#ff3355", size=14, symbol="star",
                                        line=dict(width=1, color="white")), name="Optimal"))
                        fig_ef.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(color="#ddeeff", family="Space Mono", size=10),
                            xaxis=dict(title="Volatility", gridcolor="rgba(0,200,255,0.04)", tickformat=".1%"),
                            yaxis=dict(title="Return",     gridcolor="rgba(0,200,255,0.04)", tickformat=".1%"),
                            margin=dict(l=10, r=10, t=10, b=10),
                            legend=dict(bgcolor="rgba(7,18,32,0.5)", font=dict(size=9)))
                        st.plotly_chart(fig_ef, use_container_width=True)
                else:
                    st.error("Failed to load data.")
            except Exception as e:
                st.error(f"Portfolio error: {e}")


# ─────────────────────────────────────────────────────────────────────────────
# TAB: FII / DII FLOWS
# ─────────────────────────────────────────────────────────────────────────────
with tab_fii:
    st.markdown('<p class="section-header">[ 📊 FII / DII INSTITUTIONAL FLOW — NSE INDIA ]</p>', unsafe_allow_html=True)
    st.caption("Foreign Institutional Investor & Domestic Institutional Investor daily net activity. Source: NSE India.")

    with st.spinner("Fetching FII/DII data from NSE India..."):
        fii_data = fetch_fii_dii()
        df_fii, today_fii = parse_fii_dii(fii_data)

    if df_fii is not None and today_fii is not None:
        fii_net = float(today_fii["FII Net"])
        dii_net = float(today_fii["DII Net"])
        fii_clr = "#00e87a" if fii_net >= 0 else "#ff3355"
        dii_clr = "#00e87a" if dii_net >= 0 else "#ff3355"
        combined = fii_net + dii_net
        comb_clr = "#00e87a" if combined >= 0 else "#ff3355"

        f1, f2, f3, f4 = st.columns(4)
        for col, lbl, val, clr in zip([f1,f2,f3,f4],
            ["FII Net Today (Cr)", "DII Net Today (Cr)", "Combined Net (Cr)", "Date"],
            [f"{'▲' if fii_net>=0 else '▼'} ₹{abs(fii_net):,.0f}",
             f"{'▲' if dii_net>=0 else '▼'} ₹{abs(dii_net):,.0f}",
             f"{'▲' if combined>=0 else '▼'} ₹{abs(combined):,.0f}",
             str(today_fii["Date"])[:10]],
            [fii_clr, dii_clr, comb_clr, "#ddeeff"]):
            col.markdown(f'<div class="glass-card"><p class="glass-label">{lbl}</p>'
                         f'<div class="glass-value" style="color:{clr};font-size:1.1rem;">{val}</div></div>',
                         unsafe_allow_html=True)

        sentiment_fii = "BULLISH" if fii_net > 0 else "BEARISH"
        sent_clr_fii  = "#00e87a" if fii_net > 0 else "#ff3355"
        if fii_net > 0 and dii_net > 0:
            market_view = "Both FII and DII are buying — strong institutional conviction. Typically bullish for markets."
        elif fii_net > 0 and dii_net < 0:
            market_view = "FII buying, DII selling — foreign money flowing in, domestic institutions taking profit."
        elif fii_net < 0 and dii_net > 0:
            market_view = "FII selling, DII buying — domestic institutions absorbing foreign outflows. Market resilient."
        else:
            market_view = "Both FII and DII selling — broad institutional outflow. Typically bearish for near-term."

        st.markdown(f'''<div class="glass-card" style="margin:10px 0;">
            <p class="glass-label">Market Interpretation</p>
            <div style="font-size:13px;color:{sent_clr_fii};font-weight:600;margin:4px 0;">{sentiment_fii} INSTITUTIONAL FLOW</div>
            <p style="font-size:12px;color:#a0aec0;margin:4px 0;line-height:1.6;">{market_view}</p>
        </div>''', unsafe_allow_html=True)

        if len(df_fii) > 1:
            st.markdown('<p class="section-header">[ RECENT FII / DII DAILY NET FLOWS ]</p>', unsafe_allow_html=True)
            fig_fii = go.Figure()
            fii_colors = ["#00e87a" if v >= 0 else "#ff3355" for v in df_fii["FII Net"]]
            dii_colors = ["#00c8ff" if v >= 0 else "#ff6b35" for v in df_fii["DII Net"]]
            fig_fii.add_trace(go.Bar(x=df_fii["Date"], y=df_fii["FII Net"], name="FII Net",
                marker_color=fii_colors, opacity=0.85))
            fig_fii.add_trace(go.Bar(x=df_fii["Date"], y=df_fii["DII Net"], name="DII Net",
                marker_color=dii_colors, opacity=0.85))
            fig_fii.add_hline(y=0, line_color="rgba(255,255,255,0.2)", line_width=1)
            fig_fii.update_layout(
                height=320, barmode="group",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ddeeff", family="Space Mono", size=10),
                xaxis=dict(gridcolor="rgba(0,200,255,0.04)"),
                yaxis=dict(gridcolor="rgba(0,200,255,0.04)", title="Net Flow (Cr ₹)"),
                margin=dict(l=10,r=10,t=15,b=10),
                legend=dict(bgcolor="rgba(7,18,32,0.5)", bordercolor="rgba(0,200,255,0.15)", borderwidth=1)
            )
            st.plotly_chart(fig_fii, use_container_width=True)

        st.markdown('<p class="section-header">[ DETAILED FLOW TABLE ]</p>', unsafe_allow_html=True)
        disp_fii = df_fii[["Date","FII Buy","FII Sell","FII Net","DII Buy","DII Sell","DII Net"]].copy()
        disp_fii = disp_fii.round(2)
        st.dataframe(disp_fii, use_container_width=True, hide_index=True)
        st.download_button("⬇️ Download FII/DII Data",
                           disp_fii.to_csv(index=False).encode(),
                           "fii_dii_flows.csv", "text/csv")
    else:
        st.warning("Could not fetch FII/DII data from NSE India. NSE may be blocking automated requests.")
        st.info("**Why this happens:** NSE India requires cookie-based session authentication. The data is available at nseindia.com → Market Data → FII/DII Activity.")
        st.markdown('''<div class="glass-card">
            <p class="section-header" style="margin-top:0;">Understanding FII / DII Flows</p>
            <div style="font-size:12px;color:#a0aec0;line-height:1.8;">
            <b style="color:#00c8ff;">FII (Foreign Institutional Investors)</b> — Foreign funds, hedge funds, sovereign wealth funds. 
            Their buying/selling drives large directional moves in Nifty 50. FII net positive = bullish signal.<br><br>
            <b style="color:#00c8ff;">DII (Domestic Institutional Investors)</b> — Indian mutual funds, insurance companies (LIC), banks. 
            Often act as a counterbalance — they buy when FIIs sell, providing market support.<br><br>
            <b style="color:#ffcc00;">Key Rule:</b> When both FII and DII are net buyers, markets tend to rally strongly. 
            When both are sellers, expect sharp corrections. FII flows dominate short-term direction.
            </div>
        </div>''', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB: OPTIONS CHAIN
# ─────────────────────────────────────────────────────────────────────────────
with tab_options:
    st.markdown(f'<p class="section-header">[ 🎯 OPTIONS CHAIN — {selected_name} ]</p>', unsafe_allow_html=True)
    st.caption("NSE India options data. Works for Nifty 50 stocks with active F&O contracts.")

    with st.spinner(f"Fetching options chain for {selected_name}..."):
        opt_data = fetch_options_chain(selected_ticker)
        df_chain, pcr, max_pain, expiry = parse_options_chain(opt_data, close)

    if df_chain is not None and len(df_chain) > 0:
        o1, o2, o3, o4 = st.columns(4)
        pcr_clr  = "#00e87a" if pcr and pcr > 1 else "#ff3355" if pcr and pcr < 0.7 else "#ffcc00"
        pain_clr = "#00c8ff"
        updown   = "Above" if close > (max_pain or close) else "Below"
        pct_from_pain = abs(close - max_pain) / max_pain * 100 if max_pain else 0

        for col, lbl, val, clr in zip([o1,o2,o3,o4],
            ["Spot Price","Max Pain","Put/Call Ratio","Expiry"],
            [f"₹{close:,.2f}", f"₹{max_pain:,.0f}" if max_pain else "N/A",
             f"{pcr:.3f}" if pcr else "N/A", str(expiry) if expiry else "N/A"],
            ["#ddeeff", pain_clr, pcr_clr, "#6a90aa"]):
            col.markdown(f'<div class="glass-card"><p class="glass-label">{lbl}</p>'
                         f'<div class="glass-value" style="color:{clr};font-size:1.1rem;">{val}</div></div>',
                         unsafe_allow_html=True)

        if pcr:
            if pcr > 1.2:
                pcr_interp = "HIGH PCR (>1.2) — Bearish sentiment dominant. Contrarian signal: markets may be oversold, potential reversal up."
                pi_clr = "#00e87a"
            elif pcr < 0.7:
                pcr_interp = "LOW PCR (<0.7) — Bullish sentiment dominant. Contrarian signal: markets may be overbought, potential pullback."
                pi_clr = "#ff3355"
            else:
                pcr_interp = "NEUTRAL PCR (0.7–1.2) — Balanced put/call activity. No extreme sentiment reading."
                pi_clr = "#ffcc00"
            st.markdown(f'<div class="glass-card"><p class="glass-label">PCR Interpretation</p>'
                        f'<p style="font-size:12px;color:{pi_clr};margin:4px 0;font-weight:600;">{pcr_interp}</p></div>',
                        unsafe_allow_html=True)

        if max_pain:
            mp_interp = f"Spot (₹{close:,.0f}) is {updown} max pain (₹{max_pain:,.0f}) by {pct_from_pain:.1f}%. Option sellers profit most if expiry is at ₹{max_pain:,.0f}. Gravitational pull toward max pain as expiry approaches."
            st.markdown(f'<div class="glass-card"><p class="glass-label">Max Pain Analysis</p>'
                        f'<p style="font-size:12px;color:#a0aec0;margin:4px 0;line-height:1.6;">{mp_interp}</p></div>',
                        unsafe_allow_html=True)

        st.markdown('<p class="section-header">[ OPEN INTEREST BY STRIKE ]</p>', unsafe_allow_html=True)
        spot_strikes = df_chain[(df_chain["Strike"] >= close * 0.85) & (df_chain["Strike"] <= close * 1.15)]
        if len(spot_strikes) > 0:
            fig_oi = go.Figure()
            fig_oi.add_trace(go.Bar(x=spot_strikes["Strike"], y=spot_strikes["CE OI"],
                name="Call OI", marker_color="rgba(255,51,85,0.7)"))
            fig_oi.add_trace(go.Bar(x=spot_strikes["Strike"], y=spot_strikes["PE OI"],
                name="Put OI", marker_color="rgba(0,200,255,0.7)"))
            if max_pain:
                fig_oi.add_vline(x=max_pain, line_dash="dash", line_color="#fbbf24",
                    annotation_text=f"Max Pain ₹{max_pain:,.0f}", annotation_font_color="#fbbf24")
            fig_oi.add_vline(x=close, line_dash="dot", line_color="rgba(255,255,255,0.5)",
                annotation_text=f"Spot ₹{close:,.0f}", annotation_font_color="#ddeeff")
            fig_oi.update_layout(
                height=360, barmode="group",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ddeeff", family="Space Mono", size=10),
                xaxis=dict(title="Strike Price", gridcolor="rgba(0,200,255,0.04)"),
                yaxis=dict(title="Open Interest", gridcolor="rgba(0,200,255,0.04)"),
                margin=dict(l=10,r=10,t=15,b=10),
                legend=dict(bgcolor="rgba(7,18,32,0.5)", bordercolor="rgba(0,200,255,0.15)", borderwidth=1)
            )
            st.plotly_chart(fig_oi, use_container_width=True)

        st.markdown('<p class="section-header">[ FULL OPTIONS CHAIN TABLE ]</p>', unsafe_allow_html=True)
        chain_disp = df_chain[["CE LTP","CE OI","CE IV","Strike","PE IV","PE OI","PE LTP"]].copy()
        chain_disp["ATM"] = df_chain["Strike"].apply(lambda s: "◀ ATM" if abs(s - close) == df_chain["Strike"].apply(lambda x: abs(x-close)).min() else "")
        st.dataframe(chain_disp.round(2), use_container_width=True, hide_index=True)
        st.download_button("⬇️ Download Options Chain",
                           chain_disp.round(2).to_csv(index=False).encode(),
                           f"{selected_name}_options_chain.csv", "text/csv")
    else:
        st.warning(f"Options chain not available for {selected_name}.")
        st.info("Options data is available only for stocks in the NSE F&O segment (Nifty 50 and select mid-caps). NSE may also block automated access.")
        st.markdown('''<div class="glass-card">
            <p class="section-header" style="margin-top:0;">Options Chain Concepts</p>
            <div style="font-size:12px;color:#a0aec0;line-height:1.8;">
            <b style="color:#00c8ff;">Max Pain</b> — The strike price where option buyers lose the most money at expiry. 
            Due to gamma exposure, stock prices tend to gravitate toward max pain as expiry approaches.<br><br>
            <b style="color:#00c8ff;">Put/Call Ratio (PCR)</b> — Total Put OI divided by Total Call OI. 
            PCR > 1.2 = bearish sentiment (contrarian buy signal). PCR < 0.7 = bullish sentiment (contrarian sell signal).<br><br>
            <b style="color:#00c8ff;">Open Interest (OI)</b> — Number of outstanding contracts. High OI at a strike = strong support/resistance level.<br><br>
            <b style="color:#00c8ff;">Implied Volatility (IV)</b> — Market expectation of future price movement. High IV = expensive options = expected big move.
            </div>
        </div>''', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB: FUNDAMENTALS
# ─────────────────────────────────────────────────────────────────────────────
with tab_funds:
    st.markdown(f'<p class="section-header">[ 📋 FUNDAMENTAL ANALYSIS — {selected_name} ]</p>', unsafe_allow_html=True)
    st.caption("Key financial ratios from Screener.in. Refreshed daily.")

    with st.spinner(f"Fetching fundamentals for {selected_name}..."):
        fund_data, fund_url = fetch_fundamentals(selected_ticker)

    if fund_data and any(v is not None for v in fund_data.values()):
        cols_f = st.columns(3)
        ratio_keys = [("P/E Ratio","#00c8ff"),("P/B Ratio","#ffcc00"),("ROE (%)","#00e87a"),
                      ("ROCE (%)","#00e87a"),("Debt/Equity","#ff3355"),("Div Yield (%)","#7c4dff")]
        for i, (key, clr) in enumerate(ratio_keys):
            val = fund_data.get(key)
            val_str = f"{val:.2f}" if val is not None else "N/A"
            cols_f[i % 3].markdown(
                f'<div class="glass-card"><p class="glass-label">{key}</p>'
                f'<div class="glass-value" style="color:{clr};">{val_str}</div></div>',
                unsafe_allow_html=True
            )

        ep1, ep2 = st.columns(2)
        eps  = fund_data.get("EPS (TTM)")
        prom = fund_data.get("Promoter Holding")
        ep1.markdown(
            f'<div class="glass-card"><p class="glass-label">EPS (TTM)</p>'
            f'<div class="glass-value" style="color:#fbbf24;">{"₹"+str(round(eps,2)) if eps else "N/A"}</div></div>',
            unsafe_allow_html=True)
        ep2.markdown(
            f'<div class="glass-card"><p class="glass-label">Promoter Holding</p>'
            f'<div class="glass-value" style="color:{"#00e87a" if prom and prom>50 else "#ffcc00" if prom else "#6a90aa"};">{""+str(round(prom,1))+"%" if prom else "N/A"}</div></div>',
            unsafe_allow_html=True)

        pe  = fund_data.get("P/E Ratio")
        roe = fund_data.get("ROE (%)")
        de  = fund_data.get("Debt/Equity")
        scores = []
        if pe:  scores.append("Cheap" if pe < 15 else "Fair" if pe < 30 else "Expensive")
        if roe: scores.append("High ROE" if roe > 20 else "Moderate ROE" if roe > 12 else "Low ROE")
        if de:  scores.append("Low Debt" if de < 0.5 else "Moderate Debt" if de < 1.5 else "High Debt")
        if scores:
            verdict_text = " | ".join(scores)
            verdict_clr  = "#00e87a" if "Cheap" in verdict_text or "High ROE" in verdict_text else "#ffcc00"
            st.markdown(f'<div class="glass-card"><p class="glass-label">Fundamental Verdict</p>'
                        f'<p style="font-size:13px;color:{verdict_clr};font-weight:600;margin:4px 0;">{verdict_text}</p></div>',
                        unsafe_allow_html=True)

        st.caption("Data source: Screener.in · Refreshed daily · Garbage/out-of-range values are filtered")
        st.markdown(f"[View full analysis on Screener.in]({fund_url})")
    else:
        st.warning(f"Could not fetch fundamental data for {selected_name} from Screener.in.")
        st.info("Screener.in covers most NSE-listed companies. Try large-cap stocks like RELIANCE, TCS, HDFCBANK.")

    with st.expander("📖 Ratio interpretation guide"):
        st.markdown("""
| Ratio | Good | Average | Expensive/Risky |
|---|---|---|---|
| P/E | < 15 | 15–30 | > 40 |
| P/B | < 1.5 | 1.5–4 | > 6 |
| ROE | > 20% | 12–20% | < 10% |
| ROCE | > 20% | 12–20% | < 10% |
| Debt/Equity | < 0.5 | 0.5–1.5 | > 2.0 |
| Promoter Hold | > 50% | 35–50% | < 25% |

**Indian Market Context:** Nifty 50 trades at avg P/E of ~22. Premium growth stocks (Titan, Asian Paints) command 60–80x P/E. PSU banks trade at 5–10x. Always compare within the same sector.
""")

# ─────────────────────────────────────────────────────────────────────────────
# TAB: NEWS & SENTIMENT
# ─────────────────────────────────────────────────────────────────────────────
with tab_news:
    st.markdown(f'<p class="section-header">[ NEWS & SENTIMENT — {selected_name} ]</p>', unsafe_allow_html=True)
    with st.spinner("Fetching headlines..."):
        items = fetch_news(selected_ticker, selected_name)

    if items:
        score, cat = sentiment_score(items)
        sent_clr = {"BULLISH": "#00e87a", "BEARISH": "#ff3355", "NEUTRAL": "#ffcc00"}[cat]
        ns1, ns2 = st.columns([1, 2])
        with ns1:
            st.markdown(f"""<div class="glass-card" style="text-align:center;padding:20px 12px;">
                <p class="glass-label">Sentiment</p>
                <div style="font-family:'Orbitron',sans-serif;font-size:1.8rem;font-weight:900;color:{sent_clr};margin:8px 0;">{cat}</div>
                <p style="font-size:10px;color:#6a90aa;margin:0;">Score: {score:+.3f} | {len(items)} headlines</p>
            </div>""", unsafe_allow_html=True)
        with ns2:
            bull_cnt = sum(1 for it in items if any(w in it["title"].lower().split() for w in BULL_KW))
            bear_cnt = sum(1 for it in items if any(w in it["title"].lower().split() for w in BEAR_KW))
            st.markdown(f"""<div class="glass-card">
                <p class="glass-label" style="margin-bottom:8px;">Keyword Breakdown</p>
                <div style="font-family:'Space Mono',monospace;font-size:12px;">
                    Bullish headlines: <span style="color:#00e87a;font-weight:700;">{bull_cnt}</span> &nbsp;|&nbsp;
                    Bearish headlines: <span style="color:#ff3355;font-weight:700;">{bear_cnt}</span>
                </div>
                <p style="font-size:11px;color:#6a90aa;margin-top:6px;line-height:1.6;">
                Financial keyword scoring with negation detection. Bullish terms: surge, rally, beat, upgrade...
                Bearish terms: drop, warn, miss, downgrade, loss...
                </p>
            </div>""", unsafe_allow_html=True)

        st.markdown('<p class="section-header">[ HEADLINES ]</p>', unsafe_allow_html=True)
        for it in items:
            tl      = it["title"].lower()
            is_bull = any(w in tl.split() for w in BULL_KW)
            is_bear = any(w in tl.split() for w in BEAR_KW)
            dot_clr = "#00e87a" if (is_bull and not is_bear) else "#ff3355" if is_bear else "#6a90aa"
            st.markdown(f"""<div class="glass-card" style="padding:9px 13px;margin-bottom:5px;display:flex;align-items:center;gap:10px;">
                <div style="width:7px;height:7px;border-radius:50%;background:{dot_clr};flex-shrink:0;"></div>
                <a href="{it['link']}" target="_blank" style="color:#00c8ff;text-decoration:none;font-size:12px;font-weight:600;flex:1;">{it['title']}</a>
                <span style="font-size:9px;color:#4a7090;font-family:'Space Mono';flex-shrink:0;">{it['date']}</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.info(f"No headlines found for {selected_ticker}.")
        st.caption("Large-cap stocks like TCS, RELIANCE, HDFCBANK have best news coverage.")

# ═════════════════════════════════════════════════════════════════════════════
# XERCES+ NEW TABS: HEATMAP / COMPARE / AI / JOURNAL / EXPORT
# ═════════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────────
# TAB: SECTOR HEATMAP
# ─────────────────────────────────────────────────────────────────────────────
with tab_heatmap:
    st.markdown('<p class="section-header">[ 🔥 SECTOR HEATMAP — 1-DAY PERFORMANCE ]</p>', unsafe_allow_html=True)
    st.caption("Average 1-day return across a sample of stocks in each sector. Refreshed every 30 minutes.")

    with st.spinner("Computing sector performance..."):
        _sec_df = xp.compute_sector_performance(SECTORS, max_per_sector=6)

    if _sec_df is not None and not _sec_df.empty:
        # Colored bar chart
        _colors = ["#00e87a" if v >= 0 else "#ff3355" for v in _sec_df["Avg 1D %"]]
        fig_h = go.Figure(go.Bar(
            x=_sec_df["Avg 1D %"], y=_sec_df["Sector"], orientation="h",
            marker_color=_colors, text=[f"{v:+.2f}%" for v in _sec_df["Avg 1D %"]],
            textposition="outside", textfont=dict(color="#ddeeff", size=11)
        ))
        fig_h.update_layout(
            height=max(360, 28 * len(_sec_df)), paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ddeeff", family="Space Mono", size=10),
            xaxis=dict(gridcolor="rgba(0,200,255,0.05)", ticksuffix="%", zerolinecolor="rgba(255,255,255,0.2)"),
            yaxis=dict(gridcolor="rgba(0,200,255,0.03)", autorange="reversed"),
            margin=dict(l=10, r=40, t=10, b=10),
        )
        st.plotly_chart(fig_h, use_container_width=True)
        st.markdown('<p class="section-header">[ SECTOR BREADTH TABLE ]</p>', unsafe_allow_html=True)
        st.dataframe(_sec_df, use_container_width=True, hide_index=True)

        _bull = int((_sec_df["Avg 1D %"] > 0).sum())
        _bear = int((_sec_df["Avg 1D %"] < 0).sum())
        _breadth = round(_bull / len(_sec_df) * 100, 1)
        _b_clr = "#00e87a" if _breadth > 60 else "#ff3355" if _breadth < 40 else "#ffcc00"
        st.markdown(
            f'<div class="glass-card"><p class="glass-label">Market Breadth</p>'
            f'<div class="glass-value" style="color:{_b_clr};font-size:1.5rem;">{_breadth}% Bullish</div>'
            f'<p style="font-size:11px;color:#6a90aa;margin-top:4px;">{_bull} sectors up · {_bear} sectors down · '
            f'Top: {_sec_df.iloc[0]["Sector"]} ({_sec_df.iloc[0]["Avg 1D %"]:+.2f}%) · '
            f'Bottom: {_sec_df.iloc[-1]["Sector"]} ({_sec_df.iloc[-1]["Avg 1D %"]:+.2f}%)</p></div>',
            unsafe_allow_html=True)
    else:
        st.warning("Could not compute sector heatmap. Try again in a moment.")

    st.markdown("---")
    st.markdown(f'<p class="section-header">[ ⏱️ INTRADAY (5-MIN) — {selected_name} ]</p>', unsafe_allow_html=True)
    _intra = xp.load_intraday(selected_ticker, interval="5m", period="5d")
    if _intra is not None and not _intra.empty:
        _tcol = "Datetime" if "Datetime" in _intra.columns else "Date"
        fig_i = go.Figure(go.Candlestick(
            x=_intra[_tcol], open=_intra["Open"], high=_intra["High"],
            low=_intra["Low"], close=_intra["Close"],
            increasing_line_color="#00e87a", decreasing_line_color="#ff3355",
            increasing_fillcolor="rgba(0,232,122,0.25)", decreasing_fillcolor="rgba(255,51,85,0.25)"
        ))
        fig_i.update_layout(
            height=380, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ddeeff", family="Space Mono", size=10),
            xaxis=dict(gridcolor="rgba(0,200,255,0.04)", rangeslider_visible=False),
            yaxis=dict(gridcolor="rgba(0,200,255,0.04)", tickprefix="₹"),
            margin=dict(l=10, r=10, t=15, b=10),
        )
        st.plotly_chart(fig_i, use_container_width=True)
        st.caption(f"{len(_intra)} 5-min candles over last 5 sessions.")
    else:
        st.info("Intraday data not available (indices or after-hours). Try a large-cap stock during market hours.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB: COMPARE — side by side + correlation
# ─────────────────────────────────────────────────────────────────────────────
with tab_compare:
    st.markdown('<p class="section-header">[ 🔄 COMPARE 2–4 STOCKS SIDE-BY-SIDE ]</p>', unsafe_allow_html=True)
    _cmp_defaults = [k for k in ALL_STOCKS if any(x in k for x in
                     ["Reliance (", "TCS (", "HDFC Bank ("])][:3]
    _cmp_keys = st.multiselect("Select 2 to 4 stocks", list(ALL_STOCKS.keys()),
                                default=_cmp_defaults, max_selections=4, key="cmp_sel")
    _cmp_period = st.select_slider("Period", ["3mo","6mo","1y","2y","5y"], value="1y", key="cmp_period")

    if len(_cmp_keys) >= 2:
        _tickers = [ALL_STOCKS[k] for k in _cmp_keys]
        _labels  = [k.split(" (")[0] for k in _cmp_keys]
        with st.spinner("Fetching and computing..."):
            _nrm, _corr, _stats = xp.compare_stocks(_tickers, period=_cmp_period)
        if _nrm is not None:
            _stats.index = _labels[:len(_stats)]
            _colors = ["#00c8ff","#00e87a","#ffcc00","#ff6b35"]
            fig_c = go.Figure()
            for i, t in enumerate(_nrm.columns):
                lbl = _labels[_tickers.index(t)] if t in _tickers else t
                fig_c.add_trace(go.Scatter(x=_nrm.index, y=_nrm[t], name=lbl,
                                            line=dict(color=_colors[i%4], width=2)))
            fig_c.update_layout(
                height=380, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ddeeff", family="Space Mono", size=10),
                title=dict(text=f"Normalized Price (base=100) — {_cmp_period}", font=dict(color="#00c8ff",size=12)),
                xaxis=dict(gridcolor="rgba(0,200,255,0.04)"),
                yaxis=dict(gridcolor="rgba(0,200,255,0.04)"),
                margin=dict(l=10,r=10,t=40,b=10),
                legend=dict(bgcolor="rgba(7,18,32,0.5)", bordercolor="rgba(0,200,255,0.15)", borderwidth=1)
            )
            st.plotly_chart(fig_c, use_container_width=True)

            cc1, cc2 = st.columns([1.2, 1])
            with cc1:
                st.markdown('<p class="section-header">[ CORRELATION MATRIX (daily returns) ]</p>', unsafe_allow_html=True)
                _corr_disp = _corr.copy()
                _corr_disp.columns = [_labels[_tickers.index(c)] if c in _tickers else c for c in _corr_disp.columns]
                _corr_disp.index   = _corr_disp.columns
                fig_hm = go.Figure(go.Heatmap(
                    z=_corr_disp.values, x=_corr_disp.columns, y=_corr_disp.index,
                    colorscale=[[0,"#ff3355"],[0.5,"#0a192f"],[1,"#00e87a"]],
                    zmin=-1, zmax=1, text=_corr_disp.round(2).values,
                    texttemplate="%{text}", textfont=dict(color="#ddeeff",size=11),
                    colorbar=dict(thickness=10, tickfont=dict(color="#ddeeff",size=9))
                ))
                fig_hm.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#ddeeff",family="Space Mono",size=10),
                    margin=dict(l=10,r=10,t=10,b=10))
                st.plotly_chart(fig_hm, use_container_width=True)
            with cc2:
                st.markdown('<p class="section-header">[ PERFORMANCE STATS ]</p>', unsafe_allow_html=True)
                st.dataframe(_stats, use_container_width=True)
        else:
            st.warning("Could not fetch comparison data.")
    else:
        st.info("Select at least 2 stocks to compare.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB: AI ANALYST — chatbot + thesis + news summary
# ─────────────────────────────────────────────────────────────────────────────
with tab_ai:
    st.markdown(f'<p class="section-header">[ 🤖 XERCES AI ANALYST — {selected_name} ]</p>', unsafe_allow_html=True)
    st.caption("Ask anything about this stock. Powered by Claude Sonnet 4.6 via Emergent LLM Key. "
               "Live technicals + fundamentals are injected as context automatically.")

    _model_choices = ["auto",
                      "gemini-2.5-flash", "gemini-2.5-pro",
                      "claude-sonnet-4-6", "gpt-5.4",
                      "gemini-3-flash-preview", "claude-haiku-4-5-20251001"]
    _model = st.selectbox("Model", _model_choices, index=0, key="ai_model",
                          help="'auto' → Free Gemini first, Emergent Claude fallback when quota exceeded. "
                               "gemini-2.x → free Google API. others → Emergent LLM key (paid).")
    # Show which backend served the last response
    _last = xp.get_last_backend()
    if _last["name"] != "none":
        _c = "#00e87a" if "FREE" in _last["name"] else ("#00c8ff" if "Emergent" in _last["name"] else "#ff3355")
        st.markdown(
            f'<div style="background:rgba(7,18,32,0.5);border-left:3px solid {_c};'
            f'padding:6px 10px;border-radius:4px;font-size:11px;color:#ddeeff;'
            f'font-family:Space Mono,monospace;margin-bottom:8px;">'
            f'Last call: <b style="color:{_c};">{_last["name"]}</b> · {_last["model"]} · {_last["reason"]}'
            f'</div>', unsafe_allow_html=True)

    # Load fundamentals + news into context lazily
    if "_ai_ctx_extras" not in st.session_state or st.session_state.get("_ai_ctx_ticker") != selected_ticker:
        with st.spinner("Loading fundamentals + news for AI context..."):
            _f_data, _ = fetch_fundamentals(selected_ticker)
            _news_items = fetch_news(selected_ticker, selected_name) or []
            st.session_state["_ai_ctx_extras"] = {
                "fundamentals": _f_data or {},
                "news_titles": [x.get("title","") for x in _news_items[:10]]
            }
            st.session_state["_ai_ctx_ticker"] = selected_ticker

    _ctx = dict(st.session_state["_stock_ctx"])
    _ctx["fundamentals"] = st.session_state["_ai_ctx_extras"]["fundamentals"]
    _ctx["news"]         = st.session_state["_ai_ctx_extras"]["news_titles"]

    # Chat history (session)
    _chat_key = f"aichat_{selected_ticker}"
    if _chat_key not in st.session_state:
        st.session_state[_chat_key] = []

    ai_a, ai_b, ai_c = st.columns(3)
    if ai_a.button("📝 Generate Trade Thesis", use_container_width=True, key="ai_thesis"):
        with st.spinner("AI writing thesis..."):
            _thesis = xp.ai_trade_thesis(_ctx, model=_model)
            st.session_state[_chat_key].append(("assistant", f"**📝 TRADE THESIS**\n\n{_thesis}"))
            st.session_state["_last_thesis"] = _thesis
    if ai_b.button("📰 Summarize News", use_container_width=True, key="ai_news"):
        with st.spinner("AI summarizing headlines..."):
            _summ = xp.ai_summarize_news(_ctx["news"], selected_name, model=_model)
            st.session_state[_chat_key].append(("assistant", f"**📰 NEWS SUMMARY**\n\n{_summ}"))
            st.session_state["_last_news_summary"] = _summ
    if ai_c.button("🧹 Clear Chat", use_container_width=True, key="ai_clr"):
        st.session_state[_chat_key] = []
        st.rerun()

    # Render chat
    for _role, _msg in st.session_state[_chat_key]:
        _bg = "rgba(0,200,255,0.08)" if _role == "user" else "rgba(0,232,122,0.06)"
        _brd = "#00c8ff" if _role == "user" else "#00e87a"
        _tag = "👤 YOU" if _role == "user" else "🤖 XERCES AI"
        st.markdown(
            f'<div style="background:{_bg};border-left:3px solid {_brd};padding:10px 14px;'
            f'border-radius:6px;margin-bottom:8px;color:#ddeeff;font-size:13px;line-height:1.55;">'
            f'<div style="color:{_brd};font-size:10px;font-family:Space Mono,monospace;'
            f'letter-spacing:1px;margin-bottom:4px;">{_tag}</div>{_msg}</div>',
            unsafe_allow_html=True
        )

    _q = st.chat_input(f"Ask about {selected_name}... (e.g. 'Is this a good buy right now?', "
                       f"'Explain the current signal', 'What are the key risks?')")
    if _q:
        st.session_state[_chat_key].append(("user", _q))
        with st.spinner("XERCES AI thinking..."):
            _resp = xp.ai_chat(f"xerces_{selected_ticker}", _q, _ctx, model=_model)
        st.session_state[_chat_key].append(("assistant", _resp))
        st.rerun()

    with st.expander("🔍 View context sent to AI"):
        st.code(xp._build_context(_ctx), language="text")

# ─────────────────────────────────────────────────────────────────────────────
# TAB: TRADE JOURNAL
# ─────────────────────────────────────────────────────────────────────────────
with tab_journal:
    st.markdown('<p class="section-header">[ 📓 MY TRADE JOURNAL ]</p>', unsafe_allow_html=True)
    st.caption("Log actual trades to track your real P&L and strategy performance. Saved to disk.")

    _j = xp.load_journal()

    with st.expander("➕ Add trade entry", expanded=(_j.empty)):
        jc1, jc2, jc3 = st.columns(3)
        with jc1:
            _jdate = st.date_input("Date", value=datetime.date.today(), key="j_date")
            _jtick = st.text_input("Ticker", value=selected_name.upper(), key="j_tick")
            _jside = st.selectbox("Side", ["LONG","SHORT"], key="j_side")
        with jc2:
            _jqty  = st.number_input("Qty", min_value=1, value=10, key="j_qty")
            _jent  = st.number_input("Entry ₹", min_value=0.0, value=round(close, 2), step=0.5, key="j_ent")
            _jexit = st.number_input("Exit ₹ (0 if open)", min_value=0.0, value=0.0, step=0.5, key="j_exit")
        with jc3:
            _jstrat = st.text_input("Strategy", value=backtest_strategy, key="j_strat")
            _jnotes = st.text_area("Notes", height=80, key="j_notes")

        if st.button("💾 Save Trade", use_container_width=True, key="j_save"):
            _sign = 1 if _jside == "LONG" else -1
            _pnl_val = (_jexit - _jent) * _jqty * _sign if _jexit > 0 else 0.0
            _pnl_pct = ((_jexit - _jent) / _jent * 100 * _sign) if _jexit > 0 and _jent > 0 else 0.0
            _row = {"Date": str(_jdate), "Ticker": _jtick, "Side": _jside,
                    "Qty": _jqty, "Entry": _jent, "Exit": _jexit,
                    "P&L (₹)": round(_pnl_val, 2), "P&L %": round(_pnl_pct, 2),
                    "Strategy": _jstrat, "Notes": _jnotes}
            _j = pd.concat([_j, pd.DataFrame([_row])], ignore_index=True)
            xp.save_journal(_j)
            st.success(f"Trade saved. Total: {len(_j)} entries.")
            st.rerun()

    if not _j.empty:
        # KPIs
        _closed = _j[_j["Exit"].astype(float) > 0]
        _tot_pnl = float(_closed["P&L (₹)"].astype(float).sum()) if not _closed.empty else 0.0
        _win = int((_closed["P&L (₹)"].astype(float) > 0).sum()) if not _closed.empty else 0
        _tot = len(_closed)
        _wr  = round(_win / _tot * 100, 1) if _tot > 0 else 0.0
        _avg = round(float(_closed["P&L %"].astype(float).mean()), 2) if not _closed.empty else 0.0

        jk1, jk2, jk3, jk4 = st.columns(4)
        for col, lbl, val, clr in zip(
            [jk1,jk2,jk3,jk4],
            ["Total Trades","Closed","Win Rate","Total P&L"],
            [str(len(_j)), str(_tot), f"{_wr}%", f"₹{_tot_pnl:,.2f}"],
            ["#00c8ff","#ddeeff","#00e87a" if _wr >= 50 else "#ff3355",
             "#00e87a" if _tot_pnl >= 0 else "#ff3355"]
        ):
            col.markdown(f'<div class="glass-card"><p class="glass-label">{lbl}</p>'
                         f'<div class="glass-value" style="color:{clr};font-size:1.2rem;">{val}</div></div>',
                         unsafe_allow_html=True)

        st.markdown('<p class="section-header">[ TRADE HISTORY (editable) ]</p>', unsafe_allow_html=True)
        _edited = st.data_editor(_j, use_container_width=True, num_rows="dynamic", key="j_editor")
        _je1, _je2 = st.columns(2)
        if _je1.button("💾 Save Changes", use_container_width=True, key="j_save2"):
            xp.save_journal(_edited); st.success("Journal updated."); st.rerun()
        _je2.download_button("⬇️ Download Journal CSV",
            _j.to_csv(index=False).encode(), "xerces_journal.csv", "text/csv",
            use_container_width=True)

        # Equity curve (cumulative P&L)
        if not _closed.empty:
            _cc = _closed.copy()
            _cc["Date"] = pd.to_datetime(_cc["Date"], errors="coerce")
            _cc = _cc.sort_values("Date")
            _cc["CumPnL"] = _cc["P&L (₹)"].astype(float).cumsum()
            fig_j = go.Figure(go.Scatter(x=_cc["Date"], y=_cc["CumPnL"],
                mode="lines+markers",
                line=dict(color="#00e87a", width=2),
                marker=dict(size=7, color="#00c8ff"),
                fill="tozeroy", fillcolor="rgba(0,232,122,0.08)"))
            fig_j.update_layout(
                height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#ddeeff", family="Space Mono", size=10),
                title=dict(text="Cumulative P&L Curve", font=dict(color="#00c8ff", size=12)),
                xaxis=dict(gridcolor="rgba(0,200,255,0.04)"),
                yaxis=dict(gridcolor="rgba(0,200,255,0.04)", tickprefix="₹"),
                margin=dict(l=10, r=10, t=40, b=10),
            )
            st.plotly_chart(fig_j, use_container_width=True)
    else:
        st.info("No trades logged yet. Add your first entry above.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB: EXPORT — PDF & Excel
# ─────────────────────────────────────────────────────────────────────────────
with tab_export:
    st.markdown(f'<p class="section-header">[ 📄 EXPORT REPORTS — {selected_name} ]</p>', unsafe_allow_html=True)
    st.caption("Generate a shareable PDF report or Excel workbook with all analytics on this stock.")

    ec1, ec2 = st.columns(2)

    # ── PDF ──
    with ec1:
        st.markdown('<div class="glass-card">'
                    '<p class="glass-label">📄 PDF STOCK REPORT</p>'
                    '<div class="glass-value" style="color:#00c8ff;font-size:1.1rem;">One-page analyst report</div>'
                    '<p style="font-size:11px;color:#6a90aa;margin-top:6px;">'
                    'Includes KPIs, fundamentals, and (optional) AI-generated trade thesis + news summary.'
                    '</p></div>', unsafe_allow_html=True)
        _use_ai = st.checkbox("Include AI thesis & news summary (uses LLM key)", value=False, key="pdf_ai")
        if st.button("🖨️ Generate PDF Report", use_container_width=True, key="pdf_gen"):
            with st.spinner("Building PDF..."):
                _ctx_pdf = dict(st.session_state["_stock_ctx"])
                _f_data, _ = fetch_fundamentals(selected_ticker)
                _ctx_pdf["fundamentals"] = _f_data or {}
                _thesis_txt = ""; _news_txt = ""
                if _use_ai:
                    _ctx_pdf["news"] = [x.get("title","") for x in (fetch_news(selected_ticker, selected_name) or [])[:10]]
                    _thesis_txt = xp.ai_trade_thesis(_ctx_pdf)
                    _news_txt   = xp.ai_summarize_news(_ctx_pdf["news"], selected_name)
                _pdf = xp.build_pdf_report(_ctx_pdf, _thesis_txt, _news_txt)
                st.session_state["_last_pdf"] = _pdf
                st.session_state["_last_pdf_name"] = f"{selected_name}_xerces_report.pdf"
        if st.session_state.get("_last_pdf"):
            st.download_button("⬇️ Download PDF",
                st.session_state["_last_pdf"], st.session_state["_last_pdf_name"],
                "application/pdf", use_container_width=True, key="pdf_dl")

    # ── Excel ──
    with ec2:
        st.markdown('<div class="glass-card">'
                    '<p class="glass-label">📊 EXCEL WORKBOOK</p>'
                    '<div class="glass-value" style="color:#00e87a;font-size:1.1rem;">Multi-sheet analytics</div>'
                    '<p style="font-size:11px;color:#6a90aa;margin-top:6px;">'
                    'Sheets: OHLCV + indicators, backtest trades, scanner results (if available), '
                    'trade journal, watchlist.'
                    '</p></div>', unsafe_allow_html=True)
        if st.button("📗 Generate Excel Workbook", use_container_width=True, key="xls_gen"):
            with st.spinner("Building Excel..."):
                _sheets = {
                    "OHLCV_Indicators": df[[c for c in ["Date","Open","High","Low","Close","Volume",
                                                        "SMA_20","SMA_50","SMA_200","RSI_14","MACD",
                                                        "MACD_Signal","ATR_14","Volatility_20"] if c in df.columns]].copy(),
                }
                if trades:
                    _sheets["Backtest_Trades"] = pd.DataFrame(trades)
                if st.session_state.get("scan_results"):
                    _sc = pd.DataFrame(st.session_state["scan_results"]).drop(
                        columns=["_sig","_chg","_str"], errors="ignore")
                    _sheets["Scanner_Results"] = _sc
                _jdf = xp.load_journal()
                if not _jdf.empty: _sheets["Journal"] = _jdf
                _wl = xp.load_watchlist()
                if _wl: _sheets["Watchlist"] = pd.DataFrame(_wl)
                _xbytes = xp.build_excel_bytes(_sheets)
                st.session_state["_last_xls"] = _xbytes
                st.session_state["_last_xls_name"] = f"{selected_name}_xerces.xlsx"
        if st.session_state.get("_last_xls"):
            st.download_button("⬇️ Download Excel",
                st.session_state["_last_xls"], st.session_state["_last_xls_name"],
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True, key="xls_dl")

    st.markdown('<p class="section-header" style="margin-top:20px;">[ QUICK EXPORTS ]</p>', unsafe_allow_html=True)
    q1, q2, q3 = st.columns(3)
    q1.download_button("⬇️ Chart Data CSV",
        df.to_csv(index=False).encode(), f"{selected_name}_ohlcv.csv", "text/csv",
        use_container_width=True, key="q1_dl")
    if trades:
        q2.download_button("⬇️ Backtest Trades",
            pd.DataFrame(trades).to_csv(index=False).encode(),
            f"{selected_name}_trades.csv", "text/csv",
            use_container_width=True, key="q2_dl")
    _wl = xp.load_watchlist()
    if _wl:
        q3.download_button("⬇️ Watchlist JSON",
            json.dumps(_wl, indent=2).encode(), "xerces_watchlist.json",
            "application/json", use_container_width=True, key="q3_dl")


# ─────────────────────────────────────────────────────────────────────────────
# TAB: HELP/MANUAL
# ─────────────────────────────────────────────────────────────────────────────
with tab_help:
    st.markdown("""
<div class="glass-card">
<p class="section-header" style="margin-top:0;">[ XERCES GODMODE — REFERENCE MANUAL ]</p>
<div style="font-size:11px;color:#8ab0cc;line-height:2.1;font-family:'Space Mono',monospace;">
<b style="color:#00c8ff;">RSI (14)</b> — &lt;30 oversold (buy zone). &gt;70 overbought (sell zone).<br>
<b style="color:#00c8ff;">MACD (12,26,9)</b> — MACD crossing above signal = bullish momentum. Histogram shows acceleration.<br>
<b style="color:#00c8ff;">SMA 20/50/200</b> — Golden cross (SMA50 &gt; SMA200) = major bull signal. Price &gt; SMA200 = bull market.<br>
<b style="color:#00c8ff;">Bollinger Bands</b> — Band squeeze = volatility expansion imminent. Breakout direction = trend.<br>
<b style="color:#00c8ff;">ATR (14)</b> — True range in Rs. Used for stop-loss sizing: 1.5x ATR below entry.<br>
<b style="color:#00c8ff;">Stochastic %K</b> — &lt;20 oversold, &gt;80 overbought. Combine with RSI for confirmation.<br>
<br>
<b style="color:#ffcc00;">ARIMA</b> — Fitted on log-price via 5x5 AIC grid. Validated with 60-day holdout MAPE + directional accuracy.<br>
<b style="color:#ffcc00;">Holt-Winters</b> — Exponential smoothing with additive trend. Second-opinion model alongside ARIMA.<br>
<b style="color:#ffcc00;">Consensus</b> — Average of ARIMA and Holt-Winters. More robust than either alone.<br>
<b style="color:#ffcc00;">MAPE</b> — Mean Absolute Percentage Error on 60-day holdout. Under 5% = excellent, 5-10% = good.<br>
<b style="color:#ffcc00;">Directional Accuracy</b> — % of days where forecast direction matched actual. &gt;60% = useful model.<br>
<br>
<b style="color:#7c4dff;">PORTFOLIO OPTIMIZER</b> — Markowitz MPT with 3000 Monte Carlo simulations. Finds efficient frontier.<br>
<b style="color:#7c4dff;">BACKTEST</b> — 4 strategies tested on 5-year data. Next-day open execution eliminates look-ahead bias.<br>
<b style="color:#7c4dff;">SCANNER</b> — Multi-threaded bulk scan of selected sectors with BUY/SELL/HOLD signals and position sizing.<br>
<br>
<b style="color:#00e87a;">🔥 HEATMAP</b> — Live 1-day performance across all 18 sectors, plus 5-min intraday candles for the selected stock.<br>
<b style="color:#00e87a;">🔄 COMPARE</b> — Side-by-side normalized price chart for 2–4 stocks, plus correlation matrix &amp; risk/return stats.<br>
<b style="color:#00e87a;">🤖 AI ANALYST</b> — Chat with Claude Sonnet 4.6 (or GPT-5.4 / Gemini) about the current stock. Auto-injects technicals, fundamentals &amp; news as context. One-click trade thesis &amp; news summarization.<br>
<b style="color:#00e87a;">📓 JOURNAL</b> — Log real trades, track win-rate, total P&amp;L, and cumulative equity curve. Persisted to disk.<br>
<b style="color:#00e87a;">📄 EXPORT</b> — One-click PDF report (with optional AI thesis) and multi-sheet Excel workbook.<br>
<b style="color:#00e87a;">⭐ WATCHLIST (sidebar)</b> — Save favorite stocks; persisted to disk across sessions.<br>
<b style="color:#00e87a;">🚨 ALERTS (sidebar)</b> — Set price or RSI triggers; alerts fire when you refresh with that stock loaded.<br>
<br>
<b style="color:#ffcc00;">PORTFOLIO ROTATION ADVISOR:</b> Analyzes holdings using a 1-year ARIMA + Holt-Winters consensus forecast. Recommends 'Rotate' to cash or higher projected peer alternatives if returns are weak (&lt;5%) or technicals are bearish.<br>
<br>
<b style="color:#ff3355;">SIGNAL LOGIC:</b> BUY = SMA20&gt;SMA50 AND Price&gt;SMA200 AND RSI&lt;70 AND (MACD cross up OR RSI&lt;45). SELL = opposite.<br>
<br>
<b style="color:#ff3355;">DISCLAIMER:</b> XERCES is a research tool. Not SEBI registered. Not financial advice. Data from Yahoo Finance.
</div>
</div>
""", unsafe_allow_html=True)
