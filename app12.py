import streamlit as st
from datetime import datetime
import folium
from streamlit_folium import folium_static
from PIL import Image
import os

# ---- CONFIGURATION ----
st.set_page_config(
    page_title="Luca & Ewa | Our Time",
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
</style>
""", unsafe_allow_html=True)

# ---- PASSWORD AUTH ----
# ---- THEME SWITCH ----
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True  
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode
if st.session_state.dark_mode:
    st.info("For better viewing experience, it is recommended to use the **light theme**.")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
        <div class='main-title'>🔒 Welcome to Our Time</div>
        <p style='text-align:center;'>Please enter the password to unlock the experience.</p>
        <p style='text-align:center; font-style: italic;'>Hint: city where I end up after you make a joke about a cute girl</p>
    """, unsafe_allow_html=True)
    pw = st.text_input("Password", type="password")
    if pw == "nojokolandia":
        st.session_state.authenticated = True
        st.rerun()
    else:
        if pw:
            st.error("Incorrect password")
    st.stop()

# ---- MAIN UI ----
st.markdown("<div class='main-title'>Luca & Ewa | Our Time</div>", unsafe_allow_html=True)

# ---- COUNTDOWN SECTION ----
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

# ---- MAP WITH EXPERIENCES ----
st.markdown("""
<div class='section-title'>📍 Our Places</div> """, unsafe_allow_html=True)

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
        "photos": ["alassio", "alassio2", "alassio3", "alassio4"],
        "captions": [
            "A cute girl on the phone (classic)",
            "Eyes (yours better)",
            "4 types of Ligurian Focaccia/Pizza and my type of girl",
            "Worst sandwich ever, with scam stuff from TooGoodToGo"
        ]
    },
    {
        "coords": [45.5739, 9.1641], 
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
        "coords": [45.5739, 9.1641], 
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
    }
]

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
