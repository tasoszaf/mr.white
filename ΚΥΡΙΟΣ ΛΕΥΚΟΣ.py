import streamlit as st
import random

# -----------------------
# WORDS
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

if "show_role" not in st.session_state:
    st.session_state.show_role = False

if "votes" not in st.session_state:
    st.session_state.votes = {}

# -----------------------
# UI
# -----------------------

st.title("🎭 Mr White Game")

# -----------------------
# SETUP
# -----------------------

if not st.session_state.started:

    name = st.text_input("👤 Όνομα παίκτη")

    if st.button("➕ Προσθήκη"):
        if name:
            st.session_state.players.append(name)

    st.write("👥 Παίκτες:", st.session_state.players)

    if st.button("▶ Start Game"):
        if len(st.session_state.players) >= 3:
            st.session_state.started = True
            st.session_state.game_data = assign_roles(st.session_state.players)
            st.session_state.word_pair = random.choice(WORDS)
            st.session_state.stage = "game"
        else:
            st.warning("Χρειάζονται τουλάχιστον 3 παίκτες")

# -----------------------
# GAME
# -----------------------

else:

    game = st.session_state.game_data
    words = st.session_state.word_pair

    # -------------------
    # GAME PHASE
    # -------------------
    if st.session_state.stage == "game":

        st.subheader("🎮 Συζήτηση / Παιχνίδι")

        st.write("👥 Παίκτες:", [p["name"] for p in game])

        if st.button("🗳 Πάμε ψηφοφορία"):
            st.session_state.stage = "vote"

        if st.button("👁 Δες ξανά ρόλο / λέξη"):
            st.session_state.stage = "reveal_any"

    # -------------------
    # REVEAL ANY TIME
    # -------------------
    elif st.session_state.stage == "reveal_any":

        player_name = st.selectbox(
            "Διάλεξε παίκτη",
            [p["name"] for p in game]
        )

        player = next(p for p in game if p["name"] == player_name)

        if st.button("🔍 Δείξε ρόλο"):

            if player["role"] == "mr_white":
                st.error("❌ MR WHITE (δεν έχεις λέξη)")
            elif player["role"] == "undercover":
                st.warning(f"🧠 Λέξη: {words[1]}")
            else:
                st.success(f"🧠 Λέξη: {words[0]}")

        if st.button("⬅ Πίσω"):
            st.session_state.stage = "game"

    # -------------------
    # VOTING
    # -------------------
    elif st.session_state.stage == "vote":

        st.subheader("🗳 Ψηφοφορία")

        options = [p["name"] for p in game]

        vote = st.selectbox("Ποιον ψηφίζεις;", options)

        if st.button("✔ Ψήφισε"):
            st.session_state.votes[vote] = st.session_state.votes.get(vote, 0) + 1
            st.success("Καταγράφηκε ψήφος!")

        if st.button("🏁 Τέλος ψηφοφορίας"):
            st.session_state.stage = "result"

    # -------------------
    # RESULT
    # -------------------
    elif st.session_state.stage == "result":

        st.subheader("🏆 Αποτέλεσμα")

        if st.session_state.votes:
            eliminated = max(st.session_state.votes, key=st.session_state.votes.get)
        else:
            eliminated = random.choice([p["name"] for p in game])

        st.error(f"❌ Βγήκε: {eliminated}")

        player = next(p for p in game if p["name"] == eliminated)

        st.write("🎭 Ρόλος:", player["role"])

        # MR WHITE GUESS
        if player["role"] == "mr_white":

            guess = st.text_input("🎯 Mr White μάντεψε τη λέξη:")

            if st.button("✔ Έλεγχος"):

                if guess.lower() in [words[0].lower(), words[1].lower()]:
                    st.success("🎉 Ο Mr White κέρδισε!")
                else:
                    st.error("❌ Έχασε!")

        if st.button("🔄 Νέο παιχνίδι"):
            st.session_state.clear()
