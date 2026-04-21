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
  /* Global */
  .stApp { background: linear-gradient(135deg,#0f0c29,#302b63,#24243e); color:#fff; }
  #MainMenu,footer,header { visibility:hidden; }
  .block-container { padding: 0.5rem 0.75rem 2rem !important; max-width:480px !important; }

  /* Typography */
  h1 {
    text-align:center; font-size:1.8rem !important; font-weight:900 !important;
    background:linear-gradient(45deg,#ff6b6b,#4ecdc4,#ffe66d);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    letter-spacing:3px; margin-bottom:6px !important;
  }
  h2,h3 { color:#4ecdc4 !important; font-weight:700 !important; font-size:1rem !important; text-align:center; margin-bottom:4px !important; }
  p,label,.stMarkdown { color:#e0e0e0; font-size:0.85rem; }
  .stCaption { font-size:0.75rem !important; text-align:center; }

  /* Buttons */
  .stButton > button {
    background:linear-gradient(135deg,#667eea,#764ba2) !important;
    border:none !important; border-radius:10px !important;
    color:#fff !important; font-weight:700 !important;
    padding:0.35rem 0.5rem !important; font-size:0.8rem !important;
    width:100%; transition:all 0.2s ease !important;
  }
  .stButton > button[kind="primary"] {
    background:linear-gradient(135deg,#f093fb,#f5576c) !important;
    padding:0.6rem !important; font-size:0.95rem !important;
  }
  .stButton > button:disabled { opacity:0.35 !important; }

  /* Input */
  .stTextInput > div > div > input {
    background:#fff !important; border:2px solid rgba(78,205,196,0.5) !important;
    border-radius:10px !important; color:#000 !important;
    padding:0.5rem 0.75rem !important; font-size:0.95rem !important;
  }
  [data-testid="InputInstructions"] { display:none !important; }

  /* Select */
  .stSelectbox > div > div {
    background:rgba(255,255,255,0.1) !important;
    border:2px solid rgba(78,205,196,0.3) !important;
    border-radius:10px !important; font-size:0.85rem !important;
  }

  /* Divider */
  hr { border-color:rgba(78,205,196,0.2) !important; margin:0.6rem 0 !important; }

  /* Alerts */
  .stAlert { background:rgba(255,255,255,0.05) !important; border-radius:10px !important; font-size:0.8rem !important; }

  /* Column gaps — tighter */
  [data-testid="column"] { padding:0 2px !important; }
</style>
""", unsafe_allow_html=True)

# ================= FILES =================
GAME_FILE = "game.json"

AVATAR_SEEDS = [
    "Felix","Mia","Zoe","Leo","Nina","Max","Aria","Hugo",
    "Luna","Oscar","Cleo","Finn","Nora","Eli","Vera",
    "Theo","Iris","Axel","Maya","Rex"
]

def avatar_url(seed):
    return f"https://api.dicebear.com/7.x/avataaars/svg?seed={seed}&backgroundColor=b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf"

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
            with open(GAME_FILE,"r",encoding="utf-8") as f:
                return json.load(f)
        except:
            os.remove(GAME_FILE)
    return None

def save_game(game):
    with open(GAME_FILE,"w",encoding="utf-8") as f:
        json.dump(game,f,ensure_ascii=False,indent=2)

# ================= INIT =================
if "game" not in st.session_state:
    st.session_state.game = load_game()
if "selected_avatars" not in st.session_state:
    st.session_state.selected_avatars = {}
if "current_picker" not in st.session_state:
    st.session_state.current_picker = None
if "elimination_msg" not in st.session_state:
    st.session_state.elimination_msg = None
if "mr_white_guess_mode" not in st.session_state:
    st.session_state.mr_white_guess_mode = False
if "mr_white_removed" not in st.session_state:
    st.session_state.mr_white_removed = None
if "finished" not in st.session_state:
    st.session_state.finished = False
if "winner" not in st.session_state:
    st.session_state.winner = None

# ================= HELPERS =================
def assign_roles(players):
    roles = ["mr_white","undercover"] + ["πολίτης"]*(len(players)-2)
    random.shuffle(roles)
    return [{"name":p["name"],"seed":p["seed"],"role":roles[i]} for i,p in enumerate(players)]

def check_winner(players):
    roles = [p["role"] for p in players]
    if roles.count("πολίτης") <= 1 and (roles.count("undercover")+roles.count("mr_white")) > 0:
        return "UNDERCOVER"
    if roles.count("undercover") == 0 and roles.count("mr_white") == 0:
        return "ΠΟΛΙΤΕΣ"
    return None

def reset():
    st.session_state.game = None
    st.session_state.selected_avatars = {}
    st.session_state.current_picker = None
    st.session_state.elimination_msg = None
    st.session_state.mr_white_guess_mode = False
    st.session_state.mr_white_removed = None
    st.session_state.finished = False
    st.session_state.winner = None
    if os.path.exists(GAME_FILE):
        os.remove(GAME_FILE)

# ================= UI =================
st.markdown("<h1>🎭 ΚΥΡΙΟΣ ΛΕΥΚΟΣ</h1>", unsafe_allow_html=True)

# ===== WINNER SCREEN =====
if st.session_state.finished:
    w = st.session_state.winner
    st.divider()
    if w == "undercover":
        st.markdown("<h2>🟡⚪ Νίκησαν οι Undercover & Mr. White!</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2>🟢 Νίκησαν οι Πολίτες!</h2>", unsafe_allow_html=True)
    st.divider()
    if st.button("🔄 Νέο Παιχνίδι", type="primary", use_container_width=True):
        reset()
        st.rerun()

# ===== SETUP =====
elif st.session_state.game is None:
    selected = st.session_state.selected_avatars
    taken = set(selected.keys())
    n = len(selected)

    st.markdown("<h3>👤 Επιλογή Avatar</h3>", unsafe_allow_html=True)
    st.caption(f"{n} παίκτες έχουν επιλέξει — πάτα ＋ για να επιλέξεις")

    # NAME INPUT
    if st.session_state.current_picker:
        seed = st.session_state.current_picker
        st.markdown(f"""
        <div style='text-align:center;padding:8px;background:rgba(78,205,196,0.15);
             border-radius:12px;border:2px solid rgba(78,205,196,0.4);margin-bottom:8px;'>
          <img src='{avatar_url(seed)}' width='52' style='border-radius:50%;margin-bottom:4px;display:block;margin:0 auto 4px;'/>
          <p style='margin:0;font-size:0.8rem;color:#4ecdc4;'>Γράψε το όνομά σου:</p>
        </div>
        """, unsafe_allow_html=True)
        c1,c2,c3 = st.columns([4,1,1])
        with c1:
            nm = st.text_input("nm", placeholder="Όνομα...", label_visibility="collapsed", key="name_field")
        with c2:
            if st.button("✔", use_container_width=True, key="ok_btn"):
                nm = nm.strip() if nm else ""
                if not nm:
                    st.warning("Γράψε όνομα!")
                elif nm in selected.values():
                    st.warning("Υπάρχει ήδη!")
                else:
                    st.session_state.selected_avatars[seed] = nm
                    st.session_state.current_picker = None
                    st.rerun()
        with c3:
            if st.button("✖", use_container_width=True, key="cancel_btn"):
                st.session_state.current_picker = None
                st.rerun()
        st.divider()

    # AVATAR GRID — 5 per row
    for row_start in range(0, len(AVATAR_SEEDS), 5):
        row_seeds = AVATAR_SEEDS[row_start:row_start+5]
        cols = st.columns(5)
        for j, seed in enumerate(row_seeds):
            with cols[j]:
                is_taken = seed in taken
                name_lbl = selected.get(seed,"")
                border = "3px solid #4ecdc4" if is_taken else "2px solid rgba(255,255,255,0.1)"
                opacity = "0.35" if is_taken else "1"
                st.markdown(f"""
                <div style='text-align:center;opacity:{opacity};margin-bottom:2px;'>
                  <img src='{avatar_url(seed)}' width='44'
                    style='border-radius:50%;border:{border};display:block;margin:0 auto;'/>
                  {'<div style="font-size:8px;color:#4ecdc4;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:44px;margin:0 auto;">✓'+name_lbl+'</div>' if is_taken else '<div style="height:12px;"></div>'}
                </div>
                """, unsafe_allow_html=True)
                if not is_taken:
                    if st.button("＋", key=f"p_{seed}", use_container_width=True):
                        st.session_state.current_picker = seed
                        st.rerun()

    st.divider()

    # SELECTED LIST
    if selected:
        st.markdown(f"<p style='font-size:0.8rem;margin-bottom:4px;'>🎮 Παίκτες ({n}/20):</p>", unsafe_allow_html=True)
        sel_items = list(selected.items())
        for row_start in range(0, len(sel_items), 5):
            row = sel_items[row_start:row_start+5]
            cols2 = st.columns(5)
            for j,(seed,name) in enumerate(row):
                with cols2[j]:
                    st.markdown(f"""
                    <div style='text-align:center;margin-bottom:2px;'>
                      <img src='{avatar_url(seed)}' width='38' style='border-radius:50%;'/>
                      <div style='font-size:8px;color:#fff;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;'>{name}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("✖", key=f"rm_{seed}", use_container_width=True):
                        del st.session_state.selected_avatars[seed]
                        st.rerun()

    if n < 4:
        st.warning(f"⚠️ Χρειάζονται τουλάχιστον 4 παίκτες (έχεις {n})")

    st.divider()
    if st.button("▶️ ΕΝΑΡΞΗ ΠΑΙΧΝΙΔΙΟΥ", disabled=n<4, type="primary", use_container_width=True):
        pl = [{"name":name,"seed":seed} for seed,name in selected.items()]
        assigned = assign_roles(pl)
        st.session_state.game = {"players":assigned,"all_players":[p.copy() for p in assigned],"word":random.choice(WORDS)}
        save_game(st.session_state.game)
        st.session_state.selected_avatars = {}
        st.session_state.current_picker = None
        st.rerun()

# ===== GAME =====
else:
    game = st.session_state.game
    players = game["players"]
    word = game["word"]

    # ELIMINATION BANNER
    if st.session_state.elimination_msg:
        msg = st.session_state.elimination_msg
        role_color = {"⚪ Mr. White":"#c0392b","🟡 Undercover":"#d68910","🟢 Πολίτης":"#1e8449"}
        color = role_color.get(msg["role"],"#555")
        st.markdown(f"""
        <div style='text-align:center;padding:1.2rem;background:{color}33;
             border-radius:14px;margin-bottom:10px;border:2px solid {color}88;'>
          <img src='{avatar_url(msg["seed"])}' width='64' style='border-radius:50%;margin-bottom:6px;'/>
          <div style='font-size:1.6rem;'>💀</div>
          <h3 style='margin:2px 0;color:#fff;font-size:1.3rem;'>{msg["name"]}</h3>
          <p style='color:#fff;font-size:0.95rem;'>{msg["role"]}</p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(5)
        st.session_state.elimination_msg = None
        st.rerun()

    st.markdown("<h3>🎮 ΠΑΙΚΤΕΣ</h3>", unsafe_allow_html=True)
    st.caption("Πάτα την κάρτα σου για να δεις τον ρόλο σου")

    # CARDS via components.html
    import json as _json
    cards_data = []
    for p in players:
        if p["role"] == "mr_white":
            br,bw,bc = "⚪ MR WHITE","","#c0392b"
        elif p["role"] == "undercover":
            br,bw,bc = "🟡 UNDERCOVER",word[1],"#d68910"
        else:
            br,bw,bc = "🟢 ΠΟΛΙΤΗΣ",word[0],"#1e8449"
        cards_data.append({"name":p["name"],"seed":p["seed"],"back_role":br,"back_word":bw,"back_color":bc})

    cards_json = _json.dumps(cards_data,ensure_ascii=False)
    n_players = len(players)
    n_rows = (n_players+2)//3
    card_h = 180
    total_h = n_rows*card_h + (n_rows-1)*8 + 20

    cards_html = f"""
    <style>
      body{{margin:0;font-family:'Segoe UI',sans-serif;background:transparent;}}
      .grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;padding:4px 0;}}
      .cw{{aspect-ratio:3/5;perspective:600px;cursor:pointer;}}
      .ci{{position:relative;width:100%;height:100%;transform-style:preserve-3d;transition:transform 0.6s cubic-bezier(0.4,0,0.2,1);}}
      .cw.flipped .ci{{transform:rotateX(180deg);}}
      .cf,.cb{{position:absolute;inset:0;border-radius:12px;backface-visibility:hidden;-webkit-backface-visibility:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:8px;text-align:center;}}
      .cf{{background:linear-gradient(135deg,#667eea,#764ba2);color:#fff;}}
      .cb{{transform:rotateX(180deg);color:#fff;}}
      .cf img{{width:48px;height:48px;border-radius:50%;border:2px solid rgba(255,255,255,0.3);margin-bottom:5px;}}
      .cf .cn{{font-size:10px;font-weight:800;margin-bottom:3px;word-break:break-word;}}
      .cf .ch{{font-size:8px;opacity:0.7;line-height:1.3;}}
      .cb .cr{{font-size:10px;font-weight:800;letter-spacing:1px;margin-bottom:5px;}}
      .cb .cw2{{font-size:14px;font-weight:900;white-space:nowrap;width:90%;text-align:center;}}
      .cb .cc{{font-size:8px;opacity:0.8;margin-bottom:2px;}}
      .cb .ch2{{font-size:8px;opacity:0.6;margin-top:3px;}}
    </style>
    <div class="grid" id="g"></div>
    <script>
      const cards={cards_json};
      const g=document.getElementById("g");
      const base="https://api.dicebear.com/7.x/avataaars/svg?backgroundColor=b6e3f4,c0aede,d1d4f9,ffd5dc,ffdfbf&seed=";
      cards.forEach(c=>{{
        const w=document.createElement("div");
        w.className="cw";
        const wrd=c.back_word
          ?`<div class="cc">Η λέξη σου</div><div class="cw2">${{c.back_word}}</div>`
          :`<div class="cc">Δεν έχεις λέξη</div>`;
        w.innerHTML=`<div class="ci">
          <div class="cf"><img src="${{base+c.seed}}"/><div class="cn">${{c.name}}</div><div class="ch">👆 Πάτα για ρόλο</div></div>
          <div class="cb" style="background:${{c.back_color}};"><div class="cr">${{c.back_role}}</div>${{wrd}}<div class="ch2">👆 Κρύψιμο</div></div>
        </div>`;
        w.addEventListener("click",()=>w.classList.toggle("flipped"));
        g.appendChild(w);
        const we=w.querySelector(".cw2");
        if(we){{let s=14;while(we.scrollWidth>we.clientWidth&&s>7){{s--;we.style.fontSize=s+"px";}}}}
      }});
    </script>
    """
    components.html(cards_html, height=total_h, scrolling=False)

    st.divider()
    st.markdown("<h3>⚔️ ΨΗΦΟΦΟΡΙΑ</h3>", unsafe_allow_html=True)

    # MR WHITE GUESS
    if st.session_state.mr_white_guess_mode:
        removed = st.session_state.mr_white_removed
        st.markdown(f"""
        <div style='text-align:center;padding:12px;background:rgba(192,57,43,0.25);
             border-radius:14px;border:2px solid rgba(192,57,43,0.5);margin-bottom:10px;'>
          <p style='font-size:0.9rem;color:#fff;margin:0;'>⚪ <strong>{removed['name']}</strong> ήταν Mr. White!</p>
          <p style='font-size:0.8rem;opacity:0.8;margin:4px 0 0;'>Μπορεί να μαντέψει τη λέξη;</p>
        </div>
        """, unsafe_allow_html=True)
        guess = st.text_input("Μάντεψε:", placeholder="Η λέξη...", label_visibility="collapsed")
        if st.button("✔ Έλεγχος", use_container_width=True, type="primary"):
            if guess.strip().upper() == word[0].upper():
                st.session_state.finished = True
                st.session_state.winner = "undercover"
            else:
                st.error(f"❌ Λάθος: «{guess}»")
                w = check_winner(game["players"])
                if w == "UNDERCOVER":
                    st.session_state.finished = True
                    st.session_state.winner = "undercover"
                elif w == "ΠΟΛΙΤΕΣ":
                    st.session_state.finished = True
                    st.session_state.winner = "civilians"
            st.session_state.mr_white_guess_mode = False
            st.rerun()
    else:
        names = [p["name"] for p in players]
        idx = st.selectbox("Ποιος φεύγει;", range(len(names)), format_func=lambda i: names[i])
        if st.button("🔥 Αφαίρεση Παίκτη", use_container_width=True):
            removed = players[idx]
            role_labels = {"mr_white":"⚪ Mr. White","undercover":"🟡 Undercover","πολίτης":"🟢 Πολίτης"}
            st.session_state.elimination_msg = {"name":removed["name"],"seed":removed["seed"],"role":role_labels.get(removed["role"],"")}
            game["players"] = [p for p in players if p["name"] != removed["name"]]
            save_game(game)
            w = check_winner(game["players"])
            if removed["role"] == "mr_white":
                st.session_state.mr_white_removed = removed
                st.session_state.mr_white_guess_mode = True
            elif w == "UNDERCOVER":
                st.session_state.finished = True
                st.session_state.winner = "undercover"
            elif w == "ΠΟΛΙΤΕΣ":
                st.session_state.finished = True
                st.session_state.winner = "civilians"
            st.rerun()
