import streamlit as st
import random
import json
import base64
import requests

# ---------------- CONFIG ----------------

REPO = "tasoszaf/mr.white"  # ⬅️ ΑΛΛΑΞΕ ΤΟ

FILE_PATH = "game.json"

GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]

# ---------------- WORDS ----------------

WORDS = [
    ("σκύλος", "γάτα"),
    ("θάλασσα", "λίμνη"),
    ("αυτοκίνητο", "μηχανή"),
    ("πόλη", "χωριό"),
]

# ---------------- GITHUB SAVE ----------------

def save_to_github(data):

    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"

    content = json.dumps(data, ensure_ascii=False, indent=2)
    encoded = base64.b64encode(content.encode()).decode()

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    # get existing file sha (if exists)
    r = requests.get(url, headers=headers)
    sha = None

    if r.status_code == 200:
        sha = r.json().get("sha")

    payload = {
        "message": "update game state",
        "content": encoded,
    }

    if sha:
        payload["sha"] = sha

    requests.put(url, headers=headers, json=payload)

# ---------------- GAME LOGIC ----------------

def assign_roles(players):
    roles = ["mr_white", "undercover"]

    while len(roles) < len(players):
        roles.append("πολίτης")

    random.shuffle(players)
    random.shuffle(roles)

    return [{"name": players[i], "role": roles[i]} for i in range(len(players))]

# ---------------- INIT ----------------

if "players" not in st.session_state:
    st.session_state.players = []

if "game" not in st.session_state:
    st.session_state.game = None

# ---------------- UI ----------------

st.title("🎭 Mr White (GitHub Version)")

# ---------------- SETUP ----------------

if st.session_state.game is None:

    name = st.text_input("👤 Παίκτης")

    if st.button("➕ Add"):
        if name and name not in st.session_state.players:
            st.session_state.players.append(name)

    if st.button("▶ Start Game"):
        if len(st.session_state.players) >= 3:

            game = {
                "players": assign_roles(st.session_state.players),
                "word": random.choice(WORDS),
                "index": 0,
                "eliminated": None
            }

            st.session_state.game = game
            save_to_github(game)

            st.rerun()

    st.write("👥 Players:", st.session_state.players)

# ---------------- GAME ----------------

else:

    game = st.session_state.game

    players = game["players"]

    st.subheader("🎮 Game")

    i = game["index"]

    # PLAY LOOP
    if i < len(players):

        p = players[i]

        st.write("👉", p["name"])

        if st.button("👁 Reveal"):

            if p["role"] == "mr_white":
                st.error("MR WHITE")
            elif p["role"] == "undercover":
                st.warning(game["word"][1])
            else:
                st.success(game["word"][0])

        if st.button("➡ Next"):
            game["index"] += 1
            st.session_state.game = game
            save_to_github(game)
            st.rerun()

    # ELIMINATION
    else:

        st.subheader("❌ Elimination")

        names = [p["name"] for p in players]

        idx = st.selectbox("Pick", range(len(names)), format_func=lambda i: names[i])

        if st.button("🔥 Confirm"):

            eliminated = names[idx]

            game["players"] = [p for p in players if p["name"] != eliminated]
            game["index"] = 0
            game["eliminated"] = eliminated

            st.session_state.game = game
            save_to_github(game)

            st.rerun()

    # ---------------- RESULT ----------------

    if game.get("eliminated"):

        st.error(f"❌ Out: {game['eliminated']}")

        roles = [p["role"] for p in game["players"]]

        u = roles.count("undercover")
        c = roles.count("πολίτης")

        if u == 1 and c == 1:
            st.success("🔵 UNDERCOVER WINS")

        elif u == 0:
            st.success("🟢 CIVILIANS WIN")
