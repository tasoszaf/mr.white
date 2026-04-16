import streamlit as st
import random

# -----------------------
# WORDS (εσύ τα βάζεις)
# -----------------------

WORDS = [
    ("σκύλος", "γάτα"),
    ("θάλασσα", "λίμνη"),
    ("αυτοκίνητο", "μηχανή"),
    ("πόλη", "χωριό"),
    ("ψωμί", "τυρί")
]

# -----------------------
# CORE GAME LOGIC
# -----------------------

def assign_roles(players):
    roles = ["mr_white", "undercover"]

    while len(roles) < len(players):
        roles.append("πολίτης")

    random.shuffle(players)
    random.shuffle(roles)

    return [{"name": players[i], "role": roles[i]} for i in range(len(players))]


def get_player(game, name):
    return next((p for p in game if p["name"] == name), None)


def check_game_end(players):
    roles = [p["role"] for p in players]

    undercovers = roles.count("undercover")
    civilians = roles.count("πολίτης")

    if undercovers == 1 and civilians == 1:
        return "undercover_win"

    if undercovers == 0:
        return "civilians_win"

    return "continue"

# -----------------------
# INIT STATE (SAFE)
# -----------------------

defaults = {
    "stage": "setup",
    "players": [],
    "game_data": [],
    "word_pair": None,
    "current": 0,
    "revealed": False,
    "eliminated": None
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------
# RESET FUNCTION
# -----------------------

def reset_game():
    st.session_state.stage = "setup"
    st.session_state.players = []
    st.session_state.game_data = []
    st.session_state.word_pair = None
    st.session_state.current = 0
    st.session_state.revealed = False
    st.session_state.eliminated = None

# -----------------------
# UI
# -----------------------

st.title("🎭 Mr White (Stable Version)")

# -----------------------
# SETUP
# -----------------------

if st.session_state.stage == "setup":

    name = st.text_input("👤 Όνομα παίκτη")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Προσθήκη"):
            if name and name not in st.session_state.players:
                st.session_state.players.append(name)

    with col2:
        if st.button("▶ Start Game"):
            if len(st.session_state.players) >= 3:
                st.session_state.game_data = assign_roles(st.session_state.players)
                st.session_state.word_pair = random.choice(WORDS)

                st.session_state.stage = "game"
                st.session_state.current = 0
                st.session_state.revealed = False
                st.session_state.eliminated = None
            else:
                st.warning("Χρειάζονται τουλάχιστον 3 παίκτες")

    st.write("👥 Παίκτες:", st.session_state.players)

# -----------------------
# GAME PHASE
# -----------------------

elif st.session_state.stage == "game":

    game = st.session_state.game_data
    words = st.session_state.word_pair
    i = st.session_state.current

    st.subheader("🎮 Game Phase")

    if i < len(game):

        player = game[i]

        st.write(f"👉 Παίξε στο κινητό: **{player['name']}**")

        if st.button("👁 Reveal"):
            st.session_state.revealed = True

        if st.session_state.revealed:

            if player["role"] == "mr_white":
                st.error("❌ MR WHITE (χωρίς λέξη)")
            elif player["role"] == "undercover":
                st.warning(f"🧠 Λέξη: {words[1]}")
            else:
                st.success(f"🧠 Λέξη: {words[0]}")

            if st.button("➡ Επόμενος παίκτης"):
                st.session_state.current += 1
                st.session_state.revealed = False

    else:

        st.success("🎉 Τέλος γύρου")

        options = [p["name"] for p in game]

        eliminated = st.selectbox("❌ Ποιος αποβάλλεται;", options)

        if st.button("🔥 Επιβεβαίωση"):
            st.session_state.eliminated = eliminated
            st.session_state.stage = "reveal"

# -----------------------
# REVEAL PHASE (SAFE CORE)
# -----------------------

elif st.session_state.stage == "reveal":

    game = st.session_state.game_data
    words = st.session_state.word_pair

    eliminated_name = st.session_state.eliminated

    # 🔒 SAFE CHECK 1
    if not eliminated_name:
        st.error("❌ No eliminated player selected")
        st.stop()

    player = get_player(game, eliminated_name)

    # 🔒 SAFE CHECK 2
    if player is None:
        st.error("❌ Player not found (state mismatch fixed)")
        st.stop()

    st.error(f"❌ Βγήκε: {eliminated_name}")
    st.write(f"🎭 Ρόλος: **{player['role']}**")

    # remove player safely
    remaining = [p for p in game if p["name"] != eliminated_name]
    st.session_state.game_data = remaining

    # -----------------------
    # MR WHITE LOGIC
    # -----------------------

    if player["role"] == "mr_white":

        guess = st.text_input("🎯 Mr White μάντεψε τη λέξη:")

        if st.button("✔ Έλεγχος"):

            if guess.lower() in [words[0].lower(), words[1].lower()]:
                st.success("🏆 MR WHITE ΚΕΡΔΙΣΕ!")
                reset_game()
                st.stop()
            else:
                st.error("❌ Λάθος μαντεψιά")

    # -----------------------
    # GAME END CHECK
    # -----------------------

    result = check_game_end(remaining)

    if result == "undercover_win":
        st.success("🔵 UNDERCOVER WINS")
        reset_game()

    elif result == "civilians_win":
        st.success("🟢 CIVILIANS WINS")
        reset_game()

    else:
        st.info("🎮 Συνεχίζεται...")

        if st.button("➡ Επόμενος γύρος"):
            st.session_state.stage = "game"
            st.session_state.current = 0
            st.session_state.revealed = False
            st.session_state.eliminated = None
