import streamlit as st
import random
import json
import requests
import base64

# ================= CONFIG =================


REPO = st.secrets["tasoszaf/mr.white"]
BRANCH = st.secrets["main"]

PLAYERS_FILE = "players.json"
GAME_FILE = "current_game.json"

PLAYERS_URL = f"https://api.github.com/repos/{REPO}/contents/{PLAYERS_FILE}"
GAME_URL = f"https://api.github.com/repos/{REPO}/contents/{GAME_FILE}"

# ================= WORDS =================

WORDS = [
    ("σκύλος", "γάτα"),
    ("θάλασσα", "λίμνη"),
    ("αυτοκίνητο", "μηχανή"),
    ("πόλη", "χωριό"),
]

# ================= GITHUB =================

def load_json(url):
    r = requests.get(url, headers={"Authorization": f"token {TOKEN}"})
    if r.status_code == 200:
        data = r.json()
        content = base64.b64decode(data["content"]).decode()
        return json.loads(content), data["sha"]
    return None, None

def save_json(url, data, sha=None):
    payload = {
        "message": "update game",
        "content": base64.b64encode(json.dumps(data, ensure_ascii=False).encode()).decode(),
        "branch": BRANCH
    }
    if sha:
        payload["sha"] = sha

    requests.put(url, json=payload, headers={"Authorization": f"token {TOKEN}"})

# ================= LOAD =================

players, _ = load_json(PLAYERS_URL) or ([], None)
game, game_sha = load_json(GAME_URL)

# ================= INIT =================

if "game" not in st.session_state:
    st.session_state.game = game

if st.session_state.game is None:
    st.session_state.game = None

# ================= FUNCTIONS =================

def assign_roles(players):
    roles = ["mr_white", "undercover"]
    while len(roles) < len(players):
        roles.append("πολίτης")

    p = players[:]
    random.shuffle(p)
    random.shuffle(roles)

    return {p[i]: roles[i] for i in range(len(players))}

# ================= UI =================

st.title("🎭 Mr White (LIVE SAVE GAME)")

# ================= SETUP =================

if st.session_state.game is None:

    st.subheader("Start Game")

    selected = st.multiselect("Players", players)

    if st.button("▶ Start"):

        game = {
            "players": selected,
            "roles": assign_roles(selected),
            "word": random.choice(WORDS),
            "alive": selected,
            "status": "running"
        }

        save_json(GAME_URL, game)

        st.session_state.game = game
        st.rerun()

# ================= GAME =================

else:

    game = st.session_state.game

    st.subheader("🎮 Game Running")

    st.write("Alive players:", game["alive"])

    # reveal roles
    for p in game["players"]:
        if st.button(f"👁 {p}", key=p):

            role = game["roles"][p]

            if role == "mr_white":
                st.error("MR WHITE")
            elif role == "undercover":
                st.warning(game["word"][1])
            else:
                st.success(game["word"][0])

    # ================= ELIMINATION =================

    st.divider()

    kill = st.selectbox("Eliminate player", game["alive"])

    if st.button("🔥 Remove"):

        game["alive"].remove(kill)

        save_json(GAME_URL, game)

        st.session_state.game = game

        st.rerun()

    # ================= RESET =================

    if st.button("🏁 End Game"):

        empty = {
            "players": [],
            "roles": {},
            "word": [],
            "alive": [],
            "status": "ended"
        }

        save_json(GAME_URL, empty)

        st.session_state.game = None
        st.rerun()
