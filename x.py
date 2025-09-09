import streamlit as st
from datetime import datetime
import folium
from streamlit_folium import folium_static
from PIL import Image
import os
import pandas as pd
import numpy as np
import random
import streamlit.components.v1 as components

# ---- CONFIGURATION ----
st.set_page_config(
    page_title="Luca & Ewa",
    page_icon="⏳",
    layout="centered"
)

# ---- CUSTOM CSS ----
st.markdown("""
<style>
    body {
        font-family: 'Arial', sans-serif;
    }

    .main-title {
        font-size: 3em;
        text-align: center;
        margin-top: 30px;
    }

    .section-title {
        font-size: 1.8em;
        margin-top: 40px;
        border-bottom: 2px solid;
        padding-bottom: 10px;
    }

    .countdown-container, .experience-section {
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }

    .experience-section {
        border-left: 5px solid #3498db;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .gallery-container {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        margin-top: 20px;
    }
    
    .gallery-item {
        flex: 1 1 200px;
        min-width: 200px;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .gallery-item img {
        width: 100%;
        height: 150px;
        object-fit: cover;
    }
    
    .gallery-caption {
        padding: 10px;
        background: rgba(0,0,0,0.05);
    }

    /* Light theme */
    @media (prefers-color-scheme: light) {
        body {
            background-color: #f5f5f5;
        }
        .main-title {
            color: #2C3E50;
        }
        .section-title {
            color: #34495E;
            border-color: #dcdcdc;
        }
        .countdown-container,
        .experience-section {
            background: #ffffff;
        }
    }

    /* Dark theme */
    @media (prefers-color-scheme: dark) {
        body {
            background-color: #0e1117;
        }
        .main-title {
            color: #ecf0f1;
        }
        .section-title {
            color: #ecf0f1;
            border-color: #555;
        }
        .countdown-container,
        .experience-section {
            background: #1e1e1e;
            box-shadow: 0 2px 8px rgba(255,255,255,0.05);
        }
    }
    
    /* Finance specific styles */
    .finance-header {
        background: linear-gradient(90deg, #3498db, #2ecc71);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 25px 0 15px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        font-size: 1.5em;
    }
    .finance-tip {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        margin: 20px 0;
        border-left: 5px solid #3498db;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .finance-warning {
        background-color: #fff3cd;
        border-radius: 10px;
        padding: 15px;
        margin: 20px 0;
        border-left: 5px solid #ffc107;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .scenario-box {
        border-radius: 10px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .scenario-box:hover {
        transform: translateY(-3px);
    }
    .company-card {
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: #f8f9fa;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    @media (prefers-color-scheme: dark) {
        .finance-tip { 
            background-color: #1e1e1e;
            border-left: 5px solid #2ecc71;
        }
        .finance-warning { 
            background-color: #332701;
            border-left: 5px solid #f39c12;
        }
        .scenario-box {
            background-color: #1e1e1e;
        }
        .company-card {
            background-color: #1e1e1e;
        }
    }
</style>
""", unsafe_allow_html=True)

