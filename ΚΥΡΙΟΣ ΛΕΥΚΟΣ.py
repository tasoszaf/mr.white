import streamlit as st
import random

# -----------------------
# WORD PAIRS (εσύ τα ορίζεις)
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

    return [
        {"name": players[i], "role": roles[i]}
        for i in range(len(players))
    ]

# -----------------------
# INIT STATE
# -----------------------

if "players" not in st.session_state:
    st.session_state.players = []

if "started" not in st.session_state:
    st.session_state.started = False

if "stage" not in st.session_state:
    st.session_state.stage = "setup"  # setup → game → reveal → result

if "revealed" not in st.session_state:
    st.session_state.revealed = False

if "current" not in st.session_state:
    st.session_state.current = 0

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
# GAME PHASE (REVEAL)
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

        st.success("🎉 Τέλος γύρου συζήτησης!")

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

    player = next(p for p in game if p["name"] == eliminated_name)

    st.error(f"❌ Βγήκε: {eliminated_name}")
    st.write(f"🎭 Ρόλος: **{player['role']}**")

    # remove player
    st.session_state.game_data = [
        p for p in game if p["name"] != eliminated_name
    ]

    # MR WHITE GUESS
    if player["role"] == "mr_white":

        guess = st.text_input("🎯 Mr White μάντεψε τη λέξη:")

        if st.button("✔ Έλεγχος"):

            if guess.lower() in [words[0].lower(), words[1].lower()]:
                st.success("🎉 Mr White κέρδισε!")
            else:
                st.error("❌ Mr White έχασε!")

    if st.button("➡ Επόμενος γύρος"):

        st.session_state.stage = "game"
        st.session_state.current = 0
        st.session_state.revealed = False

        # end condition
        if len(st.session_state.game_data) <= 2:
            st.success("🏆 Τέλος παιχνιδιού!")
            st.session_state.stage = "setup"
            st.session_state.players = []
            st.session_state.game_data = []
