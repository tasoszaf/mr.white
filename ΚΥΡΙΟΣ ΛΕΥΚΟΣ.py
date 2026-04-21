import streamlit as st
import streamlit.components.v1 as components
import random
import json
import os
import time

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
GAME_FILE = "game.json"

# ================= AVATAR SEEDS =================
AVATAR_SEEDS = [
    "Felix", "Mia", "Zoe", "Leo", "Nina", "Max", "Aria", "Hugo",
    "Luna", "Oscar", "Cleo", "Finn", "Nora", "Eli", "Vera",
    "Theo", "Iris", "Axel", "Maya", "Rex"
]

def avatar_url(seed):
    return f"https://api.dicebear.com/7.x/avataaars/svg?seed={seed}&backgroundColor=b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf"

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
if "last_out" not in st.session_state:
    st.session_state.last_out = None
if "mr_white_guess_mode" not in st.session_state:
    st.session_state.mr_white_guess_mode = False
if "finished" not in st.session_state:
    st.session_state.finished = False
if "winner" not in st.session_state:
    st.session_state.winner = None
if "elimination_msg" not in st.session_state:
    st.session_state.elimination_msg = None
if "selected_avatars" not in st.session_state:
    st.session_state.selected_avatars = {}
if "current_picker" not in st.session_state:
    st.session_state.current_picker = None

# ================= HELPERS =================
def assign_roles(players):
    n = len(players)
    roles = ["mr_white", "undercover"] + ["πολίτης"] * (n - 2)
    random.shuffle(roles)
    assigned = []
    for i, player in enumerate(players):
        assigned.append({
            "name": player["name"],
            "seed": player["seed"],
            "role": roles[i]
        })
    return assigned

def check_winner(players):
    roles = [p["role"] for p in players]
    civilians   = roles.count("πολίτης")
    undercovers = roles.count("undercover")
    mr_whites   = roles.count("mr_white")
    if civilians <= 1 and (undercovers + mr_whites) > 0:
        return "UNDERCOVER"
    if undercovers == 0 and mr_whites == 0:
        return "ΠΟΛΙΤΕΣ"
    return None

def reset_game():
    st.session_state.game = None
    st.session_state.last_out = None
    st.session_state.mr_white_guess_mode = False
    st.session_state.finished = False
    st.session_state.winner = None
    st.session_state.elimination_msg = None
    st.session_state.selected_avatars = {}
    st.session_state.current_picker = None
    if os.path.exists(GAME_FILE):
        os.remove(GAME_FILE)

# ================= UI =================
st.markdown("<h1>🎭 ΚΥΡΙΟΣ ΛΕΥΚΟΣ</h1>", unsafe_allow_html=True)

# ================= END SCREEN =================
if st.session_state.finished:
    winner = st.session_state.winner
    st.divider()
    if winner == "🟡 UNDERCOVER":
        st.markdown("<h2 style='text-align:center;font-size:2.5rem;'>🟡⚪ Νίκησαν οι Undercover & Mr. White!</h2>", unsafe_allow_html=True)
    elif winner == "🟢 ΠΟΛΙΤΕΣ":
        st.markdown("<h2 style='text-align:center;font-size:2.5rem;'>🟢 Νίκησαν οι Πολίτες!</h2>", unsafe_allow_html=True)
    st.divider()
    if st.button("🔄 Νέο Παιχνίδι", type="primary", use_container_width=True):
        reset_game()
        st.rerun()

