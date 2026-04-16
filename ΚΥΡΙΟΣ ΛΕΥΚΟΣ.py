import streamlit as st
import random

# ================= WORDS =================

WORDS = [
    ("σκύλος", "γάτα"),
    ("θάλασσα", "λίμνη"),
    ("αυτοκίνητο", "μηχανή"),
    ("πόλη", "χωριό"),
    ("ψωμί", "τυρί"),
]

# ================= INIT =================

if "players" not in st.session_state:
    st.session_state.players = []

if "game" not in st.session_state:
    st.session_state.game = None

if "revealed" not in st.session_state:
    st.session_state.revealed = {}

if "last_out" not in st.session_state:
    st.session_state.last_out = None

if "finished" not in st.session_state:
    st.session_state.finished = False

if "winner" not in st.session_state:
    st.session_state.winner = None

if "mr_white_guess" not in st.session_state:
    st.session_state.mr_white_guess = False

# ================= LOGIC =================

def assign_roles(players):
    roles = ["mr_white", "undercover"]

    while len(roles) < len(players):
        roles.append("πολίτης")

    random.shuffle(players)
    random.shuffle(roles)

    return [{"name": players[i], "role": roles[i]} for i in range(len(players))]


def check_winner(players):

    roles = [p["role"] for p in players]

    spies = roles.count("undercover")
    citizens = roles.count("πολίτης")

    if spies >= citizens:
        return "SPIES"

    if spies == 0:
        return "CITIZENS"

    return None


# ================= UI =================

st.title("🎭 Mr White (REVEAL / HIDE CARDS)")

# ================= SETUP =================

if st.session_state.game is None:

    name = st.text_input("👤 Παίκτης")

    if st.button("➕ Add"):
        if name and name not in st.session_state.players:
            st.session_state.players.append(name)

    if st.button("▶ Start Game"):
        if len(st.session_state.players) >= 3:

            st.session_state.game = {
                "players": assign_roles(st.session_state.players),
                "word": random.choice(WORDS),
            }

            # init reveal state
            for p in st.session_state.game["players"]:
                st.session_state.revealed[p["name"]] = False

            st.rerun()

    st.write("👥 Players:", st.session_state.players)

# ================= GAME =================

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

            # ================= REVEAL / HIDE TOGGLE =================

            if st.session_state.revealed.get(p["name"], False):

                # SHOW ROLE
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
    st.subheader("❌ Vote")

    names = [p["name"] for p in players]

    idx = st.selectbox("Ποιος φεύγει;", range(len(names)), format_func=lambda i: names[i])

    if st.button("🔥 Remove Player"):

        removed = players[idx]
        st.session_state.last_out = removed

        players = [p for p in players if p["name"] != removed["name"]]
        game["players"] = players

        if removed["role"] == "mr_white":
            st.session_state.mr_white_guess = True

        st.rerun()

    # ================= MR WHITE GUESS =================

    if st.session_state.mr_white_guess:

        st.subheader("⚪ MR WHITE GUESS")

        guess = st.text_input("Μάντεψε τη λέξη:")

        if st.button("✔ Check"):

            if guess.lower() in [word[0].lower(), word[1].lower()]:
                st.success("🏆 MR WHITE WINS")
                st.session_state.finished = True
                st.session_state.winner = "MR WHITE"
            else:
                st.error("❌ Wrong guess")

            st.session_state.mr_white_guess = False

    # ================= RESULT =================

    if st.session_state.last_out:

        removed = st.session_state.last_out

        st.error(f"❌ Out: {removed['name']}")
        st.write(f"🎭 Role: **{removed['role']}**")

        winner = check_winner(game["players"])

        if winner == "SPIES":
            st.session_state.finished = True
            st.session_state.winner = "🟡 SPIES"

        elif winner == "CITIZENS":
            st.session_state.finished = True
            st.session_state.winner = "🟢 CITIZENS"

        if st.session_state.finished:

            st.success(f"🏁 WINNER: {st.session_state.winner}")

            if st.button("🔁 Restart"):
                st.session_state.clear()
                st.rerun()

    # ================= CONTROLS =================

    st.divider()

    if st.button("🔁 Reset Reveal (Hide All Cards)"):

        for p in players:
            st.session_state.revealed[p["name"]] = False

        st.rerun()
