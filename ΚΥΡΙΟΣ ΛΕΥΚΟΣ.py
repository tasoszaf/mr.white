import streamlit as st
import random

# -----------------------
# WORD PAIRS (βάζεις εσύ)
# -----------------------

WORDS = [
    ("σκύλος", "γάτα"),
    ("θάλασσα", "λίμνη"),
    ("αυτοκίνητο", "μηχανή"),
    ("πόλη", "χωριό"),
    ("ψωμί", "τυρί")
]

# -----------------------
# ROLES
# -----------------------

def assign_roles(players):
    roles = ["mr_white", "undercover"]

    while len(roles) < len(players):
        roles.append("πολίτης")

    random.shuffle(players)
    random.shuffle(roles)

    return [{"name": players[i], "role": roles[i]} for i in range(len(players))]

# -----------------------
# WIN CHECK
# -----------------------

def check_game_end(players, mr_white_won=False):

    roles = [p["role"] for p in players]

    undercovers = roles.count("undercover")
    civilians = roles.count("πολίτης")

    # 🏆 MR WHITE WINS
    if mr_white_won:
        return "mr_white_win"

    # 🔵 UNDERCOVER WIN (1 undercover + 1 civilian)
    if undercovers == 1 and civilians == 1:
        return "undercover_win"

    # 🔵 UNDERCOVER WIN (no civilians left)
    if undercovers > 0 and civilians == 0:
        return "undercover_win"

    # 🟢 CIVILIANS WIN (no undercover)
    if undercovers == 0:
        return "civilians_win"

    return "continue"

# -----------------------
# INIT STATE
# -----------------------

if "players" not in st.session_state:
    st.session_state.players = []

if "stage" not in st.session_state:
    st.session_state.stage = "setup"

if "current" not in st.session_state:
    st.session_state.current = 0

if "revealed" not in st.session_state:
    st.session_state.revealed = False

# -----------------------
# UI
# -----------------------

st.title("🎭 Mr White Game")

# -----------------------
# SETUP
# -----------------------

if st.session_state.stage == "setup":

    name = st.text_input("👤 Όνομα παίκτη")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("➕ Προσθήκη"):
            if name:
                st.session_state.players.append(name)

    with col2:
        if st.button("▶ Start Game"):
            if len(st.session_state.players) >= 3:
                st.session_state.game_data = assign_roles(st.session_state.players)
                st.session_state.word_pair = random.choice(WORDS)

                st.session_state.stage = "game"
                st.session_state.current = 0
                st.session_state.revealed = False
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

        st.write(f"👉 Δώσε το κινητό σε: **{player['name']}**")

        if st.button("👁 Δες ρόλο"):
            st.session_state.revealed = True

        if st.session_state.revealed:

            if player["role"] == "mr_white":
                st.error("❌ MR WHITE (δεν έχεις λέξη)")
            elif player["role"] == "undercover":
                st.warning(f"🧠 Λέξη: {words[1]}")
            else:
                st.success(f"🧠 Λέξη: {words[0]}")

            if st.button("➡ Επόμενος παίκτης"):
                st.session_state.current += 1
                st.session_state.revealed = False

    else:

        st.success("🎉 Τέλος γύρου")

        eliminated = st.selectbox(
            "❌ Ποιος αποβάλλεται;",
            [p["name"] for p in game]
        )

        if st.button("🔥 Επιβεβαίωση"):

            st.session_state.eliminated = eliminated
            st.session_state.stage = "reveal"

# -----------------------
# REVEAL PHASE
# -----------------------

elif st.session_state.stage == "reveal":

    game = st.session_state.game_data
    words = st.session_state.word_pair

    eliminated_name = st.session_state.eliminated

    player = next((p for p in game if p["name"] == eliminated_name), None)

    if player is None:
        st.error("❌ Player not found")
        st.stop()

    st.error(f"❌ Βγήκε: {eliminated_name}")
    st.write(f"🎭 Ρόλος: **{player['role']}**")

    # remove player
    remaining = [p for p in game if p["name"] != eliminated_name]
    st.session_state.game_data = remaining

    # -----------------------
    # MR WHITE LOGIC
    # -----------------------

    mr_white_won = False

    if player["role"] == "mr_white":

        guess = st.text_input("🎯 Mr White μάντεψε τη λέξη:")

        if st.button("✔ Έλεγχος"):

            if guess.lower() in [words[0].lower(), words[1].lower()]:
                st.success("🏆 MR WHITE ΚΕΡΔΙΣΕ!")
                st.session_state.stage = "setup"
                st.stop()
            else:
                st.error("❌ Λάθος μαντεψιά")

    # -----------------------
    # GAME END CHECK
    # -----------------------

    result = check_game_end(remaining, mr_white_won)

    if result == "mr_white_win":
        st.success("🏆 MR WHITE WIN")
        st.session_state.stage = "setup"

    elif result == "undercover_win":
        st.success("🔵 UNDERCOVER WINS")
        st.session_state.stage = "setup"

    elif result == "civilians_win":
        st.success("🟢 CIVILIANS WIN")
        st.session_state.stage = "setup"

    else:
        st.info("🎮 Συνεχίζεται το παιχνίδι")
        if st.button("➡ Επόμενος γύρος"):
            st.session_state.stage = "game"
            st.session_state.current = 0
            st.session_state.revealed = False
