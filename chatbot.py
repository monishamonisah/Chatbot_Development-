import csv
import os
import uuid
from datetime import datetime
import requests

# Education chatbot using a locally running Ollama model.
MODEL = "llama3.2"
OLLAMA_URL = "http://localhost:11434/api/chat"
DOMAIN = "Education"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
os.makedirs(DATASET_DIR, exist_ok=True)

HISTORY_CSV = os.path.join(DATASET_DIR, "chat_history.csv")
RESPONSES_CSV = os.path.join(DATASET_DIR, "responses.csv")
LOG_FILE = os.path.join(DATASET_DIR, "chatbot_logs.txt")

def ensure_csv(path, headers):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        with open(path, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(headers)

ensure_csv(HISTORY_CSV, ["timestamp", "session_id", "user_message", "assistant_response"])
ensure_csv(RESPONSES_CSV, ["timestamp", "question_type", "question", "response", "observation"])

def log_event(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {message}\n")

def ask_ollama(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload, timeout=180)
    response.raise_for_status()
    data = response.json()
    return data["message"]["content"].strip()

def append_csv(path, row):
    with open(path, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(row)

def main():
    session_id = str(uuid.uuid4())[:8]
    messages = [{
        "role": "system",
        "content": (
            "You are StudyBuddy, a friendly education chatbot. "
            "Answer educational questions in clear, beginner-friendly English. "
            "Explain step by step when useful. If you are unsure, say so rather "
            "than inventing facts. For coding questions, provide simple examples. "
            "Do not present yourself as a substitute for a teacher."
        )
    }]

    print("=" * 55)
    print("StudyBuddy - Education Chatbot (Ollama)")
    print(f"Model: {MODEL} | Domain: {DOMAIN}")
    print("Type 'exit' or 'quit' to end the conversation.")
    print("=" * 55)

    while True:
        try:
            user_text = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_text:
            print("Please enter a question.")
            continue
        if user_text.lower() in {"exit", "quit"}:
            print("StudyBuddy: Goodbye! Keep learning.")
            break

        messages.append({"role": "user", "content": user_text})
        timestamp = datetime.now().astimezone().isoformat(timespec="seconds")

        try:
            answer = ask_ollama(messages)
        except requests.exceptions.ConnectionError:
            answer = (
                "I cannot connect to Ollama. Please open Ollama and run "
                f"'ollama run {MODEL}' in your terminal, then try again."
            )
            log_event("ERROR: Could not connect to Ollama.")
        except requests.exceptions.Timeout:
            answer = "The model took too long to respond. Please try again."
            log_event("ERROR: Ollama request timed out.")
        except (requests.RequestException, KeyError, ValueError) as exc:
            answer = "Sorry, I could not get a valid response. Check Ollama and try again."
            log_event(f"ERROR: {type(exc).__name__}: {exc}")

        print(f"\nStudyBuddy: {answer}")
        messages.append({"role": "assistant", "content": answer})

        append_csv(HISTORY_CSV, [timestamp, session_id, user_text, answer])
        append_csv(RESPONSES_CSV, [timestamp, "user_input", user_text, answer, "Review answer for accuracy and completeness"])
        log_event(f"Session {session_id} | User: {user_text} | Assistant: {answer}")

if __name__ == "__main__":
    main()
