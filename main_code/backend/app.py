from flask import Flask, request, jsonify, render_template
import ollama
import os
import csv
from datetime import datetime

app = Flask(__name__)

def load_knowledge_base():
    kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base.txt")
    with open(kb_path, "r") as f:
        return f.read()

def load_dataset():
    dataset = []
    csv_path = os.path.join(os.path.dirname(__file__), "it_dataset.csv")
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dataset.append(row)
    return dataset

def categorize_issue(question):
    dataset = load_dataset()
    question_lower = question.lower()
    best_match = None
    best_score = 0

    for row in dataset:
        issue_words = row["issue"].lower().split()
        score = sum(1 for word in issue_words if word in question_lower)
        if score > best_score:
            best_score = score
            best_match = row

    if best_match and best_score > 0:
        return {
            "category": best_match["category"],
            "subcategory": best_match["subcategory"],
            "priority": best_match["priority"],
            "matched_issue": best_match["issue"]
        }
    return {
        "category": "GENERAL",
        "subcategory": "Other",
        "priority": "LOW",
        "matched_issue": ""
    }

def get_answer(user_question, category_info):
    kb = load_knowledge_base()
    prompt = f"""You are a professional IT helpdesk assistant.
The user's issue has been categorized as: {category_info['category']} > {category_info['subcategory']} (Priority: {category_info['priority']})

Use the knowledge base below to answer the user's question.
Give clear, step-by-step instructions.
Be concise, friendly, and professional.
If the answer is not in the knowledge base, say you will escalate to a human IT agent.

Knowledge Base:
{kb}

User Question: {user_question}

Answer:"""

    response = ollama.chat(
        model="tinyllama",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "No question provided"}), 400

    category_info = categorize_issue(question)
    answer = get_answer(question, category_info)
    timestamp = datetime.now().strftime("%H:%M")

    return jsonify({
        "answer": answer,
        "category": category_info["category"],
        "subcategory": category_info["subcategory"],
        "priority": category_info["priority"],
        "timestamp": timestamp
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "running", "model": "tinyllama"})

if __name__ == "__main__":
    print("=" * 50)
    print("  IT Helpdesk Automation Assistant")
    print("  Running at http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
