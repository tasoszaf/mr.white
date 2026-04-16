import streamlit as st
import json
import random
import os

FILE = "game.json"

WORDS = [
    ("σκύλος", "γάτα"),
    ("θάλασσα", "λίμνη"),
    ("αυτοκίνητο", "μηχανή"),
    ("πόλη", "χωριό"),
    ("ψωμί", "τυρί")
]

# ---------------- FILE SYSTEM ----------------

def save_game(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_game():
    if not os.path.exists(FILE):
        return None
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

# ---------------- GAME LOGIC ----------------

def assign_roles(players):
    roles = ["mr_white", "undercover"]

    while len(roles) < len(players):
        roles.append("πολίτης")

    random.shuffle(players)
    random.shuffle(roles)

    return [{"name": players[i], "role": roles[i]} for i in range(len(players))]

def create_new_game(players):
    return {
        "players": assign_roles(players),
        "word": random.choice(WORDS),
        "stage": "game",
        "index": 0,
        "eliminated": None
    }

# ---------------- UI INIT ----------------

st.title("🎭 Mr White (JSON STABLE VERSION)")

if "players" not in st.session_state:
    st.session_state.players = []

game = load_game()

# ---------------- SETUP ----------------

if game is None:

    st.subheader("Setup")

    name = st.text_input("Όνομα")

    if st.button("➕ Προσθήκη"):
        if name and name not in st.session_state.players:
            st.session_state.players.append(name)

    if st.button("▶ Start Game"):
        if len(st.session_state.players) >= 3:
            game = create_new_game(st.session_state.players)
            save_game(game)
            st.rerun()

    st.write("👥 Παίκτες:", st.session_state.players)

# ---------------- GAME ----------------

else:

    players = game["players"]
    word = game["word"]

    st.subheader("🎮 Game")

    idx = game["index"]

    # ---------------- REVEAL ----------------

    if idx < len(players):

        p = players[idx]

        st.write("👉", p["name"])

        if st.button("👁 Reveal"):

            if p["role"] == "mr_white":
                st.error("MR WHITE")
            elif p["role"] == "undercover":
                st.warning(word[1])
            else:
                st.success(word[0])

        if st.button("➡ Next"):
            game["index"] += 1
            save_game(game)
            st.rerun()

    # ---------------- ELIMINATION ----------------

    else:

        st.subheader("❌ Αποβολή")

        names = [p["name"] for p in players]

        idx_sel = st.selectbox("Παίκτης", range(len(names)), format_func=lambda i: names[i])

        if st.button("🔥 Confirm"):

            eliminated = names[idx_sel]
            game["eliminated"] = eliminated

            # remove player
            game["players"] = [p for p in players if p["name"] != eliminated]

            save_game(game)
            st.rerun()

# ---------------- REVEAL PHASE ----------------

if game and game.get("eliminated"):

    players = game["players"]
    word = game["word"]

    eliminated = game["eliminated"]

    player = next(p for p in players if p["name"] == eliminated)

    st.error(f"❌ Βγήκε: {player['name']}")
    st.write("🎭 Ρόλος:", player["role"])

    # MR WHITE
    if player["role"] == "mr_white":

        guess = st.text_input("🎯 Μάντεψε λέξη:")

        if st.button("✔ Check"):

            if guess.lower() in [word[0].lower(), word[1].lower()]:
                st.success("🏆 MR WHITE WINS")
                os.remove(FILE)
                st.rerun()

    # WIN CONDITIONS
    roles = [p["role"] for p in players]
    u = roles.count("undercover")
    c = roles.count("πολίτης")

    if u == 1 and c == 1:
        st.success("🔵 UNDERCOVER WINS")
        os.remove(FILE)

    elif u == 0:
        st.success("🟢 CIVILIANS WIN")
        os.remove(FILE)

    if st.button("➡ Next Round"):
        game["index"] = 0
        game["eliminated"] = None
        save_game(game)
        st.rerun()
