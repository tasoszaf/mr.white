import streamlit as st
import random

WORDS = [
    ("σκύλος", "γάτα"),
    ("θάλασσα", "λίμνη"),
    ("αυτοκίνητο", "μηχανή"),
]

# ---------------- INIT (FLAT STATE) ----------------

if "players" not in st.session_state:
    st.session_state.players = []

if "game" not in st.session_state:
    st.session_state.game = []

if "word" not in st.session_state:
    st.session_state.word = None

if "stage" not in st.session_state:
    st.session_state.stage = "setup"

if "i" not in st.session_state:
    st.session_state.i = 0

if "eliminated" not in st.session_state:
    st.session_state.eliminated = None

# ---------------- LOGIC ----------------

def assign(players):
    roles = ["mr_white", "undercover"]
    while len(roles) < len(players):
        roles.append("πολίτης")

    random.shuffle(players)
    random.shuffle(roles)

    return [{"name": players[i], "role": roles[i]} for i in range(len(players))]

def reset():
    st.session_state.players = []
    st.session_state.game = []
    st.session_state.word = None
    st.session_state.stage = "setup"
    st.session_state.i = 0
    st.session_state.eliminated = None

# ---------------- UI ----------------

st.title("🎭 Mr White (FINAL STABLE CORE)")

# ---------------- SETUP ----------------

if st.session_state.stage == "setup":

    name = st.text_input("Όνομα")

    if st.button("➕ Add"):
        if name and name not in st.session_state.players:
            st.session_state.players.append(name)

    if st.button("▶ Start"):
        if len(st.session_state.players) >= 3:
            st.session_state.game = assign(st.session_state.players)
            st.session_state.word = random.choice(WORDS)
            st.session_state.stage = "game"
            st.session_state.i = 0

    st.write(st.session_state.players)

# ---------------- GAME ----------------

elif st.session_state.stage == "game":

    game = st.session_state.game

    if st.session_state.i < len(game):

        p = game[st.session_state.i]

        st.write("👉", p["name"])

        if st.button("Reveal"):

            if p["role"] == "mr_white":
                st.error("MR WHITE")
            elif p["role"] == "undercover":
                st.warning(st.session_state.word[1])
            else:
                st.success(st.session_state.word[0])

        if st.button("Next"):
            st.session_state.i += 1

    else:

        st.subheader("❌ Elimination")

        names = [p["name"] for p in game]

        idx = st.selectbox("Pick", range(len(names)), format_func=lambda i: names[i])

        if st.button("Confirm"):
            st.session_state.eliminated = names[idx]
            st.session_state.stage = "reveal"

# ---------------- REVEAL ----------------

elif st.session_state.stage == "reveal":

    game = st.session_state.game
    name = st.session_state.eliminated

    player = next(p for p in game if p["name"] == name)

    st.error(f"Out: {name}")
    st.write(player["role"])

    st.session_state.game = [p for p in game if p["name"] != name]

    roles = [p["role"] for p in st.session_state.game]
    u = roles.count("undercover")
    c = roles.count("πολίτης")

    # WIN CONDITIONS
    if player["role"] == "mr_white":
        st.success("MR WHITE LOSES ROUND / OR CAN GUESS (optional)")
        reset()

    elif u == 1 and c == 1:
        st.success("UNDERCOVER WINS")
        reset()

    elif u == 0:
        st.success("CIVILIANS WIN")
        reset()

    else:
        if st.button("Next Round"):
            st.session_state.stage = "game"
            st.session_state.i = 0
