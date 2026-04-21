import streamlit as st
import streamlit.components.v1 as components
import random
import json
import os
import time

st.set_page_config(
    page_title="ΚΥΡΙΟΣ ΛΕΥΚΟΣ",
    page_icon="🎭",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .stApp { background: #0f0c29; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    [data-testid="stAppViewContainer"] { padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

# ================= FILES =================
GAME_FILE = "game.json"

AVATAR_SEEDS = [
    "Felix","Mia","Zoe","Leo","Nina","Max","Aria","Hugo",
    "Luna","Oscar","Cleo","Finn","Nora","Eli","Vera",
    "Theo","Iris","Axel","Maya","Rex"
]

WORDS = [
("ΣΚΥΛΟΣ","ΚΟΚΑΛΟ"),("ΓΑΤΑ","ΠΟΝΤΙΚΙ"),("ΣΚΥΛΟΣ","ΛΟΥΡΙ"),("ΓΑΤΑ","ΝΙΑΟΥΡΙΣΜΑ"),("ΠΟΥΛΙ","ΦΤΕΡΟ"),("ΨΑΡΙ","ΝΕΡΟ"),("ΑΛΟΓΟ","ΣΤΑΒΛΟΣ"),("ΑΓΕΛΑΔΑ","ΓΑΛΑ"),("ΠΡΟΒΑΤΟ","ΜΑΛΛΙ"),("ΚΑΤΣΙΚΙ","ΦΑΡΜΑ"),
("ΘΑΛΑΣΣΑ","ΚΥΜΑ"),("ΘΑΛΑΣΣΑ","ΑΛΑΤΙ"),("ΛΙΜΝΗ","ΝΕΡΟ"),("ΠΟΤΑΜΙ","ΡΟΗ"),("ΒΟΥΝΟ","ΚΟΡΥΦΗ"),("ΔΑΣΟΣ","ΔΕΝΤΡΟ"),("ΔΕΝΤΡΟ","ΦΥΛΛΟ"),("ΦΥΛΛΟ","ΚΛΑΔΙ"),("ΛΟΥΛΟΥΔΙ","ΠΕΤΑΛΟ"),("ΧΟΡΤΑΡΙ","ΓΗΠΕΔΟ"),
("ΗΛΙΟΣ","ΖΕΣΤΗ"),("ΦΕΓΓΑΡΙ","ΝΥΧΤΑ"),("ΟΥΡΑΝΟΣ","ΣΥΝΝΕΦΟ"),("ΒΡΟΧΗ","ΟΜΠΡΕΛΑ"),("ΧΙΟΝΙ","ΠΑΓΟΣ"),("ΑΝΕΜΟΣ","ΦΥΣΗΜΑ"),("ΚΑΤΑΙΓΙΔΑ","ΒΡΟΝΤΗ"),("ΑΣΤΡΑΠΗ","ΦΩΣ"),("ΚΑΙΡΟΣ","ΠΡΟΒΛΕΨΗ"),("ΘΕΡΜΟΚΡΑΣΙΑ","ΖΕΣΤΗ"),
("ΣΠΙΤΙ","ΠΟΡΤΑ"),("ΣΠΙΤΙ","ΠΑΡΑΘΥΡΟ"),("ΔΩΜΑΤΙΟ","ΚΡΕΒΑΤΙ"),("ΚΟΥΖΙΝΑ","ΦΟΥΡΝΟΣ"),("ΜΠΑΝΙΟ","ΝΕΡΟ"),("ΣΑΛΟΝΙ","ΚΑΝΑΠΕΣ"),("ΤΡΑΠΕΖΙ","ΚΑΡΕΚΛΑ"),("ΝΤΟΥΛΑΠΑ","ΡΟΥΧΑ"),("ΚΛΕΙΔΙ","ΚΛΕΙΔΑΡΙΑ"),("ΦΩΣ","ΔΙΑΚΟΠΤΗΣ"),
("ΑΥΤΟΚΙΝΗΤΟ","ΤΡΟΧΟΣ"),("ΑΥΤΟΚΙΝΗΤΟ","ΒΕΝΖΙΝΗ"),("ΜΗΧΑΝΗ","ΚΡΑΝΟΣ"),("ΠΟΔΗΛΑΤΟ","ΠΕΤΑΛΙ"),("ΛΕΩΦΟΡΕΙΟ","ΣΤΑΣΗ"),("ΤΡΕΝΟ","ΓΡΑΜΜΗ"),("ΑΕΡΟΠΛΑΝΟ","ΠΤΗΣΗ"),("ΠΛΟΙΟ","ΛΙΜΑΝΙ"),("ΤΑΞΙ","ΟΔΗΓΟΣ"),("ΔΡΟΜΟΣ","ΚΙΝΗΣΗ"),
("ΑΝΘΡΩΠΟΣ","ΠΡΟΣΩΠΟ"),("ΑΝΘΡΩΠΟΣ","ΧΕΡΙ"),("ΠΑΙΔΙ","ΣΧΟΛΕΙΟ"),("ΜΑΘΗΤΗΣ","ΒΙΒΛΙΟ"),("ΔΑΣΚΑΛΟΣ","ΠΙΝΑΚΑΣ"),("ΓΙΑΤΡΟΣ","ΝΟΣΟΚΟΜΕΙΟ"),("ΝΟΣΟΚΟΜΑ","ΣΥΡΙΓΓΑ"),("ΑΣΤΥΝΟΜΙΚΟΣ","ΣΗΜΑ"),("ΠΥΡΟΣΒΕΣΤΗΣ","ΦΩΤΙΑ"),("ΜΑΓΕΙΡΑΣ","ΤΗΓΑΝΙ"),
("ΨΩΜΙ","ΦΟΥΡΝΟΣ"),("ΤΥΡΙ","ΓΑΛΑ"),("ΓΑΛΑ","ΠΟΤΗΡΙ"),("ΝΕΡΟ","ΜΠΟΥΚΑΛΙ"),("ΚΑΦΕΣ","ΚΟΥΠΑ"),("ΤΣΑΙ","ΦΛΙΤΖΑΝΙ"),("ΖΑΧΑΡΗ","ΓΛΥΚΟ"),("ΑΛΑΤΙ","ΓΕΥΣΗ"),("ΡΥΖΙ","ΠΙΑΤΟ"),("ΜΑΚΑΡΟΝΙΑ","ΣΑΛΤΣΑ"),
("ΜΗΛΟ","ΔΕΝΤΡΟ"),("ΠΟΡΤΟΚΑΛΙ","ΦΛΟΥΔΑ"),("ΜΠΑΝΑΝΑ","ΦΛΟΥΔΑ"),("ΚΕΡΑΣΙ","ΚΟΥΚΟΥΤΣΙ"),("ΚΑΡΠΟΥΖΙ","ΣΠΟΡΟΣ"),("ΣΤΑΦΥΛΙ","ΡΟΓΕΣ"),("ΛΕΜΟΝΙ","ΞΙΝΟ"),("ΦΡΑΟΥΛΑ","ΚΟΚΚΙΝΟ"),("ΑΧΛΑΔΙ","ΓΛΥΚΟ"),("ΡΟΔΑΚΙΝΟ","ΖΟΥΜΕΡΟ"),
("ΒΙΒΛΙΟ","ΣΕΛΙΔΑ"),("ΣΕΛΙΔΑ","ΚΕΙΜΕΝΟ"),("ΛΕΞΗ","ΓΡΑΜΜΑ"),("ΣΤΥΛΟ","ΜΕΛΑΝΙ"),("ΜΟΛΥΒΙ","ΞΥΛΟ"),("ΧΑΡΤΙ","ΣΗΜΕΙΩΣΗ"),("ΠΙΝΑΚΑΣ","ΚΙΜΩΛΙΑ"),("ΣΧΟΛΕΙΟ","ΤΑΞΗ"),("ΔΙΑΒΑΣΜΑ","ΜΑΘΗΣΗ"),("ΕΞΕΤΑΣΗ","ΒΑΘΜΟΣ"),
("ΚΙΘΑΡΑ","ΧΟΡΔΗ"),("ΠΙΑΝΟ","ΠΛΗΚΤΡΟ"),("ΤΡΑΓΟΥΔΙ","ΦΩΝΗ"),("ΜΟΥΣΙΚΗ","ΡΥΘΜΟΣ"),("ΝΤΡΑΜΣ","ΜΠΑΣΟ"),("ΒΙΟΛΙ","ΔΟΞΑΡΙ"),("ΣΥΝΑΥΛΙΑ","ΣΚΗΝΗ"),("ΧΕΙΡΟΚΡΟΤΗΜΑ","ΚΟΙΝΟ"),("ΤΡΑΓΟΥΔΙΣΤΗΣ","ΜΙΚΡΟΦΩΝΟ"),("ΧΟΡΟΣ","ΚΙΝΗΣΗ"),
("ΤΑΙΝΙΑ","ΟΘΟΝΗ"),("ΚΙΝΗΜΑΤΟΓΡΑΦΟΣ","ΕΙΣΙΤΗΡΙΟ"),("ΗΘΟΠΟΙΟΣ","ΡΟΛΟΣ"),("ΣΚΗΝΟΘΕΤΗΣ","ΚΑΜΕΡΑ"),("ΦΩΤΟΓΡΑΦΙΑ","ΦΛΑΣ"),("ΚΑΜΕΡΑ","ΦΑΚΟΣ"),("ΤΗΛΕΟΡΑΣΗ","ΚΑΝΑΛΙ"),("ΤΗΛΕΦΩΝΟ","ΚΛΗΣΗ"),("ΜΗΝΥΜΑ","CHAT"),("INTERNET","ΙΣΤΟΣΕΛΙΔΑ"),
("ΔΟΥΛΕΙΑ","ΓΡΑΦΕΙΟ"),("ΓΡΑΦΕΙΟ","ΥΠΟΛΟΓΙΣΤΗΣ"),("ΥΠΟΛΟΓΙΣΤΗΣ","ΠΛΗΚΤΡΟΛΟΓΙΟ"),("ΠΟΝΤΙΚΙ","ΚΛΙΚ"),("ΟΘΟΝΗ","PIXELS"),("ΛΟΓΙΣΜΙΚΟ","ΕΦΑΡΜΟΓΗ"),("ΚΩΔΙΚΑΣ","ΠΡΟΓΡΑΜΜΑ"),("ΔΕΔΟΜΕΝΑ","ΑΡΧΕΙΟ"),("ΦΑΚΕΛΟΣ","ΕΓΓΡΑΦΟ"),("ΕΚΤΥΠΩΣΗ","ΕΚΤΥΠΩΤΗΣ"),
("ΑΓΑΠΗ","ΚΑΡΔΙΑ"),("ΦΙΛΙΑ","ΕΜΠΙΣΤΟΣΥΝΗ"),("ΧΑΡΑ","ΓΕΛΙΟ"),("ΛΥΠΗ","ΔΑΚΡΥ"),("ΦΟΒΟΣ","ΣΚΟΤΑΔΙ"),("ΘΥΜΟΣ","ΦΩΝΗ"),("ΗΡΕΜΙΑ","ΣΙΩΠΗ"),("ΟΝΕΙΡΟ","ΥΠΝΟΣ"),("ΜΝΗΜΗ","ΠΑΡΕΛΘΟΝ"),("ΕΛΠΙΔΑ","ΜΕΛΛΟΝ"),
("ΧΡΟΝΟΣ","ΡΟΛΟΙ"),("ΩΡΑ","ΛΕΠΤΟ"),("ΜΕΡΑ","ΝΥΧΤΑ"),("ΕΒΔΟΜΑΔΑ","ΣΑΒΒΑΤΟΚΥΡΙΑΚΟ"),("ΜΗΝΑΣ","ΗΜΕΡΟΛΟΓΙΟ"),("ΧΘΕΣ","ΣΗΜΕΡΑ"),("ΑΥΡΙΟ","ΜΕΛΛΟΝ"),("ΣΤΙΓΜΗ","ΔΕΥΤΕΡΟΛΕΠΤΟ"),("ΑΙΩΝΑΣ","ΙΣΤΟΡΙΑ"),("ΠΑΡΕΛΘΟΝ","ΜΝΗΜΗ"),
("ΧΡΗΜΑ","ΝΟΜΙΣΜΑ"),("ΕΥΡΩ","ΚΕΡΜΑ"),("ΤΡΑΠΕΖΑ","ΛΟΓΑΡΙΑΣΜΟΣ"),("ΑΓΟΡΑ","ΠΩΛΗΤΗΣ"),("ΚΑΤΑΣΤΗΜΑ","ΠΡΟΪΟΝ"),("ΤΙΜΗ","ΚΟΣΤΟΣ"),("ΑΓΟΡΑΖΩ","ΠΟΥΛΑΩ"),("ΚΕΡΔΟΣ","ΖΗΜΙΑ"),("ΕΠΕΝΔΥΣΗ","ΡΙΣΚΟ"),("ΜΙΣΘΟΣ","ΔΟΥΛΕΙΑ"),
("ΠΟΛΗ","ΚΤΙΡΙΟ"),("ΧΩΡΙΟ","ΑΓΡΟΤΗΣ"),("ΔΡΟΜΟΣ","ΠΕΖΟΔΡΟΜΙΟ"),("ΠΛΑΤΕΙΑ","ΚΑΦΕ"),("ΓΕΦΥΡΑ","ΠΟΤΑΜΙ"),("ΣΤΑΘΜΟΣ","ΤΡΕΝΟ"),("ΑΕΡΟΔΡΟΜΙΟ","ΠΤΗΣΗ"),("ΛΙΜΑΝΙ","ΠΛΟΙΟ"),("ΓΕΙΤΟΝΙΑ","ΣΠΙΤΙΑ"),("ΧΑΡΤΗΣ","ΠΡΟΟΡΙΣΜΟΣ"),
("ΕΓΚΕΦΑΛΟΣ","ΣΚΕΨΗ"),("ΜΑΤΙ","ΟΡΑΣΗ"),("ΑΥΤΙ","ΗΧΟΣ"),("ΧΕΡΙ","ΔΑΧΤΥΛΟ"),("ΠΟΔΙ","ΒΗΜΑ"),("ΣΤΟΜΑ","ΟΜΙΛΙΑ"),("ΜΥΤΗ","ΜΥΡΩΔΙΑ"),("ΔΕΡΜΑ","ΑΦΗ"),("ΚΑΡΔΙΑ","ΠΑΛΜΟΣ"),("ΣΩΜΑ","ΥΓΕΙΑ"),
("ΠΟΛΕΜΟΣ","ΣΤΡΑΤΟΣ"),("ΕΙΡΗΝΗ","ΣΥΜΦΩΝΙΑ"),("ΟΠΛΟ","ΣΦΑΙΡΑ"),("ΜΑΧΗ","ΝΙΚΗ"),("ΗΤΤΑ","ΑΠΩΛΕΙΑ"),("ΣΤΡΑΤΗΓΟΣ","ΣΧΕΔΙΟ"),("ΣΥΓΚΡΟΥΣΗ","ΕΝΤΑΣΗ"),("ΑΣΦΑΛΕΙΑ","ΦΥΛΑΞΗ"),("ΚΙΝΔΥΝΟΣ","ΦΟΒΟΣ"),("ΗΡΩΑΣ","ΘΑΡΡΟΣ"),
("ΤΕΧΝΟΛΟΓΙΑ","ΚΑΙΝΟΤΟΜΙΑ"),("ΕΠΙΣΤΗΜΗ","ΕΡΕΥΝΑ"),("ΠΕΙΡΑΜΑ","ΔΟΚΙΜΗ"),("ΘΕΩΡΙΑ","ΑΠΟΔΕΙΞΗ"),("ΜΑΘΗΜΑΤΙΚΑ","ΑΡΙΘΜΟΣ"),("ΦΥΣΙΚΗ","ΔΥΝΑΜΗ"),("ΧΗΜΕΙΑ","ΣΤΟΙΧΕΙΟ"),("ΒΙΟΛΟΓΙΑ","ΖΩΗ"),("DNA","ΓΟΝΙΔΙΟ"),("ΥΠΟΘΕΣΗ","ΠΕΙΡΑΜΑ")
]

# ================= LOAD / SAVE =================
def load_game():
    if os.path.exists(GAME_FILE):
        try:
            with open(GAME_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            os.remove(GAME_FILE)
    return None

def save_game(game):
    with open(GAME_FILE, "w", encoding="utf-8") as f:
        json.dump(game, f, ensure_ascii=False, indent=2)

# ================= INIT =================
if "game" not in st.session_state:
    st.session_state.game = load_game()
if "phase" not in st.session_state:
    st.session_state.phase = "setup"  # setup | game | elimination | mrwhite | winner
if "selected_avatars" not in st.session_state:
    st.session_state.selected_avatars = {}
if "current_picker" not in st.session_state:
    st.session_state.current_picker = None
if "elimination_data" not in st.session_state:
    st.session_state.elimination_data = None
if "winner" not in st.session_state:
    st.session_state.winner = None
if "mr_white_removed" not in st.session_state:
    st.session_state.mr_white_removed = None
if "elim_timer_start" not in st.session_state:
    st.session_state.elim_timer_start = None

# ================= HELPERS =================
def assign_roles(players):
    n = len(players)
    roles = ["mr_white", "undercover"] + ["πολίτης"] * (n - 2)
    random.shuffle(roles)
    result = []
    for i, p in enumerate(players):
        result.append({"name": p["name"], "seed": p["seed"], "role": roles[i]})
    return result

def check_winner(players):
    roles = [p["role"] for p in players]
    if roles.count("πολίτης") <= 1 and (roles.count("undercover") + roles.count("mr_white")) > 0:
        return "UNDERCOVER"
    if roles.count("undercover") == 0 and roles.count("mr_white") == 0:
        return "ΠΟΛΙΤΕΣ"
    return None

def avatar_url(seed):
    return f"https://api.dicebear.com/7.x/avataaars/svg?seed={seed}&backgroundColor=b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf"

def reset():
    st.session_state.game = None
    st.session_state.phase = "setup"
    st.session_state.selected_avatars = {}
    st.session_state.current_picker = None
    st.session_state.elimination_data = None
    st.session_state.winner = None
    st.session_state.mr_white_removed = None
    st.session_state.elim_timer_start = None
    if os.path.exists(GAME_FILE):
        os.remove(GAME_FILE)

# ================= HANDLE ACTIONS VIA QUERY PARAMS =================
params = st.query_params
action = params.get("action", "")

if action == "pick_avatar":
    seed = params.get("seed", "")
    if seed in AVATAR_SEEDS and seed not in st.session_state.selected_avatars:
        st.session_state.current_picker = seed
    st.query_params.clear()
    st.rerun()

elif action == "confirm_name":
    seed = params.get("seed", "")
    name = params.get("name", "").strip()
    if seed and name and name not in st.session_state.selected_avatars.values():
        st.session_state.selected_avatars[seed] = name
        st.session_state.current_picker = None
    st.query_params.clear()
    st.rerun()

elif action == "cancel_pick":
    st.session_state.current_picker = None
    st.query_params.clear()
    st.rerun()

elif action == "remove_avatar":
    seed = params.get("seed", "")
    if seed in st.session_state.selected_avatars:
        del st.session_state.selected_avatars[seed]
    st.query_params.clear()
    st.rerun()

elif action == "start_game":
    selected = st.session_state.selected_avatars
    players_list = [{"name": name, "seed": seed} for seed, name in selected.items()]
    players_with_roles = assign_roles(players_list)
    word = random.choice(WORDS)
    st.session_state.game = {
        "players": players_with_roles,
        "all_players": [p.copy() for p in players_with_roles],
        "word": word,
    }
    save_game(st.session_state.game)
    st.session_state.phase = "game"
    st.session_state.selected_avatars = {}
    st.query_params.clear()
    st.rerun()

elif action == "eliminate":
    idx = int(params.get("idx", "0"))
    game = st.session_state.game
    players = game["players"]
    if 0 <= idx < len(players):
        removed = players[idx]
        role_labels = {"mr_white": "⚪ Mr. White", "undercover": "🟡 Undercover", "πολίτης": "🟢 Πολίτης"}
        st.session_state.elimination_data = {
            "name": removed["name"],
            "seed": removed["seed"],
            "role": role_labels.get(removed["role"], removed["role"]),
            "raw_role": removed["role"],
        }
        game["players"] = [p for p in players if p["name"] != removed["name"]]
        save_game(game)
        st.session_state.elim_timer_start = time.time()
        st.session_state.phase = "elimination"
        if removed["role"] == "mr_white":
            st.session_state.mr_white_removed = removed
    st.query_params.clear()
    st.rerun()

elif action == "after_elim":
    elim = st.session_state.elimination_data
    game = st.session_state.game
    winner = check_winner(game["players"])
    if elim and elim["raw_role"] == "mr_white":
        st.session_state.phase = "mrwhite"
    elif winner == "UNDERCOVER":
        st.session_state.winner = "undercover"
        st.session_state.phase = "winner"
    elif winner == "ΠΟΛΙΤΕΣ":
        st.session_state.winner = "civilians"
        st.session_state.phase = "winner"
    else:
        st.session_state.phase = "game"
        st.session_state.elimination_data = None
    st.query_params.clear()
    st.rerun()

elif action == "check_guess":
    guess = params.get("guess", "").strip().upper()
    game = st.session_state.game
    word = game["word"]
    if guess == word[0].upper():
        st.session_state.winner = "undercover"
        st.session_state.phase = "winner"
    else:
        winner = check_winner(game["players"])
        if winner == "UNDERCOVER":
            st.session_state.winner = "undercover"
            st.session_state.phase = "winner"
        elif winner == "ΠΟΛΙΤΕΣ":
            st.session_state.winner = "civilians"
            st.session_state.phase = "winner"
        else:
            st.session_state.phase = "game"
    st.query_params.clear()
    st.rerun()

elif action == "reset":
    reset()
    st.query_params.clear()
    st.rerun()

# ================= BUILD STATE FOR HTML =================
phase = st.session_state.phase
selected = st.session_state.selected_avatars
current_picker = st.session_state.current_picker
game = st.session_state.game
elimination_data = st.session_state.elimination_data
winner = st.session_state.winner
mr_white_removed = st.session_state.mr_white_removed

state = {
    "phase": phase,
    "seeds": AVATAR_SEEDS,
    "selected": selected,
    "current_picker": current_picker,
    "game": game,
    "elimination_data": elimination_data,
    "winner": winner,
    "mr_white_removed": mr_white_removed,
    "n_selected": len(selected),
}

state_json = json.dumps(state, ensure_ascii=False)

# ================= FULL HTML APP =================
html = f"""
<!DOCTYPE html>
<html lang="el">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0"/>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }}
  body {{
    font-family: 'Segoe UI', Tahoma, sans-serif;
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: #fff;
    min-height: 100vh;
    padding: 12px;
    overflow-x: hidden;
  }}
  h1 {{
    text-align: center;
    font-size: 1.8rem;
    font-weight: 900;
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #ffe66d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 3px;
    margin-bottom: 12px;
  }}
  h2 {{ color: #4ecdc4; font-size: 1.1rem; text-align: center; margin-bottom: 10px; }}
  .caption {{ text-align: center; font-size: 0.75rem; color: rgba(255,255,255,0.6); margin-bottom: 10px; }}

  /* BUTTONS */
  .btn {{
    display: block;
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 12px;
    font-size: 0.95rem;
    font-weight: 700;
    cursor: pointer;
    color: #fff;
    background: linear-gradient(135deg, #667eea, #764ba2);
    margin-top: 8px;
    letter-spacing: 0.5px;
  }}
  .btn-primary {{ background: linear-gradient(135deg, #f093fb, #f5576c); }}
  .btn-danger {{ background: linear-gradient(135deg, #e74c3c, #c0392b); }}
  .btn-success {{ background: linear-gradient(135deg, #1e8449, #27ae60); }}
  .btn-sm {{
    padding: 6px 10px;
    font-size: 0.8rem;
    border-radius: 8px;
    border: none;
    cursor: pointer;
    color: #fff;
    background: rgba(255,255,255,0.15);
    display: inline-block;
  }}
  .btn:disabled {{ opacity: 0.4; cursor: not-allowed; }}

  /* INPUT */
  input[type=text] {{
    width: 100%;
    padding: 10px 14px;
    border-radius: 10px;
    border: 2px solid rgba(78,205,196,0.5);
    background: #fff;
    color: #000;
    font-size: 1rem;
    margin-bottom: 8px;
  }}

  /* DIVIDER */
  .divider {{ border: none; border-top: 1px solid rgba(78,205,196,0.2); margin: 12px 0; }}

  /* AVATAR GRID */
  .avatar-grid {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 8px;
    margin-bottom: 10px;
  }}
  .avatar-cell {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;
  }}
  .avatar-img {{
    width: 48px;
    height: 48px;
    border-radius: 50%;
    border: 2px solid rgba(255,255,255,0.15);
    display: block;
  }}
  .avatar-img.taken {{ opacity: 0.35; border-color: #4ecdc4; }}
  .avatar-label {{ font-size: 9px; color: #4ecdc4; text-align: center; max-width: 52px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  .avatar-btn {{
    background: rgba(255,255,255,0.12);
    border: none;
    border-radius: 6px;
    color: #fff;
    font-size: 0.9rem;
    padding: 2px 8px;
    cursor: pointer;
    width: 100%;
  }}

  /* PICKER BOX */
  .picker-box {{
    background: rgba(78,205,196,0.15);
    border: 2px solid rgba(78,205,196,0.4);
    border-radius: 14px;
    padding: 12px;
    text-align: center;
    margin-bottom: 12px;
  }}
  .picker-box img {{ width: 56px; height: 56px; border-radius: 50%; margin-bottom: 6px; }}
  .picker-box p {{ font-size: 0.85rem; color: #4ecdc4; margin-bottom: 8px; }}
  .row {{ display: flex; gap: 8px; align-items: center; }}
  .row input {{ flex: 1; margin: 0; }}

  /* SELECTED LIST */
  .selected-grid {{
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 6px;
    margin-bottom: 10px;
  }}
  .selected-cell {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;
  }}
  .selected-cell img {{ width: 40px; height: 40px; border-radius: 50%; }}
  .selected-cell span {{ font-size: 9px; color: #fff; text-align: center; max-width: 48px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}

  /* GAME CARDS */
  .cards-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 8px;
    margin-bottom: 12px;
  }}
  .card-wrap {{
    aspect-ratio: 3/4;
    perspective: 800px;
    cursor: pointer;
  }}
  .card-inner {{
    position: relative;
    width: 100%;
    height: 100%;
    transform-style: preserve-3d;
    transition: transform 0.6s cubic-bezier(0.4,0,0.2,1);
  }}
  .card-wrap.flipped .card-inner {{ transform: rotateX(180deg); }}
  .card-front, .card-back {{
    position: absolute;
    inset: 0;
    border-radius: 12px;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 8px;
    text-align: center;
  }}
  .card-front {{
    background: linear-gradient(135deg, #667eea, #764ba2);
  }}
  .card-back {{ transform: rotateX(180deg); }}
  .card-front img {{ width: 52px; height: 52px; border-radius: 50%; border: 2px solid rgba(255,255,255,0.3); margin-bottom: 6px; }}
  .card-front .cname {{ font-size: 11px; font-weight: 800; margin-bottom: 4px; word-break: break-word; }}
  .card-front .chint {{ font-size: 9px; opacity: 0.7; line-height: 1.3; }}
  .card-back .role {{ font-size: 11px; font-weight: 800; letter-spacing: 1px; margin-bottom: 6px; }}
  .card-back .word {{ font-size: 15px; font-weight: 900; white-space: nowrap; overflow: hidden; width: 100%; text-align: center; }}
  .card-back .wcap {{ font-size: 9px; opacity: 0.8; margin-bottom: 2px; }}
  .card-back .whint {{ font-size: 9px; opacity: 0.6; margin-top: 4px; }}

  /* VOTE */
  select {{
    width: 100%;
    padding: 10px;
    border-radius: 10px;
    border: 2px solid rgba(78,205,196,0.3);
    background: rgba(255,255,255,0.1);
    color: #fff;
    font-size: 0.95rem;
    margin-bottom: 8px;
  }}

  /* ELIMINATION */
  .elim-box {{
    text-align: center;
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 12px;
  }}
  .elim-box img {{ width: 70px; height: 70px; border-radius: 50%; margin-bottom: 8px; }}
  .elim-box .skull {{ font-size: 2rem; }}
  .elim-box h3 {{ font-size: 1.4rem; margin: 4px 0; }}
  .elim-box p {{ font-size: 1rem; }}

  /* WINNER */
  .winner-box {{ text-align: center; padding: 24px 12px; }}
  .winner-box h2 {{ font-size: 1.5rem; color: #fff; margin-bottom: 8px; }}

  /* MR WHITE */
  .mrwhite-box {{
    text-align: center;
    padding: 16px;
    background: rgba(192,57,43,0.25);
    border: 2px solid rgba(192,57,43,0.5);
    border-radius: 16px;
    margin-bottom: 12px;
  }}
  .mrwhite-box h2 {{ color: #fff; font-size: 1.1rem; margin-bottom: 6px; }}
  .mrwhite-box p {{ font-size: 0.85rem; opacity: 0.9; }}
</style>
</head>
<body>
<h1>🎭 ΚΥΡΙΟΣ ΛΕΥΚΟΣ</h1>
<div id="app"></div>

<script>
const STATE = {state_json};
const AVATAR_BASE = "https://api.dicebear.com/7.x/avataaars/svg?backgroundColor=b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf&seed=";

function avatarUrl(seed) {{ return AVATAR_BASE + seed; }}

function navigate(params) {{
  const url = new URL(window.parent.location.href);
  Object.keys(params).forEach(k => url.searchParams.set(k, params[k]));
  window.parent.location.href = url.toString();
}}

function render() {{
  const app = document.getElementById("app");
  const p = STATE.phase;

  if (p === "setup") renderSetup(app);
  else if (p === "game") renderGame(app);
  else if (p === "elimination") renderElimination(app);
  else if (p === "mrwhite") renderMrWhite(app);
  else if (p === "winner") renderWinner(app);
}}

// ===== SETUP =====
function renderSetup(app) {{
  let html = "";

  if (STATE.current_picker) {{
    const seed = STATE.current_picker;
    html += `
      <div class="picker-box">
        <img src="${{avatarUrl(seed)}}" />
        <p>Γράψε το όνομά σου:</p>
        <div class="row">
          <input type="text" id="nameInput" placeholder="Όνομα..." autofocus />
        </div>
        <div class="row" style="margin-top:6px;">
          <button class="btn btn-success" onclick="confirmName('${{seed}}')">✔ OK</button>
          <button class="btn btn-danger" onclick="navigate({{action:'cancel_pick'}})">✖</button>
        </div>
      </div>
    `;
  }}

  html += `<h2>👤 Επιλογή Avatar</h2>
  <p class="caption">${{STATE.n_selected}} παίκτες έχουν επιλέξει</p>
  <div class="avatar-grid">`;

  STATE.seeds.forEach(seed => {{
    const isTaken = STATE.selected[seed] !== undefined;
    const name = STATE.selected[seed] || "";
    html += `<div class="avatar-cell">
      <img src="${{avatarUrl(seed)}}" class="avatar-img${{isTaken ? ' taken' : ''}}" />
      ${{isTaken
        ? `<span class="avatar-label">✓ ${{name}}</span>`
        : `<button class="avatar-btn" onclick="navigate({{action:'pick_avatar',seed:'${{seed}}'}})">＋</button>`
      }}
    </div>`;
  }});

  html += `</div>`;

  if (STATE.n_selected > 0) {{
    html += `<hr class="divider"/><p style="font-size:0.8rem;margin-bottom:6px;color:rgba(255,255,255,0.7);">🎮 Παίκτες (${{STATE.n_selected}}/20):</p>
    <div class="selected-grid">`;
    Object.entries(STATE.selected).forEach(([seed, name]) => {{
      html += `<div class="selected-cell">
        <img src="${{avatarUrl(seed)}}" />
        <span>${{name}}</span>
        <button class="btn-sm" onclick="navigate({{action:'remove_avatar',seed:'${{seed}}'}})">✖</button>
      </div>`;
    }});
    html += `</div>`;
  }}

  html += `<hr class="divider"/>`;
  if (STATE.n_selected < 4) {{
    html += `<p style="color:#ffe66d;font-size:0.8rem;text-align:center;margin-bottom:8px;">⚠️ Χρειάζονται τουλάχιστον 4 παίκτες</p>`;
  }}
  html += `<button class="btn btn-primary" ${{STATE.n_selected < 4 ? 'disabled' : ''}} onclick="navigate({{action:'start_game'}})">▶️ ΕΝΑΡΞΗ ΠΑΙΧΝΙΔΙΟΥ</button>`;

  app.innerHTML = html;
}}

function confirmName(seed) {{
  const name = document.getElementById("nameInput").value.trim();
  if (!name) return alert("Γράψε όνομα!");
  const taken = Object.values(STATE.selected);
  if (taken.includes(name)) return alert("Αυτό το όνομα υπάρχει ήδη!");
  navigate({{action:"confirm_name", seed, name}});
}}

// ===== GAME =====
function renderGame(app) {{
  const players = STATE.game.players;
  const word = STATE.game.word;

  let html = `<h2>🎮 ΠΑΙΚΤΕΣ</h2>
  <p class="caption">Πάτα την κάρτα σου για να δεις τον ρόλο σου</p>
  <div class="cards-grid" id="cardsGrid"></div>
  <hr class="divider"/>
  <h2>⚔️ ΨΗΦΟΦΟΡΙΑ</h2>
  <select id="voteSelect">`;

  players.forEach((p, i) => {{
    html += `<option value="${{i}}">${{p.name}}</option>`;
  }});

  html += `</select>
  <button class="btn btn-danger" onclick="eliminate()">🔥 Αφαίρεση Παίκτη</button>`;

  app.innerHTML = html;

  // Build cards
  const grid = document.getElementById("cardsGrid");
  players.forEach((p, i) => {{
    let backColor, backRole, backWord;
    if (p.role === "mr_white") {{
      backColor = "#c0392b"; backRole = "⚪ MR WHITE"; backWord = "";
    }} else if (p.role === "undercover") {{
      backColor = "#d68910"; backRole = "🟡 UNDERCOVER"; backWord = word[1];
    }} else {{
      backColor = "#1e8449"; backRole = "🟢 ΠΟΛΙΤΗΣ"; backWord = word[0];
    }}

    const wordHtml = backWord
      ? `<div class="wcap">Η λέξη σου</div><div class="word">${{backWord}}</div>`
      : `<div class="wcap">Δεν έχεις λέξη</div>`;

    const wrap = document.createElement("div");
    wrap.className = "card-wrap";
    wrap.innerHTML = `
      <div class="card-inner">
        <div class="card-front">
          <img src="${{avatarUrl(p.seed)}}" />
          <div class="cname">${{p.name}}</div>
          <div class="chint">👆 Πάτα για ρόλο</div>
        </div>
        <div class="card-back" style="background:${{backColor}};">
          <div class="role">${{backRole}}</div>
          ${{wordHtml}}
          <div class="whint">👆 Πάτα για κρύψιμο</div>
        </div>
      </div>
    `;
    wrap.addEventListener("click", () => wrap.classList.toggle("flipped"));
    grid.appendChild(wrap);

    // Auto-shrink word
    const wordEl = wrap.querySelector(".word");
    if (wordEl) {{
      let sz = 15;
      while (wordEl.scrollWidth > wordEl.clientWidth && sz > 8) {{
        sz--; wordEl.style.fontSize = sz + "px";
      }}
    }}
  }});
}}

function eliminate() {{
  const idx = document.getElementById("voteSelect").value;
  navigate({{action:"eliminate", idx}});
}}

// ===== ELIMINATION =====
function renderElimination(app) {{
  const e = STATE.elimination_data;
  const roleColors = {{
    "⚪ Mr. White": "#c0392b",
    "🟡 Undercover": "#d68910",
    "🟢 Πολίτης": "#1e8449"
  }};
  const color = roleColors[e.role] || "#555";

  app.innerHTML = `
    <div class="elim-box" style="background:${{color}}33; border: 2px solid ${{color}}88;">
      <img src="${{avatarUrl(e.seed)}}" />
      <div class="skull">💀</div>
      <h3>${{e.name}}</h3>
      <p>${{e.role}}</p>
    </div>
    <p id="countdown" style="text-align:center;font-size:0.85rem;color:rgba(255,255,255,0.6);margin-bottom:10px;">Συνεχίζει σε 5...</p>
    <button class="btn" onclick="navigate({{action:'after_elim'}})">Συνέχεια →</button>
  `;

  let secs = 5;
  const timer = setInterval(() => {{
    secs--;
    const el = document.getElementById("countdown");
    if (el) el.textContent = secs > 0 ? `Συνεχίζει σε ${{secs}}...` : "Έτοιμο!";
    if (secs <= 0) {{
      clearInterval(timer);
      navigate({{action:"after_elim"}});
    }}
  }}, 1000);
}}

// ===== MR WHITE GUESS =====
function renderMrWhite(app) {{
  const removed = STATE.mr_white_removed;
  app.innerHTML = `
    <div class="mrwhite-box">
      <h2>⚪ ΤΕΛΕΥΤΑΙΑ ΕΥΚΑΙΡΙΑ!</h2>
      <p>Ο <strong>${{removed.name}}</strong> ήταν Mr. White!</p>
      <p style="margin-top:4px;">Μπορεί να μαντέψει τη λέξη των πολιτών;</p>
    </div>
    <input type="text" id="guessInput" placeholder="Μάντεψε τη λέξη..." />
    <button class="btn btn-success" onclick="checkGuess()">✔ Έλεγχος</button>
  `;
}}

function checkGuess() {{
  const guess = document.getElementById("guessInput").value;
  navigate({{action:"check_guess", guess}});
}}

// ===== WINNER =====
function renderWinner(app) {{
  const w = STATE.winner;
  let msg = "";
  if (w === "undercover") msg = "🟡⚪ Νίκησαν οι Undercover & Mr. White!";
  else msg = "🟢 Νίκησαν οι Πολίτες!";

  app.innerHTML = `
    <div class="winner-box">
      <h2>${{msg}}</h2>
      <button class="btn btn-primary" style="margin-top:20px;" onclick="navigate({{action:'reset'}})">🔄 Νέο Παιχνίδι</button>
    </div>
  `;
}}

render();
</script>
</body>
</html>
"""

components.html(html, height=900, scrolling=True)