# ---- PASSWORD AUTH ----
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
        <div class='main-title'>🔒 Welcome to this autistic place</div>
        <p style='text-align:center;'>Please enter the password to unlock the experience.</p>
        <p style='text-align:center; font-style: italic;'>Hint: city where I end up after you make a joke.</p>
    """, unsafe_allow_html=True)
    pw = st.text_input("Password", type="password")
    if pw == "Nojokolandia":
        st.session_state.authenticated = True
        st.rerun()
    else:
        if pw:
            st.error("Incorrect password")
    st.stop()

# ---- SIDEBAR NAVIGATION ----
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Timeline & Countdowns",
    "Our Places & Gallery",
    "Finance Masterclass",
    "Ewa's Impossible Parkour"
])

# ---- THEME SWITCH ----
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True  
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

st.sidebar.markdown("---")
if st.sidebar.button("Toggle Light/Dark Mode"):
    toggle_theme()
    st.rerun()

if st.session_state.dark_mode:
    st.sidebar.info("Current: Dark Mode")
else:
    st.sidebar.info("Current: Light Mode")

# ---- TIMELINE & COUNTDOWNS PAGE ----
if page == "Timeline & Countdowns":
    st.markdown("<div class='main-title'>Luca & Ewa | Our Time </div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>🕒 Timeline & Countdowns</div>", unsafe_allow_html=True)

    def calculate_dates():
        today = datetime.now()
        return {
            "⏳ Next Anniversary (10 Jan)": datetime(today.year + 1, 1, 10) if today.month > 1 or (today.month == 1 and today.day > 10) else datetime(today.year, 1, 10),
            "📅 Days Since We Met (14 Jun 2024)": datetime(2024, 6, 14),
            "🎂 Days Until Luca's Bday (23 Mar)": datetime(today.year, 3, 23) if today < datetime(today.year, 3, 23) else datetime(today.year + 1, 3, 23),
            "🎂 Days Until Ewa's Bday (17 Nov)": datetime(today.year, 11, 17) if today < datetime(today.year, 11, 17) else datetime(today.year + 1, 11, 17)
        }

    def display_countdown(name, target_date):
        today = datetime.now()
        delta = target_date - today
        if "Since" in name:
            st.markdown(f"""
            <div class="countdown-container">
                <h3>{name}</h3>
                <p><strong>{(today - target_date).days} days</strong> together</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="countdown-container">
                <h3>{name}</h3>
                <p><strong>{delta.days} days</strong> remaining</p>
            </div>
            """, unsafe_allow_html=True)

    dates = calculate_dates()
    for name, date in dates.items():
        display_countdown(name, date)

# ---- OUR PLACES & GALLERY PAGE ----
elif page == "Our Places & Gallery":
    st.markdown("<div class='main-title'>Luca & Ewa | Our Time</div>", unsafe_allow_html=True)
    
    # Define all places with their photos and captions
    places = [
        {
            "coords": [45.7061, 9.3770], 
            "label": "Montevecchia", 
            "experiences": [
                {"title": "First Date"}
            ],
            "photos": ["montevecchia1", "montevecchia2", "montevecchia3"],
            "captions": [
                "Stolen shot 1",
                "Sexy sunset",
                "Stolen shot 3"
            ]
        },
        {
            "coords": [44.0059, 8.1750], 
            "label": "Alassio", 
            "experiences": [{"title": "First trip"}],
            "photos": ["alassio", "alassio2", "alassio3", "alassio4", "alassio5", "alassio6", "alassio7", "alassio8", "alassio9", "alassio10", "alassio11", "alassio12", "alassio13", "alassio14", "alassio15", "alassio16", "alassio17"],
            "captions": [
                "A cute girl on the phone (classic)",
                "Eyes (yours better)",
                "4 types of Ligurian Focaccia/Pizza and my type of girl",
                "Worst sandwich ever, with scam stuff from TooGoodToGo",
                "Classic, I had to sleep on the sofa",
                ":)",
                "Pre sagra",
                "Cute brackfast",
                "SLURP",
                "Scam aperitif",
                "You, hating my pics",
                "Kebab-girl",
                "Pre sagra, but better",
                "MY BABYYYYYYYY",
                "Strong boy",
                "Godiamo!",
                "Selfie couple"
            ]
        },
        {
            "coords": [45.582146876340424, 9.149965454736574], 
            "label": "Ewa's house (Paderno Dugnano)", 
            "experiences": [{"title": "Where I saw you for the first time & <3 <3 <3"}],
            "photos": ["paderno1", "paderno2", "paderno3", "paderno4", "paderno5", "paderno6", "paderno7", "paderno8"],
            "captions": [
                "Fucking gate",
                "<3",
                "Teaching girl",
                "Poverino 1",
                "Poverino 2",
                "7-6, forza Inter",
                "Classic awakening with you",
                "Classic fight (you always win)"
            ]
        },
        {
            "coords": [45.4773, 9.1895], 
            "label": "Chinatown Milano", 
            "experiences": [{"title": "Cute date"}],
            "photos": ["gae aulenti", "pangrattato"],
            "captions": [
                "Gae Aulenti",
                "The hard search for breadcrumbs (useless because then what you cooked with that breadcrumbs would be disgusting)"
            ]
        },
        {
            "coords": [45.5845, 9.2730], 
            "label": "Parco di Monza", 
            "experiences": [{"title": "First Kiss"}],
            "photos": ["parcodimonza1", "parcodimonza2"],
            "captions": [
                "Old Monza racetrack (this is where you were calling your father)",
                "Villa of Monza"
            ]
        },
        {
            "coords": [45.577076402711505, 9.181587485421431], 
            "label": "Parco Lago Nord Paderno Dugnano", 
            "experiences": [{"title": "Some cute dates & Inter-PSG (dios)"}],
            "photos": ["parcolagonord"],
            "captions": ["before the defeat (I will never set foot in this park again)"]
        },
        {
            "coords": [45.5836, 9.2749], 
            "label": "YIN TAO - Chinese restaurant (Monza)", 
            "experiences": [{"title": "Cute dinner"}],
            "photos": ["ristchinese"],
            "captions": ["Post chinese restaurant"]
        },
        {
            "coords": [45.5549, 8.9967], 
            "label": "Shopping Center Il Centro (Arese)", 
            "experiences": [{"title": "Shopping"}],
            "photos": ["arese"],
            "captions": ["I have a bad face, but you look hot in this dress (we'll buy it)"]
        },
        {
            "coords": [45.5904, 9.2661], 
            "label": "Luca's house (Monza)", 
            "experiences": [{"title": "Lesgoski"}],
            "photos": ["casamia", "casamia2"],
            "captions": [
                "Messi rummaging through my closet (first time at my house <3)",
                "boh.."
            ]
        },
        {
            "coords": [45.47403250724793, 9.181608857791872], 
            "label": "Acquario Civico (Milano)", 
            "experiences": [{"title": "Fish experience"}],
            "photos": ["acquario1","acquario2"],
            "captions": ["PI PU PA","PURE PURU"]
        },
        {
            "coords": [45.463063705848434, 9.171811011218445], 
            "label": "Museo della Scienza e della Tecnica (Milano)", 
            "experiences": [{"title": "Tired couple"}],
            "photos": ["museoscienza","museoscienza2"],
            "captions": ["gnam","ciao bella"]
        },     
        {
            "coords": [45.44805214504523, 9.630403052912353], 
            "label": "Crema (Sorgiva Quarantina)", 
            "experiences": [{"title": "Gay city"}],
            "photos": ["crema1","crema2"],
            "captions": ["Hot water","36 smalto bianco"]
        }, 
        {
            "coords": [50.060749013837984, 19.937806256672445], 
            "label": "Krakow", 
            "experiences": [{"title": "Polish couple part one"}],
            "photos": ["krakow1", "krakow2", "krakow3", "krakow4", "krakow5", "krakow6", "krakow7", "krakow8", "krakow9", "krakow10", "krakow11"],
            "captions": [
                "Best moment of the vacation",
                "Pics girl",
                "Soap ice cream",
                "Classic belly button moment",
                "Fucking dragon",
                "Pierogi moment",
                "Dios",
                "Partyyyy",
                "Kissss",
                "To good to go",
                "Where it all began"
            ]
        },   
        {
            "coords": [52.24368054518519, 21.015735201226697], 
            "label": "Warsaw", 
            "experiences": [{"title": "Polish couple part two"}],
            "photos": ["warsaw1", "warsaw2", "warsaw3", "warsaw4", "warsaw5", "warsaw6", "warsaw7", "warsaw8"],
            "captions": [
                "Signing the contract",
                "You who don't wait for me and ignore me",
                "Cheap food (then I couldn't digest it for 2 days)",
                "Ci sta",
                "Hi, sexy girl",
                "My babyy (memmoriesss)",
                "View point",
                "I think she is polish"
            ]
        }, 
        {
            "coords": [45.55681295098242, 9.077592577105136], 
            "label": "Long Sushi & Cocktails (Arese)", 
            "experiences": [{"title": "Sushiiii"}],
            "photos": ["sushi"],
            "captions": ["Koi Asset Management meeting"]
        } 
    ]

    # ---- MAP SECTION ----
    st.markdown("<div class='section-title'>📍 Our Places</div>", unsafe_allow_html=True)
    
    # Create the map with enhanced popups
    m = folium.Map(location=[45.7061, 9.3770], zoom_start=11)
    for i, place in enumerate(places):
        # Create popup content with experiences
        popup_content = f"<b>{place['label']}</b><br/><br/>"
        
        if place['experiences']:
            popup_content += "<b>Our Experiences:</b><ul>"
            for exp in place['experiences']:
                popup_content += f"<li><b>{exp['title']}</b>:"
            popup_content += "</ul>"
        else:
            popup_content += "Click below to see our photos from this place."
        
        folium.Marker(
            location=place["coords"],
            tooltip=place["label"],
            popup=popup_content,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)
    folium_static(m, width=700, height=500)

    # ---- GALLERY SECTION ----
    st.markdown("<div class='section-title'>📸 Our Memories Gallery</div>", unsafe_allow_html=True)

    selected_place = st.selectbox("Select a location to view photos:", [place["label"] for place in places])

    # Display gallery for selected place
    for place in places:
        if place["label"] == selected_place:
            if "photos" in place and len(place["photos"]) > 0:
                st.markdown(f"### {place['label']}")
                
                # Create columns for the gallery
                cols = st.columns(2)
                col_index = 0
                
                for i, photo in enumerate(place["photos"]):
                    try:
                        img = Image.open(f"{photo}.jpg")
                        caption = place["captions"][i] if i < len(place["captions"]) else place['label']
                        
                        with cols[col_index]:
                            st.image(img, caption=caption, use_container_width=True)
                        
                        col_index = (col_index + 1) % 2
                    except FileNotFoundError:
                        st.warning(f"Photo {photo}.jpg not found in the directory.")
            else:
                st.info(f"No photos available yet for {place['label']}")
            break

# ---- FINANCE MASTERCLASS PAGE ----
elif page == "Finance Masterclass":
    st.markdown("<div class='finance-header'>💰 Personal Finance Masterclass</div>", unsafe_allow_html=True)

    # ---- WHY INVEST? ----
    st.markdown("## 💸 Why Should You Invest?")
    st.write("""
    Money loses value over time due to inflation. Here's how prices changed for common items:
    """)
    
    infl_examples = {
        "Item": ["Fiat 500", "Gelato", "Movie ticket", "Espresso coffee", "Big Mac"],
        "1994": ["€8,000", "€0.80", "€4.50", "€0.60", "€2.50"],
        "2004": ["€10,500", "€1.60", "€6.00", "€0.80", "€3.00"],
        "2014": ["€14,000", "€1.90", "€8.00", "€1.00", "€3.80"],
        "2024": ["€18,500", "€3.20", "€10.50", "€1.20", "€4.80"]
    }

    st.dataframe(
        pd.DataFrame(infl_examples).set_index("Item"),
        use_container_width=True,
        height=200
    )

    st.markdown("""
    <div class='finance-tip'>
    <b>Key Insight:</b> At 3% inflation, prices double every 24 years (Rule of 72). 
    Your money needs to grow just to maintain its purchasing power!
    </div>
    """, unsafe_allow_html=True)

    # ---- RISK MYTHBUSTING ----
    st.markdown("## 🔍 Busting Investment Myths")
    st.write("""
    **Common fear:** "The stock market is too risky!"  
    **Reality:** While individual stocks can be volatile, a diversified portfolio has historically always recovered.
    """)

    try:
        st.image("S&Preturns.jpg", caption="S&P 500 historical returns since 1926 - All crashes recovered in time")
    except:
        st.warning("Add 'S&Preturns.jpg' to show long-term market performance")

    st.markdown("""
    <div class='finance-tip'>
    <b>Why ETFs are safer than single stocks:</b>  
     ✓ Own hundreds/thousands of companies,  
     ✓ Automatic diversification,   
     ✓ Survives individual company failures,  
     ✓ Historically 7-10% annual returns over 15+ years  
    </div>
    """, unsafe_allow_html=True)

    # ---- INVESTMENT TYPES ----
    st.markdown("## 📈 Investment Options")
    tab1, tab2 = st.tabs(["Stocks (Equities)", "Bonds (Fixed Income)"])
    
    with tab1:
        st.markdown("""
        **Characteristics:**  
        - Ownership in companies  
        - Higher volatility but higher returns (7-10% avg)  
        - Best for long-term growth (5+ years)  
        - Examples:  
          • S&P 500 ETF  
          • MSCI World ETF  
          • NASDAQ-100 ETF  
        """)
        st.markdown("""
        <div class='finance-tip'>
        💡 <b>Best for:</b> Retirement savings, long-term wealth building
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("""
        **Characteristics:**  
        - Loans to governments/companies  
        - Lower returns (2-5%) but stable  
        - Good for short-term goals (1-5 years)  
        - Examples:  
          • Italian Government Bonds (BTP)  
          • European Corporate Bonds  
          • Global Aggregate Bond ETF  
        """)
        st.markdown("""
        <div class='finance-tip'>
        💡 <b>Best for:</b> Preserving capital, reducing portfolio volatility
        </div>
        """, unsafe_allow_html=True)

    # ---- MARKET HISTORY SHOWDOWN ----
    st.markdown("## 🥊 S&P 500 vs Individual Stocks")
    st.write("""
    **Compare how $10,000 invested in 2010 would have grown in different investments:**
    """)
    
    companies = {
        "Nokia": {"return": -96, "color": "#124191", "icon": "📱"},
        "Apple": {"return": 2200, "color": "#3498db", "icon": "🍏"},
        "Enron": {"return": -100, "color": "#ff0000", "icon": "💥"},
        "Amazon": {"return": 1500, "color": "#ff9900", "icon": "📦"}
    }
    
    selected_company = st.selectbox("Select a company to compare:", list(companies.keys()))
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='company-card' style='border-left: 5px solid {companies[selected_company]["color"]}'>
            <h3>{companies[selected_company]["icon"]} {selected_company}</h3>
            <p><b>Return:</b> {companies[selected_company]["return"]}%</p>
            <p><b>Value:</b> ${10000 * (1 + companies[selected_company]["return"]/100):,.0f}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='company-card' style='border-left: 5px solid #2ecc71'>
            <h3>📊 S&P 500 ETF</h3>
            <p><b>Return:</b> 350%</p>
            <p><b>Value:</b> $45,000</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='finance-warning'>
    <b>Lesson:</b> While some stocks outperform, most underperform the market. 
    ETFs give you average market returns with much lower risk.
    </div>
    """, unsafe_allow_html=True)

    # ---- DIVERSIFICATION GAME ----
    st.markdown("## 🎮 Portfolio Builder Challenge")
    st.write("""
    **Allocate €10,000 across different assets and see how your portfolio performs in various scenarios:**
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        stocks = st.slider("Stocks (%)", 0, 100, 60)
    with col2:
        bonds = st.slider("Bonds (%)", 0, 100, 40)
    
    if (stocks + bonds) != 100:
        st.error("Your allocation must total 100%!")
    else:
        if st.button("Test My Portfolio", key="test_portfolio"):
            scenarios = {
                "Economic Boom": {"stocks": 1.20, "bonds": 1.03},
                "Recession": {"stocks": 0.75, "bonds": 1.05},
                "Normal Growth": {"stocks": 1.08, "bonds": 1.02},
                "High Inflation": {"stocks": 1.10, "bonds": 0.95}
            }
            
            for name, returns in scenarios.items():
                final_value = 10000 * (
                    (stocks/100)*returns["stocks"] + 
                    (bonds/100)*returns["bonds"]
                )
                return_pct = ((final_value/10000)-1)*100
                
                st.markdown(f"""
                <div class='scenario-box'>
                    <h4>{name}</h4>
                    <p><b>Final Value:</b> €{final_value:,.2f}</p>
                    <p><b>Return:</b> {return_pct:.1f}%</p>
                    <p><b>Breakdown:</b> 
                    Stocks: €{(10000*(stocks/100)*returns["stocks"]):,.0f} | 
                    Bonds: €{(10000*(bonds/100)*returns["bonds"]):,.0f} | 
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("""
            <div class='finance-tip'>
            <b>Key Takeaways:</b>
             • Diversification smooths out returns across different economic conditions.
             • No single scenario destroys your entire portfolio.
             • The best allocation depends on your time horizon and risk tolerance.
            </div>
            """, unsafe_allow_html=True)

    # ---- COMPOUNDING CALCULATOR ----
    st.markdown("## ✨ The Magic of Compounding")
    st.write("""
    **See how regular investments grow over time with compound interest:**
    """)
    
    calc_type = st.radio("Calculator Type", 
                        ["Lump Sum Investment", "Monthly Contributions"], 
                        horizontal=True,
                        label_visibility="visible")
    
    if calc_type == "Lump Sum Investment":
        col1, col2, col3 = st.columns(3)
        with col1:
            principal = st.number_input("Initial Investment (€)", 1000, 1000000, 10000)
        with col2:
            years = st.slider("Investment Horizon (years)", 5, 50, 20)
        with col3:
            rate = st.slider("Expected Annual Return (%)", 1, 15, 7)
        
        future_value = principal * (1 + rate/100)**years
        st.metric("Future Value", f"€{future_value:,.2f}")
        
    else:
        col1, col2, col3 = st.columns(3)
        with col1:
            monthly = st.number_input("Monthly Contribution (€)", 10, 5000, 200)
        with col2:
            years = st.slider("Investment Horizon (years)", 5, 50, 30)
        with col3:
            rate = st.slider("Expected Annual Return (%)", 1, 15, 7)
        
        months = years * 12
        monthly_rate = rate/100/12
        future_value = monthly * ((1 + monthly_rate)**months - 1) / monthly_rate
        
        st.metric("Future Value", f"€{future_value:,.2f}")
        st.caption(f"Total contributions: €{monthly * months:,.2f}")
    
    st.markdown("""
    <div class='finance-tip'>
    <b>Practical Examples:</b><br>
    • €200/month at 7% for 30 years = €243,000<br>
    • €500/month at 7% for 30 years = €608,000<br>
    • The earlier you start, the more compounding works for you!
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## � Finance Knowledge Challenge")
    st.write("Test your personal finance knowledge with this comprehensive quiz:")

    # Lista delle domande e opzioni
    questions = [
        {
            "number": 1,
            "question": "What's the 'Rule of 72' used for?",
            "options": ["Calculating taxes", "Estimating how long it takes money to double", "Determining stock prices", "Measuring inflation"],
            "answer": "Estimating how long it takes money to double",
            "explanation": "Rule of 72 estimates doubling time: 72 ÷ annual interest rate."
        },
        {
            "number": 2,
            "question": "Which investment has historically had the highest long-term returns?",
            "options": ["Savings accounts", "Government bonds", "Stock market", "Commodities"],
            "answer": "Stock market",
            "explanation": "Stocks average 7–10% long-term returns, outperforming other assets."
        },
        {
            "number": 3,
            "question": "What's the main advantage of ETFs over individual stocks?",
            "options": ["Higher guaranteed returns", "Built-in diversification", "No fees", "Short-term gains"],
            "answer": "Built-in diversification",
            "explanation": "ETFs offer instant diversification, reducing single-stock risk."
        },
        {
            "number": 4,
            "question": "Where should you keep your emergency fund?",
            "options": ["Growth stocks", "Savings account", "Cryptocurrency", "Long-term bonds"],
            "answer": "Savings account",
            "explanation": "Emergency funds should be liquid, risk-free, and accessible."
        },
        {
            "number": 5,
            "question": "How much should your emergency fund cover?",
            "options": ["1-2 months of expenses", "3-5 months of expenses", "6-12 months of expenses", "2+ years of expenses"],
            "answer": "6-12 months of expenses",
            "explanation": "This buffer helps during unemployment or big emergencies."
        },
        {
            "number": 6,
            "question": "What should you do when the market crashes?",
            "options": ["Sell everything", "Buy more", "Do nothing", "Wait for the bottom"],
            "answer": "Do nothing",
            "explanation": "Staying invested is key—markets historically recover. \
            Selling locks in losses, and timing the bottom is nearly impossible. \
            Many believe they should 'buy more' during crashes, but that's not ideal if you've already set a proper asset allocation. \
            If your portfolio is correctly built, you shouldn't have extra funds to invest—your emergency fund is not meant to be used for buying dips!"
        },
        {
            "number": 7,
            "question": "How many companies generated most of S&P 500 returns in the last decade?",
            "options": ["All equally", "About 20%", "Just 7", "Just 2"],
            "answer": "Just 7",
            "explanation": "A few tech giants (FAANG+M) drove most S&P 500 growth in recent years."
        },
        {
            "number": 8,
            "question": "What's the key difference between active and passive funds?",
            "options": ["Passive cost more", "Active try to beat the market", "Passive are more diversified", "No difference"],
            "answer": "Active try to beat the market",
            "explanation": "Passive funds track the index, while active ones try (and often fail) to outperform it."
        },
        {
            "number": 9,
            "question": "If you invest €1000 at 7% annually, what will you have after 10 years?",
            "options": ["€1070", "€1700", "€1967", "€2134"],
            "answer": "€1967",
            "explanation": "Thanks to compounding: €1000 × (1.07)^10 = €1967. Instead of €1700, here's why Einstein called it the eighth wonder of the world"
        },
        {
            "number": 10,
            "question": "How many times has the S&P 500 dropped >40% since 1950?",
            "options": ["Never", "Once", "Three times", "Seven times"],
            "answer": "Three times",
            "explanation": "Big crashes occurred in 1973–74, 2000–02, and 2007–09."
        },
        {
            "number": 11,
            "question": "What happens to bonds when interest rates rise?",
            "options": ["Increase in value", "Decrease in value", "No change", "Get called"],
            "answer": "Decrease in value",
            "explanation": "Bond prices drop when new issues offer higher interest."
        },
        {
            "number": 12,
            "question": "What's the S&P 500's average annual return since the 1950s?",
            "options": ["3-5%", "7-10%", "12-15%", "20%+"],
            "answer": "7-10%",
            "explanation": "Including dividends, S&P 500 averages this return over decades."
        },
        {
            "number": 13,
            "question": "What is 'dollar cost averaging'?",
            "options": ["Investing all at once", "Investing fixed amounts regularly", "Only investing in dollars", "Selling when down"],
            "answer": "Investing fixed amounts regularly",
            "explanation": "Dollar-cost averaging reduces timing risk and builds discipline."
        },
        {
            "number": 14,
            "question": "Which asset historically protects best against inflation?",
            "options": ["Cash", "Stocks", "Gold", "Real estate"],
            "answer": "Real estate",
            "explanation": "Property values and rents rise with inflation."
        },
        {
            "number": 15,
            "question": "What percentage of income should you invest?",
            "options": ["5-10%", "15-20%", "30-50%", "As much as possible after essentials"],
            "answer": "As much as possible after essentials",
            "explanation": "The more you invest, the greater your long-term growth."
        },
        {
            "number": 16,
            "question": "What's most important for investment growth?",
            "options": ["Market timing", "Return rate", "Time invested", "Stock picking"],
            "answer": "Time invested",
            "explanation": "Time beats timing—compound interest grows faster over long periods."
        },
        {
            "number": 17,
            "question": "What's the typical annual cost of a passive ETF?",
            "options": ["0.1-0.3%", "1-2%", "3-5%", "No cost"],
            "answer": "0.1-0.3%",
            "explanation": "Passive ETFs have very low fees compared to active funds."
        },
        {
            "number": 18,
            "question": "Which strategy has highest long-term success probability?",
            "options": ["Stock picking", "Frequent trading", "Passive ETF investing", "Following hot tips"],
            "answer": "Passive ETF investing",
            "explanation": "This strategy beats 90% of active traders long-term."
        },
        {
            "number": 19,
            "question": "When is the best time to start investing?",
            "options": ["When I have more money", "After studying 10 years", "Today", "When market is low"],
            "answer": "Today",
            "explanation": "'Time in market' beats 'timing the market'."
        },
        {
            "number": 20,
            "question": "What's most important in investment selection?",
            "options": ["Past performance", "Asset allocation", "Influencer advice", "Latest news"],
            "answer": "Asset allocation",
            "explanation": "Asset mix determines 90% of portfolio returns."
        },
    ]

    # Risposte utente
    user_answers = {}
    for q in questions:
        user_answers[q["number"]] = st.radio(
            f"{q['number']}. {q['question']}",
            q["options"],
            index=None,
            key=f"q{q['number']}"
        )

    # Bottone per mostrare i risultati
    if st.button("✅ Check Answers"):
        score = 0
        st.markdown("### 📝 Results")
        for q in questions:
            user_ans = user_answers[q["number"]]
            if user_ans == q["answer"]:
                st.success(f"✅ Q{q['number']} Correct! {q['explanation']}")
                score += 1
            else:
                st.error(f"❌ Q{q['number']} Incorrect. {q['explanation']}")

        st.markdown(f"""
        <div style='text-align: center; font-size: 1.3em; padding: 10px;'>
            🎯 <b>Final Score: {score}/20</b><br>
            { "🏆 Finance Expert!" if score >= 18 else "💪 Great Job! You're on the right track." if score >= 12 else "📘 Keep Learning! Financial literacy matters." }
        </div>
        """, unsafe_allow_html=True)

############################## - Ewa's Impossible Parkour - ####################################
elif page == "Ewa's Impossible Parkour":
    # Title and instructions outside the game (in Streamlit)
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 style='color: #ff66cc; font-family: "Press Start 2P", cursive;'>🎮 Ewa's Impossible Parkour</h1>
        <p style='font-size: 18px;'>With a big price if you'll complete the game!</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🎮 How to Play
        - **Move**: Arrow Keys or A/D
        - **Jump**: W or Up Arrow
        - **Dash (from level 3)**: Spacebar (super powerful!)
        - **Goal**: Reach the green portal at the end of each level!
        """)
    
    with col2:
        st.markdown("""
        ### ⚠️ Warning
        - The red floor is deadly
        - It gets MUCH harder as you progress
        - Dash gives you a huge horizontal boost
        - Prepare to die... a LOT!
        """)

    st.markdown("---")

    game_code = """
    <style>
      #game-container {
        width: 100%;
        height: 100%;
        position: relative;
      }
      canvas {
        image-rendering: pixelated;
        border: 4px solid #ff66cc;
        background: #121212;
        margin: 0 auto;
        display: block;
        outline: none;
      }
      .game-ui {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 1rem;
      }
      .hud {
     display: flex;
     justify-content: space-between;
     align-items: center;  /* Added for better vertical alignment */
     color: white;
     width: 90%;  /* Changed to percentage for better responsiveness */
     max-width: 1400px;  /* Added maximum width */
     font-family: monospace;
     margin: 0 auto;
     background: rgba(34, 34, 34, 0.9);  /* Added transparency */
     padding: 8px 12px;  /* Adjusted padding */
     border-radius: 6px;
     position: fixed;  /* Changed from absolute to fixed */
     top: 15px;
     left: 50%;
     transform: translateX(-50%);
     z-index: 1000;
     font-size: 14px;
     box-sizing: border-box;  /* Added for proper sizing */
    }

     /* Progress bar container */
     .progress-container {
     width: 90%;  /* Match HUD width */
     max-width: 1400px;  /* Match HUD max-width */
     position: fixed;  /* Changed from absolute */
     top: 55px;  /* Adjusted spacing from HUD */
     left: 50%;
     transform: translateX(-50%);
     z-index: 1000;
     box-sizing: border-box;
    }

     /* Base progress bar style */
     .progress-bar {
     background: rgba(68, 68, 68, 0.7);
     height: 8px;  /* Slightly thinner */
     width: 100%;
     border-radius: 4px;
     overflow: hidden;
     box-shadow: 0 2px 4px rgba(0,0,0,0.2);  /* Added depth */
    }

     /* Progress fill indicator */
     .progress-bar-fill {
     background: linear-gradient(90deg, #ff66cc, #ff3385);  /* Enhanced color */
     height: 100%;
     width: 0%;
     transition: width 0.3s ease-out;  /* Smoother transition */
    }
      button {
        background: #ff66cc;
        color: white;
        font-weight: bold;
        border: none;
        padding: 100px 200px;
        font-size: 18px;
        border-radius: 8px;
        cursor: pointer;
        margin: 10px auto;
        display: block;
        font-family: 'Press Start 2P', cursive;
      }
      .level-transition {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(0,0,0,0.8);
        color: white;
        padding: 20px;
        border-radius: 10px;
        font-family: 'Press Start 2P', cursive;
        text-align: center;
        z-index: 100;
      }
      :fullscreen {
        background-color: #121212;
      }
      :-webkit-full-screen {
        background-color: #121212;
      }
      :-moz-full-screen {
        background-color: #121212;
      }
      .win-screen {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: #0a0a23;
        display: none;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        color: white;
        font-family: 'Press Start 2P', cursive;
      }
      .video-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
        margin-top: 30px;
      }
      .video-container video {
        width: 100%;
        max-width: 400px;
        border: 3px solid #ff66cc;
      }
    </style>

    <div id="game-container">
      <button id='startButton'>START GAME</button>
      <canvas id="gameCanvas" width="800" height="400" tabindex="0"></canvas>
      <div class="hud">
        <div>❤️ Lives: <span id="lives">50</span></div>
        <div>🏆 Level: <span id="level">1</span>/5</div>
        <div>💀 Deaths: <span id="deaths">0</span></div>
        <div>⏱️ Time: <span id="timer">0</span>s</div>
      </div>
      <div class="progress-container">
        <div class="progress-bar"><div class="progress-bar-fill" id="progressFill"></div></div>
      </div>
      <div id="levelTransition" class="level-transition" style="display: none;"></div>
    </div>

    <div id="winScreen" class="win-screen">
      <h1 style="color: #ff66cc; font-size: 2.5rem; margin-bottom: 30px;">A Little Luca playing football</h1>
      <div class="drive-access-box" style="
        background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
        border-radius: 12px;
        padding: 25px;
        max-width: 500px;
        margin: 0 auto;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
     ">
      <div style="font-size: 1.8rem; margin-bottom: 15px; color: #fff;">Lesgoski</div>

      <a href="https://drive.google.com/drive/folders/1pQEcEw30mzKVgaOE4QIp8sXd-1E3yppb?usp=sharing" 

         target="_blank"
         style="
           display: inline-block;
           background: white;
           color: #ff66cc;
           padding: 12px 30px;
           border-radius: 50px;
           text-decoration: none;
           font-weight: bold;
           font-size: 1.1rem;
           transition: all 0.3s ease;
           box-shadow: 0 2px 10px rgba(0,0,0,0.1);
         "
         onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 5px 15px rgba(0,0,0,0.2)'"
         onmouseout="this.style.transform=''; this.style.boxShadow='0 2px 10px rgba(0,0,0,0.1)'">
         View Videos on Google Drive
      </a>

      <div style="margin-top: 20px; color: #fff; font-size: 0.9rem;">
      </div>
      </div>
    </div>

    <script>
    const canvas = document.getElementById('gameCanvas');
    const ctx = canvas.getContext('2d');
    const winScreen = document.getElementById('winScreen');
    let gameRunning = false;
    let keys = {};
    let level = 1;
    let maxLevel = 5;
    let lives = 50;
    let deaths = 0;
    let timer = 0;
    let interval;
    let gameStarted = false;
    let levelTransitionTime = 0;
    let animationFrameId = null;
    let isFullscreen = false;

    const gravity = 0.5;
    const playerSpeed = 4;

    let player = {
      x: 100,
      y: 100,
      width: 20,
      height: 30,
      dx: 0,
      dy: 0,
      speed: playerSpeed,
      jumpPower: -12,
      grounded: false,
      canDash: false,
    };

    let camera = { x: 0, y: 0 };
    let levelWidth = 5000;
    let movingBlocks = [];
    let ceilingBlocks = [];

    const levelData = {
      1: { 
        bg: '#121212',
        color: '#4cc9f0',
        platforms: [
          {x: 0, y: 380, w: 100, h: 30, deadly: true},
          {x: 100, y: 380, w: 100, h: 30},
          {x: 250, y: 320, w: 100, h: 20},
          {x: 400, y: 280, w: 80, h: 20},
          {x: 550, y: 250, w: 100, h: 20},
          {x: 700, y: 220, w: 100, h: 20},
          {x: 900, y: 300, w: 100, h: 20},
          {x: 1100, y: 270, w: 100, h: 20},
          {x: 1300, y: 240, w: 100, h: 20},
          {x: 1500, y: 210, w: 100, h: 20},
          {x: 1700, y: 300, w: 100, h: 20},
          {x: 1900, y: 270, w: 100, h: 20},
          {x: 2100, y: 240, w: 100, h: 20},
          {x: 2300, y: 210, w: 100, h: 20},
          {x: 2500, y: 180, w: 100, h: 20},
          {x: 2700, y: 150, w: 100, h: 20, goal: true}
        ],
        traps: [
          {x: 500, y: 280, w: 50, h: 10, deadly: true},
          {x: 800, y: 250, w: 50, h: 10, deadly: true},
          {x: 1200, y: 300, w: 50, h: 10, deadly: true},
          {x: 1600, y: 180, w: 50, h: 10, deadly: true},
          {x: 2000, y: 200, w: 50, h: 10, deadly: true},
          // Platform obstacles (short and high)
          {x: 400, y: 220, w: 30, h: 5, deadly: true},
          {x: 700, y: 180, w: 30, h: 5, deadly: true},
          {x: 1100, y: 200, w: 30, h: 5, deadly: true}
        ],
        ceilingBlocks: [],
        movingBlocks: []
      },

      2: { 
        bg: '#2a2a2a',
        color: '#f72585',
        platforms: [
          {x: 0, y: 370, w: 150, h: 30, deadly: true},
          {x: 150, y: 300, w: 130, h: 20},
          {x: 350, y: 270, w: 80, h: 20},
          {x: 500, y: 240, w: 80, h: 20},
          {x: 650, y: 330, w: 80, h: 20},
          {x: 800, y: 300, w: 80, h: 20},
          {x: 950, y: 270, w: 80, h: 20},
          {x: 1100, y: 240, w: 80, h: 20},
          {x: 1300, y: 330, w: 80, h: 20},
          {x: 1450, y: 300, w: 80, h: 20},
          {x: 1600, y: 270, w: 80, h: 20},
          {x: 1750, y: 240, w: 80, h: 20},
          {x: 1900, y: 210, w: 80, h: 20},
          {x: 2050, y: 180, w: 80, h: 20},
          {x: 2200, y: 150, w: 80, h: 20},
          {x: 2400, y: 120, w: 80, h: 20, goal: true}
        ],
        traps: [
          {x: 300, y: 300, w: 50, h: 10, deadly: true},
          {x: 600, y: 340, w: 50, h: 10, deadly: true},
          {x: 900, y: 280, w: 50, h: 10, deadly: true},
          {x: 1200, y: 240, w: 50, h: 10, deadly: true},
          {x: 1500, y: 240, w: 50, h: 10, deadly: true},
          {x: 1800, y: 200, w: 50, h: 10, deadly: true},
          {x: 2100, y: 160, w: 50, h: 10, deadly: true},
          // Platform obstacles (short and high)
          {x: 250, y: 220, w: 30, h: 5, deadly: true},
          {x: 550, y: 180, w: 30, h: 5, deadly: true},
          {x: 800, y: 200, w: 30, h: 5, deadly: true},
          {x: 1100, y: 160, w: 30, h: 5, deadly: true}
        ],
        ceilingBlocks: [
          {x: 400, y: 150, w: 40, h: 20},
          {x: 800, y: 130, w: 40, h: 20},
          {x: 1200, y: 110, w: 40, h: 20}
        ],
        movingBlocks: []
      },

      3: { 
        bg: '#1e1e2f',
        color: '#b5179e',
        platforms: [
          {x: 0, y: 370, w: 100, h: 30, deadly: true},
          {x: 150, y: 300, w: 60, h: 20},
          {x: 300, y: 330, w: 60, h: 20},
          {x: 450, y: 270, w: 60, h: 20},
          {x: 600, y: 300, w: 60, h: 20},
          {x: 750, y: 240, w: 60, h: 20},
          {x: 900, y: 270, w: 60, h: 20},
          {x: 1050, y: 210, w: 60, h: 20},
          {x: 1200, y: 240, w: 60, h: 20},
          {x: 1350, y: 180, w: 60, h: 20},
          {x: 1500, y: 210, w: 60, h: 20},
          {x: 1650, y: 150, w: 60, h: 20},
          {x: 1800, y: 180, w: 60, h: 20},
          {x: 1950, y: 120, w: 60, h: 20},
          {x: 2100, y: 150, w: 60, h: 20},
          {x: 2250, y: 90, w: 60, h: 20, goal: true}
        ],
        traps: [
          {x: 200, y: 280, w: 40, h: 10, deadly: true},
          {x: 400, y: 280, w: 40, h: 10, deadly: true},
          {x: 600, y: 135, w: 40, h: 10, deadly: true},
          {x: 900, y: 112, w: 40, h: 10, deadly: true},
          {x: 1200, y: 95, w: 40, h: 10, deadly: true},
          {x: 1500, y: 75, w: 40, h: 10, deadly: true},
          {x: 1900, y: 70, w: 40, h: 10, deadly: true},
          {x: 2200, y: 360, w: 40, h: 10, deadly: true},
          // Platform obstacles (short and high)
          {x: 150, y: 200, w: 30, h: 5, deadly: true},
          {x: 450, y: 180, w: 30, h: 5, deadly: true},
          {x: 750, y: 160, w: 30, h: 5, deadly: true},
          {x: 1050, y: 80, w: 30, h: 6, deadly: true}
        ],
        ceilingBlocks: [
          {x: 300, y: 150, w: 50, h: 20},
          {x: 600, y: 130, w: 50, h: 20},
          {x: 900, y: 110, w: 50, h: 20},
          {x: 1200, y: 90, w: 50, h: 20},
          {x: 1500, y: 70, w: 50, h: 20}
        ],
        movingBlocks: [
          {x: 1850, y: 180, w: 40, h: 20, speed: 2, range: 100, dir: 1, startX: 1800},
          {x: 2100, y: 180, w: 40, h: 20, speed: 3, range: 150, dir: 1, startX: 2100}
        ]
      },

      4: { 
        bg: '#003049',
        color: '#f8961e',
        platforms: [
          {x: 0, y: 370, w: 80, h: 30, deadly: true},
          {x: 120, y: 300, w: 50, h: 15},
          {x: 240, y: 250, w: 50, h: 15},
          {x: 360, y: 300, w: 50, h: 15},
          {x: 480, y: 200, w: 50, h: 15},
          {x: 600, y: 250, w: 50, h: 15},
          {x: 720, y: 150, w: 50, h: 15},
          {x: 840, y: 200, w: 50, h: 15},
          {x: 960, y: 100, w: 50, h: 15},
          {x: 1080, y: 150, w: 50, h: 15},
          {x: 1200, y: 300, w: 50, h: 15},
          {x: 1320, y: 250, w: 50, h: 15},
          {x: 1440, y: 200, w: 50, h: 15},
          {x: 1560, y: 150, w: 50, h: 15},
          {x: 1680, y: 100, w: 50, h: 15},
          {x: 1800, y: 50, w: 50, h: 15, goal: true}
        ],
        traps: [
          {x: 180, y: 275, w: 90, h: 10, deadly: true},
          {x: 420, y: 360, w: 30, h: 10, deadly: true},
          {x: 660, y: 360, w: 30, h: 10, deadly: true},
          {x: 900, y: 360, w: 30, h: 10, deadly: true},
          {x: 1140, y: 360, w: 30, h: 10, deadly: true},
          {x: 1380, y: 360, w: 30, h: 10, deadly: true},
          {x: 1620, y: 360, w: 30, h: 10, deadly: true},
          {x: 1860, y: 360, w: 30, h: 10, deadly: true},
          // Platform obstacles (short and high)
          {x: 145, y: 190, w: 30, h: 5, deadly: true},
          {x: 240, y: 160, w: 30, h: 5, deadly: true},
          {x: 360, y: 200, w: 30, h: 5, deadly: true},
          {x: 500, y: 195, w: 30, h: 5, deadly: true},
          {x: 600, y: 210, w: 15, h: 5, deadly: true}
        ],
        ceilingBlocks: [
          {x: 200, y: 150, w: 60, h: 15},
          {x: 400, y: 130, w: 50, h: 15},
          {x: 600, y: 110, w: 30, h: 15},
          {x: 800, y: 90, w: 40, h: 15},
          {x: 1000, y: 70, w: 40, h: 15},
          {x: 1200, y: 50, w: 40, h: 15}
        ],
        movingBlocks: [
          {x: 1400, y: 200, w: 40, h: 15, speed: 2.5, range: 120, dir: 1, startX: 1400},
          {x: 1600, y: 150, w: 40, h: 15, speed: 3, range: 150, dir: -1, startX: 1600},
          {x: 1800, y: 100, w: 40, h: 15, speed: 2, range: 100, dir: 1, startX: 1800}
        ]
      },

      5: {  
     bg: '#0a0a23',  
     color: '#ff006e',  
     platforms: [  
        // Piattaforma iniziale segmentata (OK-ROSSO-OK-ROSSO)  
        {x: 0, y: 370, w: 150, h: 30},  
        {x: 150, y: 370, w: 150, h: 30, deadly: true},  
        {x: 300, y: 370, w: 150, h: 30},  
        {x: 450, y: 370, w: 150, h: 30, deadly: true},  

        // Tunnel 1 (scelta tra 3, quello giusto è il centrale)  
        {x: 600, y: 300, w: 40, h: 10},  // Inizio tunnel (OK)  
        {x: 650, y: 250, w: 40, h: 10},  // Scelta 1 (falso, laterale sinistro)  
        {x: 750, y: 200, w: 40, h: 10},  // Scelta 2 (vero, centrale)  
        {x: 850, y: 250, w: 40, h: 10},  // Scelta 3 (falso, laterale destro)  
        {x: 900, y: 300, w: 40, h: 10},  // Uscita tunnel  

        // Pavimento rosso da saltare (nella scelta corretta)  
        {x: 770, y: 300, w: 20, h: 5, deadly: true},  

        // Tunnel 2 (scelta in alto, quello giusto è il destro)  
        {x: 1000, y: 200, w: 40, h: 10},  // Inizio tunnel  
        {x: 1050, y: 150, w: 40, h: 10},   // Scelta 1 (falso, sinistro)  
        {x: 1150, y: 100, w: 40, h: 10},  // Scelta 2 (vero, destro)  
        {x: 1250, y: 150, w: 40, h: 10},  // Scelta 3 (falso, centrale)  
        {x: 1300, y: 200, w: 40, h: 10},  // Uscita tunnel  

        // Pavimento rosso da saltare (nella scelta corretta)  
        {x: 1160, y: 180, w: 20, h: 5, deadly: true},  

        // Tunnel 3 (scelta ancora più in alto, quello giusto è il sinistro)  
        {x: 1400, y: 100, w: 40, h: 10},  // Inizio tunnel  
        {x: 1450, y: 50, w: 40, h: 10},   // Scelta 1 (vero, sinistro)  
        {x: 1550, y: 20, w: 40, h: 10},   // Scelta 2 (falso, centrale)  
        {x: 1650, y: 50, w: 40, h: 10},   // Scelta 3 (falso, destro)  
        {x: 1700, y: 100, w: 40, h: 10},  // Uscita tunnel  

        // Pavimento rosso da saltare (nella scelta corretta)  
        {x: 1460, y: 80, w: 20, h: 5, deadly: true},  

        // Piattaforma finale con traguardo  
        {x: 1800, y: 50, w: 40, h: 10, goal: true}  
     ],  
     traps: [  
        // Trappole nei tunnel sbagliati (tutte le pareti diventano rosse)  
        // Tunnel 1 (scelte sbagliate)  
        {x: 640, y: 240, w: 10, h: 60, deadly: true},  // Laterale sinistro  
        {x: 860, y: 240, w: 10, h: 60, deadly: true},  // Laterale destro  

        // Tunnel 2 (scelte sbagliate)  
        {x: 1040, y: 140, w: 10, h: 60, deadly: true},  // Sinistro  
        {x: 1260, y: 140, w: 10, h: 60, deadly: true},  // Centrale  

        // Tunnel 3 (scelte sbagliate)  
        {x: 1560, y: 10, w: 10, h: 60, deadly: true},   // Centrale  
        {x: 1660, y: 40, w: 10, h: 60, deadly: true},   // Destro  

        // Trappole mobili extra  
        {x: 500, y: 340, w: 20, h: 10, deadly: true, speed: 2, range: 100, dir: 1, startX: 500},  
        {x: 1100, y: 300, w: 20, h: 10, deadly: true, speed: 1.5, range: 80, dir: -1, startX: 1100},  
        {x: 1500, y: 200, w: 20, h: 10, deadly: true, speed: 2, range: 90, dir: 1, startX: 1500}  
     ],  
     ceilingBlocks: [  
        // Blocchi fissi sul soffitto per ostacoli  
        {x: 700, y: 50, w: 30, h: 10},  
        {x: 1200, y: 30, w: 30, h: 10},  
        {x: 1600, y: 10, w: 30, h: 10}  
     ]  
     }  
    };

    function resetGame() {
      const ld = levelData[level];
      canvas.style.backgroundColor = ld.bg;
      player = {
        x: 100,
        y: 100,
        width: 20,
        height: 30,
        dx: 0,
        dy: 0,
        speed: playerSpeed,
        jumpPower: -12,
        grounded: false,
        canDash: level >= 3,
      };
      camera.x = 0;
      levelWidth = ld.platforms[ld.platforms.length-1].x + 100;
      document.getElementById('progressFill').style.width = '0%';
      
      // Reset moving blocks
      movingBlocks = [];
      if (ld.movingBlocks) {
        movingBlocks = JSON.parse(JSON.stringify(ld.movingBlocks));
      }
      
      // Reset ceiling blocks
      ceilingBlocks = [];
      if (ld.ceilingBlocks) {
        ceilingBlocks = JSON.parse(JSON.stringify(ld.ceilingBlocks));
      }
    }

    function showLevelTransition() {
      const transition = document.getElementById('levelTransition');
      transition.style.display = 'block';
      transition.innerHTML = `<h2>LEVEL ${level}</h2><p>Get ready!</p>`;
      levelTransitionTime = 3;
      
      const countdown = setInterval(() => {
        levelTransitionTime--;
        if (levelTransitionTime <= 0) {
          clearInterval(countdown);
          transition.style.display = 'none';
          if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
          }
          animate();
        } else {
          transition.innerHTML = `<h2>LEVEL ${level}</h2><p>Starting in ${levelTransitionTime}...</p>`;
        }
      }, 1000);
    }

    function showWinScreen() {
      gameRunning = false;
      gameStarted = false;
      clearInterval(interval);
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
      winScreen.style.display = 'flex';
    }

    document.getElementById('startButton').onclick = function() {
      // Reset all game state
      gameRunning = true;
      gameStarted = true;
      level = 1;
      lives = 10;
      deaths = 0;
      timer = 0;
      
      // Hide win screen if shown
      winScreen.style.display = 'none';
      
      // Update UI
      document.getElementById('lives').textContent = lives;
      document.getElementById('deaths').textContent = deaths;
      document.getElementById('timer').textContent = timer;
      document.getElementById('level').textContent = level;
      
      // Reset timer
      clearInterval(interval);
      interval = setInterval(() => {
        timer++;
        document.getElementById('timer').textContent = timer;
      }, 1000);
      
      // Fullscreen
      if (canvas.requestFullscreen) {
        canvas.requestFullscreen().catch(err => {
          console.error('Error attempting to enable fullscreen:', err);
        }).then(() => {
          // After entering fullscreen, reposition HUD
          document.querySelector('.hud').style.top = '10px';
          document.querySelector('.progress-container').style.top = '60px';
        });
      }
      
      // Start game
      resetGame();
      showLevelTransition();
      canvas.focus();
      
      // Cancel any existing animation
      if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
      }
      animate();
    };

    // Handle fullscreen change to adjust HUD position
    document.addEventListener('fullscreenchange', function() {
      if (document.fullscreenElement) {
        document.querySelector('.hud').style.top = '10px';
        document.querySelector('.progress-container').style.top = '60px';
      } else {
        document.querySelector('.hud').style.top = '10px';
        document.querySelector('.progress-container').style.top = '60px';
      }
    });

    document.addEventListener('keydown', e => keys[e.key] = true);
    document.addEventListener('keyup', e => keys[e.key] = false);

    function loseLife() {
      deaths++;
      document.getElementById('deaths').textContent = deaths;
      lives--;
      document.getElementById('lives').textContent = lives;
      
      if (lives <= 0) {
        gameRunning = false;
        gameStarted = false;
        clearInterval(interval);
        if (document.exitFullscreen) {
          document.exitFullscreen();
        }
        setTimeout(() => {
          alert(`💀 GAME OVER!\nLevel: ${level}\nTime: ${timer}s\nDeaths: ${deaths}`);
        }, 100);
      } else {
        resetGame();
        if (animationFrameId) {
          cancelAnimationFrame(animationFrameId);
        }
        animate();
      }
    }

    function updateProgressBar() {
      const progress = Math.min((player.x / levelWidth) * 100, 100);
      document.getElementById('progressFill').style.width = progress + '%';
    }

    function updateMovingBlocks() {
      for (let i = 0; i < movingBlocks.length; i++) {
        const block = movingBlocks[i];
        block.x += block.speed * block.dir;
        
        if (block.dir > 0 && block.x > block.startX + block.range) {
          block.dir = -1;
        } else if (block.dir < 0 && block.x < block.startX) {
          block.dir = 1;
        }
      }
    }

    function animate() {
      if (!gameRunning || levelTransitionTime > 0) {
        animationFrameId = requestAnimationFrame(animate);
        return;
      }
      
      animationFrameId = requestAnimationFrame(animate);
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Update moving blocks
      updateMovingBlocks();

      // Movement
      player.dx = 0;
      if (keys['ArrowRight'] || keys['d']) player.dx = player.speed;
      if (keys['ArrowLeft'] || keys['a']) player.dx = -player.speed;
      if ((keys['w'] || keys['ArrowUp']) && player.grounded) {
        player.dy = player.jumpPower;
        player.grounded = false;
      }
      if (player.canDash && (keys[' '] || keys['Spacebar'])) {
        player.dx *= 5; // Increased dash power
        player.canDash = false;
      }

      // Physics
      player.dy += gravity;
      player.x += player.dx;
      player.y += player.dy;
      player.grounded = false;

      // Camera
      camera.x = player.x - canvas.width / 2 + player.width / 2;
      if (camera.x < 0) camera.x = 0;

      // Draw with camera offset
      ctx.save();
      ctx.translate(-camera.x, 0);

      const ld = levelData[level];

      // Draw platforms
      for (let plat of ld.platforms) {
        ctx.fillStyle = plat.goal ? '#4ad66d' : plat.deadly ? '#ff0000' : ld.color;
        ctx.fillRect(plat.x, plat.y, plat.w, plat.h);
      }

      // Draw traps
      ctx.fillStyle = '#ff0000';
      for (let trap of ld.traps) {
        ctx.fillRect(trap.x, trap.y, trap.w, trap.h);
      }

      // Draw ceiling blocks
      ctx.fillStyle = '#888';
      for (let block of ceilingBlocks) {
        ctx.fillRect(block.x, block.y, block.w, block.h);
      }

      // Draw moving blocks
      ctx.fillStyle = '#ff66cc';
      for (let block of movingBlocks) {
        ctx.fillRect(block.x, block.y, block.w, block.h);
      }

      // Collision detection
      let isOnPlatform = false;
      
      // Check platform collisions
      for (let plat of ld.platforms) {
        if (player.x < plat.x + plat.w &&
            player.x + player.width > plat.x &&
            player.y < plat.y + plat.h &&
            player.y + player.height > plat.y) {
          
          if (plat.deadly) {
            loseLife();
            ctx.restore();
            return;
          }
          
          if (player.dy > 0) {
            player.y = plat.y - player.height;
            player.dy = 0;
            player.grounded = true;
            player.canDash = level >= 3;
            isOnPlatform = true;
            
            if (plat.goal) {
              level++;
              if (level > maxLevel) {
                showWinScreen();
                ctx.restore();
                return;
              }
              
              // Reset for new level
              lives = 10 ;
              document.getElementById('lives').textContent = lives;
              document.getElementById('level').textContent = level;
              
              resetGame();
              showLevelTransition();
              ctx.restore();
              return;
            }
          }
        }
      }

      // Check trap collisions
      for (let trap of ld.traps) {
        if (player.x < trap.x + trap.w &&
            player.x + player.width > trap.x &&
            player.y < trap.y + trap.h &&
            player.y + player.height > trap.y) {
          loseLife();
          ctx.restore();
          return;
        }
      }

      // Check ceiling block collisions
      for (let block of ceilingBlocks) {
        if (player.x < block.x + block.w &&
            player.x + player.width > block.x &&
            player.y < block.y + block.h &&
            player.y + player.height > block.y) {
          // Hit head on ceiling
          player.dy = 0;
          player.y = block.y + block.h;
        }
      }

      // Check moving block collisions
      for (let block of movingBlocks) {
        if (player.x < block.x + block.w &&
            player.x + player.width > block.x &&
            player.y < block.y + block.h &&
            player.y + player.height > block.y) {
          
          // If coming from above
          if (player.dy > 0 && player.y + player.height - 5 < block.y + block.h) {
            player.y = block.y - player.height;
            player.dy = 0;
            player.grounded = true;
            player.canDash = level >= 3;
            isOnPlatform = true;
          } else {
            // Otherwise it's a collision
            loseLife();
            ctx.restore();
            return;
          }
        }
      }

      // Falling check
      if (!isOnPlatform && player.y > canvas.height) {
        loseLife();
        ctx.restore();
        return;
      }

      // Draw player
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(player.x, player.y, player.width, player.height);

      ctx.restore();

      updateProgressBar();
    }
    </script>
    """

    components.html(game_code, height=700)
