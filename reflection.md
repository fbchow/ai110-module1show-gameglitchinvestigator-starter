# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?  
  - It looked like a reasonably designed game at first glance. The objective to "guess the correct number" with the option of selecting the game difficulty seems pretty straightforward.  
- List at least two concrete bugs you noticed at the start  
  - The hints were backwards or reversed.
  - The number of attempts is incorrectly counted. It starts at 1 already -- even before the player has made a turn yet.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|"Easy mode"|"Attempts left: 6."  | "Attempts left: 5." | "Attempts: 1" `st.session_state.attempts = 1`|
|Guess of -20 |Warning or error should be raised on guesses outside the range. |"Go lower!" hint | `check_guess()` error message incorrect logic.|
|Guess of 50 |"Too low" hint |"Too high" hint | `check_guess()` error message prints opposite message.|
|"Hard" difficulty | Dynamically change upper range to reflect limits based on difficulty level. "Guess a number between 1 and 50."   | Static text in game instructions with incorrect upper bound.| "Guess a number between 1 and 100." In lines 94-95, `st.info(f"Guess a number between 1 and 100.)` |
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
  - Claude Code.  
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
  - AI correctly suggested that the logic in the guess was correct but just the hint messages needed to be swapped in `check_guess()`, lines 37-40.
  - For example: "Too High", "📈 Go HIGHER!" should be replaced with "Too High", 📉 Go LOWER!"
  - I verified this result by implementing the changes and then playing the game. I also ran the logic test cases in `test_game_logic.py` that corresponded with the hints I'd expect as a user making guesses.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
  - AI says:
```parse_guess only checks parseability, not whether the number is within the difficulty range (e.g. 1–100). "-50" or "99999" parse fine here; range validation must happen elsewhere.```
  - That's not entirely true; validation could happen here. This is a case of AI being too literal about semantics. Parsing and range validation could mean the same thing contextually here arguablly.
  - AI incorrectly suggested that whitespace surrounding an integer should still parse. I think that's too generous to be so permissive of possible valid inputs for a user. But that's subjective, so we can keep white space as a valid guess. You could test this change by playing the game and entering "  42 " as an input. Or adding this case as a unit test.
    ```def test_parse_guess_handles_whitespace():
    # Surrounding whitespace around a valid integer should still parse.
    ok, value, err = parse_guess("  42  ")
    assert ok is True
    assert value == 42
    assert err is None```

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
  - I played the game for myself after making a fix and I ran the corresponding unit tests.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  - I tested if the guess was too low. If the secret is 50 and the guess is 40, then the hint should say "Too Low" in the message.  
- Did AI help you design or understand any tests? How?
  - AI helped explain that the original test cases only tested the result variable but not the actual text content in the message.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- "Every click restarts the whole script, but session state is the one part of memory that's allowed to survive the restart."

- Claude's Explanation:  
  ```
  Session state: Think of it as a sticky note that survives the chef throwing everything out and starting over. It's a little dictionary-like storage (st.session_state) that persists across reruns for a given user's session. So instead of declaring counter = 0 at the top of your script (which would reset every rerun), you stash it in st.session_state.counter, and Streamlit keeps that value around between reruns — until the browser tab closes or the session ends.
  
  Putting it together with an analogy: Picture a whiteboard (your script) that gets erased and rewritten from scratch every time someone asks a question. Normally anything written on it disappears. But there's a locked drawer next to the whiteboard (session state) that doesn't get erased — so if you want certain numbers or choices to survive between rewrites, you put them in the drawer instead of writing them directly on the board.
  ```

---  

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  - Writing distinct unit tests to incremental changes is a good practice to adopt.
- What is one thing you would do differently next time you work with AI on a coding task?
  - I would try to change one thing at a time. And verify it. I think AI wants to do to many large changes at once; the plan mode suggested can just have too much cognitive overload. I would try to break down changes into even smaller, incremental steps.  
- In one or two sentences, describe how this project changed the way you think about AI generated code.
  - I think that AI can be useful in debugging -- given that you provide the contextual artifacts to refer to. But I think that AI can be less useful because it tries too hard to over optimize EVERYTHING at once.
