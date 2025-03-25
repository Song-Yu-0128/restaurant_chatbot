# 🍽️ Restaurant Reservation Chatbot

This is a simple conversational chatbot that helps users make restaurant reservations using natural language.

Built with:
- [Streamlit](https://streamlit.io) for the web interface
- [Cohere](https://cohere.com) API for natural language processing
- Python

---

## 🚀 Features

- Extracts reservation details like:
  - Number of people
  - Day and time
  - Name and phone number
- Handles multi-turn conversation to collect missing info
- Uses a hosted LLM to understand free-text input
- Clean UI built with Streamlit

---

## 📦 Setup & Run Locally

1. Clone the repository:
```bash
git clone https://github.com/Song-Yu-0128/restaurant_chatbot.git
cd restaurant_chatbot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Add your Cohere API key to a `.env` file:
```
COHERE_API_KEY=your_actual_key_here
```

4. Run the app:
```bash
streamlit run app.py
```

---

## 📁 File Structure

```
restaurant_chatbot/
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
└── README.md           # You're reading it!
```

---

## 📄 License

For educational use only. Part of the ESADE MSc Business Analytics course: *Prototyping with Data and AI*.
