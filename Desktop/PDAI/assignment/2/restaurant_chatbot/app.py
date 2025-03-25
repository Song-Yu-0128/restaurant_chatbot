import streamlit as st
import cohere
from dotenv import load_dotenv
import os
import json

# 1) Load Cohere key
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

# 2) Streamlit setup
st.set_page_config(page_title="Restaurant Chatbot", page_icon="🍽️")
st.title("🍽️ Restaurant Reservation Chatbot")

# 3) Define slots in the order we want to fill them
slots = ["people", "day", "time", "name", "phone"]

# 4) Initialize session state
if "slot_values" not in st.session_state:
    st.session_state.slot_values = {k: None for k in slots}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_missing_slot" not in st.session_state:
    st.session_state.last_missing_slot = None

# 5) Prompt builder (few-shot example)
def build_prompt(message: str) -> str:
    return f"""
You are an expert reservation system. Use EXACT user words for the name if provided.
Respond ONLY with a valid JSON object with these keys: "people", "day", "time", "name", "phone".
If a field is not mentioned, set it to null. No extra text.

Example:
User: "I want a table for 2 tomorrow at 8pm. My name is Alex."
JSON:
{{
  "people": 2,
  "day": "tomorrow",
  "time": "8pm",
  "name": "Alex",
  "phone": null
}}

Now, parse this user message:
User: "{message}"
JSON:
"""

# 6) Check if all slots are filled
def all_slots_filled() -> bool:
    return all(st.session_state.slot_values[s] is not None for s in slots)

# 7) Display chat history
for entry in st.session_state.chat_history:
    st.markdown(f"**{entry['role'].capitalize()}:** {entry['message']}")

# 8) Input + button
user_input = st.text_input("You:")
send_clicked = st.button("Send")

def ask_for_next_slot():
    """Ask for the next missing slot in the order of `slots`."""
    missing_slots = [s for s in slots if st.session_state.slot_values[s] is None]
    if not missing_slots:
        # Nothing is missing, all done
        return
    # Enforce the order defined by the `slots` list
    next_slot = missing_slots[0]
    st.session_state.last_missing_slot = next_slot

    questions = {
        "people": "How many people is the reservation for?",
        "day": "Which day would you like to come?",
        "time": "What time do you prefer?",
        "name": "Can I get a name for the booking?",
        "phone": "What’s your phone number?"
    }
    question = questions[next_slot]
    st.session_state.chat_history.append({"role": "assistant", "message": question})

if send_clicked and user_input.strip():
    message = user_input.strip()
    # Add user message to chat
    st.session_state.chat_history.append({"role": "user", "message": message})

    # 1) If we're waiting for a direct answer to a specific slot
    if st.session_state.last_missing_slot is not None:
        slot_to_update = st.session_state.last_missing_slot
        st.session_state.slot_values[slot_to_update] = message
        st.session_state.last_missing_slot = None

    else:
        # 2) Use LLM to parse new info from the message
        prompt = build_prompt(message)
        try:
            response = co.generate(prompt=prompt, model="command", max_tokens=100)
            raw_output = response.generations[0].text.strip()
            st.write("**LLM raw output:**", raw_output)  # debug
            prediction = json.loads(raw_output)
        except Exception as e:
            st.session_state.chat_history.append({"role": "assistant", "message": f"Error: {e}"})
            st.rerun()

        # Update each slot from LLM output
        for k in slots:
            val = prediction.get(k)
            # If LLM gave a real value, store it
            if val not in (None, ""):
                st.session_state.slot_values[k] = val

    # 3) Check if all slots are filled
    if not all_slots_filled():
        # Ask for next missing slot in the order
        ask_for_next_slot()
    else:
        # Everything filled => finalize
        summary = json.dumps(st.session_state.slot_values, indent=2)
        final_msg = f"Thanks! Here's your booking:\n```json\n{summary}\n```"
        st.session_state.chat_history.append({"role": "assistant", "message": final_msg})

    # 4) Rerun to refresh UI
    st.rerun()
