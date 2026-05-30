# IT Helpdesk Automation Assistant
**Roll No: 24ADR013 | Project 15**

A LLaMA3-powered IT helpdesk chatbot that answers common technical issues automatically.

---

## Project Structure

```
helpdesk-bot/
├── app.py               ← Flask backend (main server)
├── knowledge_base.txt   ← IT FAQs your bot learns from
├── requirements.txt     ← Python dependencies
├── README.md            ← This file
└── templates/
    └── index.html       ← Chat web interface
```

---

## Setup & Run (Step by Step)

### Step 1 — Make sure Ollama is running
Open a terminal and run:
```
ollama serve
```
In a second terminal, pull the LLaMA3 model if you haven't:
```
ollama pull llama3
```

### Step 2 — Set up Python environment
```
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install dependencies
```
pip install -r requirements.txt
```

### Step 4 — Run the chatbot server
```
python app.py
```

### Step 5 — Open the chatbot
Open your browser and go to:
```
http://localhost:5000
```

---

## How to Test via Terminal (API)
```
curl -X POST http://localhost:5000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "My internet is not working"}'
```

---

## Features
- LLaMA3-powered responses via Ollama
- IT knowledge base with 15 common issues
- Automatic issue categorization (Network, Account, Hardware, Software, Storage)
- Beautiful dark-themed chat UI
- Quick-access buttons for common issues
- Escalation to human agent for unknown issues

---

## Add More Knowledge
Open `knowledge_base.txt` and add more Q&A pairs in this format:
```
Q: Your question here?
A: Your answer here.
```
