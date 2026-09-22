import random
import time

import streamlit as st

from randq.selector import rand_draw


FLASH_SECONDS = 3


def initialize_state() -> None:
    defaults = {
        "names": [],
        "questions": [],
        "used_names": set(),
        "used_questions": set(),
        "result": None,
        "reveal_at": None,
        "name_input": "",
        "question_input": "",
        "no_repeats": False,
        "draw_error": None,
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def add_name() -> None:
    name = st.session_state.name_input.strip()
    if name:
        st.session_state.names.append(name)
        st.session_state.name_input = ""


def add_question() -> None:
    question = st.session_state.question_input.strip()
    if question:
        st.session_state.questions.append(question)
        st.session_state.question_input = ""


def reset_app() -> None:
    st.session_state.names = []
    st.session_state.questions = []
    st.session_state.used_names = set()
    st.session_state.used_questions = set()
    st.session_state.result = None
    st.session_state.reveal_at = None
    st.session_state.name_input = ""
    st.session_state.question_input = ""
    st.session_state.no_repeats = False
    st.session_state.draw_error = None


def draw_pair() -> None:
    names = st.session_state.names
    questions = st.session_state.questions
    no_repeats = st.session_state.no_repeats

    available_names = [name for name in names if name not in st.session_state.used_names]
    available_questions = [
        question
        for question in questions
        if question not in st.session_state.used_questions
    ]

    if no_repeats and (
        len(available_names) == 0 or len(available_questions) == 0
    ):
        st.session_state.result = None
        st.session_state.preview = None
        st.session_state.draw_error = (
            "No unused name or question remains. Add another item or turn off no repeats."
        )
        return

    draw_names = available_names if no_repeats else names
    draw_questions = available_questions if no_repeats else questions
    result = rand_draw(draw_names, draw_questions)

    if no_repeats:
        st.session_state.used_names.add(result[0])
        st.session_state.used_questions.add(result[1])

    st.session_state.result = result
    st.session_state.reveal_at = time.monotonic() + FLASH_SECONDS
    st.session_state.draw_error = None


@st.fragment(run_every=0.2)
def render_result() -> None:
    result = st.session_state.result
    reveal_at = st.session_state.reveal_at

    if result is None:
        return

    if reveal_at is not None and time.monotonic() < reveal_at:
        name, question = rand_draw(
            st.session_state.names, st.session_state.questions
        )
        st.info(f"{name}, please answer: {question}")
        return

    name, question = result
    st.success(f"{name}, please answer: {question}")


st.set_page_config(page_title="Random Question", page_icon="?")
initialize_state()

st.title("Random Question")
st.write("Build a roster and a question list, then draw a prompt for the class.")

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("Roster")
    st.text_input("Name", key="name_input", on_change=add_name)
    st.button("Add name", on_click=add_name, use_container_width=True)
    if st.session_state.names:
        st.write(st.session_state.names)
    else:
        st.caption("No names added yet.")

with right_column:
    st.subheader("Questions")
    st.text_input("Question", key="question_input", on_change=add_question)
    st.button("Add question", on_click=add_question, use_container_width=True)
    if st.session_state.questions:
        st.write(st.session_state.questions)
    else:
        st.caption("No questions added yet.")

st.divider()
st.checkbox("No repeats", key="no_repeats")
draw_column, reset_column = st.columns(2)
with draw_column:
    st.button(
        "Draw",
        on_click=draw_pair,
        disabled=not st.session_state.names or not st.session_state.questions,
        type="primary",
        use_container_width=True,
    )
with reset_column:
    st.button("Reset", on_click=reset_app, use_container_width=True)

if st.session_state.get("draw_error"):
    st.warning(st.session_state.draw_error)

render_result()
from randq.selector import rand_draw, rand_draw_no_repeat

st.title("Random Question Picker")

if "names" not in st.session_state:
    st.session_state.names = []
if "questions" not in st.session_state:
    st.session_state.questions = []
if "used_names" not in st.session_state:
    st.session_state.used_names = set()
if "used_questions" not in st.session_state:
    st.session_state.used_questions = set()
if "current_pick" not in st.session_state:
    st.session_state.current_pick = None


def add_name():
    if st.session_state.new_name.strip():
        st.session_state.names.append(st.session_state.new_name.strip())
        st.session_state.new_name = ""


def add_question():
    if st.session_state.new_question.strip():
        st.session_state.questions.append(st.session_state.new_question.strip())
        st.session_state.new_question = ""


col1, col2 = st.columns(2)

with col1:
    st.subheader("Names")
    st.text_input("Add a name", key="new_name")
    st.button("Add name", on_click=add_name)

with col2:
    st.subheader("Questions")
    st.text_input("Add a question", key="new_question")
    st.button("Add question", on_click=add_question)

col1, col2 = st.columns(2)
with col1:
    st.write(st.session_state.names)
with col2:
    st.write(st.session_state.questions)

no_repeats = st.checkbox("No repeats within this session")

names = st.session_state.names
questions = st.session_state.questions
# exhausted pools (with no-repeats on) disable the button instead of erroring
pool_exhausted = no_repeats and (
    not [n for n in names if n not in st.session_state.used_names]
    or not [q for q in questions if q not in st.session_state.used_questions]
)

draw_disabled = not names or not questions or pool_exhausted
if pool_exhausted:
    st.warning("All names or questions have been used. Uncheck 'No repeats' or add more.")

if st.button("Draw", disabled=draw_disabled):
    placeholder = st.empty()
    rng = random.Random()
    for _ in range(30):
        placeholder.write(f"{random.choice(names)}, please answer: {random.choice(questions)}")
        time.sleep(0.1)

    if no_repeats:
        chosen_name, chosen_question = rand_draw_no_repeat(
            names, questions, rng, st.session_state.used_names, st.session_state.used_questions
        )
        st.session_state.used_names.add(chosen_name)
        st.session_state.used_questions.add(chosen_question)
    else:
        chosen_name, chosen_question = rand_draw(names, questions, rng)

    placeholder.empty()
    st.session_state.current_pick = (chosen_name, chosen_question)

if st.session_state.current_pick is not None:
    chosen_name, chosen_question = st.session_state.current_pick
    st.success(f"{chosen_name}, please answer: {chosen_question}")