# ================= SETUP PHASE =================
elif st.session_state.game is None:

    selected = st.session_state.selected_avatars  # {seed: name}
    taken_seeds = set(selected.keys())
    n_selected = len(selected)

    # ===== CHECK QUERY PARAMS για avatar click =====
    params = st.query_params
    if "pick" in params and not st.session_state.current_picker:
        seed = params["pick"]
        if seed in AVATAR_SEEDS and seed not in taken_seeds:
            st.session_state.current_picker = seed
            st.query_params.clear()
            st.rerun()

    st.markdown("<h3 style='text-align:center;'>👤 Επιλογή Avatar</h3>", unsafe_allow_html=True)
    st.caption(f"Πάτα ένα avatar για να το επιλέξεις — {n_selected} παίκτες έχουν επιλέξει")

    # ===== NAME INPUT αν κάποιος μόλις επέλεξε avatar =====
    if st.session_state.current_picker:
        seed = st.session_state.current_picker
        st.markdown(f"""
        <div style='text-align:center; padding:1rem; background:rgba(78,205,196,0.15);
             border-radius:16px; margin-bottom:1rem; border:2px solid rgba(78,205,196,0.4);'>
            <img src='{avatar_url(seed)}' width='80' style='border-radius:50%; margin-bottom:8px;'/>
            <p style='margin:0; font-size:1rem; color:#4ecdc4;'>Επέλεξες αυτό το avatar!</p>
        </div>
        """, unsafe_allow_html=True)

        col_name, col_ok, col_cancel = st.columns([3, 1, 1])
        with col_name:
            name_input = st.text_input("Το όνομά σου:", placeholder="Γράψε όνομα...", label_visibility="collapsed", key="name_input_field")
        with col_ok:
            if st.button("✔ OK", use_container_width=True):
                name = name_input.strip() if name_input else ""
                if not name:
                    st.warning("Γράψε όνομα!")
                elif name in list(selected.values()):
                    st.warning("Αυτό το όνομα υπάρχει ήδη!")
                else:
                    st.session_state.selected_avatars[seed] = name
                    st.session_state.current_picker = None
                    st.rerun()
        with col_cancel:
            if st.button("✖", use_container_width=True):
                st.session_state.current_picker = None
                st.rerun()

        st.divider()

    # ===== AVATAR GRID =====
    import json as _json
    seeds_json = _json.dumps(AVATAR_SEEDS)
    selected_json = _json.dumps(list(taken_seeds))
    selected_names_json = _json.dumps(selected)

    avatar_grid_html = f"""
    <style>
      body {{ margin:0; font-family:'Segoe UI',sans-serif; background:transparent; }}
      .avatar-grid {{
        display: flex;
        flex-wrap: wrap;
        gap: 14px;
        justify-content: center;
        padding: 10px 0 20px;
      }}
      .avatar-card {{
        width: 100px;
        display: flex;
        flex-direction: column;
        align-items: center;
        cursor: pointer;
        border-radius: 16px;
        padding: 10px 8px 8px;
        border: 2px solid transparent;
        background: rgba(255,255,255,0.06);
        transition: all 0.2s ease;
        position: relative;
      }}
      .avatar-card:hover:not(.taken) {{
        border-color: rgba(78,205,196,0.7);
        background: rgba(78,205,196,0.12);
        transform: translateY(-3px);
      }}
      .avatar-card.taken {{
        opacity: 0.45;
        cursor: not-allowed;
        pointer-events: none;
        border-color: rgba(255,255,255,0.1);
      }}
      .avatar-card img {{
        width: 68px;
        height: 68px;
        border-radius: 50%;
        background: rgba(255,255,255,0.1);
      }}
      .avatar-name {{
        font-size: 11px;
        color: #4ecdc4;
        font-weight: 700;
        text-align: center;
        margin-top: 5px;
        max-width: 90px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }}
      .check-badge {{
        position: absolute;
        top: 6px; right: 6px;
        background: #4ecdc4;
        color: #0f0c29;
        border-radius: 50%;
        width: 20px; height: 20px;
        font-size: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 900;
      }}
    </style>

    <div class="avatar-grid" id="avatarGrid"></div>

    <script>
      const seeds = {seeds_json};
      const takenSeeds = {selected_json};
      const selectedNames = {selected_names_json};
      const grid = document.getElementById("avatarGrid");

      seeds.forEach(seed => {{
        const isTaken = takenSeeds.includes(seed);
        const name = selectedNames[seed] || "";
        const card = document.createElement("div");
        card.className = "avatar-card" + (isTaken ? " taken" : "");

        card.innerHTML = `
          ${{isTaken ? '<div class="check-badge">✓</div>' : ''}}
          <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=${{seed}}&backgroundColor=b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf" />
          ${{isTaken ? `<div class="avatar-name">${{name}}</div>` : ''}}
        `;

        if (!isTaken) {{
          card.addEventListener("click", () => {{
            const url = new URL(window.parent.location.href);
            url.searchParams.set("pick", seed);
            window.parent.location.href = url.toString();
          }});
        }}

        grid.appendChild(card);
      }});
    </script>
    """

    rows = (len(AVATAR_SEEDS) + 4) // 5
    grid_height = rows * 130 + 40
    components.html(avatar_grid_html, height=grid_height, scrolling=False)

    st.divider()

    # ===== SELECTED PLAYERS LIST =====
    if selected:
        st.markdown(f"**🎮 Παίκτες ({n_selected}/20):**")
        cols2 = st.columns(4)
        items = list(selected.items())
        for i, (seed, name) in enumerate(items):
            with cols2[i % 4]:
                st.markdown(f"""
                <div style='text-align:center; margin-bottom:8px;'>
                  <img src='{avatar_url(seed)}' width='48' style='border-radius:50%;'/>
                  <div style='font-size:12px; color:#fff; margin-top:4px;'>{name}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("✖", key=f"rem_{seed}", use_container_width=True):
                    del st.session_state.selected_avatars[seed]
                    st.rerun()

    if n_selected < 4:
        st.warning(f"⚠️ Χρειάζονται τουλάχιστον 4 παίκτες (έχεις {n_selected})")

    st.divider()

    if st.button("▶️ ΕΝΑΡΞΗ ΠΑΙΧΝΙΔΙΟΥ",
                 disabled=n_selected < 4,
                 type="primary",
                 use_container_width=True):
        players_list = [{"name": name, "seed": seed} for seed, name in selected.items()]
        players_with_roles = assign_roles(players_list)
        st.session_state.game = {
            "players": players_with_roles,
            "all_players": [p.copy() for p in players_with_roles],
            "word": random.choice(WORDS),
        }
        save_game(st.session_state.game)
        st.session_state.selected_avatars = {}
        st.session_state.current_picker = None
        st.rerun()

# ================= GAME PHASE =================
else:
    game = st.session_state.game
    players = game["players"]
    word = game["word"]

    st.markdown("<h3 style='text-align:center;'>🎮 ΠΑΙΚΤΕΣ</h3>", unsafe_allow_html=True)
    st.caption("👀 Πάτα την κάρτα σου για να δεις τον ρόλο σου — μόνος/η σου!")

    import json as _json

    cards_data = []
    for p in players:
        if p["role"] == "mr_white":
            back_role = "⚪ MR WHITE"
            back_word = ""
            back_color = "#c0392b"
        elif p["role"] == "undercover":
            back_role = "🟡 UNDERCOVER"
            back_word = word[1]
            back_color = "#d68910"
        else:
            back_role = "🟢 ΠΟΛΙΤΗΣ"
            back_word = word[0]
            back_color = "#1e8449"

        cards_data.append({
            "name": p["name"],
            "seed": p["seed"],
            "back_role": back_role,
            "back_word": back_word,
            "back_color": back_color,
        })

    cards_json = _json.dumps(cards_data, ensure_ascii=False)

    num_players = len(players)
    cards_per_row = 3
    num_rows = (num_players + cards_per_row - 1) // cards_per_row
    card_height = 260
    gap = 20
    padding = 60
    total_height = num_rows * card_height + (num_rows - 1) * gap + padding

    cards_html = f"""
    <style>
      body {{ margin:0; font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif; background:transparent; }}
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
        transition: transform 0.7s cubic-bezier(0.4,0.0,0.2,1);
      }}
      .card-wrap.flipped .card-inner {{
        transform: rotateX(180deg);
      }}
      .card-front, .card-back {{
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        border-radius: 16px;
        backface-visibility: hidden;
        -webkit-backface-visibility: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 14px;
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
      .card-front .avatar-img {{
        width: 72px;
        height: 72px;
        border-radius: 50%;
        margin-bottom: 8px;
        background: rgba(255,255,255,0.15);
        border: 2px solid rgba(255,255,255,0.3);
      }}
      .card-front .card-name {{
        font-size: 16px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-bottom: 8px;
        word-break: break-word;
      }}
      .card-front .tap-hint {{
        font-size: 11px;
        color: rgba(255,255,255,0.75);
        line-height: 1.4;
      }}
      .card-back .role-label {{
        font-size: 14px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 10px;
      }}
      .card-back .word-label {{
        font-weight: 900;
        letter-spacing: 2px;
        margin-bottom: 8px;
        width: 128px;
        box-sizing: border-box;
        white-space: nowrap;
        text-align: center;
        font-size: 22px;
      }}
      .card-back .word-caption {{
        font-size: 10px;
        opacity: 0.85;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 4px;
      }}
      .card-back .flip-back {{
        font-size: 10px;
        opacity: 0.65;
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
          : `<div class="word-caption" style="font-size:12px;opacity:0.8;">Δεν έχεις λέξη</div>`;

        const avatarUrl = `https://api.dicebear.com/7.x/avataaars/svg?seed=${{c.seed}}&backgroundColor=b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf`;

        wrap.innerHTML = `
          <div class="card-inner">
            <div class="card-front">
              <img class="avatar-img" src="${{avatarUrl}}" />
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

        const wordEl = wrap.querySelector(".word-label");
        if (wordEl) {{
          let size = 22;
          while (wordEl.scrollWidth > wordEl.clientWidth && size > 8) {{
            size--;
            wordEl.style.fontSize = size + "px";
          }}
        }}
      }});
    </script>
    """

    components.html(cards_html, height=total_height, scrolling=False)

    # ================= VOTE =================
    st.divider()
    st.markdown("<h3 style='text-align:center;'>⚔️ ΦΑΣΗ ΨΗΦΟΦΟΡΙΑΣ</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; opacity:0.8;'>Συζητήστε και αποφασίστε ποιος φεύγει</p>", unsafe_allow_html=True)

    # ================= ELIMINATION BANNER =================
    if st.session_state.elimination_msg:
        msg = st.session_state.elimination_msg
        role_color = {
            "⚪ Mr. White": "#c0392b",
            "🟡 Undercover": "#d68910",
            "🟢 Πολίτης": "#1e8449"
        }
        color = role_color.get(msg["role"], "#555")
        st.markdown(f"""
        <div style='text-align:center; padding:2rem; background:{color}33;
             border-radius:16px; margin:1rem 0; border:2px solid {color}88;'>
            <img src='{avatar_url(msg["seed"])}' width='80' style='border-radius:50%; margin-bottom:10px;'/>
            <div style='font-size:2rem; margin-bottom:0.25rem;'>💀</div>
            <h3 style='margin:0; color:#fff; font-size:1.8rem;'>{msg["name"]}</h3>
            <p style='margin:0.5rem 0 0 0; font-size:1.3rem; color:#fff;'>{msg["role"]}</p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(5)
        st.session_state.elimination_msg = None
        st.rerun()

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
        st.session_state.elimination_msg = {
            "name": removed["name"],
            "seed": removed["seed"],
            "role": role_display
        }

        players = [p for p in players if p["name"] != removed["name"]]
        game["players"] = players
        save_game(game)

        winner = check_winner(game["players"])

        if removed["role"] == "mr_white":
            st.session_state.last_out = removed
            st.session_state.mr_white_guess_mode = True
        elif winner == "UNDERCOVER":
            st.session_state.finished = True
            st.session_state.winner = "🟡 UNDERCOVER"
        elif winner == "ΠΟΛΙΤΕΣ":
            st.session_state.finished = True
            st.session_state.winner = "🟢 ΠΟΛΙΤΕΣ"
        else:
            st.session_state.last_out = None

        st.rerun()

    # ================= MR WHITE GUESS =================
    if st.session_state.mr_white_guess_mode:
        removed = st.session_state.last_out
        st.markdown(f"""
        <div style='text-align:center; padding:2rem; background:linear-gradient(135deg,rgba(192,57,43,0.3),rgba(231,76,60,0.3));
             border-radius:16px; margin:2rem 0; border:2px solid rgba(192,57,43,0.5);'>
            <h2 style='margin:0 0 1rem 0; color:#fff;'>⚪ ΤΕΛΕΥΤΑΙΑ ΕΥΚΑΙΡΙΑ!</h2>
            <p style='font-size:1.2rem; opacity:0.9;'>Ο <strong>{removed['name']}</strong> ήταν Mr. White!</p>
            <p style='opacity:0.8;'>Μπορεί να μαντέψει τη λέξη των πολιτών;</p>
        </div>
        """, unsafe_allow_html=True)

        guess = st.text_input("Μάντεψε τη λέξη:")

        if st.button("✔ Check Guess"):
            if guess.strip().upper() == word[0].upper():
                st.session_state.finished = True
                st.session_state.winner = "🟡 UNDERCOVER"
            else:
                st.error(f"❌ Λάθος μαντεψιά: «{guess}»")
                winner = check_winner(game["players"])
                if winner == "UNDERCOVER":
                    st.session_state.finished = True
                    st.session_state.winner = "🟡 UNDERCOVER"
                elif winner == "ΠΟΛΙΤΕΣ":
                    st.session_state.finished = True
                    st.session_state.winner = "🟢 ΠΟΛΙΤΕΣ"

            st.session_state.mr_white_guess_mode = False
            st.rerun()
