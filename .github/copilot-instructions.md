This is an in-class coding exercise.

## Commands

- `uv add <pkg>` to add dependencies, `uv run ...` to run things.
  Never `pip` or bare `python`.
- App: `uv run streamlit run app.py`

## Architecture

- `data.py` holds the roster and questions for `cli.py` (hardcoded
  lists). `app.py` builds its own roster and questions at runtime
  via user input — it does not read `data.py`. 
- `selector.py` implements selection logic: pure functions, no
  printing, no file I/O, no streamlit imports. Randomness is
  seedable — the caller passes an `rng`.
- `cli.py` and `app.py` are thin wrappers. They get data from
  `data.py` (or, in `app.py`, from `st.text_area` input), call
  `selector`, and display the result. Neither contains selection
  logic or hardcodes roster/question data of its own.
- A change to `selector.py` must leave both wrappers working.

## Constraints

- Standard library plus streamlit only. Ask before adding any other
  dependency.
- Preserve existing behaviour unless asked to change it.
- Reuse existing code rather than duplicating logic.
