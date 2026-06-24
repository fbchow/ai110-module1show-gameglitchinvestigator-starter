# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| decimal in input `6.9` | "Write tests in `tests/test_game_logic.py` that test decimal, whitespace, and empty input." | `test_parse_guess_rejects_decimal_input`: asserts `parse_guess("6.9")` returns `(False, None, "That is not a number.")` | Yes | The old `int(float(raw))` silently truncated `6.9` → `6`, corrupting the guess. A decimal isn't a valid integer guess, so it should be rejected outright. |
| random text input `blah` | (same prompt) | `parse_guess("blah")` falls into the `except` branch and returns `(False, None, "That is not a number.")` | Yes | Non-numeric text can't be parsed by `int()`, so the error path is the correct behavior. |
| empty / whitespace input ` ` | (same prompt) | `test_parse_guess_whitespace_only_is_empty` and `test_parse_guess_empty_input`: both assert `(False, None, "Enter a guess.")` | Yes | Used `raw.strip() == ""` so a whitespace-only string is treated as no guess, while a valid number with surrounding spaces (`"  42  "`) still parses correctly. |
| first-attempt win | "Add tests for `update_score` covering the win formula and wrong-guess penalties." | `test_first_attempt_win_awards_90`: asserts `update_score(0, "Win", 1) == 90` | Yes | `attempt_number` is 1-based (incremented before the call), so the old `100 - 10 * (attempt_number + 1)` formula gave 80 on a first-attempt win. Dropping the `+ 1` correctly awards 90. |
| later win point decay | (same prompt) | `test_later_win_points_decay`: asserts `update_score(0, "Win", 2) == 80` | Yes | Confirms each additional attempt costs 10 points off the win value. |
| late-win floor | (same prompt) | `test_win_points_floor_at_10`: asserts `update_score(0, "Win", 20) == 10` | Yes | `max(10, ...)` guarantees a win never awards fewer than 10 points even after many attempts. |
| too-high penalty parity | (same prompt) | `test_too_high_always_penalizes`: asserts `update_score(100, "Too High", 2) == 95` and `update_score(100, "Too High", 3) == 95` | Yes | The old code awarded `+5` on even attempts — a wrong guess must always cost 5, regardless of attempt parity. |
| too-low penalty | (same prompt) | `test_too_low_penalizes`: asserts `update_score(100, "Too Low", 1) == 95` | Yes | A too-low guess is incorrect, so it consistently deducts 5 points. |

```
============================= test session starts ==============================
collected 14 items

tests/test_game_logic.py .....                                           [100%]

============================== 14 passed in 0.07s ===============================
Finished running tests!
```
---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**
Add docstrings to every function in `logic_utils.py`. Review the code for PEP 8 style compliance.  

**Linting output before:**
I just simply have the function description for `get_range_for_difficulty.`  
```
# Get the range according to the difficulty level.  
```
Before lines 42 of the `parse_guess()` function used to have an `except Exception` for cases where the user enters invalid input.  
```
    try:
        value = int(raw)
    except Exception:
        return False, None, "That is not a number."
```

**Changes applied:**
The first line describes what the function does. The format is nicely indented. The arguments and outputs are separated out.  
```
def get_range_for_difficulty(difficulty: str):
    """Return the inclusive guessing range for a given difficulty level.

    Args:
        difficulty: The difficulty name, e.g. "Easy", "Normal", or "Hard".

    Returns:
        A (low, high) tuple of ints describing the inclusive range the
        secret number can fall in. Unknown difficulties fall back to the
        default range.
    """
```
<!-- Describe what you changed based on the AI's suggestions -->
AI also suggested to change the `except Exception` to  `except ValueError` to be more precise about the type of exception raised in the `try except` block. It suggested:  

One recommendation (not a strict PEP 8 formatting rule, but a style/correctness improvement flagged by most linters):

logic_utils.py:42 catches the broad except Exception:. `int()` raises `ValueError` specifically, so narrowing it is more precise and avoids masking unexpected errors:

```
    try:
        value = int(raw)
    except ValueError:
        return False, None, "That is not a number."
Want me to apply that change? Note PEP 8 only forbids bare except: — except Exception isn't a formatting violation, so I left it untouched pending your call. Everything else is already compliant.
```





---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
