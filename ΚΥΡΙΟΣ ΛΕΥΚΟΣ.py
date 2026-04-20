import streamlit as st
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

    st.subheader("🎴 Cards")

    cols = st.columns(3)

    for i, p in enumerate(players):
        with cols[i % 3]:
            st.markdown("### 🎴 CARD")
            st.write(f"👤 {p['name']}")

            if st.session_state.revealed.get(p["name"], False):
                if p["role"] == "mr_white":
                    st.error("⚪ MR WHITE")
                elif p["role"] == "undercover":
                    st.warning(word[1])
                else:
                    st.success(word[0])

                if st.button("🔒 Hide", key=f"hide{i}"):
                    st.session_state.revealed[p["name"]] = False
                    st.rerun()
            else:
                st.info("🔒 Hidden")
                if st.button("👁 Reveal", key=f"reveal{i}"):
                    st.session_state.revealed[p["name"]] = True
                    st.rerun()

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
