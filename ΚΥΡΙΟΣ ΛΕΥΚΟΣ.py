import streamlit as st
import streamlit.components.v1 as components
import random
import json
import os

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="ΚΥΡΙΟΣ ΛΕΥΚΟΣ",
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    h1 {
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 900 !important;
        background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #ffe66d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem !important;
        letter-spacing: 3px;
    }
    h2, h3 {
        color: #4ecdc4 !important;
        font-weight: 700 !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102,126,234,0.6) !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        box-shadow: 0 4px 15px rgba(245,87,108,0.4) !important;
    }
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.1) !important;
        border: 2px solid rgba(78,205,196,0.3) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 0.8rem !important;
        font-size: 1rem !important;
    }
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.1) !important;
        border: 2px solid rgba(78,205,196,0.3) !important;
        border-radius: 12px !important;
    }
    hr {
        border-color: rgba(78,205,196,0.2) !important;
        margin: 2rem 0 !important;
    }
    .stAlert {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 12px !important;
        border-left: 4px solid #4ecdc4 !important;
    }
    .stMarkdown { color: #e0e0e0; }
</style>
""", unsafe_allow_html=True)

# ================= FILES =================
PLAYERS_FILE = "players.json"
GAME_FILE = "game.json"

# ================= WORDS =================
WORDS = [
("ΣΚΥΛΟΣ", "ΚΟΚΑΛΟ"), ("ΓΑΤΑ", "ΠΟΝΤΙΚΙ"), ("ΣΚΥΛΟΣ", "ΛΟΥΡΙ"), ("ΓΑΤΑ", "ΝΙΑΟΥΡΙΣΜΑ"), ("ΠΟΥΛΙ", "ΦΤΕΡΟ"), ("ΨΑΡΙ", "ΝΕΡΟ"), ("ΑΛΟΓΟ", "ΣΤΑΒΛΟΣ"), ("ΑΓΕΛΑΔΑ", "ΓΑΛΑ"), ("ΠΡΟΒΑΤΟ", "ΜΑΛΛΙ"), ("ΚΑΤΣΙΚΙ", "ΦΑΡΜΑ"),
("ΘΑΛΑΣΣΑ", "ΚΥΜΑ"), ("ΘΑΛΑΣΣΑ", "ΑΛΑΤΙ"), ("ΛΙΜΝΗ", "ΝΕΡΟ"), ("ΠΟΤΑΜΙ", "ΡΟΗ"), ("ΒΟΥΝΟ", "ΚΟΡΥΦΗ"), ("ΔΑΣΟΣ", "ΔΕΝΤΡΟ"), ("ΔΕΝΤΡΟ", "ΦΥΛΛΟ"), ("ΦΥΛΛΟ", "ΚΛΑΔΙ"), ("ΛΟΥΛΟΥΔΙ", "ΠΕΤΑΛΟ"), ("ΧΟΡΤΑΡΙ", "ΓΗΠΕΔΟ"),
("ΗΛΙΟΣ", "ΖΕΣΤΗ"), ("ΦΕΓΓΑΡΙ", "ΝΥΧΤΑ"), ("ΟΥΡΑΝΟΣ", "ΣΥΝΝΕΦΟ"), ("ΒΡΟΧΗ", "ΟΜΠΡΕΛΑ"), ("ΧΙΟΝΙ", "ΠΑΓΟΣ"), ("ΑΝΕΜΟΣ", "ΦΥΣΗΜΑ"), ("ΚΑΤΑΙΓΙΔΑ", "ΒΡΟΝΤΗ"), ("ΑΣΤΡΑΠΗ", "ΦΩΣ"), ("ΚΑΙΡΟΣ", "ΠΡΟΒΛΕΨΗ"), ("ΘΕΡΜΟΚΡΑΣΙΑ", "ΖΕΣΤΗ"),
("ΣΠΙΤΙ", "ΠΟΡΤΑ"), ("ΣΠΙΤΙ", "ΠΑΡΑΘΥΡΟ"), ("ΔΩΜΑΤΙΟ", "ΚΡΕΒΑΤΙ"), ("ΚΟΥΖΙΝΑ", "ΦΟΥΡΝΟΣ"), ("ΜΠΑΝΙΟ", "ΝΕΡΟ"), ("ΣΑΛΟΝΙ", "ΚΑΝΑΠΕΣ"), ("ΤΡΑΠΕΖΙ", "ΚΑΡΕΚΛΑ"), ("ΝΤΟΥΛΑΠΑ", "ΡΟΥΧΑ"), ("ΚΛΕΙΔΙ", "ΚΛΕΙΔΑΡΙΑ"), ("ΦΩΣ", "ΔΙΑΚΟΠΤΗΣ"),
("ΑΥΤΟΚΙΝΗΤΟ", "ΤΡΟΧΟΣ"), ("ΑΥΤΟΚΙΝΗΤΟ", "ΒΕΝΖΙΝΗ"), ("ΜΗΧΑΝΗ", "ΚΡΑΝΟΣ"), ("ΠΟΔΗΛΑΤΟ", "ΠΕΤΑΛΙ"), ("ΛΕΩΦΟΡΕΙΟ", "ΣΤΑΣΗ"), ("ΤΡΕΝΟ", "ΓΡΑΜΜΗ"), ("ΑΕΡΟΠΛΑΝΟ", "ΠΤΗΣΗ"), ("ΠΛΟΙΟ", "ΛΙΜΑΝΙ"), ("ΤΑΞΙ", "ΟΔΗΓΟΣ"), ("ΔΡΟΜΟΣ", "ΚΙΝΗΣΗ"),
("ΑΝΘΡΩΠΟΣ", "ΠΡΟΣΩΠΟ"), ("ΑΝΘΡΩΠΟΣ", "ΧΕΡΙ"), ("ΠΑΙΔΙ", "ΣΧΟΛΕΙΟ"), ("ΜΑΘΗΤΗΣ", "ΒΙΒΛΙΟ"), ("ΔΑΣΚΑΛΟΣ", "ΠΙΝΑΚΑΣ"), ("ΓΙΑΤΡΟΣ", "ΝΟΣΟΚΟΜΕΙΟ"), ("ΝΟΣΟΚΟΜΑ", "ΣΥΡΙΓΓΑ"), ("ΑΣΤΥΝΟΜΙΚΟΣ", "ΣΗΜΑ"), ("ΠΥΡΟΣΒΕΣΤΗΣ", "ΦΩΤΙΑ"), ("ΜΑΓΕΙΡΑΣ", "ΤΗΓΑΝΙ"),
("ΨΩΜΙ", "ΦΟΥΡΝΟΣ"), ("ΤΥΡΙ", "ΓΑΛΑ"), ("ΓΑΛΑ", "ΠΟΤΗΡΙ"), ("ΝΕΡΟ", "ΜΠΟΥΚΑΛΙ"), ("ΚΑΦΕΣ", "ΚΟΥΠΑ"), ("ΤΣΑΙ", "ΦΛΙΤΖΑΝΙ"), ("ΖΑΧΑΡΗ", "ΓΛΥΚΟ"), ("ΑΛΑΤΙ", "ΓΕΥΣΗ"), ("ΡΥΖΙ", "ΠΙΑΤΟ"), ("ΜΑΚΑΡΟΝΙΑ", "ΣΑΛΤΣΑ"),
("ΜΗΛΟ", "ΔΕΝΤΡΟ"), ("ΠΟΡΤΟΚΑΛΙ", "ΦΛΟΥΔΑ"), ("ΜΠΑΝΑΝΑ", "ΦΛΟΥΔΑ"), ("ΚΕΡΑΣΙ", "ΚΟΥΚΟΥΤΣΙ"), ("ΚΑΡΠΟΥΖΙ", "ΣΠΟΡΟΣ"), ("ΣΤΑΦΥΛΙ", "ΡΟΓΕΣ"), ("ΛΕΜΟΝΙ", "ΞΙΝΟ"), ("ΦΡΑΟΥΛΑ", "ΚΟΚΚΙΝΟ"), ("ΑΧΛΑΔΙ", "ΓΛΥΚΟ"), ("ΡΟΔΑΚΙΝΟ", "ΖΟΥΜΕΡΟ"),
("ΒΙΒΛΙΟ", "ΣΕΛΙΔΑ"), ("ΣΕΛΙΔΑ", "ΚΕΙΜΕΝΟ"), ("ΛΕΞΗ", "ΓΡΑΜΜΑ"), ("ΣΤΥΛΟ", "ΜΕΛΑΝΙ"), ("ΜΟΛΥΒΙ", "ΞΥΛΟ"), ("ΧΑΡΤΙ", "ΣΗΜΕΙΩΣΗ"), ("ΠΙΝΑΚΑΣ", "ΚΙΜΩΛΙΑ"), ("ΣΧΟΛΕΙΟ", "ΤΑΞΗ"), ("ΔΙΑΒΑΣΜΑ", "ΜΑΘΗΣΗ"), ("ΕΞΕΤΑΣΗ", "ΒΑΘΜΟΣ"),
("ΚΙΘΑΡΑ", "ΧΟΡΔΗ"), ("ΠΙΑΝΟ", "ΠΛΗΚΤΡΟ"), ("ΤΡΑΓΟΥΔΙ", "ΦΩΝΗ"), ("ΜΟΥΣΙΚΗ", "ΡΥΘΜΟΣ"), ("ΝΤΡΑΜΣ", "ΜΠΑΣΟ"), ("ΒΙΟΛΙ", "ΔΟΞΑΡΙ"), ("ΣΥΝΑΥΛΙΑ", "ΣΚΗΝΗ"), ("ΧΕΙΡΟΚΡΟΤΗΜΑ", "ΚΟΙΝΟ"), ("ΤΡΑΓΟΥΔΙΣΤΗΣ", "ΜΙΚΡΟΦΩΝΟ"), ("ΧΟΡΟΣ", "ΚΙΝΗΣΗ"),
("ΤΑΙΝΙΑ", "ΟΘΟΝΗ"), ("ΚΙΝΗΜΑΤΟΓΡΑΦΟΣ", "ΕΙΣΙΤΗΡΙΟ"), ("ΗΘΟΠΟΙΟΣ", "ΡΟΛΟΣ"), ("ΣΚΗΝΟΘΕΤΗΣ", "ΚΑΜΕΡΑ"), ("ΦΩΤΟΓΡΑΦΙΑ", "ΦΛΑΣ"), ("ΚΑΜΕΡΑ", "ΦΑΚΟΣ"), ("ΤΗΛΕΟΡΑΣΗ", "ΚΑΝΑΛΙ"), ("ΤΗΛΕΦΩΝΟ", "ΚΛΗΣΗ"), ("ΜΗΝΥΜΑ", "CHAT"), ("INTERNET", "ΙΣΤΟΣΕΛΙΔΑ"),
("ΔΟΥΛΕΙΑ", "ΓΡΑΦΕΙΟ"), ("ΓΡΑΦΕΙΟ", "ΥΠΟΛΟΓΙΣΤΗΣ"), ("ΥΠΟΛΟΓΙΣΤΗΣ", "ΠΛΗΚΤΡΟΛΟΓΙΟ"), ("ΠΟΝΤΙΚΙ", "ΚΛΙΚ"), ("ΟΘΟΝΗ", "PIXELS"), ("ΛΟΓΙΣΜΙΚΟ", "ΕΦΑΡΜΟΓΗ"), ("ΚΩΔΙΚΑΣ", "ΠΡΟΓΡΑΜΜΑ"), ("ΔΕΔΟΜΕΝΑ", "ΑΡΧΕΙΟ"), ("ΦΑΚΕΛΟΣ", "ΕΓΓΡΑΦΟ"), ("ΕΚΤΥΠΩΣΗ", "ΕΚΤΥΠΩΤΗΣ"),
("ΑΓΑΠΗ", "ΚΑΡΔΙΑ"), ("ΦΙΛΙΑ", "ΕΜΠΙΣΤΟΣΥΝΗ"), ("ΧΑΡΑ", "ΓΕΛΙΟ"), ("ΛΥΠΗ", "ΔΑΚΡΥ"), ("ΦΟΒΟΣ", "ΣΚΟΤΑΔΙ"), ("ΘΥΜΟΣ", "ΦΩΝΗ"), ("ΗΡΕΜΙΑ", "ΣΙΩΠΗ"), ("ΟΝΕΙΡΟ", "ΥΠΝΟΣ"), ("ΜΝΗΜΗ", "ΠΑΡΕΛΘΟΝ"), ("ΕΛΠΙΔΑ", "ΜΕΛΛΟΝ"),
("ΧΡΟΝΟΣ", "ΡΟΛΟΙ"), ("ΩΡΑ", "ΛΕΠΤΟ"), ("ΜΕΡΑ", "ΝΥΧΤΑ"), ("ΕΒΔΟΜΑΔΑ", "ΣΑΒΒΑΤΟΚΥΡΙΑΚΟ"), ("ΜΗΝΑΣ", "ΗΜΕΡΟΛΟΓΙΟ"), ("ΧΘΕΣ", "ΣΗΜΕΡΑ"), ("ΑΥΡΙΟ", "ΜΕΛΛΟΝ"), ("ΣΤΙΓΜΗ", "ΔΕΥΤΕΡΟΛΕΠΤΟ"), ("ΑΙΩΝΑΣ", "ΙΣΤΟΡΙΑ"), ("ΠΑΡΕΛΘΟΝ", "ΜΝΗΜΗ"),
("ΧΡΗΜΑ", "ΝΟΜΙΣΜΑ"), ("ΕΥΡΩ", "ΚΕΡΜΑ"), ("ΤΡΑΠΕΖΑ", "ΛΟΓΑΡΙΑΣΜΟΣ"), ("ΑΓΟΡΑ", "ΠΩΛΗΤΗΣ"), ("ΚΑΤΑΣΤΗΜΑ", "ΠΡΟΪΟΝ"), ("ΤΙΜΗ", "ΚΟΣΤΟΣ"), ("ΑΓΟΡΑΖΩ", "ΠΟΥΛΑΩ"), ("ΚΕΡΔΟΣ", "ΖΗΜΙΑ"), ("ΕΠΕΝΔΥΣΗ", "ΡΙΣΚΟ"), ("ΜΙΣΘΟΣ", "ΔΟΥΛΕΙΑ"),
("ΠΟΛΗ", "ΚΤΙΡΙΟ"), ("ΧΩΡΙΟ", "ΑΓΡΟΤΗΣ"), ("ΔΡΟΜΟΣ", "ΠΕΖΟΔΡΟΜΙΟ"), ("ΠΛΑΤΕΙΑ", "ΚΑΦΕ"), ("ΓΕΦΥΡΑ", "ΠΟΤΑΜΙ"), ("ΣΤΑΘΜΟΣ", "ΤΡΕΝΟ"), ("ΑΕΡΟΔΡΟΜΙΟ", "ΠΤΗΣΗ"), ("ΛΙΜΑΝΙ", "ΠΛΟΙΟ"), ("ΓΕΙΤΟΝΙΑ", "ΣΠΙΤΙΑ"), ("ΧΑΡΤΗΣ", "ΠΡΟΟΡΙΣΜΟΣ"),
("ΕΓΚΕΦΑΛΟΣ", "ΣΚΕΨΗ"), ("ΜΑΤΙ", "ΟΡΑΣΗ"), ("ΑΥΤΙ", "ΗΧΟΣ"), ("ΧΕΡΙ", "ΔΑΧΤΥΛΟ"), ("ΠΟΔΙ", "ΒΗΜΑ"), ("ΣΤΟΜΑ", "ΟΜΙΛΙΑ"), ("ΜΥΤΗ", "ΜΥΡΩΔΙΑ"), ("ΔΕΡΜΑ", "ΑΦΗ"), ("ΚΑΡΔΙΑ", "ΠΑΛΜΟΣ"), ("ΣΩΜΑ", "ΥΓΕΙΑ"),
("ΠΟΛΕΜΟΣ", "ΣΤΡΑΤΟΣ"), ("ΕΙΡΗΝΗ", "ΣΥΜΦΩΝΙΑ"), ("ΟΠΛΟ", "ΣΦΑΙΡΑ"), ("ΜΑΧΗ", "ΝΙΚΗ"), ("ΗΤΤΑ", "ΑΠΩΛΕΙΑ"), ("ΣΤΡΑΤΗΓΟΣ", "ΣΧΕΔΙΟ"), ("ΣΥΓΚΡΟΥΣΗ", "ΕΝΤΑΣΗ"), ("ΑΣΦΑΛΕΙΑ", "ΦΥΛΑΞΗ"), ("ΚΙΝΔΥΝΟΣ", "ΦΟΒΟΣ"), ("ΗΡΩΑΣ", "ΘΑΡΡΟΣ"),
("ΤΕΧΝΟΛΟΓΙΑ", "ΚΑΙΝΟΤΟΜΙΑ"), ("ΕΠΙΣΤΗΜΗ", "ΕΡΕΥΝΑ"), ("ΠΕΙΡΑΜΑ", "ΔΟΚΙΜΗ"), ("ΘΕΩΡΙΑ", "ΑΠΟΔΕΙΞΗ"), ("ΜΑΘΗΜΑΤΙΚΑ", "ΑΡΙΘΜΟΣ"), ("ΦΥΣΙΚΗ", "ΔΥΝΑΜΗ"), ("ΧΗΜΕΙΑ", "ΣΤΟΙΧΕΙΟ"), ("ΒΙΟΛΟΓΙΑ", "ΖΩΗ"), ("DNA", "ΓΟΝΙΔΙΟ"), ("ΥΠΟΘΕΣΗ", "ΠΕΙΡΑΜΑ")
]

# ================= LOAD / SAVE =================
def load_players():
    if os.path.exists(PLAYERS_FILE):
        try:
            with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []

def save_players(players):
    with open(PLAYERS_FILE, "w", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=2)

def load_game():
    if os.path.exists(GAME_FILE):
        try:
            with open(GAME_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            os.remove(GAME_FILE)
            return None
    return None

def save_game(game):
    with open(GAME_FILE, "w", encoding="utf-8") as f:
        json.dump(game, f, ensure_ascii=False, indent=2)

# ================= INIT =================
if "game" not in st.session_state:
    st.session_state.game = load_game()
if "revealed" not in st.session_state:
    st.session_state.revealed = {}
if "last_out" not in st.session_state:
    st.session_state.last_out = None
if "mr_white_guess_mode" not in st.session_state:
    st.session_state.mr_white_guess_mode = False
if "mr_white_won" not in st.session_state:
    st.session_state.mr_white_won = False
if "finished" not in st.session_state:
    st.session_state.finished = False
if "winner" not in st.session_state:
    st.session_state.winner = None
if "selected_players" not in st.session_state:
    st.session_state.selected_players = []

# ================= HELPERS =================
def assign_roles(players):
    roles = ["mr_white", "undercover"] + ["πολίτης"] * (len(players) - 2)
    random.shuffle(players)
    random.shuffle(roles)
    assigned = []
    for i, player in enumerate(players):
        assigned.append({"name": player, "role": roles[i]})
    return assigned

def check_winner(players):
    roles = [p["role"] for p in players]
    civilians   = roles.count("πολίτης")
    undercovers = roles.count("undercover")
    mr_whites   = roles.count("mr_white")
    if civilians <= 1 and (undercovers + mr_whites) > 0:
        return "INFILTRATORS"
    if undercovers == 0 and mr_whites == 0:
        return "CIVILIANS"
    return None

def reset_game():
    st.session_state.game = None
    st.session_state.revealed = {}
    st.session_state.last_out = None
    st.session_state.mr_white_guess_mode = False
    st.session_state.mr_white_won = False
    st.session_state.finished = False
    st.session_state.winner = None
    st.session_state.selected_players = []
    if os.path.exists(GAME_FILE):
        os.remove(GAME_FILE)

# ================= UI =================
st.markdown("<h1>🎭 ΚΥΡΙΟΣ ΛΕΥΚΟΣ</h1>", unsafe_allow_html=True)

# ================= END SCREEN =================
if st.session_state.finished:
    game = st.session_state.game
    winner = st.session_state.winner

    st.divider()
    if winner == "⚪ MR WHITE":
        st.markdown("<h2 style='text-align: center; font-size: 2.5rem;'>⚪ Νίκησε ο Mr. White!</h2>", unsafe_allow_html=True)
    elif winner == "🟡 INFILTRATORS":
        st.markdown("<h2 style='text-align: center; font-size: 2.5rem;'>🟡 Νίκησαν οι Undercovers!</h2>", unsafe_allow_html=True)
    elif winner == "🟢 CIVILIANS":
        st.markdown("<h2 style='text-align: center; font-size: 2.5rem;'>🟢 Νίκησαν οι Πολίτες!</h2>", unsafe_allow_html=True)
    st.divider()

    if st.button("🔄 Νέο Παιχνίδι", type="primary", use_container_width=True):
        reset_game()
        st.rerun()

# ================= SETUP PHASE =================
elif st.session_state.game is None:
    st.subheader("👥 Επιλογή Παικτών")
    all_players = load_players()

    col_input, col_btn = st.columns([3, 1])
    with col_input:
        new_name = st.text_input("Προσθήκη νέου παίκτη", placeholder="Γράψε όνομα...", label_visibility="collapsed")
    with col_btn:
        if st.button("➕ Προσθήκη", use_container_width=True):
            if new_name and new_name.strip():
                all_players = load_players()
                clean_name = new_name.strip()
                if clean_name not in all_players:
                    all_players.append(clean_name)
                    save_players(all_players)
                    st.rerun()
                else:
                    st.warning(f"Ο παίκτης '{clean_name}' υπάρχει ήδη!")

    st.divider()

    if all_players:
        st.markdown("**📋 Διαθέσιμοι παίκτες:**")
        for name in all_players:
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                if name in st.session_state.selected_players:
                    st.markdown(f"✅ **{name}**")
                else:
                    st.markdown(f"**{name}**")
            with col2:
                if name not in st.session_state.selected_players:
                    if st.button("➕", key=f"add_{name}"):
                        st.session_state.selected_players.append(name)
                        st.rerun()
                else:
                    if st.button("➖", key=f"remove_{name}"):
                        st.session_state.selected_players.remove(name)
                        st.rerun()
            with col3:
                if st.button("🗑", key=f"del_{name}"):
                    all_players = load_players()
                    all_players.remove(name)
                    save_players(all_players)
                    if name in st.session_state.selected_players:
                        st.session_state.selected_players.remove(name)
                    st.rerun()
    else:
        st.info("💡 Δεν υπάρχουν αποθηκευμένοι παίκτες. Πρόσθεσε τον πρώτο!")

    st.divider()

    if st.session_state.selected_players:
        st.markdown(f"**🎮 Παίκτες στο παιχνίδι ({len(st.session_state.selected_players)}):**")
        st.success(", ".join(st.session_state.selected_players))
        if len(st.session_state.selected_players) < 3:
            st.warning(f"⚠️ Χρειάζονται τουλάχιστον 3 παίκτες (έχεις {len(st.session_state.selected_players)})")
    else:
        st.info("💡 Πάτα ➕ δίπλα από κάθε παίκτη για να τον προσθέσεις στο παιχνίδι")

    st.divider()

    if st.button("▶️ ΕΝΑΡΞΗ ΠΑΙΧΝΙΔΙΟΥ",
                 disabled=len(st.session_state.selected_players) < 3,
                 type="primary",
                 use_container_width=True):
        players_with_roles = assign_roles(st.session_state.selected_players.copy())
        st.session_state.game = {
            "players": players_with_roles,
            "all_players": [p.copy() for p in players_with_roles],
            "word": random.choice(WORDS),
        }
        save_game(st.session_state.game)
        for p in st.session_state.game["players"]:
            st.session_state.revealed[p["name"]] = False
        st.session_state.selected_players = []
        st.rerun()

# ================= GAME PHASE =================
else:
    game = st.session_state.game
    players = game["players"]
    word = game["word"]

    st.markdown("<h3 style='text-align: center;'>🎮 ΠΑΙΚΤΕΣ</h3>", unsafe_allow_html=True)
    st.caption("👀 Πάτα την κάρτα σου για να δεις τον ρόλο σου — μόνος/η σου!")

    cards_data = []
    for p in players:
        if p["role"] == "mr_white":
            back_role = "⚪ MR WHITE"
            back_word = ""
            back_color = "#c0392b"
            back_text_color = "#fff"
        elif p["role"] == "undercover":
            back_role = "🟡 UNDERCOVER"
            back_word = word[1]
            back_color = "#d68910"
            back_text_color = "#fff"
        else:
            back_role = "🟢 ΠΟΛΙΤΗΣ"
            back_word = word[0]
            back_color = "#1e8449"
            back_text_color = "#fff"

        cards_data.append({
            "name": p["name"],
            "back_role": back_role,
            "back_word": back_word,
            "back_color": back_color,
            "back_text_color": back_text_color,
        })

    import json as _json
    cards_json = _json.dumps(cards_data, ensure_ascii=False)

    # Calculate height based on number of players
    num_players = len(players)
    cards_per_row = 3
    num_rows = (num_players + cards_per_row - 1) // cards_per_row
    card_height = 240
    gap = 20
    padding = 60
    total_height = num_rows * card_height + (num_rows - 1) * gap + padding

    cards_html = f"""
    <style>
      body {{ margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: transparent; }}
      .cards-grid {{
        display: flex;
        flex-wrap: wrap;
        gap: {gap}px;
        justify-content: center;
        padding: 10px 0;
        overflow: visible;
      }}
      .card-wrap {{
        width: 160px;
        height: {card_height}px;
        perspective: 1000px;
        cursor: pointer;
        overflow: visible;
      }}
      .card-inner {{
        position: relative;
        width: 100%;
        height: 100%;
        transform-style: preserve-3d;
        transition: transform 0.7s cubic-bezier(0.4, 0.0, 0.2, 1);
      }}
      .card-wrap.flipped .card-inner {{
        transform: rotateX(180deg);
      }}
      .card-front, .card-back {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border-radius: 16px;
        backface-visibility: hidden;
        -webkit-backface-visibility: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 16px;
        box-sizing: border-box;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
      }}
      .card-front {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff;
      }}
      .card-back {{
        transform: rotateX(180deg);
        color: #fff;
      }}
      .card-front .card-icon {{
        font-size: 40px;
        margin-bottom: 10px;
      }}
      .card-front .card-name {{
        font-size: 18px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 10px;
        word-break: break-word;
      }}
      .card-front .tap-hint {{
        font-size: 12px;
        color: rgba(255,255,255,0.8);
        line-height: 1.4;
      }}
      .card-back .role-label {{
        font-size: 15px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 10px;
      }}
      .card-back .word-label {{
        font-size: 24px;
        font-weight: 900;
        background: rgba(255,255,255,0.2);
        border-radius: 10px;
        padding: 8px 16px;
        border: 2px solid rgba(255,255,255,0.3);
        letter-spacing: 2px;
        margin-bottom: 8px;
      }}
      .card-back .word-caption {{
        font-size: 11px;
        opacity: 0.85;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
      }}
      .card-back .flip-back {{
        font-size: 11px;
        opacity: 0.7;
      }}
    </style>

    <div class="cards-grid" id="cardsGrid"></div>

    <script>
      const cards = {cards_json};
      const grid = document.getElementById("cardsGrid");

      cards.forEach((c, i) => {{
        const wrap = document.createElement("div");
        wrap.className = "card-wrap";

        const wordHtml = c.back_word
          ? `<div class="word-caption">Η λέξη σου</div>
             <div class="word-label">${{c.back_word}}</div>`
          : `<div class="word-caption" style="font-size:13px;opacity:0.8;">Δεν έχεις λέξη</div>`;

        wrap.innerHTML = `
          <div class="card-inner">
            <div class="card-front">
              <div class="card-icon">🎭</div>
              <div class="card-name">${{c.name}}</div>
              <div class="tap-hint">👆 Πάτα για να δεις<br>τον ρόλο σου</div>
            </div>
            <div class="card-back" style="background:${{c.back_color}};">
              <div class="role-label">${{c.back_role}}</div>
              ${{wordHtml}}
              <div class="flip-back">👆 Πάτα για να κρύψεις</div>
            </div>
          </div>
        `;

        wrap.addEventListener("click", () => {{
          wrap.classList.toggle("flipped");
        }});

        grid.appendChild(wrap);
      }});
    </script>
    """

    components.html(cards_html, height=total_height, scrolling=False)

    # ================= VOTE =================
    st.divider()
    st.markdown("<h3 style='text-align: center;'>⚔️ ΦΑΣΗ ΨΗΦΟΦΟΡΙΑΣ</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.8;'>Συζητήστε και αποφασίστε ποιος φεύγει</p>", unsafe_allow_html=True)

    names = [p["name"] for p in players]
    idx = st.selectbox("Ποιος φεύγει;", range(len(names)), format_func=lambda i: names[i])

    if st.button("🔥 Remove Player"):
        removed = players[idx]

        role_labels = {
            "mr_white": "⚪ Mr. White",
            "undercover": "🟡 Undercover",
            "πολίτης": "🟢 Πολίτης"
        }
        role_display = role_labels.get(removed["role"], removed["role"])

        st.markdown(f"<div style='text-align: center; padding: 1rem; background: rgba(255,107,107,0.2); border-radius: 12px; margin: 1rem 0;'><h3 style='margin: 0;'>💀 {removed['name']} ήταν {role_display}</h3></div>", unsafe_allow_html=True)

        players = [p for p in players if p["name"] != removed["name"]]
        game["players"] = players
        st.session_state.revealed.pop(removed["name"], None)
        save_game(game)

        winner = check_winner(game["players"])

        if removed["role"] == "mr_white":
            st.session_state.last_out = removed
            st.session_state.mr_white_guess_mode = True
        elif winner == "INFILTRATORS":
            st.session_state.finished = True
            st.session_state.winner = "🟡 INFILTRATORS"
        elif winner == "CIVILIANS":
            st.session_state.finished = True
            st.session_state.winner = "🟢 CIVILIANS"
        else:
            st.session_state.last_out = None

        st.rerun()

    # ================= MR WHITE GUESS =================
    if st.session_state.mr_white_guess_mode:
        removed = st.session_state.last_out
        st.markdown(f"""
        <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, rgba(192,57,43,0.3), rgba(231,76,60,0.3)); border-radius: 16px; margin: 2rem 0; border: 2px solid rgba(192,57,43,0.5);'>
            <h2 style='margin: 0 0 1rem 0; color: #fff;'>⚪ ΤΕΛΕΥΤΑΙΑ ΕΥΚΑΙΡΙΑ!</h2>
            <p style='font-size: 1.2rem; opacity: 0.9;'>Ο <strong>{removed['name']}</strong> ήταν Mr. White!</p>
            <p style='opacity: 0.8;'>Μπορεί να μαντέψει τη λέξη των πολιτών;</p>
        </div>
        """, unsafe_allow_html=True)

        guess = st.text_input("Μάντεψε τη λέξη:")

        if st.button("✔ Check Guess"):
            if guess.strip().upper() == word[0].upper():
                st.session_state.finished = True
                st.session_state.winner = "⚪ MR WHITE"
            else:
                st.error(f"❌ Λάθος μαντεψιά: «{guess}»")
                winner = check_winner(game["players"])
                if winner == "INFILTRATORS":
                    st.session_state.finished = True
                    st.session_state.winner = "🟡 INFILTRATORS"
                elif winner == "CIVILIANS":
                    st.session_state.finished = True
                    st.session_state.winner = "🟢 CIVILIANS"

            st.session_state.mr_white_guess_mode = False
            st.rerun()
