import streamlit as st
import streamlit.components.v1 as components
import random
import json
import os

# ================= FILES =================

PLAYERS_FILE = "players.json"
GAME_FILE = "game.json"

# ================= WORDS =================

WORDS = [
    ("σκύλος", "γάτα"),
    ("θάλασσα", "λίμνη"),
    ("αυτοκίνητο", "μηχανή"),
    ("πόλη", "χωριό"),
    ("ψωμί", "τυρί"),
]

# ================= LOAD / SAVE =================

def load_players():
    if os.path.exists(PLAYERS_FILE):
        with open(PLAYERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_players(players):
    with open(PLAYERS_FILE, "w", encoding="utf-8") as f:
        json.dump(players, f, ensure_ascii=False, indent=2)

def load_game():
    if os.path.exists(GAME_FILE):
        with open(GAME_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
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

# ================= HELPERS =================

def assign_roles(players):
    roles = ["mr_white", "undercover"] + ["πολίτης"] * (len(players) - 2)
    shuffled = players[:]
    random.shuffle(shuffled)
    random.shuffle(roles)
    return [{"name": shuffled[i], "role": roles[i]} for i in range(len(shuffled))]

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
    if os.path.exists(GAME_FILE):
        os.remove(GAME_FILE)

# ================= UI =================

st.title("🎭 Mr White")

# ================= END SCREEN =================

if st.session_state.finished:

    game = st.session_state.game
    word = game["word"] if game else ("?", "?")
    winner = st.session_state.winner

    st.divider()

    if winner == "⚪ MR WHITE":
        st.error("## ⚪ Νίκησε ο Mr. White!")
        st.markdown("Ο Mr. White μάντεψε σωστά τη λέξη και κέρδισε μόνος του.")
    elif winner == "🟡 INFILTRATORS":
        st.warning("## 🟡 Νίκησαν οι Infiltrators!")
        st.markdown("Undercover & Mr. White επιβίωσαν — οι πολίτες έχασαν.")
    elif winner == "🟢 CIVILIANS":
        st.success("## 🟢 Νίκησαν οι Πολίτες!")
        st.markdown("Όλοι οι infiltrators αποκαλύφθηκαν!")

    st.divider()
    st.subheader("🎭 Ρόλοι παικτών")

    role_labels = {
        "mr_white":  "⚪ Mr. White",
        "undercover": "🟡 Undercover",
        "πολίτης":   "🟢 Πολίτης",
    }

    all_game_players = game.get("all_players", game["players"])

    for p in all_game_players:
        role = role_labels.get(p["role"], p["role"])
        if p["role"] == "undercover":
            st.write(f"**{p['name']}** — {role} *(λέξη: {word[1]})*")
        elif p["role"] == "πολίτης":
            st.write(f"**{p['name']}** — {role} *(λέξη: {word[0]})*")
        else:
            st.write(f"**{p['name']}** — {role}")

    st.divider()
    st.markdown(f"**Λέξη πολιτών:** {word[0]}  |  **Λέξη undercover:** {word[1]}")
    st.divider()

    if st.button("🆕 New Game", type="primary"):
        reset_game()
        st.rerun()

# ================= SETUP PHASE =================

elif st.session_state.game is None:

    st.subheader("👥 Players Setup")

    all_players = load_players()
    selected_players = []

    if all_players:
        st.markdown("**Αποθηκευμένοι παίκτες — επίλεξε ποιοι παίζουν:**")
        cols = st.columns(2)
        to_delete = []

        for i, name in enumerate(all_players):
            with cols[i % 2]:
                col_check, col_del = st.columns([4, 1])
                with col_check:
                    if st.checkbox(name, key=f"sel_{name}"):
                        selected_players.append(name)
                with col_del:
                    if st.button("🗑", key=f"del_{name}", help=f"Διαγραφή {name}"):
                        to_delete.append(name)

        if to_delete:
            updated = [p for p in all_players if p not in to_delete]
            save_players(updated)
            st.rerun()

        st.divider()

    st.markdown("**Προσθήκη νέου παίκτη:**")
    new_name = st.text_input("👤 Όνομα νέου παίκτη")

    if st.button("➕ Add Player"):
        if new_name:
            all_players = load_players()
            if new_name not in all_players:
                all_players.append(new_name)
                save_players(all_players)
                st.rerun()

    st.divider()

    if len(selected_players) >= 3:
        st.success(f"✅ Επιλεγμένοι: {', '.join(selected_players)}")
    elif selected_players:
        st.warning(f"⚠️ Χρειάζονται τουλάχιστον 3 παίκτες. Έχεις επιλέξει {len(selected_players)}.")
    else:
        st.info("Επίλεξε παίκτες ή πρόσθεσε νέους.")

    if st.button("▶ Start Game", disabled=len(selected_players) < 3):
        players_with_roles = assign_roles(selected_players.copy())
        st.session_state.game = {
            "players": players_with_roles,
            "all_players": [p.copy() for p in players_with_roles],
            "word": random.choice(WORDS),
        }
        save_game(st.session_state.game)
        for p in st.session_state.game["players"]:
            st.session_state.revealed[p["name"]] = False
        st.rerun()

# ================= GAME PHASE =================

else:

    game = st.session_state.game
    players = game["players"]
    word = game["word"]

    st.subheader("🎴 Κάρτες Παικτών")
    st.caption("Πάτα την κάρτα σου για να δεις τον ρόλο σου — μόνος/η σου!")

    # Build card data for HTML
    cards_data = []
    for p in players:
        if p["role"] == "mr_white":
            back_role = "⚪ MR WHITE"
            back_word = ""
            back_color = "#c0392b"
            back_text_color = "#fff"
        elif p["role"] == "undercover":
            back_role = "🕵️ UNDERCOVER"
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

    cards_html = f"""
    <style>
      body {{ margin: 0; font-family: sans-serif; background: transparent; }}
      .cards-grid {{
        display: flex;
        flex-wrap: wrap;
        gap: 16px;
        justify-content: center;
        padding: 8px 0 16px 0;
      }}
      .card-wrap {{
        width: 150px;
        height: 210px;
        perspective: 1000px;
        cursor: pointer;
      }}
      .card-inner {{
        position: relative;
        width: 100%;
        height: 100%;
        transform-style: preserve-3d;
        transition: transform 0.6s cubic-bezier(.4,2,.6,1);
        border-radius: 14px;
      }}
      .card-wrap.flipped .card-inner {{
        transform: rotateY(180deg);
      }}
      .card-front, .card-back {{
        position: absolute;
        width: 100%;
        height: 100%;
        border-radius: 14px;
        backface-visibility: hidden;
        -webkit-backface-visibility: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 12px;
        box-sizing: border-box;
        text-align: center;
        box-shadow: 0 4px 18px rgba(0,0,0,0.18);
      }}
      .card-front {{
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
        color: #fff;
        border: 2px solid #e94560;
      }}
      .card-front .card-icon {{
        font-size: 36px;
        margin-bottom: 10px;
      }}
      .card-front .card-name {{
        font-size: 18px;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
        word-break: break-word;
      }}
      .card-front .tap-hint {{
        font-size: 11px;
        color: #aab;
        margin-top: 6px;
        line-height: 1.4;
      }}
      .card-back {{
        transform: rotateY(180deg);
        color: #fff;
        flex-direction: column;
        gap: 10px;
      }}
      .card-back .role-label {{
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 1px;
      }}
      .card-back .word-label {{
        font-size: 22px;
        font-weight: 800;
        background: rgba(255,255,255,0.18);
        border-radius: 8px;
        padding: 6px 14px;
      }}
      .card-back .word-caption {{
        font-size: 11px;
        opacity: 0.75;
      }}
      .card-back .flip-back {{
        margin-top: 8px;
        font-size: 11px;
        opacity: 0.6;
      }}
      .pulse-ring {{
        width: 10px; height: 10px;
        border-radius: 50%;
        background: #e94560;
        animation: pulse 1.5s infinite;
        margin-bottom: 4px;
      }}
      @keyframes pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(233,69,96,0.5); }}
        70% {{ box-shadow: 0 0 0 8px rgba(233,69,96,0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(233,69,96,0); }}
      }}
    </style>

    <div class="cards-grid" id="cardsGrid"></div>

    <script>
      const cards = {cards_json};
      const grid = document.getElementById("cardsGrid");

      cards.forEach((c, i) => {{
        const wrap = document.createElement("div");
        wrap.className = "card-wrap";
        wrap.id = "card-" + i;

        const wordHtml = c.back_word
          ? `<div class="word-caption">Η λέξη σου</div>
             <div class="word-label">${{c.back_word}}</div>`
          : `<div class="word-caption" style="font-size:12px;opacity:0.7;">Δεν έχεις λέξη</div>`;

        wrap.innerHTML = `
          <div class="card-inner">
            <div class="card-front">
              <div class="pulse-ring"></div>
              <div class="card-icon">🎭</div>
              <div class="card-name">${{c.name}}</div>
              <div class="tap-hint">Πάτα για να δεις<br>τον ρόλο σου</div>
            </div>
            <div class="card-back" style="background:${{c.back_color}};">
              <div class="role-label">${{c.back_role}}</div>
              ${{wordHtml}}
              <div class="flip-back">Πάτα για να κρύψεις</div>
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

    components.html(cards_html, height=260 if len(players) <= 3 else 500, scrolling=False)

    # ================= VOTE =================

    st.divider()
    st.subheader("❌ Vote Phase")

    names = [p["name"] for p in players]
    idx = st.selectbox("Ποιος φεύγει;", range(len(names)), format_func=lambda i: names[i])

    if st.button("🔥 Remove Player"):
        removed = players[idx]
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
        st.warning(f"⚪ Ο **{removed['name']}** ήταν Mr. White! Μαντεύει τη λέξη...")

        guess = st.text_input("Μάντεψε τη λέξη:")

        if st.button("✔ Check Guess"):
            if guess.lower() in [word[0].lower(), word[1].lower()]:
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
